"""
    Файл, конфигурирующий настройки для приложения
"""
from os import environ
from pathlib import Path

from utils.exception import ConfigException, ConfigExceptionCode


class Config :
    """
        Реактивный конфиг для приложения
    """

    @property
    def LOG_DEBUG(self) -> bool :
        """
            Определяет, будет ли отображаться DEBUG-уровень в логах
        """
        if not hasattr(self, "_Config__LOG_DEBUG"):
            self.__LOG_DEBUG = environ.get("LOG_DEBUG", "false").lower() in ["true", "yes"]
        return self.__LOG_DEBUG

    @property
    def LOG_CONSOLE(self) -> bool :
        """
            Определяет, будет ли отображаться лог в консоли
        """
        if not hasattr(self, "_Config__LOG_CONSOLE"):
            self.__LOG_CONSOLE = environ.get("LOG_CONSOLE", "false").lower() in ["true", "yes"]
        return self.__LOG_CONSOLE

    @property
    def LOG_FOLDER(self) -> Path :
        """
            Определяет папку для сохранения логов
        """
        try : 
            if not hasattr(self, "_Config__LOG_FOLDER") :
                self.__LOG_FOLDER = Path(str(environ.get("LOG_FOLDER", "./logs")))
        except BaseException :
            self.__LOG_FOLDER = Path("./logs")
        return self.__LOG_FOLDER

    @property
    def LOG_FILENAME(self) -> str :
        """
            Определяет название файла, в котором будет храниться лог приложения
        """
        if not hasattr(self, "_Config__LOG_FILENAME") :
            self.__LOG_FILENAME = environ.get("LOG_FILENAME", "nosql-database-api.log")
        return self.__LOG_FILENAME

    @property
    def DATABASE_URI(self) -> str :
        """
            Определяет путь(ссылку, URI) до базы данных
        """
        if not hasattr(self, "_Config__DATABASE_URI") :
            self.__DATABASE_URI = environ.get("DATABASE_URI", "localhost:27017")
        return self.__DATABASE_URI

    @property
    def DATABASE_TIMEOUT_MS(self) -> str :
        """
            Определяет время ожидания клиента ответа от сервера в мс
        """
        try : 
            if not hasattr(self, "_Config__DATABASE_TIMEOUT_MS") :
                self.__DATABASE_TIMEOUT_MS = int(environ.get("DATABASE_TIMEOUT_MS", 1000))
        except BaseException :
            self.__DATABASE_TIMEOUT_MS = 1000
        return self.__DATABASE_TIMEOUT_MS

    @property
    def DATABASE_RECONNECTION_S(self) -> str :
        """
            Определяет время ожидания клиента ответа от сервера в мс
        """
        try : 
            if not hasattr(self, "_Config__DATABASE_RECONNECTION_S") :
                self.__DATABASE_RECONNECTION_S = int(environ.get("DATABASE_RECONNECTION_S", 600))
        except BaseException :
            self.__DATABASE_RECONNECTION_S = 100000
        return self.__DATABASE_RECONNECTION_S

    @property
    def DATABASE_FILES_DB(self) -> str :
        return "files"
    
    @property
    def DATABASE_FTP_FILES_COLLECTION(self) -> str :
        return "ftp_files"

    @property
    def DATABASE_S3_FILES_COLLECTION(self) -> str :
        return "s3_files"

    @property
    def DATABASE_SQL_GENERATOR_DB(self) -> str :
        return "sql_generator"

    @property
    def GRPC_HOST(self) -> str :
        if not hasattr(self, "_Config__GRPC_HOST") :
            self.__GRPC_HOST = environ.get("GRPC_HOST", "0.0.0.0")
        return self.__GRPC_HOST

    @property
    def GRPC_PORT(self) -> str :
        if not hasattr(self, "_Config__GRPC_PORT") :
            self.__GRPC_PORT = environ.get("GRPC_PORT", "50051")
        return self.__GRPC_PORT

    @property
    def GRPC_MAX_WORKERS(self) -> str :
        """
            Количество работающих threads у grpc-сервера
        """
        try : 
            if not hasattr(self, "_Config__GRPC_MAX_WORKERS") :
                self.__GRPC_MAX_WORKERS = int(environ.get("GRPC_MAX_WORKERS", 10))
        except BaseException :
            self.__GRPC_MAX_WORKERS = 10
        return self.__GRPC_MAX_WORKERS

    def __str__(self, indent : str = "") -> str :
        """
            Строковое представление.
                Также обновляет ENV-взятие переменных, т.к. обращается к ним напрямую
        """
        return   indent + f"LOG_DEBUG : {self.LOG_DEBUG}" + "; "\
               + indent + f"LOG_CONSOLE : {self.LOG_CONSOLE}" + "; "\
               + indent + f"LOG_FOLDER : {self.LOG_FOLDER}" + "; "\
               + indent + f"LOG_FILENAME : {self.LOG_FILENAME}" + "; "\
               + indent + f"DATABASE_URI : {self.DATABASE_URI}" + "; "\
               + indent + f"DATABASE_TIMEOUT_MS : {self.DATABASE_TIMEOUT_MS}" + "; "\
               + indent + f"DATABASE_RECONNECTION_S : {self.DATABASE_RECONNECTION_S}" + "; "\
               + indent + f"GRPC_PORT : {self.GRPC_PORT}" + "; "\
               + indent + f"GRPC_HOST : {self.GRPC_HOST}" + "; "\
               + indent + f"GRPC_MAX_WORKERS : {self.GRPC_MAX_WORKERS}"


class StorageIdentifier :
    FTP = "ftp"
    S3 = "s3"


class StorageCollection :
    @staticmethod
    def get(identifier : str = StorageIdentifier.FTP) :
        match identifier :
            case StorageIdentifier.FTP :
                return config.DATABASE_FTP_FILES_COLLECTION
            case StorageIdentifier.FTP :
                return config.DATABASE_S3_FILES_COLLECTION
            case _ :
                raise ConfigException(code=ConfigExceptionCode.INVALID_STORAGE_IDENTIFIER,
                                      detail=f"Нет такого идентификатора коллекции, {identifier}!")


FILE_KEY = "file"
DATABASE_PATH_PATH = f"{FILE_KEY}.path"


class LogCode :
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"


config = Config()