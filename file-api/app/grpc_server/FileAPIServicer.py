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
        # TODO проверка существования файла в NoSQL
        file : File = await storage.appendOne(file=FileBinary(**dict_from_message(request.file)))
        # TODO добавление в NoSQL
        return pb2.FileR(file=file.model_dump())

    @AbstractServicer.method("file-api:GetFile")
    async def GetFile(self, request : pb2.FileBaseR, context : grpc.ServicerContext):
        storage = FileStorage.get(storage_identifier=request.file.storage)
        # TODO проверка в NoSQL существования файла
        file : FileBinary = await storage.getOne(FileBase(**dict_from_message(request.file)))
        return pb2.FileBinaryR(file=file.model_dump())

    @AbstractServicer.method("file-api:PutFile")
    async def PutFile(self, request : pb2.FileBinaryR, context : grpc.ServicerContext):
        storage = FileStorage.get(storage_identifier=request.file.storage)
        file : FileBinary = await storage.putOne(FileBinary(**dict_from_message(request.file)))
        return pb2.FileR(file=file.model_dump())

    @AbstractServicer.method("file-api:DeleteFile")
    async def DeleteFile(self, request : pb2.FileBaseR, context : grpc.ServicerContext):
        storage = FileStorage.get(storage_identifier=request.file.storage)
        file : File = await storage.deleteOne(FileBase(**dict_from_message(request.file)))
        return pb2.FileR(file=file.model_dump())