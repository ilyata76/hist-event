"""
    Файл клиента для gRPC NoSQLDatabase сервера и доступа к нему
"""
import grpc
import proto.nosql_database_api_pb2 as pb2
import proto.nosql_database_api_pb2_grpc as pb2_grpc

from utils.config import config
from grpc_client.AbstractgRPCClient import AbstractgRPCClient


class NoSQLDatabaseAPIgRPCClient :
    """
        Класс доступа до gRPC сервера с NoSQLDatabase
    """

    @staticmethod
    @AbstractgRPCClient.method("nosql-database-api:Ping")
    async def Ping() :
        with grpc.insecure_channel(f"{config.NOSQL_DATABASE_GRPC_HOST}:{config.NOSQL_DATABASE_GRPC_PORT}") as channel :
            stub = pb2_grpc.NoSQLDatabaseAPIStub(channel)
            response : pb2.PingResponse = stub.Ping(pb2.PingRequest())
        return response