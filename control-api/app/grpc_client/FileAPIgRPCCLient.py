"""
    Файл клиента для gRPC FileAPi сервера и доступа к нему
"""
import grpc
import app.proto.file_api_pb2 as pb2
import app.proto.file_api_pb2_grpc as pb2_grpc

from app.utils.config import config
from app.grpc_client.AbstractgRPCClient import AbstractgRPCClient
from app.schemas.File import FileBinary, FileBase


class FileAPIgRPCCLient :
    """
        Класс доступа до gRPC сервера с FileAPI
    """

    @staticmethod
    @AbstractgRPCClient.method("file-api:Ping")
    async def Ping() :
        with grpc.insecure_channel(f"{config.FILE_API_GRPC_HOST}:{config.FILE_API_GRPC_PORT}") as channel :
            stub = pb2_grpc.FileAPIStub(channel)
            response : pb2.PingResponse = stub.Ping(pb2.PingRequest())
        return response

    @staticmethod
    @AbstractgRPCClient.method("file-api:AddFile")
    async def AddFile(file : FileBinary) :
        with grpc.insecure_channel(f"{config.FILE_API_GRPC_HOST}:{config.FILE_API_GRPC_PORT}") as channel :
            stub = pb2_grpc.FileAPIStub(channel)
            response : pb2.AddFileResponse = stub.AddFile(pb2.AddFileRequest(storage=file.storage, 
                                                                             path=str(file.path), 
                                                                             filename=file.filename,
                                                                             file=file.file))
        return response
    
    @staticmethod
    @AbstractgRPCClient.method("file-api:GetFile")
    async def GetFile(file : FileBase) :
        with grpc.insecure_channel(f"{config.FILE_API_GRPC_HOST}:{config.FILE_API_GRPC_PORT}") as channel :
            stub = pb2_grpc.FileAPIStub(channel)
            response : pb2.GetFileResponse = stub.GetFile(pb2.GetFileRequest(storage=file.storage, 
                                                                             path=str(file.path)))
        return response
    
    @staticmethod
    @AbstractgRPCClient.method("file-api:PutFile")
    async def PutFile(file : FileBinary) :
        with grpc.insecure_channel(f"{config.FILE_API_GRPC_HOST}:{config.FILE_API_GRPC_PORT}") as channel :
            stub = pb2_grpc.FileAPIStub(channel)
            response : pb2.PutFileResponse = stub.PutFile(pb2.PutFileRequest(storage=file.storage, 
                                                                             path=str(file.path),
                                                                             filename=file.filename,
                                                                             file=file.file))
        return response
    
    @staticmethod
    @AbstractgRPCClient.method("file-api:DeleteFile")
    async def DeleteFile(file : FileBase) :
        with grpc.insecure_channel(f"{config.FILE_API_GRPC_HOST}:{config.FILE_API_GRPC_PORT}") as channel :
            stub = pb2_grpc.FileAPIStub(channel)
            response : pb2.DeleteFileResponse = stub.DeleteFile(pb2.DeleteFileRequest(storage=file.storage, 
                                                                                      path=str(file.path)))
        return response