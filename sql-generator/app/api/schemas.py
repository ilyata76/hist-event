from pydantic import BaseModel

class Ping(BaseModel) :
    result : str

class PostSQL(BaseModel) :
    result : int

class PostYAML(BaseModel) :
    errors : list[str]