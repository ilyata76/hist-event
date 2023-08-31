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
        Класс для определения ключевых слов в {КЛЮЧЕВОЕ СЛОВО:1}[description]
    """
    date = "date"
    person = "person"
    place = "place"


class YamlKeywords :
    """
        Для определения некоторых параметров YAML конфигураций
    """
    dates = "dates"
    persons = "persons"
    places = "places"