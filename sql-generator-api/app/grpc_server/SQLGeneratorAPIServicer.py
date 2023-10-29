"""
    Файл логики gRPC-сервера
"""
import grpc
import proto.sql_generator_api_pb2 as pb2
import proto.sql_generator_api_pb2_grpc as pb2_grpc

from grpc_server.AbstractServicer import AbstractServicer
from utils.dict_from import dictFromMessage
from schemas.File import FileKeyword, FileKeywordList
from processor.Validator import Validator


class SQLGeneratorAPIServicer(pb2_grpc.SQLGeneratorAPIServicer) :
    """
        Логика сервера (сервисер))
    """

    @AbstractServicer.method("sql-generator-api:Ping")
    async def Ping(self, request : pb2.PingR, context : grpc.ServicerContext) :
        return pb2.PongR(pong="Pong!")


    @AbstractServicer.method("sql-generator-api:Validate")
    async def Validate(self, request : pb2.ManyFilesR, context : grpc.ServicerContext) :
        v = Validator()
        await v.validateFiles(files=FileKeywordList(files=[FileKeyword(**dictFromMessage(x)) for x in request.files]))
        return pb2.Status(status="aboba validate!")


    @AbstractServicer.method("sql-generator-api:Parse")
    async def Parse(self, request : pb2.ManyFilesR, context : grpc.ServicerContext) :
        print(request.files)
        print(request.identifier)
        return pb2.Status(status="aboba parse!")


    @AbstractServicer.method("sql-generator-api:Generate")
    async def Generate(self, request : pb2.ManyFilesR, context : grpc.ServicerContext) :
        print(request.files)
        print(request.identifier)
        return pb2.Status(status="aboba generate!")