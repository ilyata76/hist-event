from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class StorageR(_message.Message):
    __slots__ = ["storage"]
    STORAGE_FIELD_NUMBER: _ClassVar[int]
    storage: str
    def __init__(self, storage: _Optional[str] = ...) -> None: ...

class PingR(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class PongR(_message.Message):
    __slots__ = ["pong"]
    PONG_FIELD_NUMBER: _ClassVar[int]
    pong: str
    def __init__(self, pong: _Optional[str] = ...) -> None: ...

class FileR(_message.Message):
    __slots__ = ["file"]
    FILE_FIELD_NUMBER: _ClassVar[int]
    file: File
    def __init__(self, file: _Optional[_Union[File, _Mapping]] = ...) -> None: ...

class FileBaseR(_message.Message):
    __slots__ = ["file"]
    FILE_FIELD_NUMBER: _ClassVar[int]
    file: FileBase
    def __init__(self, file: _Optional[_Union[FileBase, _Mapping]] = ...) -> None: ...

class StorageSegmentR(_message.Message):
    __slots__ = ["storage", "start", "end"]
    STORAGE_FIELD_NUMBER: _ClassVar[int]
    START_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    storage: str
    start: int
    end: int
    def __init__(self, storage: _Optional[str] = ..., start: _Optional[int] = ..., end: _Optional[int] = ...) -> None: ...

class FileSegmentR(_message.Message):
    __slots__ = ["files"]
    FILES_FIELD_NUMBER: _ClassVar[int]
    files: _containers.RepeatedCompositeFieldContainer[File]
    def __init__(self, files: _Optional[_Iterable[_Union[File, _Mapping]]] = ...) -> None: ...

class IdentifierR(_message.Message):
    __slots__ = ["identifier"]
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    identifier: str
    def __init__(self, identifier: _Optional[str] = ...) -> None: ...

class IdentifierMetaR(_message.Message):
    __slots__ = ["identifier", "status", "name"]
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    identifier: str
    status: str
    name: str
    def __init__(self, identifier: _Optional[str] = ..., status: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class ManyFilesIdentifierR(_message.Message):
    __slots__ = ["files", "identifier"]
    FILES_FIELD_NUMBER: _ClassVar[int]
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    files: _containers.RepeatedCompositeFieldContainer[FileBaseKeyword]
    identifier: str
    def __init__(self, files: _Optional[_Iterable[_Union[FileBaseKeyword, _Mapping]]] = ..., identifier: _Optional[str] = ...) -> None: ...

class FileBaseIdentifierR(_message.Message):
    __slots__ = ["file", "identifier"]
    FILE_FIELD_NUMBER: _ClassVar[int]
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    file: FileBase
    identifier: str
    def __init__(self, file: _Optional[_Union[FileBase, _Mapping]] = ..., identifier: _Optional[str] = ...) -> None: ...

class CountR(_message.Message):
    __slots__ = ["count"]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    count: int
    def __init__(self, count: _Optional[int] = ...) -> None: ...

class FileBase(_message.Message):
    __slots__ = ["storage", "path"]
    STORAGE_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    storage: str
    path: str
    def __init__(self, storage: _Optional[str] = ..., path: _Optional[str] = ...) -> None: ...

class File(_message.Message):
    __slots__ = ["storage", "path", "filename"]
    STORAGE_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    storage: str
    path: str
    filename: str
    def __init__(self, storage: _Optional[str] = ..., path: _Optional[str] = ..., filename: _Optional[str] = ...) -> None: ...

class FileBaseKeyword(_message.Message):
    __slots__ = ["storage", "path", "keyword"]
    STORAGE_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    KEYWORD_FIELD_NUMBER: _ClassVar[int]
    storage: str
    path: str
    keyword: str
    def __init__(self, storage: _Optional[str] = ..., path: _Optional[str] = ..., keyword: _Optional[str] = ...) -> None: ...
