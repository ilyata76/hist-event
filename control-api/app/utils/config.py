"""
    Файл, конфигурирующий настройки для приложения
"""
from os import environ
from pathlib import Path


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
            self.__LOG_FILENAME = environ.get("LOG_FILENAME", "control-api.log")
        return self.__LOG_FILENAME

    @property 
    def NOSQL_DATABASE_GRPC_HOST(self) -> str :
        if not hasattr(self, "_Config__NOSQL_DATABASE_GRPC_HOST") :
            self.__NOSQL_DATABASE_GRPC_HOST = environ.get("NOSQL_DATABASE_GRPC_HOST", "localhost")
        return self.__NOSQL_DATABASE_GRPC_HOST
    
    @property 
    def NOSQL_DATABASE_GRPC_PORT(self) -> str :
        if not hasattr(self, "_Config__NOSQL_DATABASE_GRPC_PORT") :
            self.__NOSQL_DATABASE_GRPC_PORT = environ.get("NOSQL_DATABASE_GRPC_PORT", "50051")
        return self.__NOSQL_DATABASE_GRPC_PORT

    @property 
    def FILE_API_GRPC_HOST(self) -> str :
        if not hasattr(self, "_Config__FILE_API_GRPC_HOST") :
            self.__FILE_API_GRPC_HOST = environ.get("FILE_API_GRPC_HOST", "localhost")
        return self.__FILE_API_GRPC_HOST
    
    @property 
    def FILE_API_GRPC_PORT(self) -> str :
        if not hasattr(self, "_Config__FILE_API_GRPC_PORT") :
            self.__FILE_API_GRPC_PORT = environ.get("FILE_API_GRPC_PORT", "50052")
        return self.__FILE_API_GRPC_PORT

    def __str__(self, indent : str = "") -> str :
        """
            Строковое представление.
                Также обновляет ENV-взятие переменных, т.к. обращается к ним напрямую
        """
        return   indent + f"LOG_DEBUG : {self.LOG_DEBUG}" + "; "\
               + indent + f"LOG_CONSOLE : {self.LOG_CONSOLE}" + "; "\
               + indent + f"LOG_FOLDER : {self.LOG_FOLDER}" + "; "\
               + indent + f"LOG_FILENAME : {self.LOG_FILENAME}" + "; "\
               + indent + f"NOSQL_DATABASE_GRPC_HOST : {self.NOSQL_DATABASE_GRPC_HOST}" + "; "\
               + indent + f"NOSQL_DATABASE_GRPC_PORT : {self.NOSQL_DATABASE_GRPC_PORT}" + "; "\
               + indent + f"FILE_API_GRPC_HOST : {self.FILE_API_GRPC_HOST}" + "; "\
               + indent + f"FILE_API_GRPC_PORT : {self.FILE_API_GRPC_PORT}"


class LogCode :
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"


class StorageIdentifier :
    FTP = "ftp"
    S3 = "s3"


config = Config()