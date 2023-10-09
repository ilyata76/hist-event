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

    def __str__(self, indent : str = "") -> str :
        """
            Строковое представление.
                Также обновляет ENV-взятие переменных, т.к. обращается к ним напрямую
        """
        return   indent + f"LOG_DEBUG : {self.LOG_DEBUG}" + "\n"\
               + indent + f"LOG_CONSOLE : {self.LOG_CONSOLE}" + "\n"\
               + indent + f"LOG_FOLDER : {self.LOG_FOLDER}" + "\n"\
               + indent + f"LOG_FILENAME : {self.LOG_FILENAME}" + "\n"\
               + indent + f"DATABASE_URI : {self.DATABASE_URI}" + "\n"\
               + indent + f"DATABASE_TIMEOUT_MS : {self.DATABASE_TIMEOUT_MS}" + "\n"\
               + indent + f"DATABASE_RECONNECTION_S : {self.DATABASE_RECONNECTION_S}"


FILE_KEY = "file"
DATABASE_FILENAME_PATH = f"{FILE_KEY}.filename"

config = Config()