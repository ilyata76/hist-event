"""
    Схемы для файлов
"""
from pathlib import Path
from pydantic import BaseModel, field_serializer


class FileBase(BaseModel) :
    """
        Базовая схема файла
    """
    path : Path  # PATHLIKE /a/b/file.txt
    storage : str # s3, ftp, etc.

    @field_serializer("path")
    def serialize_path(self, path: Path, _info) :
        return path.as_posix()


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


class FileBaseKeyword(FileBase) :
    keyword : str


class FileKeyword(File) :
    """
        Дополненная схема файла ключевым словом (для связи с SQL-gen)
    """
    keyword : str