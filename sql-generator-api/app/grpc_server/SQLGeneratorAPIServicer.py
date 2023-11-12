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
from schemas.File import FileBaseKeyword
from schemas.StatusIdentifier import Identifier, StatusIdentifier
from processor.Validator import Validator
from processor.Parser import Parser
from entity.Storage import StorageManager
from utils.config import EntityKeyword
from utils.exception import *



def splitFiles(request : list[FileBaseKeyword]) :
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


    @Servicer.methodAsyncDecorator("sql-generator-api:Parse")
    async def Parse(self, request : pb2.ManyFilesIdentifierR, context) :
        st_id = await NoSQLDatabaseAPIgRPCClient.GetSQLGeneratorStatus(Identifier(identifier=request.identifier))
        if st_id.status != "validated" :
            raise ParsingException(code=ParsingExceptionCode.FILES_DONT_VALIDATED,
                                   detail=f"Для {request.identifier} не было проведено операции валидации")
        storage = StorageManager()
        parser = Parser(storage)
        files = await NoSQLDatabaseAPIgRPCClient.GetSQLGeneratorFiles(identifier=Identifier(identifier=request.identifier))
        files, bonds_file = splitFiles(files)
        await parser.parseFilesRecursiveToFillStorage(FileAPIgRPCCLient.GetFile, files=files, iterator=0)
        await parser.resolveAllLinksInEntitiesTexts()
        if bonds_file : 
            await parser.parseAndResolveEventBondsFileToStorage(FileAPIgRPCCLient.GetFile, file=bonds_file)
        print(storage)
        # TODO вызвать для текущего Storage сделать .saveToNoSQL()
        await NoSQLDatabaseAPIgRPCClient.PutSQLGeneratorStatus(StatusIdentifier(identifier=request.identifier,
                                                                                status="parsed"))
        status = (await NoSQLDatabaseAPIgRPCClient.GetSQLGeneratorStatus(Identifier(identifier=request.identifier))).status
        return pb2.IdentifierStatusR(status=status,
                                     identifier=request.identifier)



    @Servicer.methodAsyncDecorator("sql-generator-api:Generate")
    async def Generate(self, request : pb2.ManyFilesIdentifierR, context) :
        st_id = await NoSQLDatabaseAPIgRPCClient.GetSQLGeneratorStatus(Identifier(identifier=request.identifier))
        if st_id.status != "parsed" :
            raise ParsingException(code=ParsingExceptionCode.FILES_DONT_VALIDATED,
                                   detail=f"Для {request.identifier} не было проведено операции парсинга и сохранении в базе nosql")
        # вызвать для Storage метод а-ля .restoreFromNoSQL()
        await NoSQLDatabaseAPIgRPCClient.PutSQLGeneratorStatus(StatusIdentifier(identifier=request.identifier,
                                                                                status="generated"))
        status = (await NoSQLDatabaseAPIgRPCClient.GetSQLGeneratorStatus(Identifier(identifier=request.identifier))).status
        return pb2.IdentifierStatusR(status=status,
                                     identifier=request.identifier)


    # TODO method all-3
    # он не будет лишний раз читать из базы и сущности, и статусы

    @Servicer.methodAsyncDecorator("sql-generator-api:PutSQLGeneratorStatus")
    async def PutSQLGeneratorStatus(self, request : pb2.IdentifierStatusR, context) :
        print(request.status, request.identifier)
        response_from_nosql : StatusIdentifier = await NoSQLDatabaseAPIgRPCClient.PutSQLGeneratorStatus(StatusIdentifier(**dictFromMessage(request)))
        return pb2.IdentifierStatusR(**response_from_nosql.model_dump())


    @Servicer.methodAsyncDecorator("sql-generator-api:GetSQLGeneratorStatus")
    async def GetSQLGeneratorStatus(self, request : pb2.IdentifierR, context) :
        print(request.identifier)
        response_from_nosql : StatusIdentifier = await NoSQLDatabaseAPIgRPCClient.GetSQLGeneratorStatus(Identifier(**dictFromMessage(request)))
        return pb2.IdentifierStatusR(**response_from_nosql.model_dump())


    @Servicer.methodAsyncDecorator("sql-generator-api:GetSQLGeneratorFiles")
    async def GetSQLGeneratorFiles(self, request : pb2.IdentifierR, context) :
        files = await NoSQLDatabaseAPIgRPCClient.GetSQLGeneratorFiles(identifier=Identifier(identifier=request.identifier))
        return pb2.ManyFilesIdentifierR(identifier=request.identifier,
                                        files=[file.model_dump() for file in files])