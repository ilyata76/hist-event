"""
    Схемы для файлов
"""
from pydantic import BaseModel


class File(BaseModel) :
    """
        Главная схема файла
    """
    filename : str
    path : str


class FileBinary(File) :
    """
        Дополненная бинарным содержанием схема файла
    """
    file : bytes