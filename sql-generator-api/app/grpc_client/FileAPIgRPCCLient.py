"""
    Файл клиента для gRPC FileAPi сервера и доступа к нему
"""
import proto.file_api_pb2 as pb2
import proto.file_api_pb2_grpc as pb2_grpc

from config import FILE_IP
from utils import dictFromGoogleMessage
from schemas import FileBinary, FileBase, File

from .AbstractgRPCClient import AbstractgRPCClient as GrpcClient


class FileAPIgRPCCLient :
    """
        Класс доступа до gRPC сервера с FileAPI.
            Его методы вызываются в коде при обработке запросов.
    """

    @staticmethod
    @GrpcClient.methodAsyncDecorator("file-api:GetFile", FILE_IP)
    async def GetFile(file : FileBase, channel = None) -> FileBinary :
        stub = pb2_grpc.FileAPIStub(channel)
        request = pb2.FileBaseR(file=file.model_dump())
        response : pb2.FileBinaryR = stub.GetFile(request)
        return FileBinary(**dictFromGoogleMessage(response.file))


    @staticmethod
    @GrpcClient.methodAsyncDecorator("file-api:PutFile", FILE_IP)
    async def PutFile(file : FileBinary, channel = None) -> File :
        stub = pb2_grpc.FileAPIStub(channel)
        request = pb2.FileBinaryR(file=file.model_dump())
        response : pb2.FileR = stub.PutFile(request)
        return File(**dictFromGoogleMessage(response.file))