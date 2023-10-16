from ftplib import FTP

from storage.Storage import FTPStorage, S3Storage
from utils.config import StorageIdentifier
from utils.exception import ConfigException, ConfigExceptionCode


# для предотвращения постоянного переподключения
ftp = FTPStorage(FTP())
s3 = S3Storage()

class FileStorage :
    """
        ФАБРИКА, только возвращает заранее созданные глобальные переменные
    """

    @staticmethod
    def get(storage_identifier : str = StorageIdentifier.FTP):
        match storage_identifier :
            case StorageIdentifier.FTP :
                return ftp
            case StorageIdentifier.S3 :
                return s3
            case _ :
                raise ConfigException(code=ConfigExceptionCode.INVALID_STORAGE_IDENTIFIER,
                                      detail=f"Нет такого хранилища, {storage_identifier}")