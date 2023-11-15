"""
    Классы работы с сущностями.
        Эти классы - компромиссное решение, обусловленное в первую очередь
        легкостью добавления новых сущностей (получается, что нужно добавить сюда сущность, а в EntityBonds - связать со строками)
"""
import datetime

from pydantic import BaseModel

from config import EntityContentKeyword as ECK, EntityKeyword as EK
from utils import validate as v


class EntityLink(BaseModel) :
    entity : str | None = None
    id : int | None = None


def NOV(value) :
    """null or value"""
    return "null" if not value else str(f"'{value}'")


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
        v.validateEntityOnDict(entity_identifier, dict_entity)
        v.validateFieldOnExisting(ECK.id, entity_identifier, dict_entity)
        v.validateFieldOnExisting(ECK.name, entity_identifier, dict_entity)
        v.validateFieldOnCasting(ECK.id, entity_identifier, dict_entity, int)

    def textsToParseLinks(self) -> list[str] :
        """Тексты, которые будут проходить проверку на {вставки:id}, чтобы заполнить links & ex_links"""
        return [self.description]

    def foreignKeys(self) -> list[EntityLink] :
        """Foreign-key поля для проверки, что эти сущности уже существуют"""
        return [] # никаких нет

    @staticmethod
    def dropTableIfExists() -> str :
        return f"DROP TABLE IF EXISTS {EK.entities} CASCADE;"

    @staticmethod
    def createTableRows() -> str :
        s  = f"\t{ECK.id} INTEGER PRIMARY KEY"  + ",\n"
        s += f"\t{ECK.name} TEXT NOT NULL"      + ",\n"
        s += f"\t{ECK.description} TEXT"        + ",\n"
        s += f"\t{ECK.links} TEXT ARRAY"        + ",\n"
        s += f"\t{ECK.ex_links} TEXT ARRAY"
        return s

    @staticmethod
    def createTable() -> str :
        return f"CREATE TABLE {EK.entities} (\n{Entity.createTableRows()}\n);"

    def insertIntoTableColumns(self) -> str :
        links, ex_links = set(), set()
        for k, v in self.links.items() : links.add(f"{k}:{list(v)}")
        for k, v in self.ex_links.items() : ex_links.add(f"{k}:{list(v)}") 
        links = NOV(links)
        if links != "'null'" and links != "null" : 
            links = links[1:len(links)-1].replace("\'", "\"") ## здесь убираются кавычки, замещаются одинарные на двойные (для постгреса)
            links = NOV(links)
        ex_links = NOV(ex_links)
        if ex_links != "'null'" and ex_links != "null" : 
            ex_links = ex_links[1:len(ex_links)-1].replace("\'", "\"") ## таким образом, получаем '{"aboba:{1}", "", ""}'
            ex_links = NOV(ex_links)
        return ", ".join([NOV(self.id), NOV(self.name), NOV(self.description), links, ex_links])

    def insertIntoTableValue(self) -> str :
        return f"\t({self.insertIntoTableColumns()})"

    @staticmethod
    def insertIntoTableHead() -> str :
        return f"INSERT INTO {EK.entities} VALUES"

    @staticmethod
    def nullReflection() -> str :
        return "null, null, null, null, null"


class DateTime(BaseModel) :
    date : datetime.date | str
    time : datetime.time | None = None

    @staticmethod
    def validate(entity_identifier : str, dict_entity : dict) :
        v.validateEntityOnDict(entity_identifier, dict_entity)
        v.validateFieldOnExisting(ECK.date, entity_identifier, dict_entity)
        if dict_entity[ECK.date] != "..." : # TODO: разные варианты могут быть: нет данных, настоящее время и пр.
            v.validateFieldOnCasting(ECK.date, entity_identifier, dict_entity, datetime.date.fromisoformat)
        if ECK.time in dict_entity.keys() and dict_entity[ECK.time] != "...":
            v.validateFieldOnCasting(ECK.time, entity_identifier, dict_entity, datetime.time.fromisoformat)

    @staticmethod
    def createTableRows(prefix : str) -> str :
        s  = f"\t{prefix}_{ECK.date} DATE" + ",\n"
        s += f"\t{prefix}_{ECK.time} TIME"
        return s

    def insertIntoTableColumns(self) -> str :
        return ", ".join([NOV(self.date), NOV(self.time)])

    @staticmethod
    def nullReflection() -> str :
        return "null, null"


