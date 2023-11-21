"""
    Файл логики gRPC-сервера
"""
import proto.file_api_pb2 as pb2
import proto.file_api_pb2_grpc as pb2_grpc

from grpc_client import NoSQLDatabaseAPIgRPCClient
from schemas import FileBinary, File, FileBase, Range, Storage
from utils import dictFromGoogleMessage
from storage import FileStorageFabric

from .AbstractServicer import AbstractServicer as Servicer


class FileAPIServicer(pb2_grpc.FileAPIServicer) :
    """
        Логика сервера (сервисер))
    """
    
    @Servicer.methodAsyncDecorator("file-api:Ping")
    async def Ping(self, request : pb2.PingR, context) :
        return pb2.PongR(pong="pong")


    @Servicer.methodAsyncDecorator("file-api:AddFile")
    async def AddFile(self, request : pb2.FileBinaryR, context) :
        storage = FileStorageFabric.get(Storage(request.file.storage))
        file = File(**dictFromGoogleMessage(request.file))
        await NoSQLDatabaseAPIgRPCClient.AddFileMetaInfo(file)
        file : File = await storage.appendOne(FileBinary(**file.model_dump(),
                                                         file=request.file.file))
        return pb2.FileR(file=file.model_dump())


    @Servicer.methodAsyncDecorator("file-api:GetFile")
    async def GetFile(self, request : pb2.FileBaseR, context):
        storage = FileStorageFabric.get(Storage(request.file.storage))
        file = FileBase(**dictFromGoogleMessage(request.file))
        await NoSQLDatabaseAPIgRPCClient.GetFileMetaInfo(file)
        file : FileBinary = await storage.getOne(file)
        return pb2.FileBinaryR(file=file.model_dump())


    @Servicer.methodAsyncDecorator("file-api:PutFile")
    async def PutFile(self, request : pb2.FileBinaryR, context):
        storage = FileStorageFabric.get(Storage(request.file.storage))
        file = File(**dictFromGoogleMessage(request.file))
        await NoSQLDatabaseAPIgRPCClient.PutFileMetaInfo(file)
        file : FileBinary = await storage.putOne(FileBinary(**file.model_dump(),
                                                            file=request.file.file))
        return pb2.FileR(file=file.model_dump())


    @Servicer.methodAsyncDecorator("file-api:DeleteFile")
    async def DeleteFile(self, request : pb2.FileBaseR, context):
        storage = FileStorageFabric.get(Storage(request.file.storage))
        file = FileBase(**dictFromGoogleMessage(request.file))
        await NoSQLDatabaseAPIgRPCClient.DeleteFileMetaInfo(file)
        file : File = await storage.deleteOne(file)
        return pb2.FileR(file=file.model_dump())


    @Servicer.methodAsyncDecorator("file-api:GetFileMetaInfo")
    async def GetFileMetaInfo(self, request : pb2.FileBaseR, context):
        file = FileBase(**dictFromGoogleMessage(request.file))
        file : File = await NoSQLDatabaseAPIgRPCClient.GetFileMetaInfo(file)
        return pb2.FileR(file=file.model_dump())


    @Servicer.methodAsyncDecorator("file-api:GetManyFilesMetaInfo")
    async def GetManyFilesMetaInfo(self, request : pb2.StorageSegmentR, context):
        files = await NoSQLDatabaseAPIgRPCClient.GetManyFilesMetaInfo(storage=Storage(request.storage),
                                                                      range=Range(start=request.start,
                                                                                  end=request.end))
        return pb2.FileSegmentR(**files.model_dump())


    @Servicer.methodAsyncDecorator("file-api:GetFilesMetaInfoCount")
    async def GetFilesMetaInfoCount(self, request : pb2.StorageR, context) :
        count = (await NoSQLDatabaseAPIgRPCClient.GetFilesMetaInfoCount(Storage(request.storage))).count
        return pb2.CountR(count=count)