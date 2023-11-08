"""
    Классы работы с сущностями.
        Эти классы - компромиссное решение, обусловленное в первую очередь
        легкостью добавления новых сущностей (получается, что нужно добавить сюда сущность, а в EntityBonds - связать со строками)
"""
import datetime

from pydantic import BaseModel

from utils.config import EntityContentKeyword as ECK
from utils.validate import *


class EntityLink(BaseModel) :
    entity : str | None = None
    id : int | None = None


class Entity(BaseModel) :
    """
        Класс базовой сущности.
            Сущность определяет поля, а также всю работу с ними - от валидации до генерации SQL.
    """
    id : int
    name : str
    description : str | None = None
    links : dict[str, set[int]] = {} # на кого ссылаемся
    ex_links : dict[str, set[int]] = {} # кто ссылается на нас

    @staticmethod
    def validate(entity_identifier : str, dict_entity : dict) :
        """Базовая функция валидации всех сущностей"""
        validateEntityOnDict(entity_identifier, dict_entity)
        validateFieldOnExisting(ECK.id, entity_identifier, dict_entity)
        validateFieldOnExisting(ECK.name, entity_identifier, dict_entity)
        validateFieldOnCasting(ECK.id, entity_identifier, dict_entity, int)

    def textsToParseLinks(self) -> list[str] :
        """Тексты, которые будут проходить проверку на {вставки:id}, чтобы заполнить links & ex_links"""
        return [self.description]

    def foreignKeys(self) -> list[EntityLink] :
        """Foreign-key поля для проверки, что эти сущности уже существуют"""
        return [] # никаких нет


class DateTime(BaseModel) :
    date : datetime.date | str
    time : datetime.time | None = None

    @staticmethod
    def validate(entity_identifier : str, dict_entity : dict) :
        validateEntityOnDict(entity_identifier, dict_entity)
        validateFieldOnExisting(ECK.date, entity_identifier, dict_entity)
        if dict_entity[ECK.date] != "..." : # TODO: разные варианты могут быть: нет данных, настоящее время и пр.
            validateFieldOnCasting(ECK.date, entity_identifier, dict_entity, datetime.date.fromisoformat)
        if ECK.time in dict_entity.keys() and dict_entity[ECK.time] != "...":
            validateFieldOnCasting(ECK.time, entity_identifier, dict_entity, datetime.time.fromisoformat)


class DateProcess(BaseModel) :
    start : DateTime | None = None
    end : DateTime | None = None

    @staticmethod
    def validate(entity_identifier : str, dict_entity : dict) :
        validateEntityOnDict(entity_identifier, dict_entity)
        validateFieldOnExisting(ECK.start, entity_identifier, dict_entity)
        validateFieldOnExisting(ECK.end, entity_identifier, dict_entity)
        DateTime.validate(entity_identifier, dict_entity[ECK.start])
        DateTime.validate(entity_identifier, dict_entity[ECK.end])


class Date(Entity) :
    """
        -   id: int
            name:
            point:      <---- OR
                date: ISO
                time: ISO
            process:    <---- OR
                start:
                    date: ISO
                    time: ISO
                end:
                    date: ISO
                    time: ISO
            description:
    """
    process : DateProcess | None = None
    point : DateTime | None = None

    @staticmethod
    def validate(entity_identifier : str, dict_entity : dict) :
        Entity.validate(entity_identifier, dict_entity)
        validateFieldOnOneOfExisting([ECK.point, ECK.process], entity_identifier, dict_entity)
        validateFieldOnCrossExcluding([ECK.point, ECK.process], entity_identifier, dict_entity)
        if ECK.point in dict_entity.keys() :
            DateTime.validate(entity_identifier, dict_entity[ECK.point])
        if ECK.process in dict_entity.keys() :
            DateProcess.validate(entity_identifier, dict_entity[ECK.process])


class Geo(BaseModel) :
    latitude : float
    longitude : float

    @staticmethod
    def validate(entity_identifier : str, dict_entity : dict) :
        validateEntityOnDict(entity_identifier, dict_entity)
        validateFieldOnExisting(ECK.latitude, entity_identifier, dict_entity)
        validateFieldOnExisting(ECK.longitude, entity_identifier, dict_entity)
        validateFieldOnCasting(ECK.latitude, entity_identifier, dict_entity, float)
        validateFieldOnCasting(ECK.longitude, entity_identifier, dict_entity, float)


class Place(Entity) :
    """
        -   id: int
            name:
            description:
            geo:
                latitude: float
                longitude: float
    """
    geo : Geo | None = None

    @staticmethod
    def validate(entity_identifier : str, dict_entity : dict) :
        Entity.validate(entity_identifier, dict_entity)
        if ECK.geo in dict_entity.keys() :
            Geo.validate(entity_identifier, dict_entity[ECK.geo])


class Person(Entity) :
    """
        -   id: int
            name:
            description:
            date: int
    """
    date : int

    @staticmethod
    def validate(entity_identifier : str, dict_entity : dict) :
        Entity.validate(entity_identifier, dict_entity)
        validateFieldOnExisting(ECK.date, entity_identifier, dict_entity)
        validateFieldOnCasting(ECK.date, entity_identifier, dict_entity, int)
    
    def foreignKeys(self) -> list[EntityLink]:
        return super().foreignKeys() + [EntityLink(entity=ECK.date, id=self.date)]


