"""
    Схемы, определяющие "ДРУГОЕ" как сущность
"""
from loguru import logger
from schemas.Entity import BaseEntity, BaseStorage


class Other(BaseEntity) :
    """
        Модель, описывающая сущность "другого"
    """
    meta : str | None = None


class OtherStorage(BaseStorage) :
    """
        Класс управления набором "другого".
        Используется в первую очередь для лёгкого доступа 
            и регистрации других сущностей.
    """

    def append(self, other : Other) -> bool :
        logger.info(f"Добавление 'другого' {other} в {self.name}")
        return super().append(other)
    
    def get(self, id : int) -> Other | None :
        logger.info(f"Получение 'другого' {id} из {self.name}")
        return super().get(id)
    
    def registerEntity(self, id : int, entity_id : int, field : str) -> bool :
        logger.info(f"Регистрация в хранилище 'другого' {self.name} новой сущности {entity_id}[{field}] для {id}")
        return super().registerEntity(id, entity_id, field)