"""
    Файл клиента для gRPC NoSQLDatabase сервера и доступа к нему
"""
import app.proto.nosql_database_api_pb2 as pb2
import app.proto.nosql_database_api_pb2_grpc as pb2_grpc

from app.config import NOSQL_IP
from app.schemas import PongService

from .AbstractgRPCClient import AbstractgRPCClient


class NoSQLDatabaseAPIgRPCClient :
    """
        Класс доступа до gRPC сервера с NoSQLDatabase.
            Его методы вызываются в коде при обработке запросов.
    """

    @staticmethod
    @AbstractgRPCClient.methodAsyncDecorator("nosql-database-api:Ping", NOSQL_IP)
    async def Ping(channel = None) -> PongService :
        stub = pb2_grpc.NoSQLDatabaseAPIStub(channel)
        request = pb2.PingR()
        response : pb2.PongR = stub.Ping(request)
        return PongService(pong=response.pong, service="nosql-database-api")