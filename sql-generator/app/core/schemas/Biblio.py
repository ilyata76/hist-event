"""
    Схемы, определяющие библиографический источник (мнение автора) как сущность
"""
from loguru import logger
from core.schemas.Entity import BaseEntity, BaseStorage
from config import ConfigKeywords
from core.processes.utils import NOV


class Biblio(BaseEntity) :
    """
        Модель, описывающая сущность библиографического источника
    """
    author : str | None = None
    date : str | None = None
    state : str | None = None
    period : str | None = None
    link : str | None = None


class BiblioStorage(BaseStorage) :
    """
        Класс управления набором библиографических источников.
        Используется в первую очередь для лёгкого доступа 
            и регистрации других сущностей.
    """

    def append(self, biblio : Biblio) -> bool :
        logger.info(f"Добавление библиографического источника {biblio} в {self.name}")
        return super().append(biblio)
    
    def get(self, id : int) -> Biblio | None :
        logger.info(f"Получение библиографического источника {id} из {self.name}")
        return super().get(id)
    
    def registerEntity(self, id : int, entity_id : int, field : str) -> bool :
        logger.info(f"Регистрация в хранилище библиографических источников {self.name} новой сущности {entity_id}[{field}] для {id}")
        return super().registerEntity(id, entity_id, field)
    
    ##################

    def dropTableSQL(self) -> str:
        return super().dropTableSQL() + " -- банк библиографических источников"


    def generateTableSQL(self) -> str:
        """
            Генерация SQL таблицы для библиографического источника
        """
        str_include  = f"\t{ConfigKeywords.author} TEXT NOT NULL,\n"
        str_include += f"\t{ConfigKeywords.link} TEXT,\n"
        str_include += f"\t{ConfigKeywords.date} TEXT,\n"
        str_include += f"\t{ConfigKeywords.state} TEXT, \n"
        str_include += f"\t{ConfigKeywords.period} TEXT"
        return super().generateTableSQL(str_include)
    

    def fillTableSQL(self) -> str:
        """
            Заполнение таблицы
        """
        result = f"INSERT INTO {self.name} VALUES \n"
        ary = []

        for key in self.storage :
            x = self.storage[key]
            if type(x) is Biblio :
                str_include  = f"\t  {NOV(x.author)}, {NOV(x.link)}, {NOV(x.date)},\n"
                str_include += f"\t  {NOV(x.state)}, {NOV(x.period)}"
                str_result = super().fillTableSQL(x, str_include)
                ary.append(str_result)
        result += ",\n".join(ary)
        result += ";"
        return result