"""
    Файл логики gRPC-сервера
"""
import uuid
import proto.sql_generator_api_pb2 as pb2
import proto.sql_generator_api_pb2_grpc as pb2_grpc

from grpc_server.AbstractServicer import AbstractServicer as Servicer
from grpc_client.FileAPIgRPCCLient import FileAPIgRPCCLient
from grpc_client.NoSQLDatabaseAPIgRPCClient import NoSQLDatabaseAPIgRPCClient
from utils.dict_from import dictFromMessage
from schemas.File import FileBaseKeyword, FileBase, FileBinary
from schemas.StatusIdentifier import Identifier, StatusIdentifier
from processor.Validator import Validator
from processor.Parser import Parser
from processor.Generator import Generator
from entity.Storage import StorageManager
from utils.config import EntityKeyword
from utils.exception import *



def splitFiles(request : list[FileBaseKeyword]) -> tuple[list[FileBaseKeyword], FileBaseKeyword] :
    """Разделить файлы от запроса на обычные и файл для связей"""
    files : list[FileBaseKeyword] = []
    bonds_file : FileBaseKeyword = None
    for file in request :
        if file.keyword == EntityKeyword.bonds :
            bonds_file = file
        else :
            files.append(file)
    return files, bonds_file


async def createNewIdentifier() -> str :
    """Создать новый идентификатор для операций"""
    id = uuid.uuid4().__str__()
    try :
        await NoSQLDatabaseAPIgRPCClient.GetSQLGeneratorStatus(Identifier(identifier=id))
        return await createNewIdentifier()
    except BaseException :
        return id


async def checkOperationStatusValidated(identifier : str) -> None :
    st_id = await NoSQLDatabaseAPIgRPCClient.GetSQLGeneratorStatus(Identifier(identifier=identifier))
    if st_id.status != "validated" and st_id.status != "parsed" :
        raise ParsingException(code=ParsingExceptionCode.FILES_DONT_VALIDATED,
                               detail=f"Для {identifier} не было проведено операции валидации")
    return None


async def parseFilesToStorage(parser : Parser, identifier : str) -> Parser :
    files = await NoSQLDatabaseAPIgRPCClient.GetSQLGeneratorFiles(Identifier(identifier=identifier))
    files, bonds_file = splitFiles(files)
    await parser.parseFilesRecursiveToFillStorage(FileAPIgRPCCLient.GetFile, 
                                                  files=files, 
                                                  iterator=0)
    await parser.resolveAllLinksInEntitiesTexts()
    if bonds_file : 
        await parser.parseAndResolveEventBondsFileToStorage(FileAPIgRPCCLient.GetFile, 
                                                            file=bonds_file)
    return parser



class SQLGeneratorAPIServicer(pb2_grpc.SQLGeneratorAPIServicer) :
    """
        Логика сервера (сервисер))
    """

    @Servicer.methodAsyncDecorator("sql-generator-api:Ping")
    async def Ping(self, request : pb2.PingR, context) :
        return pb2.PongR(pong="Pong!")


    @Servicer.methodAsyncDecorator("sql-generator-api:Validate")
    async def Validate(self, request : pb2.ManyFilesR, context) :
        validator = Validator()
        files, bonds_file = splitFiles([FileBaseKeyword(**dictFromMessage(file)) for file in request.files])
        for file in files :
            await validator.readAndValidateFileEntities(FileAPIgRPCCLient.GetFile, file)
        if bonds_file :
            await validator.readAndValidateFileBonds(FileAPIgRPCCLient.GetFile, bonds_file)
        identifier = await createNewIdentifier()
        await NoSQLDatabaseAPIgRPCClient.PutSQLGeneratorStatus(StatusIdentifier(identifier=identifier,
                                                                                status="validated"))
        await NoSQLDatabaseAPIgRPCClient.PutSQLGeneratorFiles(files=[FileBaseKeyword(**dictFromMessage(file)) for file in request.files],
                                                              identifier=Identifier(identifier=identifier))
        status = (await NoSQLDatabaseAPIgRPCClient.GetSQLGeneratorStatus(Identifier(identifier=identifier))).status
        return pb2.IdentifierStatusR(status=status, identifier=identifier)


    @Servicer.methodAsyncDecorator("sql-generator-api:ParseAndGenerate")
    async def ParseAndGenerate(self, request : pb2.ManyFilesIdentifierR, context) :
        # PARSE
        await checkOperationStatusValidated(request.identifier)
        storage = StorageManager()
        parser = Parser(storage)
        generator = Generator(storage)
        parser = await parseFilesToStorage(parser, request.identifier)
        status = (await NoSQLDatabaseAPIgRPCClient.PutSQLGeneratorStatus(StatusIdentifier(identifier=request.identifier,
                                                                                          status="parsed"))).status
        # AND GENERATE
        sql_string = await generator.readAndGenerateSQLFromStorage()
        sql_path = f"/sql/{request.identifier}.sql"
        sql_storage = "ftp"
        await FileAPIgRPCCLient.PutFile(FileBinary(path=sql_path, 
                                                   storage=sql_storage, 
                                                   filename="main.sql",
                                                   file=bytes(sql_string, encoding="utf-8")))
        await NoSQLDatabaseAPIgRPCClient.PutSQLGeneratorSQLFile(FileBase(path=sql_path,
                                                                         storage=sql_storage),
                                                                Identifier(identifier=request.identifier))
        status = (await NoSQLDatabaseAPIgRPCClient.PutSQLGeneratorStatus(StatusIdentifier(identifier=request.identifier,
                                                                                          status="generated"))).status
        return pb2.IdentifierStatusR(status=status,
                                     identifier=request.identifier)


    @Servicer.methodAsyncDecorator("sql-generator-api:GetSQLGeneratorStatus")
    async def GetSQLGeneratorStatus(self, request : pb2.IdentifierR, context) :
        response_from_nosql : StatusIdentifier = await NoSQLDatabaseAPIgRPCClient.GetSQLGeneratorStatus(Identifier(**dictFromMessage(request)))
        return pb2.IdentifierStatusR(**response_from_nosql.model_dump())


    @Servicer.methodAsyncDecorator("sql-generator-api:GetSQLGeneratorFiles")
    async def GetSQLGeneratorFiles(self, request : pb2.IdentifierR, context) :
        files : list[FileBaseKeyword] = await NoSQLDatabaseAPIgRPCClient.GetSQLGeneratorFiles(Identifier(identifier=request.identifier))
        return pb2.ManyFilesIdentifierR(identifier=request.identifier,
                                        files=[file.model_dump() for file in files])
    

    @Servicer.methodAsyncDecorator("sql-generator-api:GetSQLGeneratorSQLFile")
    async def GetSQLGeneratorSQLFile(self, request : pb2.IdentifierR, context) :
        file : FileBase = await NoSQLDatabaseAPIgRPCClient.GetSQLGeneratorSQLFile(Identifier(identifier=request.identifier))
        return pb2.FileBaseIdentifierR(file=file.model_dump(),
                                       identifier=request.identifier)