"""
    Файл логики gRPC-сервера
"""
import grpc
import proto.nosql_database_api_pb2 as pb2
import proto.nosql_database_api_pb2_grpc as pb2_grpc

from grpc_server.AbstractServicer import AbstractServicer as Servicer
import database
from schemas.File import File, FileBase, FileBaseKeyword, FileBaseKeywordList
from schemas.Range import Range
from schemas.StatusIdentifier import StatusIdentifier, Identifier
from utils.dict_from_message import dict_from_message


class NoSQLDatabaseAPIServicer(pb2_grpc.NoSQLDatabaseAPIServicer) :
    """
        Логика сервера (сервисер))
    """
  
    @Servicer.method("nosql-database-api:Ping")
    async def Ping(self, request : pb2.PingR, context) :
        return pb2.PongR(pong="Pong!")


    @Servicer.method("nosql-database-api:AddFileMetaInfo")
    async def AddFileMetaInfo(self, request : pb2.FileR, context) :
        file : File = await database.files.appendOne(file=File(**dict_from_message(request.file)))
        return pb2.FileR(file=file.model_dump())


    @Servicer.method("nosql-database-api:GetFileMetaInfo")
    async def GetFileMetaInfo(self, request : pb2.FileBaseR, context) :
        file : File = await database.files.getOne(file=FileBase(**dict_from_message(request.file)))
        return pb2.FileR(file=file.model_dump())


    @Servicer.method("nosql-database-api:PutFileMetaInfo")
    async def PutFileMetaInfo(self, request : pb2.FileR, context) :
        file : File = await database.files.putOne(file=File(**dict_from_message(request.file)))
        return pb2.FileR(file=file.model_dump())


    @Servicer.method("nosql-database-api:DeleteFileMetaInfo")
    async def DeleteFileMetaInfo(self, request : pb2.FileBaseR, context) :
        file : File = await database.files.deleteOne(file=FileBase(**dict_from_message(request.file)))
        return pb2.FileR(file=file.model_dump())


    @Servicer.method("nosql-database-api:GetManyFilesMetaInfo")
    async def GetManyFilesMetaInfo(self, request : pb2.StorageSegmentR, context) :
        files : list[File] = await database.files.getMany(range=Range(start=request.start, 
                                                          end=request.end), 
                                                          storage_identifier=request.storage)
        return pb2.FileSegmentR(files=[x.model_dump() for x in files])


    @Servicer.method("nosql-database-api:PutSQLGeneratorStatus")
    async def PutSQLGeneratorStatus(self, request : pb2.IdentifierStatusR, context) :
        st_id : StatusIdentifier = await database.sql_gen.putStatus(StatusIdentifier(**dict_from_message(request)))
        return pb2.IdentifierStatusR(**st_id.model_dump())


    @Servicer.method("nosql-database-api:GetSQLGeneratorStatus")
    async def GetSQLGeneratorStatus(self, request : pb2.IdentifierR, context) :
        st_id : StatusIdentifier = await database.sql_gen.getStatus(Identifier(**dict_from_message(request)))
        return pb2.IdentifierStatusR(**st_id.model_dump())


    @Servicer.method("nosql-database-api:PutSQLGeneratorFiles")
    async def PutSQLGeneratorFiles(self, request : pb2.ManyFilesIdentifierR, context) :
        st_id : Identifier = await database.sql_gen.putFiles(Identifier(identifier=request.identifier),
                                                             files=FileBaseKeywordList(files=[FileBaseKeyword(**dict_from_message(file)) for file in request.files]))
        return pb2.IdentifierR(**st_id.model_dump())
    

    @Servicer.method("nosql-database-api:GetSQLGeneratorFiles")
    async def GetSQLGeneratorFiles(self, request : pb2.IdentifierR, context) :
        st_id : FileBaseKeywordList = await database.sql_gen.getFiles(Identifier(identifier=request.identifier))
        return pb2.ManyFilesIdentifierR(files=[file.model_dump() for file in st_id.files],
                                        identifier=request.identifier)


    @Servicer.method("nosql-database-api:PutSQLGeneratorSQLFile")
    async def PutSQLGeneratorSQLFile(self, request : pb2.FileBaseIdentifierR, context) :
        file = await database.sql_gen.putSQL(identifier=Identifier(identifier=request.identifier),
                                             file=FileBase(**dict_from_message(request.file)))
        return pb2.FileBaseIdentifierR(file=file.model_dump(),
                                       identifier=request.identifier)


    @Servicer.method("nosql-database-api:GetSQLGeneratorSQLFile")
    async def GetSQLGeneratorSQLFile(self, request : pb2.IdentifierR, context) :
        file = await database.sql_gen.getSQL(identifier=Identifier(identifier=request.identifier))
        return pb2.FileBaseIdentifierR(file=file.model_dump(),
                                       identifier=request.identifier)