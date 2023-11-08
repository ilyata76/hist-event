"""
    Для pyparsing
"""
from pydantic import BaseModel


class ParseResult(BaseModel) :
    keyword : str
    number : int
    name : str