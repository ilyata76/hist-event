"""
    Схемы, определяющие персоналию как сущность
"""
from loguru import logger
from schemas.Entity import BaseEntity, BaseStorage, BaseEntityConfig
from schemas.Date import Date
from schemas.Place import Place


class Person(BaseEntity) :
    """
        Модель, описывающая сущность персоналии
    """
    dates : set[Date] | None = None
    places : set[Place] | None = None


class PersonConfig(BaseEntityConfig) :
    """
        Константы для парсинга, как у BaseEntityConfig
    """
    dates : str = "dates"
    places : str = "places"


class PersonStorage(BaseStorage) :
    """
        Класс управления набором дат.
        Используется в первую очередь для лёгкого доступа 
            и регистрации ивентов.
    """

    def append(self, person : Person) -> bool :
        logger.info("Добавление персоналии person={person}", person=person)
        return super().append(person)
    
    def get(self, id : int) -> Person | None :
        logger.info("Получение персоналии id={id}", id=id)
        return super().get(id)
    
    def registerEvent(self, id : int, event_id : int) -> bool :
        logger.info("Регистрация ивента для персоналии id={id}, event_id={event_id}", id=id, event_id=event_id)
        return super().registerEvent(id, event_id)
    
    def registerDate(self, id : int , date_id : int) -> bool :
        """
            "Зарегистрировать" дату. 
                Будет регистрировать во время прохода по description персоналии.
        """
        logger.info("Регистрация даты для персоналии id={id}, date_id={date_id}", id=id, date_id=date_id)

        res = False
        try : 
            person = self.get(id)
            if person :
                if person.dates is None :
                    person.dates = set([date_id])
                else :
                    person.dates.add(date_id)
                res = True
        except Exception as exc:
            logger.error("Ошибка во время регистрации даты{date} для сущности{entity} в Storage exc={exc}", 
                         date=date_id, exc=exc, entity=id)
        logger.debug("Регистрация даты{date} для сущности{entity} в Storage res={res}", 
                     entity=id, date=date_id, res=res)
        return res
    
    def registerPlace(self, id : int, place_id : int) -> bool :
        """
            "Зарегистрировать" место. 
                Будет регистрировать во время прохода по description персоналии.
        """
        logger.info("Регистрация места для персоналии id={id}, place_id={place_id}", id=id, place_id=place_id)

        res = False
        try : 
            person = self.get(id)
            if person :
                if person.places is None :
                    person.places = set([place_id])
                else :
                    person.places.add(place_id)
                res = True
        except Exception as exc:
            logger.error("Ошибка во время регистрации места{place} для сущности{entity} в Storage exc={exc}", 
                         place=place_id, exc=exc, entity=id)
        logger.debug("Регистрация места{place} для сущности{entity} в Storage res={res}", 
                     entity=id, place=place_id, res=res)
        return res