class DateProcess(BaseModel) :
    start : DateTime | None = None
    end : DateTime | None = None

    @staticmethod
    def validate(entity_identifier : str, dict_entity : dict) :
        v.validateEntityOnDict(entity_identifier, dict_entity)
        v.validateFieldOnExisting(ECK.start, entity_identifier, dict_entity)
        v.validateFieldOnExisting(ECK.end, entity_identifier, dict_entity)
        DateTime.validate(entity_identifier, dict_entity[ECK.start])
        DateTime.validate(entity_identifier, dict_entity[ECK.end])

    @staticmethod
    def createTableRows() -> str :
        s  = DateTime.createTableRows("start") + ",\n"
        s += DateTime.createTableRows("end")
        return s

    def insertIntoTableColumns(self) -> str :
        start = self.start.insertIntoTableColumns() if self.start else DateTime.nullReflection()
        end = self.end.insertIntoTableColumns() if self.end else DateTime.nullReflection()
        return ", ".join([start, end])

    @staticmethod
    def nullReflection() -> str :
        return ", ".join([DateTime.nullReflection(), DateTime.nullReflection()])


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
        v.validateFieldOnOneOfExisting([ECK.point, ECK.process], entity_identifier, dict_entity)
        v.validateFieldOnCrossExcluding([ECK.point, ECK.process], entity_identifier, dict_entity)
        if ECK.point in dict_entity.keys() :
            DateTime.validate(entity_identifier, dict_entity[ECK.point])
        if ECK.process in dict_entity.keys() :
            DateProcess.validate(entity_identifier, dict_entity[ECK.process])

    @staticmethod
    def dropTableIfExists() -> str :
        return f"DROP TABLE IF EXISTS {EK.dates} CASCADE;"

    @staticmethod
    def createTableRows() -> str :
        s  = Entity.createTableRows()      + ",\n"
        s += DateProcess.createTableRows() + ",\n"
        s += DateTime.createTableRows("point")
        return s

    @staticmethod 
    def createTable() :
        return f"CREATE TABLE {EK.dates} (\n{Date.createTableRows()}\n);"

    def insertIntoTableColumns(self) -> str :
        process = self.process.insertIntoTableColumns() if self.process else DateProcess.nullReflection()
        point = self.point.insertIntoTableColumns() if self.point else DateTime.nullReflection()
        return ", ".join([super().insertIntoTableColumns(), process, point])

    @staticmethod
    def insertIntoTableHead() -> str :
        return f"INSERT INTO {EK.dates} VALUES"

    @staticmethod
    def nullReflection() -> str :
        return ", ".join([Entity.nullReflection(), DateProcess.nullReflection(), DateTime.nullReflection()])



