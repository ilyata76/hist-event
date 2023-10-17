"""
    Файл логики gRPC-сервера
"""
import grpc
import proto.file_api_pb2 as pb2
import proto.nosql_database_api_pb2 as nosql_pb2
import proto.file_api_pb2_grpc as pb2_grpc

from grpc_server.AbstractServicer import AbstractServicer
from grpc_client.NoSQLDatabaseAPIgRPCClient import NoSQLDatabaseAPIgRPCClient
from storage import FileStorage
from schemas.File import FileBinary, File, FileBase
from schemas.Range import Range
from utils.dict_from_message import dict_from_message


class FileAPIServicer(pb2_grpc.FileAPIServicer) :
    """
        Логика сервера (сервисер))
    """
    
    @AbstractServicer.method("file-api:Ping")
    async def Ping(self, request : pb2.PingR, context : grpc.ServicerContext) :
        return pb2.PongR(pong="pong")

    @AbstractServicer.method("file-api:AddFile")
    async def AddFile(self, request : pb2.FileBinaryR, context : grpc.ServicerContext) :
        storage = FileStorage.get(storage_identifier=request.file.storage)
        await NoSQLDatabaseAPIgRPCClient.AddFileMetaInfo(File(**dict_from_message(request.file)))
        file : File = await storage.appendOne(FileBinary(**dict_from_message(request.file)))
        return pb2.FileR(file=file.model_dump())

    @AbstractServicer.method("file-api:GetFile")
    async def GetFile(self, request : pb2.FileBaseR, context : grpc.ServicerContext):
        storage = FileStorage.get(storage_identifier=request.file.storage)
        await NoSQLDatabaseAPIgRPCClient.GetFileMetaInfo(FileBase(**dict_from_message(request.file)))
        file : FileBinary = await storage.getOne(FileBase(**dict_from_message(request.file)))
        return pb2.FileBinaryR(file=file.model_dump())

    @AbstractServicer.method("file-api:PutFile")
    async def PutFile(self, request : pb2.FileBinaryR, context : grpc.ServicerContext):
        storage = FileStorage.get(storage_identifier=request.file.storage)
        await NoSQLDatabaseAPIgRPCClient.PutFileMetaInfo(File(**dict_from_message(request.file)))
        file : FileBinary = await storage.putOne(FileBinary(**dict_from_message(request.file)))
        return pb2.FileR(file=file.model_dump())

    @AbstractServicer.method("file-api:DeleteFile")
    async def DeleteFile(self, request : pb2.FileBaseR, context : grpc.ServicerContext):
        storage = FileStorage.get(storage_identifier=request.file.storage)
        await NoSQLDatabaseAPIgRPCClient.DeleteFileMetaInfo(FileBase(**dict_from_message(request.file)))
        file : File = await storage.deleteOne(FileBase(**dict_from_message(request.file)))
        return pb2.FileR(file=file.model_dump())
    
    @AbstractServicer.method("file-api:GetFileMetaInfo")
    async def GetFileMetaInfo(self, request : pb2.FileBaseR, context : grpc.ServicerContext):
        file : nosql_pb2.FileR = await NoSQLDatabaseAPIgRPCClient.GetFileMetaInfo(FileBase(**dict_from_message(request.file)))
        return pb2.FileR(file=dict_from_message(file.file))
    
    @AbstractServicer.method("file-api:GetManyFilesMetaInfo")
    async def GetManyFilesMetaInfo(self, request : pb2.StorageSegmentR, context : grpc.ServicerContext):
        files : nosql_pb2.FileSegmentR = await NoSQLDatabaseAPIgRPCClient.GetManyFilesMetaInfo(storage=request.storage,
                                                                                               range=Range(start=request.start,
                                                                                                           end=request.end))
        return pb2.FileSegmentR(files=[pb2.File(**dict_from_message(file)) for file in files.files])