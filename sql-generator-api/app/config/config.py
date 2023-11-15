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
        return self.__AddNewParameter(param="LOG_FILENAME", value=environ.get("LOG_FILENAME", "sql-generator-api.log"),
                                      default="sql-generator-api.log", cast=str, reread=False)

    @property
    def GRPC_HOST(self) -> str :
        """Хост текущего grpc-сервера"""
        return self.__AddNewParameter(param="GRPC_HOST", value=environ.get("GRPC_HOST", "0.0.0.0"),
                                      default="0.0.0.0", cast=str, reread=False)

    @property
    def GRPC_PORT(self) -> str :
        """Порт текущего grpc-сервера"""
        return self.__AddNewParameter(param="GRPC_PORT", value=environ.get("GRPC_PORT", "50053"),
                                      default="50053", cast=str, reread=False)

    @property 
    def FILE_API_GRPC_HOST(self) -> str :
        """До grpc управления файлами"""
        return self.__AddNewParameter(param="FILE_API_GRPC_HOST", value=environ.get("FILE_API_GRPC_HOST", "localhost"),
                                      default="localhost", cast=str, reread=False)

    @property 
    def FILE_API_GRPC_PORT(self) -> str :
        """До grpc управления файлами"""
        return self.__AddNewParameter(param="FILE_API_GRPC_PORT", value=environ.get("FILE_API_GRPC_PORT", "50052"),
                                      default="50052", cast=str, reread=False)

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
    def PARSE_NAME_SPECIAL_SYMBOLS(self) -> str :
        """Для pyparsing для {вставок:1}[?]"""
        return self.__AddNewParameter(param="PARSE_NAME_SPECIAL_SYMBOLS", value=environ.get("PARSE_NAME_SPECIAL_SYMBOLS", " _-/\\:()?!"),
                                      default=" _-/\\:()?!", cast=str, reread=False)

    @property 
    def PARSE_KEYWORD_SPECIAL_SYMBOLS(self) -> str :
        """Для pyparsing для {вставок:1}[?]"""
        return self.__AddNewParameter(param="PARSE_KEYWORD_SPECIAL_SYMBOLS", value=environ.get("PARSE_KEYWORD_SPECIAL_SYMBOLS", "_"),
                                      default="_", cast=str, reread=False)

    @property
    def GRPC_MAX_WORKERS(self) -> int :
        """Количество работающих threads у текущего сервера grpc"""
        return self.__AddNewParameter(param="GRPC_MAX_WORKERS", value=environ.get("GRPC_MAX_WORKERS", 10),
                                      default=10, cast=int, reread=False)

    @property
    def MAX_ITERATION_PARSE(self) -> int :
        """Количество обходов файлов для разрешения обратной вложенности"""
        return self.__AddNewParameter(param="MAX_ITERATION_PARSE", value=environ.get("MAX_ITERATION_PARSE", 10),
                                      default=10, cast=int, reread=False) - 1

    def __str__(self, indent : str = "") -> str :
        """
            Строковое представление.
                Также обновляет ENV-взятие переменных, т.к. обращается к ним напрямую
        """
        return " ; ".join([f"{indent}{x} : {getattr(self, x)}" for x in ["LOG_DEBUG", "LOG_CONSOLE", "LOG_FOLDER", "LOG_FILENAME",
                                                                "GRPC_PORT", "GRPC_HOST", "GRPC_MAX_WORKERS",
                                                                "MAX_ITERATION_PARSE", "FILE_API_GRPC_HOST", "FILE_API_GRPC_PORT",
                                                                "NOSQL_DATABASE_GRPC_HOST", "NOSQL_DATABASE_GRPC_PORT",
                                                                "PARSE_KEYWORD_SPECIAL_SYMBOLS", "PARSE_NAME_SPECIAL_SYMBOLS"]])


config = Config()

NOSQL_IP = f"{config.NOSQL_DATABASE_GRPC_HOST}:{config.NOSQL_DATABASE_GRPC_PORT}"
FILE_IP = f"{config.FILE_API_GRPC_HOST}:{config.FILE_API_GRPC_PORT}"