class Geo(BaseModel) :
    latitude : float
    longitude : float

    @staticmethod
    def validate(entity_identifier : str, dict_entity : dict) :
        v.validateEntityOnDict(entity_identifier, dict_entity)
        v.validateFieldOnExisting(ECK.latitude, entity_identifier, dict_entity)
        v.validateFieldOnExisting(ECK.longitude, entity_identifier, dict_entity)
        v.validateFieldOnCasting(ECK.latitude, entity_identifier, dict_entity, float)
        v.validateFieldOnCasting(ECK.longitude, entity_identifier, dict_entity, float)

    @staticmethod
    def createTableRows() -> str :
        s  = f"\t{ECK.latitude} FLOAT" + ",\n"
        s += f"\t{ECK.longitude} FLOAT"
        return s

    def insertIntoTableColumns(self) -> str :
        return ", ".join([NOV(self.latitude), NOV(self.longitude)])

    @staticmethod
    def nullReflection() -> str :
        return "null, null"


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

    @staticmethod
    def dropTableIfExists() -> str :
        return f"DROP TABLE IF EXISTS {EK.places} CASCADE;"

    @staticmethod
    def createTableRows() -> str :
        s  = Entity.createTableRows() + ",\n"
        s += Geo.createTableRows()
        return s

    @staticmethod 
    def createTable() -> str :
        return f"CREATE TABLE {EK.places} (\n{Place.createTableRows()}\n);"

    def insertIntoTableColumns(self) -> str :
        geo = self.geo.insertIntoTableColumns() if self.geo else Geo.nullReflection()
        return ", ".join([super().insertIntoTableColumns(), geo])

    @staticmethod
    def insertIntoTableHead() -> str :
        return f"INSERT INTO {EK.places} VALUES"

    @staticmethod
    def nullReflection() -> str :
        return ", ".join([super().insertIntoTableColumns(), Entity.nullReflection(), Geo.nullReflection()])


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
        v.validateFieldOnExisting(ECK.date, entity_identifier, dict_entity)
        v.validateFieldOnCasting(ECK.date, entity_identifier, dict_entity, int)
    
    def foreignKeys(self) -> list[EntityLink] :
        return super().foreignKeys() + [EntityLink(entity=ECK.date, id=self.date)]

    @staticmethod
    def dropTableIfExists() -> str :
        return f"DROP TABLE IF EXISTS {EK.persons} CASCADE;"

    @staticmethod
    def createTableRows() -> str :
        s  = Entity.createTableRows() + ",\n"
        s += f"\t{ECK.date} INTEGER NOT NULL" + ",\n"
        s += f"\t\tCONSTRAINT FK_{ECK.date}_id FOREIGN KEY ({ECK.date}) REFERENCES {EK.dates}({ECK.id})"
        return s

    @staticmethod 
    def createTable() -> str :
        return f"CREATE TABLE {EK.persons} (\n{Person.createTableRows()}\n);"

    def insertIntoTableColumns(self) -> str :
        return ", ".join([super().insertIntoTableColumns(), NOV(self.date)])

    @staticmethod
    def insertIntoTableHead() -> str :
        return f"INSERT INTO {EK.persons} VALUES"

    @staticmethod
    def nullReflection() -> str :
        return ", ".join([Entity.nullReflection(), "null"])


