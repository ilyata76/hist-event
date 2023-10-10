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
