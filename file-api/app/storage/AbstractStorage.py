"""
    Файл описывает работу с хранилищами
"""
from logger import logger
from utils import cutLog
from utils.exception import *
from schemas import FileBinary, File, FileBase


class AbstractStorage :
    """
        Класс описывает операции с хранилищем и файлами в нём
    """
    def __init__(self) :
        pass

    def methodAsyncDecorator(path : str) :
        """
            Декоратор для методов над хранилищем
        """
        def gRPCMethod(function) :
            async def wrap(self, *args, **kwargs) :
                self.connect()
                prefix = f"[STORAGE] : {path} : {cutLog(args)} : {cutLog(kwargs)}"
                try : 
                    logger.debug(f"{prefix} : PENDING")
                    result = await function(self, *args, **kwargs)
                    logger.info(f"{prefix} : {cutLog(result)}")
                    return result
                except StorageException as exc:
                    raise exc
                except BaseException as exc:
                    logger.exception(f"{prefix} : {type(exc)}:{exc}")
                    raise RuntimeError(f"При работа с хранилищами произошла непредвиденная ошибка : {type(exc)}:{exc}")
            return wrap
        return gRPCMethod

    def connect(self) :
        """Тестовое подключение, подключение"""
        raise StorageException(code=StorageExceptionCode.METHOD_NOT_REALIZED,
                               detail="Хранилище не реализует метод connect")       

    @methodAsyncDecorator("storage:appendOne")
    async def appendOne(self, file : FileBinary) -> File:
        raise StorageException(code=StorageExceptionCode.METHOD_NOT_REALIZED,
                               detail="Хранилище не реализует метод appendOne")

    @methodAsyncDecorator("storage:getOne")
    async def getOne(self, file : FileBase) -> FileBinary:
        raise StorageException(code=StorageExceptionCode.METHOD_NOT_REALIZED,
                               detail="Хранилище не реализует метод getOne")

    @methodAsyncDecorator("storage:deleteOne")
    async def deleteOne(self, file : FileBase) -> File:
        raise StorageException(code=StorageExceptionCode.METHOD_NOT_REALIZED,
                               detail="Хранилище не реализует метод deleteOne")


    @methodAsyncDecorator("storage:putOne")
    async def putOne(self, file : FileBinary) -> File:
        raise StorageException(code=StorageExceptionCode.METHOD_NOT_REALIZED,
                               detail="Хранилище не реализует метод putOne")