from typing import NewType

from pydantic import BaseModel


Identifier = NewType("Identifier", str)
Status = NewType("Status", str)


class Meta(BaseModel) :
    status : Status
    name : str


class MetaIdentifier(Meta) :
    identifier : Identifier


class MetaIdentifierList(BaseModel) :
    metas : list[MetaIdentifier]