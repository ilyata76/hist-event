"""
    Схемы, определяющие дату как сущность
"""
from loguru import logger
from schemas.Entity import BaseEntity, BaseStorage
import inspect
from config import ConfigKeywords
from processes.utils import NOV


class Date(BaseEntity) :
    """
        Модель, описывающая сущность даты
    """
    date : str | None = None # date
    time : str | None = None # time
    start : str | None = None # datetime
    end : str | None = None # datetime
    start_date : str | None = None # date
    start_time : str | None = None # time
    end_date : str | None = None # date
    end_time : str | None = None # time


class DateStorage(BaseStorage) :
    """
        Класс управления набором дат.
        Используется в первую очередь для лёгкого доступа 
            и регистрации других сущностей.
    """

    def append(self, date : Date) -> bool :
        logger.info(f"Добавление даты {date} в {self.name}")
        return super().append(date)
    
    def get(self, id : int) -> Date | None :
        logger.info(f"Получение даты {id} из {self.name}")
        return super().get(id)
    
    def registerEntity(self, id : int, entity_id : int, field : str) -> bool :
        logger.info(f"Регистрация в хранилище дат {self.name} новой сущности {entity_id}[{field}] для {id}")
        return super().registerEntity(id, entity_id, field)
    
    ###################

    def dropTableSQL(self) -> str:
        return super().dropTableSQL() + " -- банк дат, на которые будут ссылаться другие сущности"


    def generateTableSQL(self) -> str:
        """
            Генерация SQL таблицы для даты
        """
        str_include  = f"\t{ConfigKeywords.date} DATE,\n"
        str_include += f"\t{ConfigKeywords.time} TIME,\n"
        str_include += f"\t{ConfigKeywords.start_date} DATE,\n"
        str_include += f"\t{ConfigKeywords.start_time} TIME,\n"
        str_include += f"\t{ConfigKeywords.end_date} DATE,\n"
        str_include += f"\t{ConfigKeywords.end_time} TIME"
        return super().generateTableSQL(str_include)


    def fillTableSQL(self) -> str:
        """
            Заполнение таблицы
        """
        result = f"INSERT INTO {self.name} VALUES \n"
        ary = []

        for key in self.storage :
            x = self.storage[key]
            if type(x) is Date :
                str_include  = f"\t  {NOV(x.date)}, {NOV(x.time)},\n"
                str_include += f"\t  {NOV(x.start_date)}, {NOV(x.start_time)},\n"
                str_include += f"\t  {NOV(x.end_date)}, {NOV(x.end_time)}"
                str_result = super().fillTableSQL(x, str_include)
                ary.append(str_result)

        result += ",\n".join(ary)
        result += ";"
        return result