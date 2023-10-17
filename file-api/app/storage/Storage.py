"""
    Файл описывает работу с хранилищами
"""
from io import BytesIO
from pathlib import Path
from ftplib import FTP

from utils.logger import logger
from utils.config import LogCode, config
from utils.exception import StorageException, StorageExceptionCode
from schemas.File import FileBinary, File, FileBase


class AbstractStorage :
    """
        Класс описывает операции с хранилищем и файлами в нём
    """
    def __init__(self) :
        pass

    def method(path : str) :
        """
            Декоратор для методов над хранилищем
        """
        def gRPCMethod(function) :
            async def wrap(self, *args, **kwargs) :
                self.connect()
                prefix = f"[STORAGE] : {path}"
                try : 
                    logger.debug(f"{prefix} : {LogCode.PENDING}")
                    result = await function(self, *args, **kwargs)
                    logger.info(f"{prefix} : {LogCode.SUCCESS}")
                    return result
                except StorageException as exc:
                    raise exc
                except BaseException as exc:
                    logger.exception(f"{prefix} : {LogCode.ERROR} : {type(exc)}:{exc}")
                    raise RuntimeError(f"При работа с хранилищами произошла непредвиденная ошибка : {type(exc)}:{exc}")
            return wrap
        return gRPCMethod

    def connect(self) :
        """Тестовое подключение, подключение"""
        raise StorageException(code=StorageExceptionCode.METHOD_NOT_REALIZED,
                               detail="Хранилище не реализует метод connect")       

    @method("storage:appendOne")
    async def appendOne(self, file : FileBinary) -> File:
        raise StorageException(code=StorageExceptionCode.METHOD_NOT_REALIZED,
                               detail="Хранилище не реализует метод appendOne")

    @method("storage:getOne")
    async def getOne(self, file : FileBase) -> FileBinary:
        raise StorageException(code=StorageExceptionCode.METHOD_NOT_REALIZED,
                               detail="Хранилище не реализует метод getOne")

    @method("storage:deleteOne")
    async def deleteOne(self, file : FileBase) -> File:
        raise StorageException(code=StorageExceptionCode.METHOD_NOT_REALIZED,
                               detail="Хранилище не реализует метод deleteOne")

    @method("storage:putOne")
    async def putOne(self, file : FileBinary) -> File:
        raise StorageException(code=StorageExceptionCode.METHOD_NOT_REALIZED,
                               detail="Хранилище не реализует метод putOne")


class FTPStorage(AbstractStorage) :

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

    @AbstractStorage.method("ftp:appendOne")
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

    @AbstractStorage.method("ftp:getOne")
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

    @AbstractStorage.method("ftp:putOne")
    async def putOne(self, file : FileBinary) -> File :
        """Добавляет файл независимо от его существования"""
        logger.info(f"{self.prefix()} Замена файла по пути {file.path}")
        self.__createFolerFromFilePath(file.path)
        self.ftp.storbinary(f"STOR {file.path}", BytesIO(file.file))
        logger.info(f"{self.prefix()} Заменен файл {file.path}")
        return File(**file.model_dump())

    @AbstractStorage.method("ftp:deleteOne")
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


class S3Storage(AbstractStorage) :
    """
        Не реализован TODO
    """
    pass


