"""
    Схемы, определяющие сущность
"""
from loguru import logger
from pydantic import BaseModel


class BaseEntity(BaseModel) :
    """
        Сущность описывается несколькими полями
    """
    name : str
    id : int
    events : set[int] | None = None
    description : str | None = None


class BaseEntityConfig :
    """
        Описать константы, по которым будет идти сравнение
            при парсинге
    """
    name : str = "name"
    id : str = "id"
    events : str = "events"
    description : str = "description"



class BaseStorage() :
    """
        Класс управления набором дат/персоналий/мест.
        Используется в первую очередь для лёгкого доступа 
            и регистрации ивентов.
    """

    def __init__(self) :
        logger.debug("Создание класса Storage")
        self.storage = {}


    def append(self, entity : BaseEntity) -> bool :
        """
            Добавить в словарь
        """
        res = True
        try :
            self.storage.update({entity.id : entity})
            res = True
        except Exception as exc:
            logger.error("Ошибка во время добавления в Storage exc={exc}", exc=exc)
        logger.debug("Добавление сущности в Storage res={res}", res=res)
        return res


    def get(self, id) -> BaseEntity | None :
        """
            Взятие по индексу. Вернёт None, если такого нет
        """
        res = None
        try : 
            res = self.storage.get(id, None)
        except Exception as exc:
            logger.error("Ошибка во взятия по индексу в Storage exc={exc}", exc=exc)
        logger.debug("Получение сущности из Storage res={res}", res=res)
        return res


    def registerEvent(self, id, event_id) -> bool :
        """
            "Зарегистрировать" событие. Будет проходить во время
                обхода текстов событий event_id ... {entity:id}[name]
        """
        res = False
        try : 
            entity = self.get(id)
            if entity :
                if entity.events is None :
                    entity.events = set([event_id])
                else :
                    entity.events.add(event_id)
                res = True
        except Exception as exc:
            logger.error("Ошибка во время регистрации ивента{event} для сущности{entity} в Storage exc={exc}", 
                         event=event_id, exc=exc, entity=id)
        logger.debug("Регистрация события{event} для сущности{entity} в Storage res={res}", 
                     entity=id, event=event_id, res=res)
        return res


    def __str__(self) -> str :
        """
            Для принта и логов
        """
        try : 
            return self.storage.__str__()
        except :
            return "None"