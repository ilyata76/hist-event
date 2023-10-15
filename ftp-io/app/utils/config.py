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
            self.__LOG_FILENAME = environ.get("LOG_FILENAME", "ftp-io.log")
        return self.__LOG_FILENAME

    @property
    def FTP_USERNAME(self) -> str :
        if not hasattr(self, "_Config__FTP_USERNAME") :
            self.__FTP_USERNAME = environ.get("FTP_USERNAME", "admin")
        return self.__FTP_USERNAME

    @property
    def FTP_PASSWORD(self) -> str :
        if not hasattr(self, "_Config__FTP_PASSWORD") :
            self.__FTP_PASSWORD = environ.get("FTP_PASSWORD", "admin")
        return self.__FTP_PASSWORD

    @property
    def FTP_PORT(self) -> str :
        try : 
            if not hasattr(self, "_Config__FTP_PORT") :
                self.__FTP_PORT = int(environ.get("FTP_PORT", 21))
        except BaseException :
            self.__FTP_PORT = 21
        return self.__FTP_PORT

    @property
    def FTP_HOST(self) -> str :
        if not hasattr(self, "_Config__FTP_HOST") :
            self.__FTP_HOST = environ.get("FTP_HOST", "localhost")
        return self.__FTP_HOST

    @property
    def FILES_FOLDER(self) -> str :
        try : 
            if not hasattr(self, "_Config__FILES_FOLDER") :
                self.__FILES_FOLDER = Path(environ.get("FILES_FOLDER", "./files"))
        except BaseException :
            self.__FILES_FOLDER = Path("./files")
        return self.__FILES_FOLDER

    def __str__(self, indent : str = "") -> str :
        """
            Строковое представление.
                Также обновляет ENV-взятие переменных, т.к. обращается к ним напрямую
        """
        return   indent + f"LOG_DEBUG : {self.LOG_DEBUG}" + "; "\
               + indent + f"LOG_CONSOLE : {self.LOG_CONSOLE}" + "; "\
               + indent + f"LOG_FOLDER : {self.LOG_FOLDER}" + "; "\
               + indent + f"LOG_FILENAME : {self.LOG_FILENAME}" + "; "\
               + indent + f"FTP_USERNAME : {self.FTP_USERNAME}" + "; "\
               + indent + f"FTP_PASSWORD : {'specified' if self.FTP_PASSWORD is not None else 'not specified'}" + "; "\
               + indent + f"FTP_HOST : {self.FTP_HOST}" + "; "\
               + indent + f"FTP_PORT : {self.FTP_PORT}" + "; "\
               + indent + f"FILES_FOLDER : {self.FILES_FOLDER}"


config = Config()