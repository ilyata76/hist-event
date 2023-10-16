"""
    Файл логики gRPC-сервера
"""
import grpc
import proto.nosql_database_api_pb2 as pb2
import proto.nosql_database_api_pb2_grpc as pb2_grpc

from grpc_server.AbstractServicer import AbstractServicer
import database
from schemas.File import File


class NoSQLDatabaseAPIServicer(pb2_grpc.NoSQLDatabaseAPIServicer) :
    """
        Логика сервера (сервисер))
    """
  
    @AbstractServicer.method("nosql-database-api:Ping")
    async def Ping(self, request : pb2.PingRequest, context : grpc.ServicerContext):
        return pb2.PingResponse(pong="Pong!")