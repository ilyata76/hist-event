"""
    Схемы, определяющие дату как сущность
"""
from loguru import logger
from pydantic import BaseModel


class Date(BaseModel) :
    """
        Модель, описывающая сущность даты
    """
    name : str
    id : int
    events : set[int] | None = None
    description : str | None = None


class DateStorage() :
    """
        Класс управления набором дат.
        Используется в первую очередь для лёгкого доступа 
            и регистрации ивентов.
    """

    def __init__(self) :
        logger.debug("Создание класса DateStorage")
        self.storage = {}


    def append(self, date : Date) -> bool :
        """
            Добавить в словарь
        """
        res = True
        try :
            self.storage.update({date.id : date})
            res = True
        except Exception as exc:
            logger.error("Ошибка во время добавления в DateStorage exc={exc}", exc=exc)
        logger.debug("Добавление даты в DateStorage res={res}", res=res)
        return res


    def get(self, id) -> Date | None :
        """
            Взятие по индексу. Вернёт None, если такого нет
        """
        res = None
        try : 
            res = self.storage.get(id, None)
        except Exception as exc:
            logger.error("Ошибка во взятия по индексу в DateStorage exc={exc}", exc=exc)
        logger.debug("Получение даты из DateStorage res={res}", res=res)
        return res
    

    def registerEvent(self, id, event_id) -> bool :
        """
            "Зарегистрировать" событие. Будет проходить во время
                обхода текстов событий event_id ... {date:id}[name]
        """
        res = False
        try : 
            date = self.get(id)
            if date :
                if date.events is None :
                    date.events = set([event_id])
                else :
                    date.events.add(event_id)
                res = True
        except Exception as exc:
            logger.error("Ошибка во время регистрации ивента{event} для даты{date} в DateStorage exc={exc}", 
                         event=event_id, exc=exc, date=id)
        logger.debug("Регистрация события{event} для даты{date} в DateStorage res={res}", 
                     date=id, event=event_id, res=res)
        return res


    def __str__(self) -> str :
        """
            Для принта и логов
        """
        try : 
            return self.storage.__str__()
        except :
            return "None"