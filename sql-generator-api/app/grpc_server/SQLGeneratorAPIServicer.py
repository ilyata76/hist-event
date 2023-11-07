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
        files = [FileKeyword(**dictFromMessage(x)) for x in request.files]
        for file in files :
            file_binary = await FileAPIgRPCCLient.GetFile(file=FileBase(path=file.path, 
                                                                        storage=file.storage))
            await validator.readAndValidateFileEntities(file=FileBinaryKeyword(**file_binary.model_dump(),
                                                                               keyword=file.keyword))
        # TODO работа с идентификатором
        return pb2.Status(status="aboba validate!")


    @Servicer.methodDecorator("sql-generator-api:Parse")
    async def Parse(self, request : pb2.ManyFilesR, context : grpc.ServicerContext) :
        parser = Parser()
        files = [FileKeyword(**dictFromMessage(x)) for x in request.files]
        for file in files :
            file_binary = await FileAPIgRPCCLient.GetFile(file=FileBase(path=file.path, 
                                                                        storage=file.storage))
            await parser.readAndParseFileEntities(file=FileBinaryKeyword(**file_binary.model_dump(),
                                                                         keyword=file.keyword))
        # TODO вызвать Saver для текущего Storage сделать .save()
        # TODO работа с идентификатором
        return pb2.Status(status="aboba parse!")


    @Servicer.methodDecorator("sql-generator-api:Generate")
    async def Generate(self, request : pb2.ManyFilesR, context : grpc.ServicerContext) :
        # TODO работа с идентификатором
        print(request.files)
        print(request.identifier)
        return pb2.Status(status="aboba generate!")


    # TODO method all-3
    # он не будет лишний раз читать из базы и сущности, и статусы