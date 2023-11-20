"""
    Файл с методами работы с FTP-сервером
"""
from pathlib import Path

from fastapi import APIRouter, Request, UploadFile, Response

from app.grpc_client import FileAPIgRPCCLient
from app.schemas import FileBinary, File, FileBase, Range, FileList

from .restMethodAsyncDecorator import restMethodAsyncDecorator


file = APIRouter(prefix="/file")


def preparePath(path : str) -> Path :
    return Path(path)



@file.get("/meta/{storage}",
          tags=["file"], name="Получить мета информацию отрезка файлов",
          response_model=FileList,
          description="Взять мета-информацию файлов через NoSQlDatabaseAPI")
@restMethodAsyncDecorator
async def fileFTPGetByPath(request : Request,
                           storage : str,
                           start : int = 0,
                           end : int = 10) -> FileList:
    range = Range(start=start, end=end)
    return await FileAPIgRPCCLient.GetManyFilesMetaInfo(storage=storage, range=range)


@file.get("/meta/{storage}/{path:path}",
          tags=["file"], name="Получить мета информацию конкретного файла",
          response_model=File,
          description="Взять мета-информацию через NoSQlDatabaseAPI")
@restMethodAsyncDecorator
async def fileFTPGetMetaByPath(request : Request,
                               storage : str, path : str) -> File :
    file = FileBase(path=preparePath(path), storage=storage)
    return await FileAPIgRPCCLient.GetFileMetaInfo(file)


@file.get("/{storage}/{path:path}",
          tags=["file"], name="Получить сам файл",
          response_class=Response,
          description="Скачать файл из хранилища через FileAPI")
@restMethodAsyncDecorator
async def fileFTPGetByPath(request : Request,
                           storage : str, path : str) -> UploadFile :
    file = FileBase(path=preparePath(path), storage=storage)
    grpc_response = await FileAPIgRPCCLient.GetFile(file)
    response = Response(content=grpc_response.file) # bytes
    response.headers["Content-Disposition"] = f"attachment; filename={grpc_response.filename}"
    return response


@file.put("/{storage}/{path:path}",
          tags=["file"], name="Заместить/разместить файл в хранилище",
          response_model=File,
          description="Заменить файл в хранилище через FileAPI")
@restMethodAsyncDecorator
async def fileFTPPutByPath(request : Request,
                           storage : str, path : str,
                           file : UploadFile) -> File :
    file = FileBinary(path=preparePath(path), storage=storage,
                      filename=preparePath(path).name, file=(await file.read()))
    return await FileAPIgRPCCLient.PutFile(file)


@file.delete("/{storage}/{path:path}",
             tags=["file"], name="Полностью удалить файл",
             response_model=File,
             description="Удалить файл в хранилище через FileAPI")
@restMethodAsyncDecorator
async def fileFTPDeleteByPath(request : Request,
                              storage : str, path : str) -> File :
    file = FileBase(path=preparePath(path), storage=storage)
    return await FileAPIgRPCCLient.DeleteFile(file)


@file.post("/{storage}/{path:path}",
           tags=["file"], name="Разместить файл в хранилище",
           response_model=File,
           description="Загрузить файл в хранилище через FileAPI")
@restMethodAsyncDecorator
async def fileFTPPostByPath(request : Request, 
                            storage : str, path : str,
                            file : UploadFile) -> File :
    file = FileBinary(path=preparePath(path), storage=storage,
                      filename=preparePath(path).name, file=(await file.read()))
    return await FileAPIgRPCCLient.AddFile(file)