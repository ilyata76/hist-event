"""
    Файл клиента для gRPC NoSQLDatabase сервера и доступа к нему
"""
from functools import wraps

import grpc
import proto.nosql_database_api_pb2 as pb2
import proto.nosql_database_api_pb2_grpc as pb2_grpc

from utils.config import config
from grpc_client.AbstractgRPCClient import AbstractgRPCClient as GrpcClient
from schemas.Ping import Pong
from schemas.StatusIdentifier import StatusIdentifier, Identifier
from schemas.File import FileBaseKeyword, FileBase
from utils.dict_from import dictFromMessage


class NoSQLDatabaseAPIgRPCClient :
    """
        Класс доступа до gRPC сервера с NoSQLDatabase.
            Его методы вызываются в коде при обработке запросов.
    """

    @staticmethod
    @GrpcClient.methodAsyncDecorator("nosql-database-api:Ping",
                                     f"{config.NOSQL_DATABASE_GRPC_HOST}:{config.NOSQL_DATABASE_GRPC_PORT}")
    async def Ping(channel = None) -> Pong :
        stub = pb2_grpc.NoSQLDatabaseAPIStub(channel)
        response : pb2.PongR = stub.Ping(pb2.PingR())
        return Pong(**dictFromMessage(response))


    @staticmethod
    @GrpcClient.methodAsyncDecorator("nosql-database-api:PutSQLGeneratorStatus",
                                     f"{config.NOSQL_DATABASE_GRPC_HOST}:{config.NOSQL_DATABASE_GRPC_PORT}")
    async def PutSQLGeneratorStatus(status_identifier : StatusIdentifier, channel = None) -> StatusIdentifier :
        stub = pb2_grpc.NoSQLDatabaseAPIStub(channel)
        response : pb2.IdentifierStatusR = stub.PutSQLGeneratorStatus(pb2.IdentifierStatusR(**status_identifier.model_dump()))
        return StatusIdentifier(**dictFromMessage(response))


    @staticmethod
    @GrpcClient.methodAsyncDecorator("nosql-database-api:GetSQLGeneratorStatus",
                                     f"{config.NOSQL_DATABASE_GRPC_HOST}:{config.NOSQL_DATABASE_GRPC_PORT}")
    async def GetSQLGeneratorStatus(identifier : Identifier, channel = None) -> StatusIdentifier :
        stub = pb2_grpc.NoSQLDatabaseAPIStub(channel)
        response : pb2.IdentifierStatusR = stub.GetSQLGeneratorStatus(pb2.IdentifierR(**identifier.model_dump()))
        return StatusIdentifier(**dictFromMessage(response))


    @staticmethod
    @GrpcClient.methodAsyncDecorator("nosql-database-api:PutSQLGeneratorFiles",
                                     f"{config.NOSQL_DATABASE_GRPC_HOST}:{config.NOSQL_DATABASE_GRPC_PORT}")
    async def PutSQLGeneratorFiles(files : list[FileBaseKeyword], identifier : Identifier, channel = None) -> Identifier:
        stub = pb2_grpc.NoSQLDatabaseAPIStub(channel)
        response : pb2.IdentifierR = stub.PutSQLGeneratorFiles(pb2.ManyFilesIdentifierR(files=[file.model_dump() for file in files],
                                                                                        identifier=identifier.identifier))
        return Identifier(**dictFromMessage(response))


    @staticmethod
    @GrpcClient.methodAsyncDecorator("nosql-database-api:GetSQLGeneratorFiles",
                                     f"{config.NOSQL_DATABASE_GRPC_HOST}:{config.NOSQL_DATABASE_GRPC_PORT}")
    async def GetSQLGeneratorFiles(identifier : Identifier, channel = None) -> list[FileBaseKeyword]:
        stub = pb2_grpc.NoSQLDatabaseAPIStub(channel)
        response : pb2.ManyFilesIdentifierR = stub.GetSQLGeneratorFiles(pb2.IdentifierR(identifier=identifier.identifier))
        return [FileBaseKeyword(**dictFromMessage(file)) for file in response.files]


    @staticmethod
    @GrpcClient.methodAsyncDecorator("nosql-database-api:GetSQLGeneratorSQLFile",
                                     f"{config.NOSQL_DATABASE_GRPC_HOST}:{config.NOSQL_DATABASE_GRPC_PORT}")
    async def GetSQLGeneratorSQLFile(identifier : Identifier, channel = None) -> FileBase :
        stub = pb2_grpc.NoSQLDatabaseAPIStub(channel)
        response : pb2.FileBaseIdentifierR = stub.GetSQLGeneratorSQLFile(pb2.IdentifierR(identifier=identifier.identifier))
        return FileBase(**dictFromMessage(response.file))


    @staticmethod
    @GrpcClient.methodAsyncDecorator("nosql-database-api:PutSQLGeneratorSQLFile",
                                     f"{config.NOSQL_DATABASE_GRPC_HOST}:{config.NOSQL_DATABASE_GRPC_PORT}")
    async def PutSQLGeneratorSQLFile(file : FileBase, identifier : Identifier, channel = None) -> FileBase :
        stub = pb2_grpc.NoSQLDatabaseAPIStub(channel)
        response : pb2.FileBaseIdentifierR = stub.PutSQLGeneratorSQLFile(pb2.FileBaseIdentifierR(file=file.model_dump(),
                                                                                                 identifier=identifier.identifier))
        return FileBase(**dictFromMessage(response.file))