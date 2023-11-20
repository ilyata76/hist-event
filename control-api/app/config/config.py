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
        return self.__AddNewParameter(param="LOG_FILENAME", value=environ.get("LOG_FILENAME", "control-api.log"),
                                      default="control-api.log", cast=str, reread=False)

    @property
    def LOG_CUT_LEN(self) -> int :
        """Максимальное количество символов при логировании"""
        return self.__AddNewParameter(param="LOG_CUT_LEN", value=environ.get("LOG_CUT_LEN", 200),
                                      default=200, cast=int, reread=False)

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
    def SQL_GENERATOR_API_GRPC_HOST(self) -> str :
        """До grpc с процессами валидации->генерации"""
        return self.__AddNewParameter(param="SQL_GENERATOR_API_GRPC_HOST", value=environ.get("SQL_GENERATOR_API_GRPC_HOST", "localhost"),
                                      default="localhost", cast=str, reread=False)
    
    @property 
    def SQL_GENERATOR_API_GRPC_PORT(self) -> str :
        """До grpc с процессами валидации->генерации"""
        return self.__AddNewParameter(param="SQL_GENERATOR_API_GRPC_PORT", value=environ.get("SQL_GENERATOR_API_GRPC_PORT", "50053"),
                                      default="50053", cast=str, reread=False)

    def __str__(self, indent : str = "") -> str :
        """
            Строковое представление.
                Также обновляет ENV-взятие переменных, т.к. обращается к ним напрямую
        """
        return " ; ".join([f"{indent}{x} : {getattr(self, x)}" for x in ["LOG_DEBUG", "LOG_CONSOLE", "LOG_CUT_LEN",
                                                                         "LOG_FOLDER", "LOG_FILENAME",
                                                                         "SQL_GENERATOR_API_GRPC_HOST", "SQL_GENERATOR_API_GRPC_PORT",
                                                                         "FILE_API_GRPC_HOST", "FILE_API_GRPC_PORT",
                                                                         "NOSQL_DATABASE_GRPC_HOST", "NOSQL_DATABASE_GRPC_PORT"]])


config = Config()