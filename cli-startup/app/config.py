"""
    Конфигурирующиеся и постоянные переменные
"""
import os

yaml_folder = str(os.environ.get("YAML_FOLDER", "./yamls"))
debug = bool(os.environ.get("DEBUG_MODE", True))



class ParseResult :
    """
        Класс для определения констант в контексте парсера
    """
    keyword = "keyword"
    number = "number"
    name = "name"

