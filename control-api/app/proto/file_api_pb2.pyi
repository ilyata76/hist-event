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

class FileBinaryR(_message.Message):
    __slots__ = ["file"]
    FILE_FIELD_NUMBER: _ClassVar[int]
    file: FileBinary
    def __init__(self, file: _Optional[_Union[FileBinary, _Mapping]] = ...) -> None: ...

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

class GetManyFilesMetaInfoRequest(_message.Message):
    __slots__ = ["storage", "start", "end"]
    STORAGE_FIELD_NUMBER: _ClassVar[int]
    START_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    storage: str
    start: int
    end: int
    def __init__(self, storage: _Optional[str] = ..., start: _Optional[int] = ..., end: _Optional[int] = ...) -> None: ...

class GetManyFilesMetaInfoResponse(_message.Message):
    __slots__ = ["TODO"]
    TODO_FIELD_NUMBER: _ClassVar[int]
    TODO: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, TODO: _Optional[_Iterable[str]] = ...) -> None: ...

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

class FileBinary(_message.Message):
    __slots__ = ["storage", "path", "filename", "file"]
    STORAGE_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    FILE_FIELD_NUMBER: _ClassVar[int]
    storage: str
    path: str
    filename: str
    file: bytes
    def __init__(self, storage: _Optional[str] = ..., path: _Optional[str] = ..., filename: _Optional[str] = ..., file: _Optional[bytes] = ...) -> None: ...
