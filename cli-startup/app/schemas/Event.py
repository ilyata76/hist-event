"""
    Схемы, определяющие событие как сущность
"""
from loguru import logger
from schemas.Entity import BaseEntity, BaseStorage


class Event(BaseEntity) :
    """
        Модель, описывающая сущность события
    """
    date : str | None = None
    min : str | None = None
    max : str | None = None
    level : str | None = None


class EventStorage(BaseStorage) :
    """
        Класс управления набором событий.
        Используется в первую очередь для лёгкого доступа 
            и регистрации других сущностей.
    """

    def append(self, event : Event) -> bool :
        logger.info(f"Добавление события {event} в {self.name}")
        return super().append(event)
    
    def get(self, id : int) -> Event | None :
        logger.info(f"Получение события {id} из {self.name}")
        return super().get(id)
    
    def registerEntity(self, id : int, entity_id : int, field : str) -> bool :
        logger.info(f"Регистрация в хранилище событий {self.name} новой сущности {entity_id}[{field}] для {id}")
        return super().registerEntity(id, entity_id, field)