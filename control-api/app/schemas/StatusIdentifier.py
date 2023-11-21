from typing import NewType

from pydantic import BaseModel


Identifier = NewType("identifier", str)
Status = NewType("status", str)


class StatusIdentifier(BaseModel) :
    identifier : Identifier
    status : Status


class StatusMeta(StatusIdentifier) :
    name : str