"""
    Классы работы с сущностями
"""
import datetime
from pydantic import BaseModel

from utils.exception import ValidationException as VE, ValidationExceptionCode as VECode
from utils.config import EntityContentKeyword as ECK


class Entity(BaseModel) :
    """
        Класс базовой сущности.
            Сущность определяет поля, а также всю работу с ними - от валидации до генерации SQL.
    """
    id : int
    name : str

    @staticmethod
    def validate(entity_identifier : str, dict_entity : dict) :
        """Базовая функция валидации всех сущностей"""
        if type(dict_entity) != dict :
            raise VE(code=VECode.INVALID_FIELD_OR_ENTITY_TYPE,
                     detail=f"Сущность {entity_identifier} представлена неправильно")
        if ECK.id not in dict_entity.keys() :
            raise VE(code=VECode.INVALID_FIELD,
                     detail=f"У сущности {entity_identifier} поле {ECK.id} является обязательным")
        if ECK.name not in dict_entity.keys() :
            raise VE(code=VECode.INVALID_FIELD,
                     detail=f"У сущности {entity_identifier} поле {ECK.name} является обязательным")
        try :
            int(dict_entity[ECK.id])
        except :
            raise VE(code=VECode.INVALID_FIELD_CONTENT,
                     detail=f"У сущности {entity_identifier} поле {ECK.id} должно быть целочисленным типом")


class DateTime(BaseModel) :
    date : datetime.date | str
    time : datetime.time | None = None

    @staticmethod
    def validate(entity_identifier: str, dict_entity: dict) :
        if type(dict_entity) != dict :
            raise VE(code=VECode.INVALID_FIELD_OR_ENTITY_TYPE,
                     detail=f"Сущность {entity_identifier} в поле -->|{ECK.start} {ECK.end}/{ECK.point}|<-- представлена неправильно")
        if ECK.date not in dict_entity.keys() :
            raise VE(code=VECode.INVALID_FIELD,
                     detail=f"У сущности {entity_identifier} поле {ECK.date} является обязательным")
        if dict_entity[ECK.date] != "..." : # TODO: разные варианты могут быть: нет данных, настоящее время и пр.
            try :
                datetime.date.fromisoformat(dict_entity[ECK.date])
            except :
                raise VE(code=VECode.INVALID_FIELD_CONTENT,
                         detail=f"У сущности {entity_identifier} поле {ECK.date} должно представлять собой строку даты формата ISO или '...'")
        if ECK.time in dict_entity.keys() and dict_entity[ECK.time] != "...":
            try :
                datetime.time.fromisoformat(dict_entity[ECK.time])
            except :
                raise VE(code=VECode.INVALID_FIELD_CONTENT,
                         detail=f"У сущности {entity_identifier} поле {ECK.time} должно представлять собой стоку времени формата ISO или '...'")


class DateProcess(BaseModel) :
    start : DateTime | None = None
    end : DateTime | None = None

    @staticmethod
    def validate(entity_identifier: str, dict_entity: dict) :
        if type(dict_entity) != dict :
            raise VE(code=VECode.INVALID_FIELD_OR_ENTITY_TYPE,
                    detail=f"Сущность {entity_identifier} в поле -->|{ECK.process}|<-- представлена неправильно")
        if not (ECK.start in dict_entity.keys() and\
                ECK.end in dict_entity.keys()) :
            raise VE(code=VECode.INVALID_FIELD,
                     detail=f"У сущности {entity_identifier} в поле -->|{ECK.process}|<-- поля {ECK.start} и {ECK.end} является обязательным")
        DateTime.validate(entity_identifier, dict_entity[ECK.start])
        DateTime.validate(entity_identifier, dict_entity[ECK.end])


class Date(Entity) :
    """
        -   id:
            name:
            point:      <---- OR
                date:
                time:
            process:    <---- OR
                start:
                    date:
                    time:
                end:
                    date:
                    time:
            description:
    """
    process : DateProcess | None = None
    point : DateTime | None = None
    description : str | None = None

    @staticmethod
    def validate(entity_identifier: str, dict_entity: dict) :
        Entity.validate(entity_identifier, dict_entity)
        # должны существовать либо process-метки, либо point-метка
        if ECK.point in dict_entity.keys() and\
           ECK.process in dict_entity.keys() :
            raise VE(code=VECode.CROSS_EXCLUDING_FIELDS,
                     detail=f"У сущности {entity_identifier} поля {ECK.point} и {ECK.process} являются взаимоисключающими")
        if not (ECK.point in dict_entity.keys() or\
                ECK.process in dict_entity.keys()) :
            raise VE(code=VECode.INVALID_FIELD,
                     detail=f"У сущности {entity_identifier} одно из полей {ECK.point}/ {ECK.process} является обязательным")
        if ECK.point in dict_entity.keys() :
            DateTime.validate(entity_identifier, dict_entity[ECK.point])
        if ECK.process in dict_entity.keys() :
            DateProcess.validate(entity_identifier, dict_entity[ECK.process])


class Event(Entity) :
    pass