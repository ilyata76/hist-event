from .config import config
from utils.exception import ConfigException,\
                            ConfigExceptionCode


class StorageIdentifier :
    FTP = "ftp"
    S3 = "s3"


class StorageCollection :
    @staticmethod
    def get(identifier : str = StorageIdentifier.FTP) :
        match identifier :
            case StorageIdentifier.FTP :
                return config.DATABASE_FTP_FILES_COLLECTION
            case StorageIdentifier.S3 :
                return config.DATABASE_S3_FILES_COLLECTION
            case _ :
                raise ConfigException(code=ConfigExceptionCode.INVALID_STORAGE_IDENTIFIER,
                                      detail=f"Нет такого идентификатора хранилища, {identifier}")