class Link(BaseModel) :
    web : str | None = None
    native : str | None = None

    @staticmethod
    def validate(entity_identifier : str, dict_entity : dict) :
        v.validateEntityOnDict(entity_identifier, dict_entity)
        v.validateFieldOnOneOfExisting([ECK.web, ECK.native], entity_identifier, dict_entity)
        #validateFieldOnCrossExcluding([ECK.web, ECK.native], entity_identifier, dict_entity)
        if ECK.web in dict_entity.keys() :
            v.validateFieldOnHTTP(ECK.web, entity_identifier, dict_entity)

    @staticmethod
    def createTableRows() -> str :
        s  = f"\t{ECK.web} TEXT" + ",\n"
        s += f"\t{ECK.native} TEXT"
        return s

    def insertIntoTableColumns(self) -> str :
        return ", ".join([NOV(self.web), NOV(self.native)])

    @staticmethod
    def nullReflection() -> str :
        return "null, null"


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
                web: http <--- OR/AND
                native:   <--- OR/AND
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
            v.validateFieldOnCasting(ECK.author, entity_identifier, dict_entity, int)
        if ECK.date in dict_entity.keys() :
            v.validateFieldOnCasting(ECK.date, entity_identifier, dict_entity, int)
        if ECK.link in dict_entity.keys() :
            Link.validate(entity_identifier, dict_entity[ECK.link])

    def foreignKeys(self) -> list[EntityLink] :
        return super().foreignKeys() + [EntityLink(entity=ECK.date, id=self.date) if self.date else None,
                                        EntityLink(entity=ECK.author, id=self.author) if self.author else None]

    @staticmethod
    def dropTableIfExists() -> str :
        return f"DROP TABLE IF EXISTS {EK.biblios} CASCADE;"

    @staticmethod
    def createTableRows() -> str :
        s  = Entity.createTableRows()   + ",\n"
        s += f"\t{ECK.period} TEXT"     + ",\n"
        s += f"\t{ECK.state} TEXT"      + ",\n"
        s += f"\t{ECK.author} INTEGER"  + ",\n" # NOT NULL не гарантируется
        s += f"\t{ECK.date} INTEGER"    + ",\n" # NOT NULL не гарантируется
        s += Link.createTableRows()
        return s

    @staticmethod 
    def createTable() -> str :
        return f"CREATE TABLE {EK.biblios} (\n{Biblio.createTableRows()}\n);"

    def insertIntoTableColumns(self) -> str :
        link = self.link.insertIntoTableColumns() if self.link else Link.nullReflection()
        return ", ".join([super().insertIntoTableColumns(), NOV(self.period), NOV(self.state), NOV(self.author), NOV(self.date), link])

    @staticmethod
    def insertIntoTableHead() -> str :
        return f"INSERT INTO {EK.biblios} VALUES"

    @staticmethod
    def nullReflection() -> str :
        return ", ".join([Entity.nullReflection(), "null, null, null, null", Link.nullReflection()])



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
        v.validateFieldOnExisting(ECK.biblio, entity_identifier, dict_entity)
        v.validateFieldOnCasting(ECK.biblio, entity_identifier, dict_entity, int)

    def foreignKeys(self) -> list[EntityLink]:
        return super().foreignKeys() + [EntityLink(entity=ECK.biblio, id=self.biblio)]

    @staticmethod
    def dropTableIfExists() -> str :
        return f"DROP TABLE IF EXISTS {EK.biblio_fragments} CASCADE;"

    @staticmethod
    def createTableRows() -> str :
        s  = Entity.createTableRows()           + ",\n"
        s += f"\t{ECK.biblio} INTEGER NOT NULL" + ",\n"
        s += f"\t\tCONSTRAINT FK_{ECK.biblio}_id FOREIGN KEY ({ECK.biblio}) REFERENCES {EK.biblios}({ECK.id})"
        return s

    @staticmethod 
    def createTable() -> str :
        return f"CREATE TABLE {EK.biblio_fragments} (\n{BiblioFragment.createTableRows()}\n);"

    def insertIntoTableColumns(self) -> str :
        return ", ".join([super().insertIntoTableColumns(), NOV(self.biblio)])

    @staticmethod
    def insertIntoTableHead() -> str :
        return f"INSERT INTO {EK.biblio_fragments} VALUES"

    @staticmethod
    def nullReflection() -> str :
        return ", ".join([Entity.nullReflection(), "null"])


