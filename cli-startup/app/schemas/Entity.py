"""
    Схемы, определяющие сущность
"""
from loguru import logger
from pydantic import BaseModel


class BaseEntity(BaseModel) :
    """
        Сущность описывается несколькими полями
    """
    # базовая часть
    name : str
    id : int
    events : set[int] | None = None
    description : str | None = None
    # часть, которая может быть заполнена в зависимости
    #   от типа сущности
    dates : set[int] | None = None
    ex_dates : set[int] | None = None # ссылки от внешних источников
    places : set[int] | None = None
    ex_places : set[int] | None = None # ссылки от внешних источников
    persons : set[int] | None = None
    ex_persons : set[int] | None = None # ссылки от внешних источников


class BaseStorage() :
    """
        Класс управления набором дат/персоналий/мест.
        Используется в первую очередь для лёгкого доступа 
            и регистрации ивентов.
    """

    def __init__(self, name = None) :
        logger.debug("Создание класса Storage")
        self.storage = {}
        self.name = name if name else "BaseStorage"


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
            raise exc
        logger.debug("Добавление сущности в Storage res={res}", res=res)
        return res


    def get(self, id : int) -> BaseEntity | None :
        """
            Взятие по индексу. Вернёт None, если такого нет
        """
        res = None
        try : 
            res = self.storage.get(id, None)
        except Exception as exc:
            logger.error("Ошибка во взятия по индексу в Storage exc={exc}", exc=exc)
            raise exc
        logger.debug("Получение сущности из Storage res={res}", res=res)
        return res


    def registerEntity(self, id : int, entity_id : int, field : str) -> bool :
        """
            Зарегистрировать одну сущность для другой по field. Если существует, конечно.
                field - см. ConfigKeywords.dates ex_dates и др.
        """
        res = False
        try : 
            entity = self.get(id)

            if entity and field in entity.model_fields :
                att_field = getattr(entity, field)
                if att_field is None :
                    setattr(entity, field, set([entity_id]))
                else :
                    att_field.add(entity_id)
                res = True

        except Exception as exc:
            logger.error("Сохранение/регтстрация сущности {entity_id} по полю {field} для сущности {id} в хранилище {name}. exc={exc}", 
                         field=field, entity_id=entity_id, exc=exc, id=id, name=self.name)
            raise exc
        
        logger.debug(f"Сохранение/регтстрация сущности {entity_id} по полю {field} для сущности {id} в хранилище {self.name}. res={res}")
        return res


    def saveEntity(self, id : int, entity_id : int, field : str) -> bool :
        """
            Другое название для registerEntity (для читаемости).
                field - см. ConfigKeywords.dates ex_dates и др.
        """
        print("переход")
        return self.registerEntity(id, entity_id, field)


    def __str__(self) -> str :
        """
            Для принта и логов
        """
        try : 
            result = self.name + "\n"
            for key in self.storage :
                result += str(key) + "  :  " + str(self.storage[key]) + "\n"
            return result
        except Exception as exc:
            logger.error("Ошибка во время вывода _str_ exc={exc}", exc=exc)
            return "Error"