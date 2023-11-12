"""
    Файл с методами работы с FTP-сервером
"""
from pathlib import Path
from fastapi import APIRouter, Request, UploadFile, Response

from app.utils.config import StorageIdentifier
from app.utils.dict_from_message import dict_from_message
from app.rest_api.log_and_except import log_and_except
from app.grpc_client.FileAPIgRPCCLient import FileAPIgRPCCLient
# from app.grpc_client.NoSQLDatabaseAPIgRPCClient import NoSQLDatabaseAPIgRPCClient
from app.schemas.File import FileBinary, File, FileBase
from app.schemas.Range import Range


file = APIRouter(prefix="/file")


@file.get("/meta",
          tags=["file"],
          name="Files Meta Info From Storage",
          response_model=list[File],
          description="Взять мета-информацию файлов через NoSQlDatabaseAPI")
@log_and_except
async def fileFTPGetByPath(request : Request,
                           storage : str = StorageIdentifier.FTP,
                           start : int = 0,
                           end : int = 10) -> list[File]:
    # если будет медленно, используем сразу доступ до NoSQL
    # response = await NoSQLDatabaseAPIgRPCClient.GetManyFilesMetaInfo(storage=storage,
    #                                                                  range=Range(start=start, 
    #                                                                              end=end))
    response = await FileAPIgRPCCLient.GetManyFilesMetaInfo(storage=storage,
                                                            range=Range(start=start, 
                                                                        end=end))
    return [dict_from_message(file) for file in response.files]


@file.get("/meta/{path:path}",
          tags=["file"],
          name="File Meta Info From Storage",
          response_model=File,
          description="Взять мета-информацию через NoSQlDatabaseAPI")
@log_and_except
async def fileFTPGetMetaByPath(request : Request,
                               path : str,
                               storage : str = StorageIdentifier.FTP) -> File :
    # если будет медленно, используем сразу доступ до NoSQL
    # response = await NoSQLDatabaseAPIgRPCClient.GetFileMetaInfo(FileBase(path=Path(path),
    #                                                                      storage=storage))
    response = await FileAPIgRPCCLient.GetFileMetaInfo(FileBase(path=Path(path),
                                                                storage=storage))
    return response.file


@file.get("/{path:path}",
          tags=["file"],
          name="File From Storage",
          response_class=Response,
          description="Скачать файл из хранилища через FileAPI")
@log_and_except
async def fileFTPGetByPath(request : Request,
                           path : str,
                           storage : str = StorageIdentifier.FTP) -> UploadFile :
    grpc_response = await FileAPIgRPCCLient.GetFile(FileBase(path=Path(path), 
                                                             storage=storage))
    response = Response(content=grpc_response.file.file)
    response.headers["Content-Disposition"] = f"attachment; filename={grpc_response.file.filename}"
    return response


@file.put("/{path:path}",
          tags=["file"],
          name="Put File to Storage",
          response_model=File,
          description="Заменить файл в хранилище через FileAPI")
@log_and_except
async def fileFTPPutByPath(request : Request,
                           path : str,
                           file : UploadFile,
                           storage : str = StorageIdentifier.FTP) -> File :
    filepath = Path(path)
    file_bytes = await file.read()
    response = await FileAPIgRPCCLient.PutFile(FileBinary(path=filepath, 
                                                          storage=storage,
                                                          filename=filepath.name,
                                                          file=file_bytes))
    return response.file


@file.delete("/{path:path}",
             tags=["file"],
             name="Delete File from Storage",
             response_model=File,
             description="Удалить файл в хранилище через FileAPI")
@log_and_except
async def fileFTPDeleteByPath(request : Request,
                              path : str,
                              storage : str = StorageIdentifier.FTP) -> File :
    response = await FileAPIgRPCCLient.DeleteFile(FileBase(path=Path(path), 
                                                           storage=storage))
    return response.file


@file.post("/{path:path}",
           tags=["file"],
           name="File To Storage",
           response_model=File,
           description="Загрузить файл в хранилище через FileAPI")
@log_and_except
async def fileFTPPostByPath(request : Request,
                            path : str,
                            file : UploadFile,
                            storage : str = StorageIdentifier.FTP) -> File :
    filepath = Path(path)
    file_bytes = await file.read()
    response = await FileAPIgRPCCLient.AddFile(FileBinary(path=filepath, 
                                                          storage=storage,
                                                          filename=filepath.name,
                                                          file=file_bytes))
    return response.file