class Link(BaseModel) :
    web : str | None = None
    native : str | None = None

    @staticmethod
    def validate(entity_identifier : str, dict_entity : dict) :
        validateEntityOnDict(entity_identifier, dict_entity)
        validateFieldOnOneOfExisting([ECK.web, ECK.native], entity_identifier, dict_entity)
        validateFieldOnCrossExcluding([ECK.web, ECK.native], entity_identifier, dict_entity)
        if ECK.web in dict_entity.keys() :
            validateFieldOnHTTP(ECK.web, entity_identifier, dict_entity)


class Biblio(Entity) :
    """
        -   id: int
            name:
            description:
            date: int
            author: int
            state:
            period:
            link:
                web: http <--- OR
                native:   <--- OR
    """
    period : str | None = None
    state : str | None = None
    author : int | None = None
    date : int | None = None
    link : Link | None = None

    @staticmethod
    def validate(entity_identifier : str, dict_entity : dict) :
        Entity.validate(entity_identifier, dict_entity)
        if ECK.author in dict_entity.keys() :
            validateFieldOnCasting(ECK.author, entity_identifier, dict_entity, int)
        if ECK.date in dict_entity.keys() :
            validateFieldOnCasting(ECK.date, entity_identifier, dict_entity, int)
        if ECK.link in dict_entity.keys() :
            Link.validate(entity_identifier, dict_entity[ECK.link])

    def foreignKeys(self) -> list[EntityLink]:
        return super().foreignKeys() + [EntityLink(entity=ECK.date, id=self.date) if self.date else None,
                                        EntityLink(entity=ECK.author, id=self.author) if self.author else None]


class BiblioFragment(Entity) :
    """
        -   id: int
            name:
            description:
            biblio: int
    """
    biblio : int

    @staticmethod
    def validate(entity_identifier : str, dict_entity : dict) :
        Entity.validate(entity_identifier, dict_entity)
        validateFieldOnExisting(ECK.biblio, entity_identifier, dict_entity)
        validateFieldOnCasting(ECK.biblio, entity_identifier, dict_entity, int)

    def foreignKeys(self) -> list[EntityLink]:
        return super().foreignKeys() + [EntityLink(entity=ECK.biblio, id=self.biblio)]


class Source(Entity) :
    """
        -   id: int
            name:
            description:
            author: int
            date: int
            type:
            subtype:
            link: Link
    
    """
    author : int | None = None
    date : int | None = None
    type : str | None = None
    subtype : str | None = None
    link : Link | None = None

    @staticmethod
    def validate(entity_identifier : str, dict_entity : dict) :
        Entity.validate(entity_identifier, dict_entity)
        if ECK.author in dict_entity.keys() :
            validateFieldOnCasting(ECK.author, entity_identifier, dict_entity, int)
        if ECK.date in dict_entity.keys() :
            validateFieldOnCasting(ECK.date, entity_identifier, dict_entity, int)
        if ECK.link in dict_entity.keys() :
            Link.validate(entity_identifier, dict_entity[ECK.link])

    def foreignKeys(self) -> list[EntityLink]:
        return super().foreignKeys() + [EntityLink(entity=ECK.date, id=self.date) if self.date else None,
                                        EntityLink(entity=ECK.author, id=self.author) if self.author else None]


class SourceFragment(Entity) :
    """
        -   id: int
            name:
            description:
            source: int
    """
    source : int

    @staticmethod
    def validate(entity_identifier : str, dict_entity : dict) :
        Entity.validate(entity_identifier, dict_entity)
        validateFieldOnExisting(ECK.source, entity_identifier, dict_entity)
        validateFieldOnCasting(ECK.source, entity_identifier, dict_entity, int)

    def foreignKeys(self) -> list[EntityLink]:
        return super().foreignKeys() + [EntityLink(entity=ECK.source, id=self.source)]


class Event(Entity) :
    """
        -   id: int
            name:
            description:
            date: int
            min:
            max:
            level: str
    """
    date : int
    min : str
    max : str
    level : str | None = None

    @staticmethod
    def validate(entity_identifier : str, dict_entity : dict) :
        Entity.validate(entity_identifier, dict_entity)
        validateFieldOnExisting(ECK.date, entity_identifier, dict_entity)
        validateFieldOnExisting(ECK.min, entity_identifier, dict_entity)
        validateFieldOnExisting(ECK.max, entity_identifier, dict_entity)
        validateFieldOnCasting(ECK.date, entity_identifier, dict_entity, int)
        # TODO level можно ограничить!

    def foreignKeys(self) -> list[EntityLink]:
        return super().foreignKeys() + [EntityLink(entity=ECK.date, id=self.date)]

    def textsToParseLinks(self) -> list[str]:
        return [self.min, self.max]


class Other(Entity) :
    """
        -   id: int
            name:
            description:
    """
    meta : str | None = None

    @staticmethod
    def validate(entity_identifier : str, dict_entity : dict) :
        Entity.validate(entity_identifier, dict_entity)


class Bond(BaseModel) :
    """
        -   event: int
            parents: set[int]
            childs : set[int]
            prerequisites : set[int]
    """
    event : int
    parents : set[int] | None = None
    childs : set[int] | None = None
    prerequisites : set[int] | None = None

    @staticmethod
    def validate(entity_identifier : str, dict_entity : dict) :
        validateFieldOnExisting(ECK.event, entity_identifier, dict_entity)
        validateFieldOnCasting(ECK.event, entity_identifier, dict_entity, int)
        if ECK.parents in dict_entity.keys() :
            validateFieldOnListInt(ECK.parents, entity_identifier, dict_entity)
        if ECK.childs in dict_entity.keys() :
            validateFieldOnListInt(ECK.childs, entity_identifier, dict_entity)
        if ECK.prerequisites in dict_entity.keys() :
            validateFieldOnListInt(ECK.prerequisites, entity_identifier, dict_entity)