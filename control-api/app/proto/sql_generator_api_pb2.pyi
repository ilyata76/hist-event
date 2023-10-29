from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PingR(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class PongR(_message.Message):
    __slots__ = ["pong"]
    PONG_FIELD_NUMBER: _ClassVar[int]
    pong: str
    def __init__(self, pong: _Optional[str] = ...) -> None: ...

class ManyFilesR(_message.Message):
    __slots__ = ["files", "main_sql", "identifier"]
    FILES_FIELD_NUMBER: _ClassVar[int]
    MAIN_SQL_FIELD_NUMBER: _ClassVar[int]
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    files: _containers.RepeatedCompositeFieldContainer[File]
    main_sql: File
    identifier: str
    def __init__(self, files: _Optional[_Iterable[_Union[File, _Mapping]]] = ..., main_sql: _Optional[_Union[File, _Mapping]] = ..., identifier: _Optional[str] = ...) -> None: ...

class Status(_message.Message):
    __slots__ = ["status", "identifier"]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    status: str
    identifier: str
    def __init__(self, status: _Optional[str] = ..., identifier: _Optional[str] = ...) -> None: ...

class File(_message.Message):
    __slots__ = ["storage", "path", "filename", "keyword"]
    STORAGE_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    KEYWORD_FIELD_NUMBER: _ClassVar[int]
    storage: str
    path: str
    filename: str
    keyword: str
    def __init__(self, storage: _Optional[str] = ..., path: _Optional[str] = ..., filename: _Optional[str] = ..., keyword: _Optional[str] = ...) -> None: ...
