"""
    Файл логики gRPC-сервера
"""
import proto.nosql_database_api_pb2 as pb2
import proto.nosql_database_api_pb2_grpc as pb2_grpc

import database
from schemas import *
from utils import dictFromGoogleMessage

from .AbstractServicer import AbstractServicer as Servicer


class NoSQLDatabaseAPIServicer(pb2_grpc.NoSQLDatabaseAPIServicer) :
    """
        Логика сервера (сервисер))
    """

    @Servicer.methodAsyncDecorator("nosql-database-api:Ping")
    async def Ping(self, request : pb2.PingR, context) :
        return pb2.PongR(pong="Pong!")


    @Servicer.methodAsyncDecorator("nosql-database-api:AddFileMetaInfo")
    async def AddFileMetaInfo(self, request : pb2.FileR, context) :
        file : File = await database.files.appendOne(File(**dictFromGoogleMessage(request.file)))
        return pb2.FileR(file=file.model_dump())


    @Servicer.methodAsyncDecorator("nosql-database-api:GetFileMetaInfo")
    async def GetFileMetaInfo(self, request : pb2.FileBaseR, context) :
        file : File = await database.files.getOne(FileBase(**dictFromGoogleMessage(request.file)))
        return pb2.FileR(file=file.model_dump())


    @Servicer.methodAsyncDecorator("nosql-database-api:PutFileMetaInfo")
    async def PutFileMetaInfo(self, request : pb2.FileR, context) :
        file : File = await database.files.putOne(File(**dictFromGoogleMessage(request.file)))
        return pb2.FileR(file=file.model_dump())


    @Servicer.methodAsyncDecorator("nosql-database-api:DeleteFileMetaInfo")
    async def DeleteFileMetaInfo(self, request : pb2.FileBaseR, context) :
        file : File = await database.files.deleteOne(FileBase(**dictFromGoogleMessage(request.file)))
        return pb2.FileR(file=file.model_dump())


    @Servicer.methodAsyncDecorator("nosql-database-api:GetManyFilesMetaInfo")
    async def GetManyFilesMetaInfo(self, request : pb2.StorageSegmentR, context) :
        files : FileList = await database.files.getMany(Range(start=request.start, end=request.end), 
                                                        Storage(request.storage))
        return pb2.FileSegmentR(**files.model_dump())


    @Servicer.methodAsyncDecorator("nosql-database-api:PutSQLGeneratorMeta")
    async def PutSQLGeneratorMeta(self, request : pb2.IdentifierMetaR, context) :
        meta = await database.sql_gen.putMeta(Identifier(request.identifier),
                                              Meta(status=request.status,
                                                   name=request.name))
        return pb2.IdentifierMetaR(identifier=request.identifier,
                                   status=meta.status,
                                   name=meta.name)


    @Servicer.methodAsyncDecorator("nosql-database-api:GetSQLGeneratorMeta")
    async def GetSQLGeneratorMeta(self, request : pb2.IdentifierR, context) :
        meta = await database.sql_gen.getMeta(Identifier(request.identifier))
        return pb2.IdentifierMetaR(identifier=request.identifier,
                                   status=meta.status,
                                   name=meta.name)


    @Servicer.methodAsyncDecorator("nosql-database-api:PutSQLGeneratorFiles")
    async def PutSQLGeneratorFiles(self, request : pb2.ManyFilesIdentifierR, context) :
        files = FileBaseKeywordList(files=[FileBaseKeyword(**dictFromGoogleMessage(file)) for file in request.files])
        await database.sql_gen.putFiles(Identifier(request.identifier), files=files)
        return pb2.IdentifierR(identifier=request.identifier)


    @Servicer.methodAsyncDecorator("nosql-database-api:GetSQLGeneratorFiles")
    async def GetSQLGeneratorFiles(self, request : pb2.IdentifierR, context) :
        st_id : FileBaseKeywordList = await database.sql_gen.getFiles(Identifier(request.identifier))
        return pb2.ManyFilesIdentifierR(files=[file.model_dump() for file in st_id.files],
                                        identifier=request.identifier)


    @Servicer.methodAsyncDecorator("nosql-database-api:PutSQLGeneratorSQLFile")
    async def PutSQLGeneratorSQLFile(self, request : pb2.FileBaseIdentifierR, context) :
        file = await database.sql_gen.putSQL(identifier=Identifier(request.identifier),
                                             file=FileBase(**dictFromGoogleMessage(request.file)))
        return pb2.FileBaseIdentifierR(file=file.model_dump(),
                                       identifier=request.identifier)


    @Servicer.methodAsyncDecorator("nosql-database-api:GetSQLGeneratorSQLFile")
    async def GetSQLGeneratorSQLFile(self, request : pb2.IdentifierR, context) :
        file = await database.sql_gen.getSQL(identifier=Identifier(request.identifier))
        return pb2.FileBaseIdentifierR(file=file.model_dump(),
                                       identifier=request.identifier)


    @Servicer.methodAsyncDecorator("nosql-database-api:GetFilesMetaInfoCount")
    async def GetFilesMetaInfoCount(self, request : pb2.StorageR, context) :
        count = (await database.files.getCount(request.storage)).count
        return pb2.CountR(count=count)


    @Servicer.methodAsyncDecorator("nosql-database-api:GetSQLGeneratorSQLIDs")
    async def GetSQLGeneratorSQLIDs(self, request : pb2.NothingR, context) :
        metas = await database.sql_gen.getAllSQLIDs()
        return pb2.ManyIdentifierMetaR(**metas.model_dump())