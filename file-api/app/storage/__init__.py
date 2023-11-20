from ftplib import FTP

from config import StorageIdentifier
from utils.exception import *
from schemas import Storage

from .FTPStorage import FTPStorage
from .S3Storage import S3Storage


# для предотвращения постоянного переподключения
ftp = FTPStorage(FTP(timeout=1000))
s3 = S3Storage()


class FileStorageFabric :
    """
        Класс (полуфабрика), только возвращает заранее созданные глобальные переменные
    """

    @staticmethod
    def get(storage : Storage = StorageIdentifier.FTP):
        match storage :
            case StorageIdentifier.FTP :
                return ftp
            case StorageIdentifier.S3 :
                return s3
            case _ :
                raise ConfigException(code=ConfigExceptionCode.INVALID_STORAGE_IDENTIFIER,
                                      detail=f"Нет такого хранилища, {storage}")