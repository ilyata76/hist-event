"""
    Схемы для файлов
"""
from pathlib import Path

from pydantic import BaseModel, field_serializer, Field


class FileBase(BaseModel) :
    """Базовая схема файла"""
    path : Path  # PATHLIKE /a/b/file.txt
    storage : str # s3, ftp, etc.

    @field_serializer("path")
    def serialize_path(self, path: Path, _info) :
        return path.as_posix()


class FileBaseList(BaseModel) :
    files : list[FileBase]


class FileBaseKeyword(FileBase) :
    """Ключевое слово dates, others etc."""
    keyword : str


class FileBaseKeywordList(BaseModel) :
    files : list[FileBaseKeyword]


class File(FileBase) :
    """Главная схема файла, дополненная именем"""
    filename : str | None = None


class FileList(BaseModel) :
    files : list[File]


class FileKeyword(File) :
    """Ключевое слово dates, others etc."""
    keyword : str


class FileKeywordList(BaseModel) :
    files : list[FileKeyword]


class FileBinary(File) :
    """Дополненная бинарным содержанием схема файла"""
    file : bytes = Field(repr=False)


class FileBinaryList(BaseModel) :
    files : list[FileBinary]


class FileBinaryKeyword(FileBinary) :
    """Ключевое слово dates, others etc."""
    keyword : str


class FileBinaryKeywordList(BaseModel) :
    files : list[FileBinaryKeyword]