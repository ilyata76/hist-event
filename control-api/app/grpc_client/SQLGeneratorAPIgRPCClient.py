"""
    Файл клиента для gRPC NoSQLDatabase сервера и доступа к нему
"""
import grpc
import app.proto.sql_generator_api_pb2 as pb2
import app.proto.sql_generator_api_pb2_grpc as pb2_grpc

from app.schemas.File import FileKeyword
from app.utils.config import config
from app.grpc_client.AbstractgRPCClient import AbstractgRPCClient


class SQLGeneratorAPIgRPCClient :
    """
        Класс доступа до gRPC сервера с SQL-Generator.
            Его методы вызываются в коде при обработке запросов.
    """

    @staticmethod
    @AbstractgRPCClient.method("sql-generator-api:Ping")
    async def Ping() :
        with grpc.insecure_channel(f"{config.SQL_GENERATOR_API_GRPC_HOST}:{config.SQL_GENERATOR_API_GRPC_PORT}") as channel :
            stub = pb2_grpc.SQLGeneratorAPIStub(channel)
            response : pb2.PongR = stub.Ping(pb2.PingR())
        return response

    @staticmethod
    @AbstractgRPCClient.method("sql-generator-api:Validate")
    async def Validate(files : list[FileKeyword], identifier : str) :
        with grpc.insecure_channel(f"{config.SQL_GENERATOR_API_GRPC_HOST}:{config.SQL_GENERATOR_API_GRPC_PORT}") as channel :
            stub = pb2_grpc.SQLGeneratorAPIStub(channel)
            response : pb2.StatusR = stub.Validate(pb2.ManyFilesR(files=[file.model_dump() for file in files],
                                                                 identifier=identifier))
        return response

    @staticmethod
    @AbstractgRPCClient.method("sql-generator-api:Parse")
    async def Parse(files : list[FileKeyword], identifier : str) :
        with grpc.insecure_channel(f"{config.SQL_GENERATOR_API_GRPC_HOST}:{config.SQL_GENERATOR_API_GRPC_PORT}") as channel :
            stub = pb2_grpc.SQLGeneratorAPIStub(channel)
            response : pb2.StatusR = stub.Parse(pb2.ManyFilesR(files=[file.model_dump() for file in files],
                                                              identifier=identifier))
        return response

    @staticmethod
    @AbstractgRPCClient.method("sql-generator-api:Generate")
    async def Generate(files : list[FileKeyword], identifier : str) :
        with grpc.insecure_channel(f"{config.SQL_GENERATOR_API_GRPC_HOST}:{config.SQL_GENERATOR_API_GRPC_PORT}") as channel :
            stub = pb2_grpc.SQLGeneratorAPIStub(channel)
            response : pb2.StatusR = stub.Generate(pb2.ManyFilesR(files=[file.model_dump() for file in files],
                                                                 identifier=identifier))
        return response

    @staticmethod
    @AbstractgRPCClient.method("sql-generator-api:PutSQLGeneratorStatus")
    async def PutSQLGeneratorStatus(identifier : str, status : str) :
        with grpc.insecure_channel(f"{config.SQL_GENERATOR_API_GRPC_HOST}:{config.SQL_GENERATOR_API_GRPC_PORT}") as channel :
            stub = pb2_grpc.SQLGeneratorAPIStub(channel)
            response : pb2.IdentifierStatusR = stub.PutSQLGeneratorStatus(pb2.IdentifierStatusR(identifier=identifier, 
                                                                                      status=status))
        return response

    @staticmethod
    @AbstractgRPCClient.method("sql-generator-api:GetSQLGeneratorStatus")
    async def GetSQLGeneratorStatus(identifier : str) :
        with grpc.insecure_channel(f"{config.SQL_GENERATOR_API_GRPC_HOST}:{config.SQL_GENERATOR_API_GRPC_PORT}") as channel :
            stub = pb2_grpc.SQLGeneratorAPIStub(channel)
            response : pb2.IdentifierStatusR = stub.GetSQLGeneratorStatus(pb2.IdentifierR(identifier=identifier))
        return response