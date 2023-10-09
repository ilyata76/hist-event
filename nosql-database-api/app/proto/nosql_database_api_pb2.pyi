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

class PutFileRequest(_message.Message):
    __slots__ = ["filename", "path"]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    filename: str
    path: str
    def __init__(self, filename: _Optional[str] = ..., path: _Optional[str] = ...) -> None: ...

class PutFileResponse(_message.Message):
    __slots__ = ["filename", "path"]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    filename: str
    path: str
    def __init__(self, filename: _Optional[str] = ..., path: _Optional[str] = ...) -> None: ...

class DeleteFileRequest(_message.Message):
    __slots__ = ["filename"]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    filename: str
    def __init__(self, filename: _Optional[str] = ...) -> None: ...

class DeleteFileResponse(_message.Message):
    __slots__ = ["filename", "path"]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    filename: str
    path: str
    def __init__(self, filename: _Optional[str] = ..., path: _Optional[str] = ...) -> None: ...

class AddFileRequest(_message.Message):
    __slots__ = ["filename", "path"]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    filename: str
    path: str
    def __init__(self, filename: _Optional[str] = ..., path: _Optional[str] = ...) -> None: ...

class AddFileResponse(_message.Message):
    __slots__ = ["filename", "path"]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    filename: str
    path: str
    def __init__(self, filename: _Optional[str] = ..., path: _Optional[str] = ...) -> None: ...

class GetFileRequest(_message.Message):
    __slots__ = ["filename"]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    filename: str
    def __init__(self, filename: _Optional[str] = ...) -> None: ...

class GetFileResponse(_message.Message):
    __slots__ = ["filename", "path"]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    filename: str
    path: str
    def __init__(self, filename: _Optional[str] = ..., path: _Optional[str] = ...) -> None: ...

class GetManyFilesRequest(_message.Message):
    __slots__ = ["start_pos", "limit"]
    START_POS_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    start_pos: int
    limit: int
    def __init__(self, start_pos: _Optional[int] = ..., limit: _Optional[int] = ...) -> None: ...

class GetManyFilesResponse(_message.Message):
    __slots__ = ["TODO"]
    TODO_FIELD_NUMBER: _ClassVar[int]
    TODO: str
    def __init__(self, TODO: _Optional[str] = ...) -> None: ...
