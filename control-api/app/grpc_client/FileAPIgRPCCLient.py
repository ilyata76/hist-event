"""
    Файл клиента для gRPC FileAPi сервера и доступа к нему
"""
import grpc
import app.proto.file_api_pb2 as pb2
import app.proto.file_api_pb2_grpc as pb2_grpc

from app.utils.config import config
from app.grpc_client.AbstractgRPCClient import AbstractgRPCClient
from app.schemas.File import FileBinary, FileBase
from app.schemas.Range import Range


class FileAPIgRPCCLient :
    """
        Класс доступа до gRPC сервера с FileAPI.
            Его методы вызываются в коде при обработке запросов.
    """

    @staticmethod
    @AbstractgRPCClient.method("file-api:Ping")
    async def Ping() :
        with grpc.insecure_channel(f"{config.FILE_API_GRPC_HOST}:{config.FILE_API_GRPC_PORT}") as channel :
            stub = pb2_grpc.FileAPIStub(channel)
            response : pb2.PongR = stub.Ping(pb2.PingR())
        return response


    @staticmethod
    @AbstractgRPCClient.method("file-api:AddFile")
    async def AddFile(file : FileBinary) :
        with grpc.insecure_channel(f"{config.FILE_API_GRPC_HOST}:{config.FILE_API_GRPC_PORT}") as channel :
            stub = pb2_grpc.FileAPIStub(channel)
            response : pb2.FileR = stub.AddFile(pb2.FileBinaryR(file=file.model_dump()))
        return response


    @staticmethod
    @AbstractgRPCClient.method("file-api:GetFile")
    async def GetFile(file : FileBase) :
        with grpc.insecure_channel(f"{config.FILE_API_GRPC_HOST}:{config.FILE_API_GRPC_PORT}") as channel :
            stub = pb2_grpc.FileAPIStub(channel)
            response : pb2.FileBinaryR = stub.GetFile(pb2.FileBaseR(file=file.model_dump()))
        return response


    @staticmethod
    @AbstractgRPCClient.method("file-api:PutFile")
    async def PutFile(file : FileBinary) :
        with grpc.insecure_channel(f"{config.FILE_API_GRPC_HOST}:{config.FILE_API_GRPC_PORT}") as channel :
            stub = pb2_grpc.FileAPIStub(channel)
            response : pb2.FileR = stub.PutFile(pb2.FileBinaryR(file=file.model_dump()))
        return response


    @staticmethod
    @AbstractgRPCClient.method("file-api:DeleteFile")
    async def DeleteFile(file : FileBase) :
        with grpc.insecure_channel(f"{config.FILE_API_GRPC_HOST}:{config.FILE_API_GRPC_PORT}") as channel :
            stub = pb2_grpc.FileAPIStub(channel)
            response : pb2.FileR = stub.DeleteFile(pb2.FileBaseR(file=file.model_dump()))
        return response


    @staticmethod
    @AbstractgRPCClient.method("file-api:GetFileMetaInfo")
    async def GetFileMetaInfo(file : FileBase) :
        with grpc.insecure_channel(f"{config.FILE_API_GRPC_HOST}:{config.FILE_API_GRPC_PORT}") as channel :
            stub = pb2_grpc.FileAPIStub(channel)
            response : pb2.FileR = stub.GetFileMetaInfo(pb2.FileBaseR(file=file.model_dump()))
        return response


    @staticmethod
    @AbstractgRPCClient.method("file-api:GetManyFilesMetaInfo")
    async def GetManyFilesMetaInfo(storage : str, range : Range) : 
        with grpc.insecure_channel(f"{config.FILE_API_GRPC_HOST}:{config.FILE_API_GRPC_PORT}") as channel :
            stub = pb2_grpc.FileAPIStub(channel)
            response : pb2.FileSegmentR = stub.GetManyFilesMetaInfo(pb2.StorageSegmentR(storage=storage,
                                                                                        start=range.start,
                                                                                        end=range.end))
        return response