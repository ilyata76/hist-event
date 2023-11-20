"""
    Файл клиента для gRPC NoSQLDatabase сервера и доступа к нему
"""
import proto.nosql_database_api_pb2 as pb2
import proto.nosql_database_api_pb2_grpc as pb2_grpc

from config import NOSQL_IP
from schemas import *
from utils import dictFromGoogleMessage

from .AbstractgRPCClient import AbstractgRPCClient as GrpcClient


class NoSQLDatabaseAPIgRPCClient :
    """
        Класс доступа до gRPC сервера с NoSQLDatabase.
            Его методы вызываются в коде при обработке запросов.
    """

    @staticmethod
    @GrpcClient.methodAsyncDecorator("nosql-database-api:PutSQLGeneratorStatus", NOSQL_IP)
    async def PutSQLGeneratorStatus(identifier : Identifier, status : Status, channel = None) -> Status :
        stub = pb2_grpc.NoSQLDatabaseAPIStub(channel)
        request = pb2.IdentifierStatusR(identifier=identifier, status=status)
        response : pb2.IdentifierStatusR = stub.PutSQLGeneratorStatus(request)
        return Status(response.status)


    @staticmethod
    @GrpcClient.methodAsyncDecorator("nosql-database-api:GetSQLGeneratorStatus", NOSQL_IP)
    async def GetSQLGeneratorStatus(identifier : Identifier, channel = None) -> Status :
        stub = pb2_grpc.NoSQLDatabaseAPIStub(channel)
        request = pb2.IdentifierR(identifier=identifier)
        response : pb2.IdentifierStatusR = stub.GetSQLGeneratorStatus(request)
        return Status(response.status)


    @staticmethod
    @GrpcClient.methodAsyncDecorator("nosql-database-api:PutSQLGeneratorFiles", NOSQL_IP)
    async def PutSQLGeneratorFiles(files : FileBaseKeywordList, identifier : Identifier, channel = None) -> Identifier :
        stub = pb2_grpc.NoSQLDatabaseAPIStub(channel)
        request = pb2.ManyFilesIdentifierR(identifier=identifier, **files.model_dump())
        response : pb2.IdentifierR = stub.PutSQLGeneratorFiles(request)
        return Identifier(response.identifier)


    @staticmethod
    @GrpcClient.methodAsyncDecorator("nosql-database-api:GetSQLGeneratorFiles", NOSQL_IP)
    async def GetSQLGeneratorFiles(identifier : Identifier, channel = None) -> FileBaseKeywordList :
        stub = pb2_grpc.NoSQLDatabaseAPIStub(channel)
        request = pb2.IdentifierR(identifier=identifier)
        response : pb2.ManyFilesIdentifierR = stub.GetSQLGeneratorFiles(request)
        return FileBaseKeywordList(files=[FileBaseKeyword(**dictFromGoogleMessage(file)) for file in response.files])


    @staticmethod
    @GrpcClient.methodAsyncDecorator("nosql-database-api:GetSQLGeneratorSQLFile", NOSQL_IP)
    async def GetSQLGeneratorSQLFile(identifier : Identifier, channel = None) -> FileBase :
        stub = pb2_grpc.NoSQLDatabaseAPIStub(channel)
        request = pb2.IdentifierR(identifier=identifier)
        response : pb2.FileBaseIdentifierR = stub.GetSQLGeneratorSQLFile(request)
        return FileBase(**dictFromGoogleMessage(response.file))


    @staticmethod
    @GrpcClient.methodAsyncDecorator("nosql-database-api:PutSQLGeneratorSQLFile", NOSQL_IP)
    async def PutSQLGeneratorSQLFile(file : FileBase, identifier : Identifier, channel = None) -> FileBase :
        stub = pb2_grpc.NoSQLDatabaseAPIStub(channel)
        request = pb2.FileBaseIdentifierR(file=file.model_dump(), identifier=identifier)
        response : pb2.FileBaseIdentifierR = stub.PutSQLGeneratorSQLFile(request)
        return FileBase(**dictFromGoogleMessage(response.file))