"""
    Файл переопределяет некоторые исключения для последующей их обработки
"""
from enum import Enum


class MyException(Exception) :
    def __init__(self, *, code : int, detail : str) :
        self.code = code
        self.detail = detail
    
    def __str__(self) -> str :
        return self.detail


class ConfigExceptionCode(Enum) :
    INVALID_KEYWORD = 1

class ConfigException(MyException) :
    """
        Класс для ошибок, связанных с какими-либо конфигурирующими переменными
    """


class ValidationExceptionCode(Enum) :
    INVALID_FIELD = 1
    INVALID_FIELD_CONTENT = 2
    CROSS_EXCLUDING_FIELDS = 3
    INVALID_FIELD_OR_ENTITY_TYPE = 4

class ValidationException(MyException) :
    """
        Класс для ошибок, возвращаемых при проваленной валидации
    """