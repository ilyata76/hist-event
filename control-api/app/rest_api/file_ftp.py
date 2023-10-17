"""
    Файл с методами работы с FTP-сервером
"""
from pathlib import Path
from fastapi import APIRouter, Request, UploadFile, Response

from app.utils.config import StorageIdentifier
from app.rest_api.log_and_except import log_and_except
from app.grpc_client.FileAPIgRPCCLient import FileAPIgRPCCLient
from app.schemas.File import FileBinary, File, FileBase


file_ftp = APIRouter(prefix="/file/ftp")

@file_ftp.get("/")
@log_and_except
async def fileFTPGetByPath(request : Request,
                           start : int = 0,
                           end : int = 10) :
    return "aboba"


@file_ftp.get("/{path:path}",
              tags=["file"],
              name="File From FTP",
              response_class=Response,
              description="Скачать файл из хранилища через FileAPI")
@log_and_except
async def fileFTPGetByPath(request : Request,
                           path : str) -> UploadFile:
    grpc_response = await FileAPIgRPCCLient.GetFile(FileBase(path=Path(path), 
                                                             storage=StorageIdentifier.FTP))
    response = Response(content=grpc_response.file.file)
    response.headers["Content-Disposition"] = f"attachment; filename={grpc_response.file.filename}"
    return response


@file_ftp.put("/{path:path}",
              tags=["file"],
              name="Put File to FTP",
              response_model=File,
              description="Заменить файл в хранилище через FileAPI")
@log_and_except
async def fileFTPPutByPath(request : Request,
                           path : str,
                           file : UploadFile) -> File:
    filepath = Path(path)
    file_bytes = await file.read()
    response = await FileAPIgRPCCLient.PutFile(FileBinary(path=filepath, 
                                                          storage=StorageIdentifier.FTP,
                                                          filename=filepath.name,
                                                          file=file_bytes))
    return response.file


@file_ftp.delete("/{path:path}",
                 tags=["file"],
                 name="Delete File from FTP",
                 response_model=File,
                 description="Удалить файл в хранилище через FileAPI")
@log_and_except
async def fileFTPDeleteByPath(request : Request,
                              path : str) -> File:
    response = await FileAPIgRPCCLient.DeleteFile(FileBase(path=Path(path), 
                                                           storage=StorageIdentifier.FTP))
    return response.file


@file_ftp.post("/{path:path}",
               tags=["file"],
               name="File To FTP",
               response_model=File,
               description="Загрузить файл в хранилище через FileAPI")
@log_and_except
async def fileFTPPostByPath(request : Request,
                            path : str,
                            file : UploadFile) -> File:
    filepath = Path(path)
    file_bytes = await file.read()
    response = await FileAPIgRPCCLient.AddFile(FileBinary(path=filepath, 
                                                          storage=StorageIdentifier.FTP,
                                                          filename=filepath.name,
                                                          file=file_bytes))
    return response.file