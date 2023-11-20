"""
    Файл клиента для gRPC NoSQLDatabase сервера и доступа к нему
"""
import app.proto.sql_generator_api_pb2 as pb2
import app.proto.sql_generator_api_pb2_grpc as pb2_grpc

from app.config import SQL_GEN_IP
from app.schemas import *
from app.utils import dictFromGoogleMessage

from .AbstractgRPCClient import AbstractgRPCClient


class SQLGeneratorAPIgRPCClient :
    """
        Класс доступа до gRPC сервера с SQL-Generator.
            Его методы вызываются в коде при обработке запросов.
    """

    @staticmethod
    @AbstractgRPCClient.methodAsyncDecorator("sql-generator-api:Ping", SQL_GEN_IP)
    async def Ping(channel = None) -> PongService :
        stub = pb2_grpc.SQLGeneratorAPIStub(channel)
        request = pb2.PingR()
        response : pb2.PongR = stub.Ping(request)
        return PongService(pong=response.pong, service="sql-generator-api")


    @staticmethod
    @AbstractgRPCClient.methodAsyncDecorator("sql-generator-api:Validate", SQL_GEN_IP)
    async def Validate(files : FileBaseKeywordList, channel = None) -> StatusIdentifier :
        stub = pb2_grpc.SQLGeneratorAPIStub(channel)
        request = pb2.ManyFilesR(**files.model_dump())
        response : pb2.IdentifierStatusR = stub.Validate(request)
        return StatusIdentifier(status=response.status, identifier=response.identifier)


    @staticmethod
    @AbstractgRPCClient.methodAsyncDecorator("sql-generator-api:ParseAndGenerate", SQL_GEN_IP)
    async def ParseAndGenerate(identifier : Identifier, channel = None) -> StatusIdentifier :
        stub = pb2_grpc.SQLGeneratorAPIStub(channel)
        request = pb2.IdentifierR(identifier=identifier)
        response : pb2.IdentifierStatusR = stub.ParseAndGenerate(request)
        return StatusIdentifier(status=response.status, identifier=response.identifier)


    @staticmethod
    @AbstractgRPCClient.methodAsyncDecorator("sql-generator-api:GetSQLGeneratorStatus", SQL_GEN_IP)
    async def GetSQLGeneratorStatus(identifier : Identifier, channel = None) -> StatusIdentifier :
        stub = pb2_grpc.SQLGeneratorAPIStub(channel)
        request = pb2.IdentifierR(identifier=identifier)
        response : pb2.IdentifierStatusR = stub.GetSQLGeneratorStatus(request)
        return StatusIdentifier(status=response.status, identifier=response.identifier)


    @staticmethod
    @AbstractgRPCClient.methodAsyncDecorator("sql-generator-api:GetSQLGeneratorFiles", SQL_GEN_IP)
    async def GetSQLGeneratorFiles(identifier : Identifier, channel = None) -> FileBaseKeywordList :
        stub = pb2_grpc.SQLGeneratorAPIStub(channel)
        request = pb2.IdentifierR(identifier=identifier)
        response : pb2.ManyFilesIdentifierR = stub.GetSQLGeneratorFiles(request)
        return FileBaseKeywordList(files=[FileBaseKeyword(**dictFromGoogleMessage(file)) for file in response.files])


    @staticmethod
    @AbstractgRPCClient.methodAsyncDecorator("sql-generator-api:GetSQLGeneratorSQLFile", SQL_GEN_IP)
    async def GetSQLGeneratorSQLFile(identifier : Identifier, channel = None) -> FileBase :
        stub = pb2_grpc.SQLGeneratorAPIStub(channel)
        request = pb2.IdentifierR(identifier=identifier)
        response : pb2.FileBaseIdentifierR = stub.GetSQLGeneratorSQLFile(request)
        return FileBase(**dictFromGoogleMessage(response.file))