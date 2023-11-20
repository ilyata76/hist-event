"""
    Файл, конфигурирующий настройки для приложения
"""
from os import environ
from pathlib import Path


class Config :
    """
        Реактивный конфиг для приложения
    """

    def __AddNewParameter(self, *, param, value, default, 
                          cast : type = str, reread : bool = False):
        try :
            if not hasattr(self, f"_Config__{param}") or reread :
                setattr(self, f"_Config__{param}", cast(value))
        except BaseException :
            setattr(self, f"_Config__{param}", default)
        return getattr(self, f"_Config__{param}")

    @property
    def LOG_DEBUG(self) -> bool :
        """Будет ли отображаться DEBUG-уровень (и все выше) в логах"""
        return self.__AddNewParameter(param="LOG_DEBUG", value=environ.get("LOG_DEBUG", "false").lower() in ["true", "yes"],
                                      default=False, cast=bool, reread=False)

    @property
    def LOG_CONSOLE(self) -> bool :
        """Будет ли отображаться лог в консоли"""
        return self.__AddNewParameter(param="LOG_CONSOLE", value=environ.get("LOG_CONSOLE", "false").lower() in ["true", "yes"],
                                      default=False, cast=bool, reread=False)

    @property
    def LOG_FOLDER(self) -> Path :
        """Папка для сохранения логов"""
        return self.__AddNewParameter(param="LOG_FOLDER", value=environ.get("LOG_FOLDER", "./logs"),
                                      default=Path("./logs"), cast=Path, reread=False)

    @property
    def LOG_FILENAME(self) -> str :
        """Название файла лога"""
        return self.__AddNewParameter(param="LOG_FILENAME", value=environ.get("LOG_FILENAME", "nosql-database-api.log"),
                                      default="nosql-database-api.log", cast=str, reread=False)

    @property
    def LOG_CUT_LEN(self) -> int :
        """Максимальное количество символов при логировании"""
        return self.__AddNewParameter(param="LOG_CUT_LEN", value=environ.get("LOG_CUT_LEN", 200),
                                      default=200, cast=int, reread=False)

    @property
    def DATABASE_HOST(self) -> str :
        return self.__AddNewParameter(param="DATABASE_HOST", value=environ.get("DATABASE_HOST", "localhost"),
                                      default="localhost", cast=str, reread=False)

    @property
    def DATABASE_PORT(self) -> str :
        return self.__AddNewParameter(param="DATABASE_PORT", value=environ.get("DATABASE_PORT", "27017"),
                                      default="27017", cast=str, reread=False)

    @property
    def DATABASE_TIMEOUT_MS(self) -> int :
        """Время ожидания ответа от базы"""
        return self.__AddNewParameter(param="DATABASE_TIMEOUT_MS", value=environ.get("DATABASE_TIMEOUT_MS", 1000),
                                      default=1000, cast=int, reread=False)

    @property
    def DATABASE_RECONNECTION_S(self) -> int :
        """Время, через которое клиент попытается переподключиться к базе"""
        return self.__AddNewParameter(param="DATABASE_RECONNECTION_S", value=environ.get("DATABASE_RECONNECTION_S", 1000),
                                      default=1000, cast=int, reread=False)

    @property
    def DATABASE_FILES_DB(self) -> str :
        return self.__AddNewParameter(param="DATABASE_FILES_DB", value=environ.get("DATABASE_FILES_DB", "files"),
                                      default="files", cast=str, reread=False)

    @property
    def DATABASE_FTP_FILES_COLLECTION(self) -> str :
        return self.__AddNewParameter(param="DATABASE_FTP_FILES_COLLECTION", value=environ.get("DATABASE_FTP_FILES_COLLECTION", "ftp_files"),
                                      default="ftp_files", cast=str, reread=False)

    @property
    def DATABASE_S3_FILES_COLLECTION(self) -> str :
        return self.__AddNewParameter(param="DATABASE_S3_FILES_COLLECTION", value=environ.get("DATABASE_S3_FILES_COLLECTION", "s3_files"),
                                      default="s3_files", cast=str, reread=False)

    @property
    def DATABASE_SQL_GENERATOR_DB(self) -> str :
        """Всё, что связано с сервисом sql-gen (связанные файлы, статус операции)"""
        return self.__AddNewParameter(param="DATABASE_SQL_GENERATOR_DB", value=environ.get("DATABASE_SQL_GENERATOR_DB", "sql_generator"),
                                      default="sql_generator", cast=str, reread=False)

    @property
    def GRPC_HOST(self) -> str :
        """Хост текущего grpc-сервера"""
        return self.__AddNewParameter(param="GRPC_HOST", value=environ.get("GRPC_HOST", "0.0.0.0"),
                                      default="0.0.0.0", cast=str, reread=False)

    @property
    def GRPC_PORT(self) -> str :
        """Порт текущего grpc-сервера"""
        return self.__AddNewParameter(param="GRPC_PORT", value=environ.get("GRPC_PORT", "50051"),
                                      default="50051", cast=str, reread=False)

    @property
    def GRPC_MAX_WORKERS(self) -> int :
        """Количество работающих threads у текущего сервера grpc"""
        return self.__AddNewParameter(param="GRPC_MAX_WORKERS", value=environ.get("GRPC_MAX_WORKERS", 10),
                                      default=10, cast=int, reread=False)

    def __str__(self, indent : str = "") -> str :
        """
            Строковое представление.
                Также обновляет ENV-взятие переменных, т.к. обращается к ним напрямую
        """
        return " ; ".join([f"{indent}{x} : {getattr(self, x)}" for x in ["LOG_DEBUG", "LOG_CONSOLE", "LOG_CUT_LEN",
                                                                         "LOG_FOLDER", "LOG_FILENAME", "DATABASE_TIMEOUT_MS",
                                                                         "GRPC_PORT", "GRPC_HOST", "DATABASE_RECONNECTION_S",
                                                                         "GRPC_MAX_WORKERS", "DATABASE_HOST", "DATABASE_PORT"]])


config = Config()