"""
    Схемы, определяющие исторический источник как сущность
"""
from loguru import logger
from schemas import BaseEntity, BaseStorage
from config import ConfigKeywords
from processes.utils import NOV


class Source(BaseEntity) :
    """
        Модель, описывающая сущность исторического источника
    """
    author : str | None = None
    link : str | None = None
    date : int | None = None # ссылка на date FK
    type : str | None = None
    subtype : str | None = None


class SourceStorage(BaseStorage) :
    """
        Класс управления набором источников.
        Используется в первую очередь для лёгкого доступа 
            и регистрации других сущностей.
    """

    def append(self, source : Source) -> bool :
        logger.info(f"Добавление источника {source} в {self.name}")
        return super().append(source)
    
    def get(self, id : int) -> Source | None :
        logger.info(f"Получение источника {id} из {self.name}")
        return super().get(id)
    
    def registerEntity(self, id : int, entity_id : int, field : str) -> bool :
        logger.info(f"Регистрация в хранилище источников {self.name} новой сущности {entity_id}[{field}] для {id}")
        return super().registerEntity(id, entity_id, field)
    
    ##################

    def dropTableSQL(self) -> str:
        return super().dropTableSQL() + " -- банк исторических разных источников"


    def generateTableSQL(self) -> str:
        """
            Генерация SQL таблицы для источника
        """
        str_include  = f"\t{ConfigKeywords.author} TEXT NOT NULL,\n"
        str_include += f"\t{ConfigKeywords.link} TEXT,\n"
        str_include += f"\t{ConfigKeywords.date} INTEGER NOT NULL,\n"
        str_include += f"\t\tCONSTRAINT FK_date_id FOREIGN KEY ({ConfigKeywords.date}) REFERENCES {ConfigKeywords.dates}({ConfigKeywords.id}), \n"
        str_include += f"\t{ConfigKeywords.type} TEXT,\n"
        str_include += f"\t{ConfigKeywords.subtype} TEXT"
        return super().generateTableSQL(str_include)
    

    def fillTableSQL(self) -> str:
        """
            Заполнение таблицы
        """
        result = f"INSERT INTO {self.name} VALUES \n"
        ary = []

        for key in self.storage :
            x = self.storage[key]
            if type(x) is Source :
                str_include  = f"\t  {NOV(x.author)}, {NOV(x.link)}, {NOV(x.date)},\n"
                str_include += f"\t  {NOV(x.type)}, {NOV(x.subtype)}"
                str_result = super().fillTableSQL(x, str_include)
                ary.append(str_result)
        result += ",\n".join(ary)
        result += ";"
        return result