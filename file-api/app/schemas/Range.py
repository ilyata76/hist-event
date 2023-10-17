"""
    Схемы для числовых отрезков и пр.
"""
from pydantic import BaseModel


class Range(BaseModel) :
    start : int
    end : int | None = None