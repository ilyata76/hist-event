"""
    Файл логики gRPC-сервера
"""
import grpc
import proto.sql_generator_api_pb2 as pb2
import proto.sql_generator_api_pb2_grpc as pb2_grpc

from grpc_server.AbstractServicer import AbstractServicer as Servicer
from grpc_client.FileAPIgRPCCLient import FileAPIgRPCCLient
from utils.dict_from import dictFromMessage
from schemas.File import FileKeyword, FileBase, FileBinaryKeyword
from processor.Validator import Validator
from processor.Parser import Parser
from entity.Storage import StorageManager
from utils.config import EntityKeyword



def splitFiles(request : pb2.ManyFilesR) :
    """Разделить файлы от запроса на обычные и файл для связей"""
    files : list[FileKeyword] = []
    bonds_file : FileKeyword = None
    for file in request.files :
        if file.keyword == EntityKeyword.bonds :
            bonds_file = FileKeyword(**dictFromMessage(file))
        else :
            files.append(FileKeyword(**dictFromMessage(file)))
    return files, bonds_file


class SQLGeneratorAPIServicer(pb2_grpc.SQLGeneratorAPIServicer) :
    """
        Логика сервера (сервисер))
    """

    @Servicer.methodDecorator("sql-generator-api:Ping")
    async def Ping(self, request : pb2.PingR, context : grpc.ServicerContext) :
        return pb2.PongR(pong="Pong!")


    @Servicer.methodDecorator("sql-generator-api:Validate")
    async def Validate(self, request : pb2.ManyFilesR, context : grpc.ServicerContext) :
        validator = Validator()
        files, bonds_file = splitFiles(request)
        for file in files :
            file_binary = await FileAPIgRPCCLient.GetFile(file=FileBase(path=file.path, storage=file.storage))
            await validator.readAndValidateFileEntities(file=FileBinaryKeyword(**file_binary.model_dump(), keyword=file.keyword))
        if bonds_file :
            file_binary = await FileAPIgRPCCLient.GetFile(file=FileBase(path=bonds_file.path, storage=bonds_file.storage))
            await validator.readAndValidateFileBonds(file=FileBinaryKeyword(**file_binary.model_dump(), keyword=bonds_file.keyword))
        # TODO работа с идентификатором
        return pb2.Status(status="aboba validate!")


    @Servicer.methodDecorator("sql-generator-api:Parse")
    async def Parse(self, request : pb2.ManyFilesR, context : grpc.ServicerContext) :
        storage = StorageManager()
        parser = Parser(storage)
        files, bonds_file = splitFiles(request)
        await parser.parseFilesRecursiveToFillStorage(FileAPIgRPCCLient.GetFile, files=files, iterator=0)
        await parser.resolveAllLinksInEntitiesTexts()
        if bonds_file : 
            bonds_file_binary = await FileAPIgRPCCLient.GetFile(file=FileBase(path=bonds_file.path, storage=bonds_file.storage))
            await parser.parseAndResolveEventBondsFileToStorage(file=FileBinaryKeyword(**bonds_file_binary.model_dump(), keyword=bonds_file.keyword))
        print(storage)
        # TODO вызвать для текущего Storage сделать .saveToNoSQL()
        # TODO работа с идентификатором
        return pb2.Status(status="OK!")


    @Servicer.methodDecorator("sql-generator-api:Generate")
    async def Generate(self, request : pb2.ManyFilesR, context : grpc.ServicerContext) :
        # TODO работа с идентификатором
        # вызвать для Storage метод а-ля .restoreFromNoSQL()
        print(request.files)
        print(request.identifier)
        return pb2.Status(status="aboba generate!")


    # TODO method all-3
    # он не будет лишний раз читать из базы и сущности, и статусы

    # TODO servicer decorator like in storage
    # & processor decorator & client