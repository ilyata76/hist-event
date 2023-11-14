from pydantic import BaseModel


class ParseResult(BaseModel) :
    """Для pyparsing"""
    keyword : str
    number : int
    name : str