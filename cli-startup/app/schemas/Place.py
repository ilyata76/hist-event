"""
    Схемы, определяющие место как сущность
"""
from loguru import logger
from schemas.Entity import BaseEntity, BaseStorage, BaseEntityConfig
from schemas.Date import Date


class Place(BaseEntity) :
    """
        Модель, описывающая сущность места
    """
    dates : set[Date] | None = None


class PlaceConfig(BaseEntityConfig) :
    """
        Константы для парсинга, как у BaseEntityConfig
    """
    dates : str = "dates"


class PlaceStorage(BaseStorage) :
    """
        Класс управления набором дат.
        Используется в первую очередь для лёгкого доступа 
            и регистрации ивентов.
    """

    def append(self, place : Place) -> bool :
        logger.info("Добавление места place={place}", place=place)
        return super().append(place)
    
    def get(self, id : int) -> Place | None :
        logger.info("Получение места id={id}", id=id)
        return super().get(id)
    
    def registerEvent(self, id : int, event_id : int) -> bool :
        logger.info("Регистрация ивента для места id={id}, event_id={event_id}", id=id, event_id=event_id)
        return super().registerEvent(id, event_id)
    
    def registerDate(self, id : int , date_id : int) -> bool :
        """
            "Зарегистрировать" дату. 
                Будет регистрировать во время прохода по description места.
        """
        logger.info("Регистрация даты для персоналии id={id}, date_id={date_id}", id=id, date_id=date_id)

        res = False
        try : 
            place = self.get(id)
            if place :
                if place.dates is None :
                    place.dates = set([date_id])
                else :
                    place.dates.add(date_id)
                res = True
        except Exception as exc:
            logger.error("Ошибка во время регистрации даты{date} для сущности{entity} в Storage exc={exc}", 
                         date=date_id, exc=exc, entity=id)
        logger.debug("Регистрация даты{date} для сущности{entity} в Storage res={res}", 
                     entity=id, date=date_id, res=res)
        return res