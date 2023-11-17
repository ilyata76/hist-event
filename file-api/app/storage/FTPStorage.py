"""
    Файл описывает работу с хранилищами
"""
from io import BytesIO
from pathlib import Path
from ftplib import FTP

from logger import logger
from config import config
from utils.exception import *
from schemas import FileBinary, File, FileBase

from .AbstractStorage import AbstractStorage as Storage


class FTPStorage(Storage) :

    def __init__(self, ftp : FTP = FTP()) :
        self.ftp = ftp

    def prefix(self) : 
        return f"[STORAGE][FTP]"

    def connect(self):
        """Используется в method декораторе"""
        try :
            logger.debug(f"{self.prefix()} Проверка установленного подключения к FTP")
            self.ftp.pwd()
        except BaseException : # если не смогли проверить, т.е. нас отключило
            try : 
                logger.debug(f"{self.prefix()} Подключение к FTP")
                self.ftp.connect(config.FTP_HOST, config.FTP_PORT)
                self.ftp.login(config.FTP_USERNAME, config.FTP_PASSWORD)
            except Exception as exc :
                raise StorageException(code=StorageExceptionCode.SERVICE_UNAVAILABLE,
                                       detail="Невозможно подключиться к FTP-хранилищу")
    
    def __createFolerFromFilePath(self, path : Path) :
        """Создать папку по пути path до имени файла"""
        logger.debug(f"{self.prefix()} Созадние папки для пути {path}")
        for path in path.parents.__reversed__() :
            try :
                self.ftp.mkd(path.as_posix())
            except Exception :
                pass

    def __checkFileExists(self, path : Path) :
        """Проверяет существование файла в директории по пути path"""
        logger.debug(f"{self.prefix()} Проверка, что файл {path} существует")
        try :
            self.ftp.retrbinary(f"RETR {path}", lambda byt : None)
            return True
        except Exception :
            return False

    @Storage.methodAsyncDecorator("ftp:appendOne")
    async def appendOne(self, file : FileBinary) -> File:
        """Поднимет исключение, если файл существует"""
        logger.debug(f"{self.prefix()} Добавление нового файла {file.path}")
        if self.__checkFileExists(file.path) :
            raise StorageException(code=StorageExceptionCode.ALREADY_EXISTS,
                                   detail="FTP: Такой файл уже существует")
        self.__createFolerFromFilePath(file.path)
        self.ftp.storbinary(f"STOR {file.path}", BytesIO(file.file))
        logger.info(f"{self.prefix()} Был добавлен файл {file.path}")
        return File(**file.model_dump())

    @Storage.methodAsyncDecorator("ftp:getOne")
    async def getOne(self, file : FileBase) -> FileBinary:
        """Поднимет ислкючение, если файла не существует"""
        logger.debug(f"{self.prefix()} Взятие файла {file.path}")
        file_bytes : bytes = b""
        def save_byts(bts : bytes) :
            nonlocal file_bytes
            file_bytes += bts
            return None
        try : 
            self.ftp.retrbinary(f"RETR {file.path}", save_byts)
        except Exception:
            raise StorageException(code=StorageExceptionCode.ENTITY_DOESNT_EXISTS,
                                   detail="FTP: такого файла не существует!")
        logger.info(f"{self.prefix()} Возвращён файл {file.path}")
        return FileBinary(path=file.path,
                          storage=file.storage,
                          filename=file.path.name,
                          file=file_bytes)

    @Storage.methodAsyncDecorator("ftp:putOne")
    async def putOne(self, file : FileBinary) -> File :
        """Добавляет файл независимо от его существования"""
        logger.info(f"{self.prefix()} Замена файла по пути {file.path}")
        self.__createFolerFromFilePath(file.path)
        self.ftp.storbinary(f"STOR {file.path}", BytesIO(file.file))
        logger.info(f"{self.prefix()} Заменен файл {file.path}")
        return File(**file.model_dump())

    @Storage.methodAsyncDecorator("ftp:deleteOne")
    async def deleteOne(self, file : FileBase) -> File :
        """Поднимет исключение, если файл не существует"""
        logger.debug(f"{self.prefix()} Удаление файла {file.path}")
        if not self.__checkFileExists(file.path) :
            raise StorageException(code=StorageExceptionCode.ENTITY_DOESNT_EXISTS,
                                   detail="FTP: такого файла не существует!")
        self.ftp.delete(file.path.as_posix())
        logger.info(f"{self.prefix()} Удалён файл {file.path}")
        return File(path=file.path,
                    storage=file.storage,
                    filename=file.path.name)

