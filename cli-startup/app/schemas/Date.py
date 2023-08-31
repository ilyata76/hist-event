"""
    Схемы, определяющие дату сущность
"""
from loguru import logger
from schemas.Entity import BaseEntity, BaseStorage, BaseEntityConfig


class Date(BaseEntity) :
    """
        Модель, описывающая сущность даты
    """


class DateConfig(BaseEntityConfig) :
    """
        Константы для парсинга, как у BaseEntityConfig
    """


class DateStorage(BaseStorage) :
    """
        Класс управления набором дат.
        Используется в первую очередь для лёгкого доступа 
            и регистрации ивентов.
    """

    def append(self, date : Date) -> bool :
        logger.info("Добавление даты date={date}", date=date)
        return super().append(date)
    
    def get(self, id : int) -> Date | None :
        logger.info("Получение даты id={id}", id={id})
        return super().get(id)
    
    def registerEvent(self, id : int, event_id : int) -> bool :
        logger.info("Регистрация ивента для даты id={id} event_id={event_id}", id=id, event_id=event_id)
        return super().registerEvent(id, event_id)