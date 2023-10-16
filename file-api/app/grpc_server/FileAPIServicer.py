"""
    Файл логики gRPC-сервера
"""
from pathlib import Path

import grpc
import proto.file_api_pb2 as pb2
import proto.file_api_pb2_grpc as pb2_grpc

from grpc_server.AbstractServicer import AbstractServicer
from storage import FileStorage
from schemas.File import FileBinary, File, FileBase


class FileAPIServicer(pb2_grpc.FileAPIServicer) :
    """
        Логика сервера (сервисер))
    """
    
    @AbstractServicer.method("file-api:Ping")
    async def Ping(self, request : pb2.PingRequest, context : grpc.ServicerContext) :
        return pb2.PingResponse(pong="pong")

    @AbstractServicer.method("file-api:AddFile")
    async def AddFile(self, request : pb2.AddFileRequest, context : grpc.ServicerContext) :
        storage = FileStorage.get(storage_identifier=request.storage)
        # TODO проверка существования файла в NoSQL
        file : File = await storage.appendOne(FileBinary(path=request.path,
                                                         filename=request.filename,
                                                         file=request.file,
                                                         storage=request.storage))
        # TODO добавление в NoSQL
        return pb2.AddFileResponse(storage=file.storage, 
                                   path=str(file.path), 
                                   filename=file.filename)

    @AbstractServicer.method("file-api:GetFile")
    async def GetFile(self, request : pb2.GetFileRequest, context : grpc.ServicerContext):
        storage = FileStorage.get(storage_identifier=request.storage)
        # TODO проверка в NoSQL существования файла
        file : FileBinary = await storage.getOne(FileBase(path=request.path,
                                                          storage=request.storage))
        return pb2.GetFileResponse(storage=file.storage,
                                   path=str(file.path),
                                   filename=file.filename,
                                   file=file.file)

    @AbstractServicer.method("file-api:PutFile")
    async def PutFile(self, request : pb2.PutFileRequest, context : grpc.ServicerContext):
        storage = FileStorage.get(storage_identifier=request.storage)
        file : FileBinary = await storage.putOne(FileBinary(path=request.path,
                                                            filename=request.filename,
                                                            file=request.file,
                                                            storage=request.storage))
        return pb2.PutFileResponse(storage=file.storage,
                                   path=str(file.path),
                                   filename=file.filename)

    @AbstractServicer.method("file-api:DeleteFile")
    async def DeleteFile(self, request : pb2.DeleteFileRequest, context : grpc.ServicerContext):
        storage = FileStorage.get(storage_identifier=request.storage)
        file : File = await storage.deleteOne(FileBase(path=request.path,
                                                       storage=request.storage))
        return pb2.DeleteFileResponse(storage=file.storage,
                                      path=str(file.path),
                                      filename=file.filename)