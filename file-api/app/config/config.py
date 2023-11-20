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
        return self.__AddNewParameter(param="LOG_FILENAME", value=environ.get("LOG_FILENAME", "file-api.log"),
                                      default="file-api.log", cast=str, reread=False)

    @property
    def LOG_CUT_LEN(self) -> int :
        """Максимальное количество символов при логировании"""
        return self.__AddNewParameter(param="LOG_CUT_LEN", value=environ.get("LOG_CUT_LEN", 200),
                                      default=200, cast=int, reread=False)

    @property
    def GRPC_HOST(self) -> str :
        """Хост текущего grpc-сервера"""
        return self.__AddNewParameter(param="GRPC_HOST", value=environ.get("GRPC_HOST", "0.0.0.0"),
                                      default="0.0.0.0", cast=str, reread=False)

    @property
    def GRPC_PORT(self) -> str :
        """Порт текущего grpc-сервера"""
        return self.__AddNewParameter(param="GRPC_PORT", value=environ.get("GRPC_PORT", "50052"),
                                      default="50052", cast=str, reread=False)

    @property
    def FTP_USERNAME(self) -> str :
        """Админка"""
        return self.__AddNewParameter(param="FTP_USERNAME", value=environ.get("FTP_USERNAME", "admin"),
                                      default="admin", cast=str, reread=False)

    @property
    def FTP_PASSWORD(self) -> str :
        """Админка"""
        return self.__AddNewParameter(param="FTP_PASSWORD", value=environ.get("FTP_PASSWORD", "admin"),
                                      default="admin", cast=str, reread=False)

    @property
    def FTP_PORT(self) -> int :
        """Админка"""
        return self.__AddNewParameter(param="FTP_PORT", value=environ.get("FTP_PORT", 21),
                                      default=21, cast=int, reread=False)

    @property
    def FTP_HOST(self) -> str :
        """Админка"""
        return self.__AddNewParameter(param="FTP_HOST", value=environ.get("FTP_HOST", "localhost"),
                                      default="localhost", cast=str, reread=False)

    @property 
    def NOSQL_DATABASE_GRPC_HOST(self) -> str :
        """До grpc вспомогательного хранилища"""
        return self.__AddNewParameter(param="NOSQL_DATABASE_GRPC_HOST", value=environ.get("NOSQL_DATABASE_GRPC_HOST", "localhost"),
                                      default="localhost", cast=str, reread=False)
    
    @property 
    def NOSQL_DATABASE_GRPC_PORT(self) -> str :
        """До grpc вспомогательного хранилища"""
        return self.__AddNewParameter(param="NOSQL_DATABASE_GRPC_PORT", value=environ.get("NOSQL_DATABASE_GRPC_PORT", "50051"),
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
                                                                         "LOG_FOLDER", "LOG_FILENAME",
                                                                         "GRPC_PORT", "GRPC_HOST", 
                                                                         "GRPC_MAX_WORKERS", "FTP_USERNAME",
                                                                         "FTP_HOST", "FTP_PORT",
                                                                         "NOSQL_DATABASE_GRPC_HOST", "NOSQL_DATABASE_GRPC_PORT"]])


config = Config()

NOSQL_IP = f"{config.NOSQL_DATABASE_GRPC_HOST}:{config.NOSQL_DATABASE_GRPC_PORT}"