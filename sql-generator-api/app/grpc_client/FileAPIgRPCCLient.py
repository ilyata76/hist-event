"""
    Файл клиента для gRPC FileAPi сервера и доступа к нему
"""
import grpc
import proto.file_api_pb2 as pb2
import proto.file_api_pb2_grpc as pb2_grpc

from utils.config import config
from utils.dict_from import dictFromMessage
from grpc_client.AbstractgRPCClient import AbstractgRPCClient
from schemas.File import FileBinary, FileBase
from schemas.Ping import Pong


class FileAPIgRPCCLient :
    """
        Класс доступа до gRPC сервера с FileAPI.
            Его методы вызываются в коде при обработке запросов.
    """

    @staticmethod
    @AbstractgRPCClient.method("file-api:Ping")
    async def Ping() -> Pong :
        with grpc.insecure_channel(f"{config.FILE_API_GRPC_HOST}:{config.FILE_API_GRPC_PORT}") as channel :
            stub = pb2_grpc.FileAPIStub(channel)
            response : pb2.PongR = stub.Ping(pb2.PingR())
        return Pong(**dictFromMessage(response))


    @staticmethod
    @AbstractgRPCClient.method("file-api:GetFile")
    async def GetFile(file : FileBase) -> FileBinary:
        with grpc.insecure_channel(f"{config.FILE_API_GRPC_HOST}:{config.FILE_API_GRPC_PORT}") as channel :
            stub = pb2_grpc.FileAPIStub(channel)
            response : pb2.FileBinaryR = stub.GetFile(pb2.FileBaseR(file=file.model_dump()))
        return FileBinary(**dictFromMessage(response.file))