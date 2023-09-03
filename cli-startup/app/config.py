"""
    Конфигурирующиеся и постоянные переменные
"""
import os

yaml_folder = str(os.environ.get("YAML_FOLDER", "./yamls"))
sql_folder = str(os.environ.get("SQL_FOLDER", "./sqls"))
debug = bool(os.environ.get("DEBUG_MODE", False))
use_console_debug = bool(os.environ.get("DEBUG_CONSOLE", False))
max_reparse_count = int(os.environ.get("MAX_REPARSE_COUNT", 10))


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
    # person специфика
    person : str = "person"
    # place специфика
    geo : str = "geo"
    # source специфика
    link : str = "link"
    author : str = "author"
    # other специфика
    meta : str = "meta"
    # event специфика
    min : str = "min"
    max : str = "max"
    level : str = "level"
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