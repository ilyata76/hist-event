from pydantic import BaseModel


class Identifier(BaseModel) :
    identifier : str


class Status(BaseModel) :
    status : str


class StatusIdentifier(Status, 
                       Identifier) :
    pass