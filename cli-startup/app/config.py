"""
    Конфигурирующиеся и постоянные переменные
"""
import os

yaml_folder = str(os.environ.get("YAML_FOLDER", "./yamls"))

sql_folder = str(os.environ.get("SQL_FOLDER", "./sqls"))

debug = os.environ.get("DEBUG_MODE", "false")
if debug.lower() == "false" or debug.lower() == "no" :
    debug = False
else :
    debug = True

use_console_debug = os.environ.get("DEBUG_CONSOLE", "false")
if use_console_debug.lower() == "false" or use_console_debug.lower() == "no" :
    use_console_debug = False
else :
    use_console_debug = True

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