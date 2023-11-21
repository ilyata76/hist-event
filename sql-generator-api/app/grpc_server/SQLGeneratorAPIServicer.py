"""
    Файл логики gRPC-сервера
"""
import uuid

import proto.sql_generator_api_pb2 as pb2
import proto.sql_generator_api_pb2_grpc as pb2_grpc

from config import EntityKeyword, StorageIdentifier, SQL_PATH
from schemas import FileBaseKeyword, FileBase, FileBinary, FileBaseKeywordList,\
                    Identifier, Status, Meta
from entity import StorageManager
from utils import dictFromGoogleMessage
from utils.exception import *
from processor import *
from grpc_client import FileAPIgRPCCLient, NoSQLDatabaseAPIgRPCClient

from .AbstractServicer import AbstractServicer as Servicer


def splitFiles(request : FileBaseKeywordList) -> tuple[list[FileBaseKeyword], FileBaseKeyword] :
    """Разделить файлы от запроса на обычные и файл для связей"""
    files : list[FileBaseKeyword] = []
    bonds_file : FileBaseKeyword = None
    for file in request.files :
        if file.keyword == EntityKeyword.bonds :
            bonds_file = file
        else :
            files.append(file)
    return files, bonds_file


async def createNewIdentifier() -> Status :
    """Создать новый идентификатор для операций"""
    id = uuid.uuid4().__str__()
    try :
        await NoSQLDatabaseAPIgRPCClient.GetSQLGeneratorMeta(Identifier(id))
        return await createNewIdentifier()
    except BaseException :
        return Status(id)


async def checkOperationStatusValidated(identifier : Identifier) -> Meta :
    meta = await NoSQLDatabaseAPIgRPCClient.GetSQLGeneratorMeta(identifier)
    status = meta.status
    if status != "validated" and status != "parsed" and status != "generated" :
        raise ParsingException(code=ParsingExceptionCode.FILES_DONT_VALIDATED,
                               detail=f"Для {identifier} не было проведено операции валидации")
    return meta


async def parseFilesToStorage(parser : Parser, identifier : Identifier) -> Parser :
    files = await NoSQLDatabaseAPIgRPCClient.GetSQLGeneratorFiles(identifier)
    files, bonds_file = splitFiles(files)
    await parser.parseFilesRecursiveToFillStorage(FileAPIgRPCCLient.GetFile, 
                                                  files=files, 
                                                  iterator=0)
    await parser.resolveAllLinksInEntitiesTexts()

    if bonds_file : 
        await parser.parseAndResolveEventBondsFileToStorage(FileAPIgRPCCLient.GetFile, 
                                                            file=bonds_file)
    return parser


async def validateFiles(validator : Validator, files : FileBaseKeywordList) :
    files, bonds_file = splitFiles(files)
    for file in files :
        await validator.readAndValidateFileEntities(FileAPIgRPCCLient.GetFile, file)
    if bonds_file :
        await validator.readAndValidateFileBonds(FileAPIgRPCCLient.GetFile, bonds_file)


class SQLGeneratorAPIServicer(pb2_grpc.SQLGeneratorAPIServicer) :
    """
        Логика сервера (сервисер))
    """

    @Servicer.methodAsyncDecorator("sql-generator-api:Ping")
    async def Ping(self, request : pb2.PingR, context) :
        return pb2.PongR(pong="Pong!")


    @Servicer.methodAsyncDecorator("sql-generator-api:Validate")
    async def Validate(self, request : pb2.ManyFilesNameR, context) :
        validator = Validator()
        file_list = FileBaseKeywordList(files=[FileBaseKeyword(**dictFromGoogleMessage(file)) for file in request.files])
        await validateFiles(validator, file_list)
        identifier = await createNewIdentifier()
        meta = await NoSQLDatabaseAPIgRPCClient.PutSQLGeneratorMeta(Identifier(identifier), Meta(status="validated",
                                                                                                   name=request.name))
        await NoSQLDatabaseAPIgRPCClient.PutSQLGeneratorFiles(file_list, Identifier(identifier))
        meta = await NoSQLDatabaseAPIgRPCClient.GetSQLGeneratorMeta(Identifier(identifier))
        return pb2.IdentifierMetaR(**meta.model_dump(), identifier=identifier)


    @Servicer.methodAsyncDecorator("sql-generator-api:ParseAndGenerate")
    async def ParseAndGenerate(self, request : pb2.ManyFilesIdentifierR, context) :
        identifier = Identifier(request.identifier)
        meta = await checkOperationStatusValidated(identifier)
        storage = StorageManager()
        parser = Parser(storage)
        generator = Generator(storage)
        # PARSE
        parser = await parseFilesToStorage(parser, identifier)
        meta = await NoSQLDatabaseAPIgRPCClient.PutSQLGeneratorMeta(identifier, 
                                                                    Meta(status="parsed", name=meta.name))
        # AND GENERATE
        sql_string = await generator.readAndGenerateSQLFromStorage()
        sql_path = SQL_PATH(request.identifier)
        sql_storage = StorageIdentifier.FTP
        await FileAPIgRPCCLient.PutFile(FileBinary(path=sql_path, 
                                                   storage=sql_storage, 
                                                   filename="main.sql",
                                                   file=bytes(sql_string, encoding="utf-8")))
        await NoSQLDatabaseAPIgRPCClient.PutSQLGeneratorSQLFile(FileBase(path=sql_path,
                                                                         storage=sql_storage),
                                                                identifier)
        meta = await NoSQLDatabaseAPIgRPCClient.PutSQLGeneratorMeta(identifier, 
                                                                    Meta(status="generated", name=meta.name))
        return pb2.IdentifierMetaR(**meta.model_dump(), identifier=identifier)


    @Servicer.methodAsyncDecorator("sql-generator-api:GetSQLGeneratorMeta")
    async def GetSQLGeneratorMeta(self, request : pb2.IdentifierR, context) :
        identifier = Identifier(request.identifier)
        meta = await NoSQLDatabaseAPIgRPCClient.GetSQLGeneratorMeta(identifier)
        return pb2.IdentifierMetaR(**meta.model_dump(), identifier=identifier)


    @Servicer.methodAsyncDecorator("sql-generator-api:GetSQLGeneratorFiles")
    async def GetSQLGeneratorFiles(self, request : pb2.IdentifierR, context) :
        identifier = Identifier(request.identifier)
        files = await NoSQLDatabaseAPIgRPCClient.GetSQLGeneratorFiles(identifier)
        return pb2.ManyFilesIdentifierR(identifier=identifier, **files.model_dump())


    @Servicer.methodAsyncDecorator("sql-generator-api:GetSQLGeneratorSQLFile")
    async def GetSQLGeneratorSQLFile(self, request : pb2.IdentifierR, context) :
        identifier = Identifier(request.identifier)
        file = await NoSQLDatabaseAPIgRPCClient.GetSQLGeneratorSQLFile(identifier)
        return pb2.FileBaseIdentifierR(identifier=request.identifier, file=file.model_dump())


    @Servicer.methodAsyncDecorator("sql-generator-api:GetSQLGeneratorSQLIDs")
    async def GetSQLGeneratorSQLIDs(self, request : pb2.NothingR, context):
        metalist = await NoSQLDatabaseAPIgRPCClient.GetSQLGeneratorSQLIDs()
        return pb2.ManyIdentifierMetaR(**metalist.model_dump())