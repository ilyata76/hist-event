"""
    Файл переопределяет некоторые исключения для последующей их обработки
"""
from enum import Enum


class DBExceptionCode(Enum) :
    """
        Коды для DBException.code
    """
    SERVICE_UNAVAIABLE = 1
    ENTITY_EXISTS = 2
    INVALIDATED = 3
    TOO_LARGE = 4
    OPERATION_ERROR = 5
    METHOD_NOT_REALIZED = 6
    ENTITY_DONT_EXISTS = 7


class DBException(Exception) :
    """
        Класс для ошибок, связанных с работой баз данных
    """

    def __init__(self, *, code : int, detail : str) :
        self.code = code
        self.detail = detail
    
    def __str__(self) -> str :
        return self.detail