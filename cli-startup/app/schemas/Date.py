"""
    Схемы, определяющие дату как сущность
"""
from loguru import logger
from schemas.Entity import BaseEntity, BaseStorage


class Date(BaseEntity) :
    """
        Модель, описывающая сущность даты
    """
    date : str | None = None


class DateStorage(BaseStorage) :
    """
        Класс управления набором дат.
        Используется в первую очередь для лёгкого доступа 
            и регистрации других сущностей.
    """

    def append(self, date : Date) -> bool :
        logger.info(f"Добавление даты {date} в {self.name}")
        return super().append(date)
    
    def get(self, id : int) -> Date | None :
        logger.info(f"Получение даты {id} из {self.name}")
        return super().get(id)
    
    def registerEntity(self, id : int, entity_id : int, field : str) -> bool :
        logger.info(f"Регистрация в хранилище дат {self.name} новой сущности {entity_id}[{field}] для {id}")
        return super().registerEntity(id, entity_id, field)