"""
    Файл клиента для gRPC FileAPi сервера и доступа к нему
"""
import proto.file_api_pb2 as pb2
import proto.file_api_pb2_grpc as pb2_grpc

from utils.config import config
from utils.dict_from import dictFromMessage
from grpc_client.AbstractgRPCClient import AbstractgRPCClient as GrpcClient
from schemas.File import FileBinary, FileBase, File
from schemas.Ping import Pong


class FileAPIgRPCCLient :
    """
        Класс доступа до gRPC сервера с FileAPI.
            Его методы вызываются в коде при обработке запросов.
    """

    @staticmethod
    @GrpcClient.methodAsyncDecorator("file-api:Ping",
                                     f"{config.FILE_API_GRPC_HOST}:{config.FILE_API_GRPC_PORT}")
    async def Ping(channel = None) -> Pong :
        stub = pb2_grpc.FileAPIStub(channel)
        response : pb2.PongR = stub.Ping(pb2.PingR())
        return Pong(**dictFromMessage(response))


    @staticmethod
    @GrpcClient.methodAsyncDecorator("file-api:GetFile",
                                     f"{config.FILE_API_GRPC_HOST}:{config.FILE_API_GRPC_PORT}")
    async def GetFile(file : FileBase, channel = None) -> FileBinary :
        stub = pb2_grpc.FileAPIStub(channel)
        response : pb2.FileBinaryR = stub.GetFile(pb2.FileBaseR(file=file.model_dump()))
        return FileBinary(**dictFromMessage(response.file))


    @staticmethod
    @GrpcClient.methodAsyncDecorator("file-api:PutFile",
                                     f"{config.FILE_API_GRPC_HOST}:{config.FILE_API_GRPC_PORT}")
    async def PutFile(file : FileBinary, channel = None) -> File :
        stub = pb2_grpc.FileAPIStub(channel)
        response : pb2.FileR = stub.PutFile(pb2.FileBinaryR(file=file.model_dump()))
        return File(**dictFromMessage(response.file))