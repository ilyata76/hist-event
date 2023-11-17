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


class StorageExceptionCode(Enum) :
    """
        Коды для StorageException.code
    """
    METHOD_NOT_REALIZED = 1
    SERVICE_UNAVAILABLE = 2
    ALREADY_EXISTS = 3
    ENTITY_DOESNT_EXISTS = 4

class StorageException(MyException) :
    """
        Класс для ошибок, связанных с работой хранилищ
    """


class ConfigExceptionCode(Enum) :
    INVALID_STORAGE_IDENTIFIER = 1

class ConfigException(MyException) :
    """
        Класс для ошибок, связанных с какими-либо конфигурирующими переменными
    """