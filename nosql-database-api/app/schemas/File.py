"""
    Схемы для файлов
"""
from pydantic import BaseModel


class FileBase(BaseModel) :
    """
        Базовая схема файла
    """
    path : str  # PATHLIKE /a/b/file.txt
    storage : str # s3, ftp, etc.


class File(FileBase) :
    """
        Главная схема файла, дополненная именем
    """
    filename : str #


class FileBinary(File) :
    """
        Дополненная бинарным содержанием схема файла
    """
    file : bytes