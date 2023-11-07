"""
    Файл клиента для gRPC FileAPi сервера и доступа к нему
"""
import grpc
import proto.file_api_pb2 as pb2
import proto.file_api_pb2_grpc as pb2_grpc

from utils.config import config
from utils.dict_from import dictFromMessage
from grpc_client.AbstractgRPCClient import AbstractgRPCClient as GrpcClient
from schemas.File import FileBinary, FileBase
from schemas.Ping import Pong


class FileAPIgRPCCLient :
    """
        Класс доступа до gRPC сервера с FileAPI.
            Его методы вызываются в коде при обработке запросов.
    """

    @staticmethod
    def channelDecorator(function) :
        async def wrap(channel = None, *args, **kwargs) :
            if not channel : 
                with grpc.insecure_channel(f"{config.FILE_API_GRPC_HOST}:{config.FILE_API_GRPC_PORT}") as channel :
                    return await function(channel=channel, *args, **kwargs)
            else : 
                return await function(channel=channel, *args, **kwargs)
        return wrap


    @staticmethod
    @GrpcClient.methodDecorator("file-api:Ping")
    @channelDecorator
    async def Ping(channel = None) -> Pong :
        stub = pb2_grpc.FileAPIStub(channel)
        response : pb2.PongR = stub.Ping(pb2.PingR())
        return Pong(**dictFromMessage(response))


    @staticmethod
    @GrpcClient.methodDecorator("file-api:GetFile")
    @channelDecorator
    async def GetFile(file : FileBase, channel = None) -> FileBinary:
        stub = pb2_grpc.FileAPIStub(channel)
        response : pb2.FileBinaryR = stub.GetFile(pb2.FileBaseR(file=file.model_dump()))
        return FileBinary(**dictFromMessage(response.file))