class Source(Entity) :
    """
        -   id: int
            name:
            description:
            author: int
            date: int
            type:
            subtype:
            link:
                web: http <--- OR/AND
                native:   <--- OR/AND
    """
    type : str | None = None
    subtype : str | None = None
    author : int | None = None
    date : int | None = None
    link : Link | None = None

    @staticmethod
    def validate(entity_identifier : str, dict_entity : dict) :
        Entity.validate(entity_identifier, dict_entity)
        if ECK.author in dict_entity.keys() :
            v.validateFieldOnCasting(ECK.author, entity_identifier, dict_entity, int)
        if ECK.date in dict_entity.keys() :
            v.validateFieldOnCasting(ECK.date, entity_identifier, dict_entity, int)
        if ECK.link in dict_entity.keys() :
            Link.validate(entity_identifier, dict_entity[ECK.link])

    def foreignKeys(self) -> list[EntityLink]:
        return super().foreignKeys() + [EntityLink(entity=ECK.date, id=self.date) if self.date else None,
                                        EntityLink(entity=ECK.author, id=self.author) if self.author else None]

    @staticmethod
    def dropTableIfExists() -> str :
        return f"DROP TABLE IF EXISTS {EK.sources} CASCADE;"

    @staticmethod
    def createTableRows() -> str :
        s  = Entity.createTableRows()   + ",\n"
        s += f"\t{ECK.type} TEXT"       + ",\n"
        s += f"\t{ECK.subtype} TEXT"    + ",\n"
        s += f"\t{ECK.author} INTEGER"  + ",\n" # NOT NULL не гарантируется
        s += f"\t{ECK.date} INTEGER"    + ",\n" # NOT NULL не гарантируется
        s += Link.createTableRows()
        return s

    @staticmethod 
    def createTable() -> str :
        return f"CREATE TABLE {EK.sources} (\n{Source.createTableRows()}\n);"

    def insertIntoTableColumns(self) -> str :
        link = self.link.insertIntoTableColumns() if self.link else Link.nullReflection()
        return ", ".join([super().insertIntoTableColumns(), NOV(self.type), NOV(self.subtype), NOV(self.author), NOV(self.date), link])

    @staticmethod
    def insertIntoTableHead() -> str :
        return f"INSERT INTO {EK.sources} VALUES"

    @staticmethod
    def nullReflection() -> str :
        return ", ".join([Entity.nullReflection(), "null, null, null, null", Link.nullReflection()])


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
        v.validateFieldOnExisting(ECK.source, entity_identifier, dict_entity)
        v.validateFieldOnCasting(ECK.source, entity_identifier, dict_entity, int)

    def foreignKeys(self) -> list[EntityLink]:
        return super().foreignKeys() + [EntityLink(entity=ECK.source, id=self.source)]

    @staticmethod
    def dropTableIfExists() -> str :
        return f"DROP TABLE IF EXISTS {EK.source_fragments} CASCADE;"

    @staticmethod
    def createTableRows() -> str :
        s  = Entity.createTableRows()           + ",\n"
        s += f"\t{ECK.source} INTEGER NOT NULL" + ",\n"
        s += f"\t\tCONSTRAINT FK_{ECK.source}_id FOREIGN KEY ({ECK.source}) REFERENCES {EK.sources}({ECK.id})"
        return s

    @staticmethod 
    def createTable() -> str :
        return f"CREATE TABLE {EK.source_fragments} (\n{SourceFragment.createTableRows()}\n);"

    def insertIntoTableColumns(self) -> str :
        return ", ".join([super().insertIntoTableColumns(), NOV(self.source)])

    @staticmethod
    def insertIntoTableHead() -> str :
        return f"INSERT INTO {EK.source_fragments} VALUES"

    @staticmethod
    def nullReflection() -> str :
        return ", ".join([Entity.nullReflection(), "null"])


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
        v.validateFieldOnExisting(ECK.date, entity_identifier, dict_entity)
        v.validateFieldOnExisting(ECK.min, entity_identifier, dict_entity)
        v.validateFieldOnExisting(ECK.max, entity_identifier, dict_entity)
        v.validateFieldOnCasting(ECK.date, entity_identifier, dict_entity, int)
        # TODO level можно ограничить!

    def foreignKeys(self) -> list[EntityLink]:
        return super().foreignKeys() + [EntityLink(entity=ECK.date, id=self.date)]

    def textsToParseLinks(self) -> list[str]:
        return [self.min, self.max]

    @staticmethod
    def dropTableIfExists() -> str :
        return f"DROP TABLE IF EXISTS {EK.events} CASCADE;"

    @staticmethod
    def createTableRows() -> str :
        s  = Entity.createTableRows()           + ",\n"
        s += f"\t{ECK.date} INTEGER NOT NULL"   + ",\n"
        s += f"\t\tCONSTRAINT FK_{ECK.date}_id FOREIGN KEY ({ECK.date}) REFERENCES {EK.dates}({ECK.id})" + ",\n"
        s += f"\t{ECK.min} TEXT NOT NULL"       + ",\n"
        s += f"\t{ECK.max} TEXT NOT NULL"       + ",\n"
        s += f"\t{ECK.level} TEXT"
        return s

    @staticmethod 
    def createTable() -> str :
        return f"CREATE TABLE {EK.events} (\n{Event.createTableRows()}\n);"

    def insertIntoTableColumns(self) -> str :
        return ", ".join([super().insertIntoTableColumns(), NOV(self.date), NOV(self.min), NOV(self.max), NOV(self.level)])

    @staticmethod
    def insertIntoTableHead() -> str :
        return f"INSERT INTO {EK.events} VALUES"

    @staticmethod
    def nullReflection() -> str :
        return ", ".join([Entity.nullReflection(), "null, null, null, null"])


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

    @staticmethod
    def dropTableIfExists() -> str :
        return f"DROP TABLE IF EXISTS {EK.others} CASCADE;"

    @staticmethod
    def createTableRows() -> str :
        s  = Entity.createTableRows() + ",\n"
        s += f"\t{ECK.meta} TEXT"
        return s

    @staticmethod 
    def createTable() -> str :
        return f"CREATE TABLE {EK.others} (\n{Other.createTableRows()}\n);"

    def insertIntoTableColumns(self) -> str :
        return ", ".join([super().insertIntoTableColumns(), NOV(self.meta)])

    @staticmethod
    def insertIntoTableHead() -> str :
        return f"INSERT INTO {EK.others} VALUES"

    @staticmethod
    def nullReflection() -> str :
        return ", ".join([Entity.nullReflection(), "null"])


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
        v.validateFieldOnExisting(ECK.event, entity_identifier, dict_entity)
        v.validateFieldOnCasting(ECK.event, entity_identifier, dict_entity, int)
        if ECK.parents in dict_entity.keys() :
            v.validateFieldOnListInt(ECK.parents, entity_identifier, dict_entity)
        if ECK.childs in dict_entity.keys() :
            v.validateFieldOnListInt(ECK.childs, entity_identifier, dict_entity)
        if ECK.prerequisites in dict_entity.keys() :
            v.validateFieldOnListInt(ECK.prerequisites, entity_identifier, dict_entity)

    @staticmethod
    def dropTableIfExists() -> str :
        return f"DROP TABLE IF EXISTS {EK.bonds} CASCADE;"

    @staticmethod
    def createTableRows() -> str :
        s  = f"\t{ECK.id} SERIAL PRIMARY KEY"     + ",\n"
        s += f"\t{ECK.event} INTEGER FOREIGN KEY" + ",\n"
        s += f"\t\tCONSTRAINT FK_{ECK.event}_id FOREIGN KEY ({ECK.event}) REFERENCES {EK.events}({ECK.id})"
        s += f"\t{ECK.parents} INTEGER ARRAY"     + ",\n"
        s += f"\t{ECK.childs} INTEGER ARRAY"      + ",\n"
        s += f"\t{ECK.prerequisites} INTEGER ARRAY"
        return s

    @staticmethod 
    def createTable() -> str :
        return f"CREATE TABLE {EK.bonds} (\n{Bond.createTableRows()}\n);"

    def insertIntoTableColumns(self) -> str :
        return ", ".join([NOV(self.event), NOV(self.parents), NOV(self.childs), NOV(self.prerequisites)])

    @staticmethod
    def insertIntoTableHead() -> str :
        return f"INSERT INTO {EK.bonds} VALUES"

    @staticmethod
    def nullReflection() -> str :
        return ", ".join(["null, null, null, null"])