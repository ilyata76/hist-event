"""
    Конфигурирующиеся и постоянные переменные
"""
import os

yaml_folder = str(os.environ.get("YAML_FOLDER", "./yamls"))
debug = bool(os.environ.get("DEBUG_MODE", False))
use_console_debug = bool(os.environ.get("DEBUG_CONSOLE", False))



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


class ConfigKeywords :
    """
        Для парсинга.
            Определяют константы для конфигов каждой из моделей
    """    
    name : str = "name"
    id : str = "id"
    events : str = "events"
    description : str = "description"
    dates : str = "dates"
    persons : str = "persons"
    places : str = "places"
    sources : str = "sources"
    ex_dates : str = "ex_dates"
    ex_places : str = "ex_places"
    ex_persons : str = "ex_persons"
    ex_sources : str = "ex_sources"