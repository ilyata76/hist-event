"""
    Файл клиента для gRPC NoSQLDatabase сервера и доступа к нему
"""
import proto.nosql_database_api_pb2 as pb2
import proto.nosql_database_api_pb2_grpc as pb2_grpc

from config import NOSQL_IP
from utils import dictFromGoogleMessage
from schemas import *

from .AbstractgRPCClient import AbstractgRPCClient


class NoSQLDatabaseAPIgRPCClient :
    """
        Класс доступа до gRPC сервера с NoSQLDatabase.
            Его методы вызываются в коде при обработке запросов.
    """
    
    @staticmethod
    @AbstractgRPCClient.methodAsyncDecorator("nosql-database-api:AddFileMetaInfo", NOSQL_IP)
    async def AddFileMetaInfo(file : File, channel = None) -> File :
        stub = pb2_grpc.NoSQLDatabaseAPIStub(channel)
        request = pb2.FileR(file=file.model_dump())
        response : pb2.FileR = stub.AddFileMetaInfo(request)
        return File(**dictFromGoogleMessage(response.file))


    @staticmethod
    @AbstractgRPCClient.methodAsyncDecorator("nosql-database-api:GetFileMetaInfo", NOSQL_IP)
    async def GetFileMetaInfo(file : FileBase, channel = None) -> File :
        stub = pb2_grpc.NoSQLDatabaseAPIStub(channel)
        request = pb2.FileBaseR(file=file.model_dump())
        response : pb2.FileR = stub.GetFileMetaInfo(request)
        return File(**dictFromGoogleMessage(response.file))


    @staticmethod
    @AbstractgRPCClient.methodAsyncDecorator("nosql-database-api:PutFileMetaInfo", NOSQL_IP)
    async def PutFileMetaInfo(file : File, channel = None) -> File :
        stub = pb2_grpc.NoSQLDatabaseAPIStub(channel)
        request = pb2.FileR(file=file.model_dump())
        response : pb2.FileR = stub.PutFileMetaInfo(request)
        return File(**dictFromGoogleMessage(response.file))


    @staticmethod
    @AbstractgRPCClient.methodAsyncDecorator("nosql-database-api:DeleteFileMetaInfo", NOSQL_IP)
    async def DeleteFileMetaInfo(file : FileBase, channel = None) -> File :
        stub = pb2_grpc.NoSQLDatabaseAPIStub(channel)
        request = pb2.FileBaseR(file=file.model_dump())
        response : pb2.FileR = stub.DeleteFileMetaInfo(request)
        return File(**dictFromGoogleMessage(response.file))


    @staticmethod
    @AbstractgRPCClient.methodAsyncDecorator("nosql-database-api:GetManyFilesMetaInfo", NOSQL_IP)
    async def GetManyFilesMetaInfo(storage : Storage, range : Range, channel = None) -> FileList :
        stub = pb2_grpc.NoSQLDatabaseAPIStub(channel)
        request = pb2.StorageSegmentR(storage=storage, start=range.start, end=range.end)
        response : pb2.FileSegmentR = stub.GetManyFilesMetaInfo(request)
        return FileList(files=[File(**dictFromGoogleMessage(file)) for file in response.files])


    @staticmethod
    @AbstractgRPCClient.methodAsyncDecorator("nosql-database-api:GetFilesMetaInfoCount", NOSQL_IP)
    async def GetFilesMetaInfoCount(storage : Storage, channel = None) -> Count :
        stub = pb2_grpc.NoSQLDatabaseAPIStub(channel)
        request = pb2.StorageR(storage=storage)
        response : pb2.CountR = stub.GetFilesMetaInfoCount(request)
        return Count(count=response.count)