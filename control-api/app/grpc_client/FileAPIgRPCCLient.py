"""
    Файл клиента для gRPC FileAPi сервера и доступа к нему
"""
import app.proto.file_api_pb2 as pb2
import app.proto.file_api_pb2_grpc as pb2_grpc

from app.utils import dictFromGoogleMessage
from app.config import FILE_IP
from app.schemas import *

from .AbstractgRPCClient import AbstractgRPCClient


class FileAPIgRPCCLient :
    """
        Класс доступа до gRPC сервера с FileAPI.
            Его методы вызываются в коде при обработке запросов.
    """

    @staticmethod
    @AbstractgRPCClient.methodAsyncDecorator("file-api:Ping", FILE_IP)
    async def Ping(channel = None) -> PongService :
        stub = pb2_grpc.FileAPIStub(channel)
        request = pb2.PingR()
        response : pb2.PongR = stub.Ping(request)
        return PongService(pong=response.pong, service="file-api")


    @staticmethod
    @AbstractgRPCClient.methodAsyncDecorator("file-api:AddFile", FILE_IP)
    async def AddFile(file : FileBinary, channel = None) -> File :
        stub = pb2_grpc.FileAPIStub(channel)
        request = pb2.FileBinaryR(file=file.model_dump())
        response : pb2.FileR = stub.AddFile(request)
        return File(**dictFromGoogleMessage(response.file))


    @staticmethod
    @AbstractgRPCClient.methodAsyncDecorator("file-api:GetFile", FILE_IP)
    async def GetFile(file : FileBase, channel = None) -> FileBinary :
        stub = pb2_grpc.FileAPIStub(channel)
        request = pb2.FileBaseR(file=file.model_dump())
        response : pb2.FileBinaryR = stub.GetFile(request)
        return FileBinary(**dictFromGoogleMessage(response.file))


    @staticmethod
    @AbstractgRPCClient.methodAsyncDecorator("file-api:PutFile", FILE_IP)
    async def PutFile(file : FileBinary, channel = None) -> File :
        stub = pb2_grpc.FileAPIStub(channel)
        request = pb2.FileBinaryR(file=file.model_dump())
        response : pb2.FileR = stub.PutFile(request)
        return File(**dictFromGoogleMessage(response.file))


    @staticmethod
    @AbstractgRPCClient.methodAsyncDecorator("file-api:DeleteFile", FILE_IP)
    async def DeleteFile(file : FileBase, channel = None) -> File :
        stub = pb2_grpc.FileAPIStub(channel)
        request = pb2.FileBaseR(file=file.model_dump())
        response : pb2.FileR = stub.DeleteFile(request)
        return File(**dictFromGoogleMessage(response.file))


    @staticmethod
    @AbstractgRPCClient.methodAsyncDecorator("file-api:GetFileMetaInfo", FILE_IP)
    async def GetFileMetaInfo(file : FileBase, channel = None) -> File :
        stub = pb2_grpc.FileAPIStub(channel)
        request = pb2.FileBaseR(file=file.model_dump())
        response : pb2.FileR = stub.GetFileMetaInfo(request)
        return File(**dictFromGoogleMessage(response.file))


    @staticmethod
    @AbstractgRPCClient.methodAsyncDecorator("file-api:GetManyFilesMetaInfo", FILE_IP)
    async def GetManyFilesMetaInfo(storage : str, range : Range, channel = None) -> FileList : 
        stub = pb2_grpc.FileAPIStub(channel)
        request = pb2.StorageSegmentR(storage=storage, start=range.start, end=range.end)
        response : pb2.FileSegmentR = stub.GetManyFilesMetaInfo(request)
        return FileList(files=[File(**dictFromGoogleMessage(file)) for file in response.files])