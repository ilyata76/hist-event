"""
    Схемы, определяющие место как сущность
"""
from loguru import logger
from schemas.Entity import BaseEntity, BaseStorage


class Place(BaseEntity) :
    """
        Модель, описывающая сущность места
    """


class PlaceStorage(BaseStorage) :
    """
        Класс управления набором мест.
        Используется в первую очередь для лёгкого доступа 
            и регистрации других сущностей.
    """

    def append(self, place : Place) -> bool :
        logger.info(f"Добавление места {place} в {self.name}")
        return super().append(place)

    def get(self, id : int) -> Place | None :
        logger.info(f"Получение места {id} из {self.name}")
        return super().get(id)
    
    def registerEntity(self, id : int, entity_id : int, field : str) -> bool :
        logger.info(f"Регистрация в хранилище мест {self.name} новой сущности {entity_id}[{field}] для {id}")
        return super().registerEntity(id, entity_id, field)