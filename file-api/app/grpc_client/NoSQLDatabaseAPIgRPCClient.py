"""
    Файл клиента для gRPC NoSQLDatabase сервера и доступа к нему
"""
import grpc
import proto.nosql_database_api_pb2 as pb2
import proto.nosql_database_api_pb2_grpc as pb2_grpc

from utils.config import config
from schemas.File import FileBase, File
from schemas.Range import Range
from grpc_client.AbstractgRPCClient import AbstractgRPCClient


class NoSQLDatabaseAPIgRPCClient :
    """
        Класс доступа до gRPC сервера с NoSQLDatabase
    """

    @staticmethod
    @AbstractgRPCClient.method("nosql-database-api:Ping")
    async def Ping() :
        with grpc.insecure_channel(f"{config.NOSQL_DATABASE_GRPC_HOST}:{config.NOSQL_DATABASE_GRPC_PORT}") as channel :
            stub = pb2_grpc.NoSQLDatabaseAPIStub(channel)
            response : pb2.PongR = stub.Ping(pb2.PingR())
        return response
    
    @staticmethod
    @AbstractgRPCClient.method("nosql-database-api:AddFileMetaInfo")
    async def AddFileMetaInfo(file : File) :
        with grpc.insecure_channel(f"{config.NOSQL_DATABASE_GRPC_HOST}:{config.NOSQL_DATABASE_GRPC_PORT}") as channel :
            stub = pb2_grpc.NoSQLDatabaseAPIStub(channel)
            response : pb2.FileR = stub.AddFileMetaInfo(pb2.FileR(file=file.model_dump()))
        return response

    @staticmethod
    @AbstractgRPCClient.method("nosql-database-api:GetFileMetaInfo")
    async def GetFileMetaInfo(file : FileBase) :
        with grpc.insecure_channel(f"{config.NOSQL_DATABASE_GRPC_HOST}:{config.NOSQL_DATABASE_GRPC_PORT}") as channel :
            stub = pb2_grpc.NoSQLDatabaseAPIStub(channel)
            response : pb2.FileR = stub.GetFileMetaInfo(pb2.FileBaseR(file=file.model_dump()))
        return response

    @staticmethod
    @AbstractgRPCClient.method("nosql-database-api:PutFileMetaInfo")
    async def PutFileMetaInfo(file : File) :
        with grpc.insecure_channel(f"{config.NOSQL_DATABASE_GRPC_HOST}:{config.NOSQL_DATABASE_GRPC_PORT}") as channel :
            stub = pb2_grpc.NoSQLDatabaseAPIStub(channel)
            response : pb2.FileR = stub.PutFileMetaInfo(pb2.FileR(file=file.model_dump()))
        return response

    @staticmethod
    @AbstractgRPCClient.method("nosql-database-api:DeleteFileMetaInfo")
    async def DeleteFileMetaInfo(file : FileBase) :
        with grpc.insecure_channel(f"{config.NOSQL_DATABASE_GRPC_HOST}:{config.NOSQL_DATABASE_GRPC_PORT}") as channel :
            stub = pb2_grpc.NoSQLDatabaseAPIStub(channel)
            response : pb2.FileR = stub.DeleteFileMetaInfo(pb2.FileBaseR(file=file.model_dump()))
        return response

    @staticmethod
    @AbstractgRPCClient.method("nosql-database-api:GetManyFilesMetaInfo")
    async def GetManyFilesMetaInfo(storage : str, range : Range) :
        with grpc.insecure_channel(f"{config.NOSQL_DATABASE_GRPC_HOST}:{config.NOSQL_DATABASE_GRPC_PORT}") as channel :
            stub = pb2_grpc.NoSQLDatabaseAPIStub(channel)
            response : pb2.FileSegmentR = stub.GetManyFilesMetaInfo(pb2.StorageSegmentR(storage=storage,
                                                                                        start=range.start,
                                                                                        end=range.end))
        return response