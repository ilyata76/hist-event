"""
    Схемы, определяющие сущность и основные операции над сущностью
"""
from loguru import logger
from pydantic import BaseModel
from config import ConfigKeywords
from processes.utils import NOV


class BaseEntity(BaseModel) :
    """
        Сущность описывается несколькими полями
    """
    id : int
    # базовая часть
    name : str | None = None
    description : str | None = None
    # часть, которая может быть заполнена во время регистрации и сохранения
    #   других сущностей
    events : set[int] | None = None
    ex_events : set[int] | None = None
    dates : set[int] | None = None
    ex_dates : set[int] | None = None # ссылки от внешних источников
    places : set[int] | None = None
    ex_places : set[int] | None = None # ссылки от внешних источников
    persons : set[int] | None = None
    ex_persons : set[int] | None = None # ссылки от внешних источников
    sources : set[int] | None = None
    ex_sources : set[int] | None = None # ссылки от внешних источников
    others : set[int] | None = None
    ex_others : set[int] | None = None #
    source_fragments : set[int] | None = None
    ex_source_fragments : set[int] | None = None #
    biblios : set[int] | None = None
    ex_biblios : set[int] | None = None
    biblio_fragments : set[int] | None = None
    ex_biblio_fragments : set[int] | None = None


class BaseStorage() :
    """
        Класс управления набором дат/персоналий/мест и прочими сущностями.
        Используется в первую очередь для лёгкого доступа 
            и регистрации других сущностей.
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
        return self.registerEntity(id, entity_id, field)
    

    def dropTableSQL(self, str_include : str = "") -> str : 
        logger.debug(f"Удаление таблиц SQL для {self.name}")
        return f"""DROP TABLE IF EXISTS {self.name} CASCADE;"""
    


    
    def generateTableSQL(self, str_include : str = "") -> str :
        logger.debug(f"Создание таблиц SQL для {self.name}")

        str_result  = f"CREATE TABLE {self.name} (\n"
        str_result += f"\t{ConfigKeywords.id} INTEGER PRIMARY KEY,\n"
        str_result += f"\t{ConfigKeywords.name} TEXT,\n"
        str_result += f"\t{ConfigKeywords.description} TEXT,\n"
        if str_include : str_result += f"{str_include},\n"
        str_result += f"\t{ConfigKeywords.events} INTEGER ARRAY,\n"
        str_result += f"\t{ConfigKeywords.ex_events} INTEGER ARRAY,\n"
        str_result += f"\t{ConfigKeywords.dates} INTEGER ARRAY,\n"
        str_result += f"\t{ConfigKeywords.ex_dates} INTEGER ARRAY,\n"
        str_result += f"\t{ConfigKeywords.places} INTEGER ARRAY,\n"
        str_result += f"\t{ConfigKeywords.ex_places} INTEGER ARRAY,\n"
        str_result += f"\t{ConfigKeywords.persons} INTEGER ARRAY,\n"
        str_result += f"\t{ConfigKeywords.ex_persons} INTEGER ARRAY,\n"
        str_result += f"\t{ConfigKeywords.sources} INTEGER ARRAY,\n"
        str_result += f"\t{ConfigKeywords.ex_sources} INTEGER ARRAY,\n"
        str_result += f"\t{ConfigKeywords.others} INTEGER ARRAY,\n"
        str_result += f"\t{ConfigKeywords.ex_others} INTEGER ARRAY,\n"
        str_result += f"\t{ConfigKeywords.source_fragments} INTEGER ARRAY,\n"
        str_result += f"\t{ConfigKeywords.ex_source_fragments} INTEGER ARRAY,\n"
        str_result += f"\t{ConfigKeywords.biblios} INTEGER ARRAY,\n"
        str_result += f"\t{ConfigKeywords.ex_biblios} INTEGER ARRAY,\n"
        str_result += f"\t{ConfigKeywords.biblio_fragments} INTEGER ARRAY,\n"
        str_result += f"\t{ConfigKeywords.ex_biblio_fragments} INTEGER ARRAY\n"
        str_result += f");"

        return str_result
    

    def fillTableSQL(self, element : BaseEntity, str_include : str = "") -> str :
        logger.debug(f"Заполнение таблиц SQL для {self.name}")

        str_result  = f"\t( {NOV(element.id)}, {NOV(element.name)}, {NOV(element.description)},\n"
        if str_include : str_result += f"{str_include},\n"
        str_result += f"\t  {NOV(element.events)}, {NOV(element.ex_events)},\n"
        str_result += f"\t  {NOV(element.dates)}, {NOV(element.ex_dates)},\n"
        str_result += f"\t  {NOV(element.places)}, {NOV(element.ex_places)},\n"
        str_result += f"\t  {NOV(element.persons)}, {NOV(element.ex_persons)},\n"
        str_result += f"\t  {NOV(element.sources)}, {NOV(element.ex_sources)},\n"
        str_result += f"\t  {NOV(element.others)}, {NOV(element.ex_others)},\n"
        str_result += f"\t  {NOV(element.source_fragments)}, {NOV(element.ex_source_fragments)},\n"
        str_result += f"\t  {NOV(element.biblios)}, {NOV(element.ex_biblios)},\n"
        str_result += f"\t  {NOV(element.biblio_fragments)}, {NOV(element.ex_biblio_fragments)} )"

        return str_result


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