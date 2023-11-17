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
        return self.__AddNewParameter(param="LOG_FILENAME", value=environ.get("LOG_FILENAME", "ftp-io.log"),
                                      default="ftp-io.log", cast=str, reread=False)

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
    def FILES_FOLDER(self) -> Path :
        """Название файла лога"""
        return self.__AddNewParameter(param="FILES_FOLDER", value=environ.get("FILES_FOLDER", "./files"),
                                      default=Path("./files"), cast=Path, reread=False)

    def __str__(self, indent : str = "") -> str :
        """
            Строковое представление.
                Также обновляет ENV-взятие переменных, т.к. обращается к ним напрямую
        """
        return " ; ".join([f"{indent}{x} : {getattr(self, x)}" for x in ["LOG_DEBUG", "LOG_CONSOLE", "LOG_FOLDER", "LOG_FILENAME",
                                                                         "FTP_USERNAME", "FTP_HOST","FTP_PORT", "FILES_FOLDER"]])


config = Config()