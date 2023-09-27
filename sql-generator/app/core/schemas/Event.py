"""
    Схемы, определяющие событие как сущность
"""
from loguru import logger
from core.schemas.Entity import BaseEntity, BaseStorage
from config import ConfigKeywords
from core.processes.utils import NOV


class Event(BaseEntity) :
    """
        Модель, описывающая сущность события
    """
    date : int | None = None # ссылка на дату
    min : str | None = None
    max : str | None = None
    level : str | None = None


class EventStorage(BaseStorage) :
    """
        Класс управления набором событий.
        Используется в первую очередь для лёгкого доступа 
            и регистрации других сущностей.
    """

    def append(self, event : Event) -> bool :
        logger.info(f"Добавление события {event} в {self.name}")
        return super().append(event)
    
    def get(self, id : int) -> Event | None :
        logger.info(f"Получение события {id} из {self.name}")
        return super().get(id)
    
    def registerEntity(self, id : int, entity_id : int, field : str) -> bool :
        logger.info(f"Регистрация в хранилище событий {self.name} новой сущности {entity_id}[{field}] для {id}")
        return super().registerEntity(id, entity_id, field)
    
    ###################

    def dropTableSQL(self) -> str:
        return super().dropTableSQL() + " -- банк событий, главной сущности базы данных"


    def generateTableSQL(self) -> str:
        """
            Генерация SQL таблицы для даты
        """
        str_include  = f"\t{ConfigKeywords.date} INTEGER NOT NULL,\n"
        str_include += f"\t\tCONSTRAINT FK_date_id FOREIGN KEY ({ConfigKeywords.date}) REFERENCES {ConfigKeywords.dates}({ConfigKeywords.id}),\n"
        str_include += f"\t{ConfigKeywords.min} TEXT NOT NULL,\n"
        str_include += f"\t{ConfigKeywords.max} TEXT NOT NULL,\n"
        str_include += f"\t{ConfigKeywords.level} TEXT"
        return super().generateTableSQL(str_include)
    

    def fillTableSQL(self) -> str:
        """
            Заполнение таблицы
        """
        result = f"INSERT INTO {self.name} VALUES \n"
        ary = []

        for key in self.storage :
            x = self.storage[key]
            if type(x) is Event :
                str_include  = f"\t  {NOV(x.date)},\n"
                str_include += f"\t  {NOV(x.min)},\n"
                str_include += f"\t  {NOV(x.max)},\n"
                str_include += f"\t  {NOV(x.level)}"
                str_result = super().fillTableSQL(x, str_include)
                ary.append(str_result)
        result += ",\n".join(ary)
        result += ";"
        return result