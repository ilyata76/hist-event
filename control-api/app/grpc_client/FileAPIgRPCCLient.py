"""
    Файл клиента для gRPC FileAPi сервера и доступа к нему
"""
import grpc
import app.proto.file_api_pb2 as pb2
import app.proto.file_api_pb2_grpc as pb2_grpc

from app.utils.config import config
from app.grpc_client.AbstractgRPCClient import AbstractgRPCClient


class FileAPIgRPCCLient :
    """
        Класс доступа до gRPC сервера с FileAPI
    """

    @staticmethod
    @AbstractgRPCClient.method("file-api:/ping")
    async def Ping() :
        with grpc.insecure_channel(f"{config.FILE_API_GRPC_HOST}:{config.FILE_API_GRPC_PORT}") as channel:
            stub = pb2_grpc.FileAPIStub(channel)
            response : pb2.PingResponse = stub.Ping(pb2.PingRequest())
        return response