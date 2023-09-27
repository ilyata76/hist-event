"""
    Конфигурирующиеся и постоянные переменные
"""
import os, sys
from pathlib import Path
from loguru import logger

yaml_folder = Path(str(os.environ.get("YAML_FOLDER", "./files/yamls")))
sql_folder = Path(str(os.environ.get("SQL_FOLDER", "./files/sqls")))
stdout_log_folder = Path(str(os.environ.get("STDOUT_LOG_FOLDER", "./files/stdout-logs")))

files_folder = Path(str(os.environ.get("FILES_FOLDER", "./files")))

ftp_username = str(os.environ.get("FTP_USERNAME", "admin"))
ftp_password = str(os.environ.get("FTP_PASSWORD", "admin"))

ftp_host = str(os.environ.get("FTP_HOST", "localhost"))
ftp_port = int(os.environ.get("FTP_PORT", 21))

debug = os.environ.get("DEBUG_MODE", "false")
if debug.lower() == "false" or debug.lower() == "no" :
    debug = False
else :
    debug = True

use_log_console= os.environ.get("LOG_CONSOLE", "false")
if use_log_console.lower() == "false" or use_log_console.lower() == "no" :
    use_log_console = False
else :
    use_log_console = True

max_reparse_count = int(os.environ.get("MAX_REPARSE_COUNT", 10))

logs_folder = Path(str(os.environ.get("LOGS_FOLDER", "./logs")))
logs_filename = str(os.environ.get("LOGS_FILENAME", "sql-generator.log"))

parse_keyword_special_symbols = str(os.environ.get("PARSE_KEYWORD_SPECIAL_SYMBOLS", "_"))
parse_name_special_symbols = str(os.environ.get("PARSE_NAME_SPECIAL_SYMBOLS", " _-/\\:()?!"))


logger_configured : bool = False

def configure_logger() : 
    """
    """
    global logger_configured
    if logger_configured :
        return
    
    logger.remove(0)
    logger.add(sys.stderr, level="WARNING")

    level = "DEBUG" if debug else "INFO"

    logger.add(logs_folder.joinpath(logs_filename), 
                   format="{time} {level} {message}", level=level, rotation="4 MB", compression="zip")
    
    if use_log_console :
        logger.add(sys.stdout, level=level)
    
    logger_configured = True


class ParseResult :
    """
        Класс для определения констант в контексте парсера
    """
    keyword = "keyword"
    number = "number"
    name = "name"


class ParseKeywords :
    """
        Класс для определения ключевых слов в {>КЛЮЧЕВОЕ СЛОВО<:1}[description]
    """
    date = "date"
    person = "person"
    place = "place"
    source = "source"
    other = "other"
    event = "event"
    source_fragment = "source_fragment"
    biblio = "biblio"
    biblio_fragment = "biblio_fragment"


class ConfigKeywords :
    """
        Для парсинга.
            Определяют константы для конфигов каждой из моделей
    """
    name : str = "name"
    id : str = "id"
    events : str = "events"
    description : str = "description"
    # date & event специфика
    date : str = "date"
    time : str = "time"
    start_date : str = "start_date"
    end_date : str = "end_date"
    start_time : str = "start_time"
    end_time : str = "end_time"
    start : str = "start"
    end : str = "end"
    # person специфика
    person : str = "person"
    # place специфика
    geo : str = "geo"
    # source специфика
    link : str = "link"
    author : str = "author"
    type : str = "type"
    subtype : str = "subtype"
    # other специфика
    meta : str = "meta"
    # event специфика
    min : str = "min"
    max : str = "max"
    level : str = "level"
    # source_fragment специфика
    source : str = "source"
    # biblio специфика
    state : str = "state"
    period : str = "period"
    # biblio_fragment специфика
    biblio : str = "biblio"
    # bond специфика
    event : str = "event"
    parents : str = "parents"
    childs : str = "childs"
    prerequisites : str = "prerequisites"
    ##
    dates : str = "dates"
    persons : str = "persons"
    places : str = "places"
    sources : str = "sources"
    others : str = "others"
    ex_dates : str = "ex_dates"
    ex_places : str = "ex_places"
    ex_persons : str = "ex_persons"
    ex_sources : str = "ex_sources"
    ex_others : str = "ex_others"
    events : str = "events"
    ex_events : str = "ex_events"
    source_fragments : str = "source_fragments"
    ex_source_fragments : str = "ex_source_fragments"
    biblios : str = "biblios"
    ex_biblios : str = "ex_biblios"
    biblio_fragments : str = "biblio_fragments"
    ex_biblio_fragments : str = "ex_biblio_fragments"
    bonds : str = "bonds"
    #
    bondswithoutid : str = "bondswithoutid"
    eventsbonds : str = "eventsbonds"


class ConfigPathKeywords:
    """
        Ключевые слова для путей, главным образом для класса Paths
    """
    path_yaml_folder = "path_yaml_folder"
    path_sql_folder = "path_sql_folder"
    dates_path = "dates_path"
    persons_path = "persons_path"
    places_path = "places_path"
    sources_path = "sources_path"
    others_path = "others_path"
    events_path = "events_path"
    biblios_path = "biblios_path"
    bonds_path = "bonds_path"
    main_sql_path = "main_sql_path"
    
    # пути отсчитываются от path-yaml-folder
    dates_default_path = "dates.yaml"
    persons_default_path = "persons.yaml"
    places_default_path = "places.yaml"
    sources_default_path = "sources.yaml"
    others_default_path = "others.yaml"
    events_default_path = "events.yaml"
    biblios_default_path = "biblios.yaml"
    bonds_default_path = "bonds.yaml"
    
    # от path-sql-folder
    main_sql_default_path = "main.sql"