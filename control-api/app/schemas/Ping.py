"""
    Для REST
"""
from pydantic import BaseModel


class Pong(BaseModel) :
    """
        Модель возврата на запрос /ping
    """
    pong : str


class PongReponse(Pong) :
    """
        Модель возврата на запрос /ping, но с уточнением сервиса
    """
    service : str