"""
    Схемы, определяющие персоналию как сущность
"""
from loguru import logger
from schemas.Entity import BaseEntity, BaseStorage
import inspect
from processes.utils import NOV
from config import ConfigKeywords


class Person(BaseEntity) :
    """
        Модель, описывающая сущность персоналии
    """
    person : str | None = None
    date : int | None = None # даты жизни


class PersonStorage(BaseStorage) :
    """
        Класс управления набором персон.
        Используется в первую очередь для лёгкого доступа 
            и регистрации других сущностей.
    """

    def append(self, person : Person) -> bool :
        logger.info(f"Добавление персоналии {person} в {self.name}")
        return super().append(person)

    def get(self, id : int) -> Person | None :
        logger.info(f"Получение персоналии {id} из {self.name}")
        return super().get(id)
    
    def registerEntity(self, id : int, entity_id : int, field : str) -> bool :
        logger.info(f"Регистрация в хранилище персон {self.name} новой сущности {entity_id}[{field}] для {id}")
        return super().registerEntity(id, entity_id, field)
    
    ###################

    def dropTableSQL(self) -> str:
        return super().dropTableSQL() + " -- банк исторических личностей, или по-другому персон"


    def generateTableSQL(self) -> str:
        """
            Генерация SQL таблицы для даты
        """
        str_include  = f"\t{ConfigKeywords.date} INTEGER NOT NULL,\n"
        str_include += f"\t\tCONSTRAINT FK_date_id FOREIGN KEY ({ConfigKeywords.date}) REFERENCES {ConfigKeywords.dates}({ConfigKeywords.id}),\n"
        str_include += f"\t{ConfigKeywords.person} TEXT NOT NULL"
        return super().generateTableSQL(str_include)
    

    def fillTableSQL(self) -> str:
        """
            Заполнение таблицы
        """
        result = f"INSERT INTO {self.name} VALUES \n"
        ary = []

        for key in self.storage :
            x = self.storage[key]
            if type(x) is Person :
                str_include  = f"\t  {NOV(x.date)}, {NOV(x.person)}"
                str_result = super().fillTableSQL(x, str_include)
                ary.append(str_result)
        
        result += ",\n".join(ary)
        result += ";"
        return result