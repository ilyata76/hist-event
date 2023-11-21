from typing import NewType

from pydantic import BaseModel


Status = NewType("Status", str)
Identifier = NewType("identifier", str)


class Meta(BaseModel) :
    status : Status
    name : str


class MetaIdentifier(Meta) :
    identifier : Identifier


class MetaIdentifierList(BaseModel) :
    metas : list[MetaIdentifier]