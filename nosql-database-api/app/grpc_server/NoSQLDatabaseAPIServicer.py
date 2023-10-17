"""
    Файл логики gRPC-сервера
"""
import grpc
import proto.nosql_database_api_pb2 as pb2
import proto.nosql_database_api_pb2_grpc as pb2_grpc

from grpc_server.AbstractServicer import AbstractServicer
import database
from schemas.File import File, FileBase
from schemas.Range import Range
from utils.dict_from_message import dict_from_message


class NoSQLDatabaseAPIServicer(pb2_grpc.NoSQLDatabaseAPIServicer) :
    """
        Логика сервера (сервисер))
    """
  
    @AbstractServicer.method("nosql-database-api:Ping")
    async def Ping(self, request : pb2.PingR, context : grpc.ServicerContext):
        return pb2.PongR(pong="Pong!")

    @AbstractServicer.method("nosql-database-api:AddFileMetaInfo")
    async def AddFileMetaInfo(self, request : pb2.FileR, context : grpc.ServicerContext):
        file : File = await database.files.appendOne(file=File(**dict_from_message(request.file)))
        return pb2.FileR(file=file.model_dump())

    @AbstractServicer.method("nosql-database-api:GetFileMetaInfo")
    async def GetFileMetaInfo(self, request : pb2.FileBaseR, context : grpc.ServicerContext):
        file : File = await database.files.getOne(file=FileBase(**dict_from_message(request.file)))
        return pb2.FileR(file=file.model_dump())

    @AbstractServicer.method("nosql-database-api:PutFileMetaInfo")
    async def PutFileMetaInfo(self, request : pb2.FileR, context : grpc.ServicerContext):
        file : File = await database.files.putOne(file=File(**dict_from_message(request.file)))
        return pb2.FileR(file=file.model_dump())

    @AbstractServicer.method("nosql-database-api:DeleteFileMetaInfo")
    async def DeleteFileMetaInfo(self, request : pb2.FileBaseR, context : grpc.ServicerContext):
        file : File = await database.files.deleteOne(file=FileBase(**dict_from_message(request.file)))
        return pb2.FileR(file=file.model_dump())
    
    @AbstractServicer.method("nosql-database-api:GetManyFilesMetaInfo")
    async def GetManyFilesMetaInfo(self, request : pb2.StorageSegmentR, context : grpc.ServicerContext):
        files : list[File] = await database.files.getMany(range=Range(start=request.start, 
                                                          end=request.end), 
                                                          storage_identifier=request.storage)
        return pb2.FileSegmentR(files=[x.model_dump() for x in files])