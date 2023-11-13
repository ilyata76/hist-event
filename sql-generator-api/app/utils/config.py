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
            self.__LOG_FILENAME = environ.get("LOG_FILENAME", "sql-generator-api.log")
        return self.__LOG_FILENAME

    @property
    def GRPC_HOST(self) -> str :
        if not hasattr(self, "_Config__GRPC_HOST") :
            self.__GRPC_HOST = environ.get("GRPC_HOST", "0.0.0.0")
        return self.__GRPC_HOST

    @property
    def GRPC_PORT(self) -> str :
        if not hasattr(self, "_Config__GRPC_PORT") :
            self.__GRPC_PORT = environ.get("GRPC_PORT", "50053")
        return self.__GRPC_PORT

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
    def PARSE_NAME_SPECIAL_SYMBOLS(self) -> str :
        if not hasattr(self, "_Config__PARSE_NAME_SPECIAL_SYMBOLS") :
            self.__PARSE_NAME_SPECIAL_SYMBOLS = environ.get("PARSE_NAME_SPECIAL_SYMBOLS", " _-/\\:()?!")
        return self.__PARSE_NAME_SPECIAL_SYMBOLS

    @property 
    def PARSE_KEYWORD_SPECIAL_SYMBOLS(self) -> str :
        if not hasattr(self, "_Config__PARSE_KEYWORD_SPECIAL_SYMBOLS") :
            self.__PARSE_KEYWORD_SPECIAL_SYMBOLS = environ.get("PARSE_KEYWORD_SPECIAL_SYMBOLS", "_")
        return self.__PARSE_KEYWORD_SPECIAL_SYMBOLS

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

    @property
    def MAX_ITERATION_PARSE(self) -> str :
        """
            Количество работающих threads у grpc-сервера
        """
        try : 
            if not hasattr(self, "_Config__MAX_ITERATION_PARSE") :
                self.__MAX_ITERATION_PARSE = int(environ.get("MAX_ITERATION_PARSE", 10)) - 1
        except BaseException :
            self.__MAX_ITERATION_PARSE = 9
        return self.__MAX_ITERATION_PARSE

    def __str__(self, indent : str = "") -> str :
        """
            Строковое представление.
                Также обновляет ENV-взятие переменных, т.к. обращается к ним напрямую
        """
        return   indent + f"LOG_DEBUG : {self.LOG_DEBUG}" + "; "\
               + indent + f"LOG_CONSOLE : {self.LOG_CONSOLE}" + "; "\
               + indent + f"LOG_FOLDER : {self.LOG_FOLDER}" + "; "\
               + indent + f"LOG_FILENAME : {self.LOG_FILENAME}" + "; "\
               + indent + f"GRPC_PORT : {self.GRPC_PORT}" + "; "\
               + indent + f"GRPC_HOST : {self.GRPC_HOST}" + "; "\
               + indent + f"GRPC_MAX_WORKERS : {self.GRPC_MAX_WORKERS}" + "; "\
               + indent + f"MAX_ITERATION_PARSE : {self.MAX_ITERATION_PARSE}" + "; "\
               + indent + f"FILE_API_GRPC_HOST : {self.FILE_API_GRPC_HOST}" + "; "\
               + indent + f"FILE_API_GRPC_PORT : {self.FILE_API_GRPC_PORT}" + "; "\
               + indent + f"NOSQL_DATABASE_GRPC_HOST : {self.NOSQL_DATABASE_GRPC_HOST}" + "; "\
               + indent + f"NOSQL_DATABASE_GRPC_PORT : {self.NOSQL_DATABASE_GRPC_PORT}"


class StorageIdentifier :
    FTP = "ftp"
    S3 = "s3"


class LogCode :
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"


class EntityKeyword :
    ENTITY = "entity"
    entities = "entities"
    DATE = "date"
    dates = "dates"
    PLACE = "place"
    places = "places"
    PERSON = "person"
    AUTHOR = "author"
    persons = "persons"
    BIBLIO = "biblio"
    biblios = "biblios"
    BIBLIO_FRAGMENT = "biblio_fragment"
    biblio_fragments = "biblio_fragments"
    SOURCE = "source"
    sources = "sources"
    SOURCE_FRAGMENT = "source_fragment"
    source_fragments = "source_fragments"
    EVENT = "event"
    events = "events"
    OTHER = "other"
    others = "others"
    bonds = "bonds"
    BOND = "bond"
    

class EntityContentKeyword :
    id = "id"
    name = "name"
    description = "description"
    start = "start"
    end = "end"
    point = "point"
    process = "process"
    date = "date"
    time = "time"
    web = "web"
    native = "native"
    author = "author"
    state = "state"
    period = "period"
    link = "link"
    geo = "geo"
    latitude = "latitude"
    longitude = "longitude"
    biblio = "biblio"
    source = "source"
    type = "type"
    subtype = "subtype"
    min = "min"
    max = "max"
    event = "event"
    parents = "parents"
    childs = "childs"
    prerequisites = "prerequisites"
    links = "links"
    ex_links = "ex_links"
    meta = "meta"
    level = "level"


config = Config()