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
    __slots__ = ["files"]
    FILES_FIELD_NUMBER: _ClassVar[int]
    files: _containers.RepeatedCompositeFieldContainer[FileBaseKeyword]
    def __init__(self, files: _Optional[_Iterable[_Union[FileBaseKeyword, _Mapping]]] = ...) -> None: ...

class ManyFilesIdentifierR(_message.Message):
    __slots__ = ["files", "identifier"]
    FILES_FIELD_NUMBER: _ClassVar[int]
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    files: _containers.RepeatedCompositeFieldContainer[FileBaseKeyword]
    identifier: str
    def __init__(self, files: _Optional[_Iterable[_Union[FileBaseKeyword, _Mapping]]] = ..., identifier: _Optional[str] = ...) -> None: ...

class IdentifierR(_message.Message):
    __slots__ = ["identifier"]
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    identifier: str
    def __init__(self, identifier: _Optional[str] = ...) -> None: ...

class IdentifierStatusR(_message.Message):
    __slots__ = ["identifier", "status"]
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    identifier: str
    status: str
    def __init__(self, identifier: _Optional[str] = ..., status: _Optional[str] = ...) -> None: ...

class FileBaseKeyword(_message.Message):
    __slots__ = ["storage", "path", "keyword"]
    STORAGE_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    KEYWORD_FIELD_NUMBER: _ClassVar[int]
    storage: str
    path: str
    keyword: str
    def __init__(self, storage: _Optional[str] = ..., path: _Optional[str] = ..., keyword: _Optional[str] = ...) -> None: ...
