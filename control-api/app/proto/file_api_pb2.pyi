from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class PingRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class PingResponse(_message.Message):
    __slots__ = ["pong"]
    PONG_FIELD_NUMBER: _ClassVar[int]
    pong: str
    def __init__(self, pong: _Optional[str] = ...) -> None: ...

class AddFileRequest(_message.Message):
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

class AddFileResponse(_message.Message):
    __slots__ = ["storage", "path", "filename"]
    STORAGE_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    storage: str
    path: str
    filename: str
    def __init__(self, storage: _Optional[str] = ..., path: _Optional[str] = ..., filename: _Optional[str] = ...) -> None: ...

class GetFileRequest(_message.Message):
    __slots__ = ["storage", "path"]
    STORAGE_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    storage: str
    path: str
    def __init__(self, storage: _Optional[str] = ..., path: _Optional[str] = ...) -> None: ...

class GetFileResponse(_message.Message):
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

class GetFileMetaInfoRequest(_message.Message):
    __slots__ = ["storage", "path"]
    STORAGE_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    storage: str
    path: str
    def __init__(self, storage: _Optional[str] = ..., path: _Optional[str] = ...) -> None: ...

class GetFileMetaInfoResponse(_message.Message):
    __slots__ = ["storage", "path", "filename"]
    STORAGE_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    storage: str
    path: str
    filename: str
    def __init__(self, storage: _Optional[str] = ..., path: _Optional[str] = ..., filename: _Optional[str] = ...) -> None: ...

class DeleteFileRequest(_message.Message):
    __slots__ = ["storage", "path"]
    STORAGE_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    storage: str
    path: str
    def __init__(self, storage: _Optional[str] = ..., path: _Optional[str] = ...) -> None: ...

class DeleteFileResponse(_message.Message):
    __slots__ = ["storage", "path", "filename"]
    STORAGE_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    storage: str
    path: str
    filename: str
    def __init__(self, storage: _Optional[str] = ..., path: _Optional[str] = ..., filename: _Optional[str] = ...) -> None: ...

class PutFileRequest(_message.Message):
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

class PutFileResponse(_message.Message):
    __slots__ = ["storage", "path", "filename"]
    STORAGE_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    storage: str
    path: str
    filename: str
    def __init__(self, storage: _Optional[str] = ..., path: _Optional[str] = ..., filename: _Optional[str] = ...) -> None: ...

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
    TODO: str
    def __init__(self, TODO: _Optional[str] = ...) -> None: ...
