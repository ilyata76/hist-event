from pydantic import BaseModel


class Ping(BaseModel) :
    result : str


class PostProcess(BaseModel) :
    result : int
    stdout : bytes


class PostYAML(BaseModel) :
    errors : list[str]