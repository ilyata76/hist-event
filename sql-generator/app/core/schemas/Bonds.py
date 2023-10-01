"""
    Схемы управления абстракцией связей
"""
from pydantic import BaseModel
from loguru import logger
from config import ConfigKeywords
from core.processes.utils import NOV


class Bond(BaseModel) :
    """
        Определяет связь как абстракцию (отличается от остальных сущностей)
    """
    event : int | None = None # id envets FK
    parents : set[int] | None = None
    childs : set[int] | None = None
    prerequisites : set[int] | None = None


class BondStorage() :
    """
        Управление связями (необобщается до сущностей)
    """

    def __init__(self, name = None) :
        logger.debug("Создание класса BondStorage")
        self.storage = {}
        self.name = name if name else "BondStorage"


    def append(self, bond : Bond) -> bool :
        """
            Добавить в словарь новую связь
        """
        res = True
        try :
            self.storage.update({bond.event : bond})
            res = True
        except Exception as exc:
            logger.error("Ошибка во время добавления в BondStorage exc={exc}", exc=exc)
            raise exc
        logger.info("Добавление сущности в BondStorage res={res}", res=res)
        return res
    

    def get(self, event_id : int) -> Bond | None :
        """
            Взятие по Event ID. Вернёт None, если такого нет
        """
        res = None
        try : 
            res = self.storage.get(event_id, None)
        except Exception as exc:
            logger.error("Ошибка во взятия по индексу в BondStorage exc={exc}", exc=exc)
            raise exc
        logger.info("Получение сущности из BondStorage res={res}", res=res)
        return res
    

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
        

    def dropTableSQL(self) -> str : 
        logger.info(f"Удаление таблицы SQL для {self.name}")
        return f"""DROP TABLE IF EXISTS {self.name} CASCADE;"""
    
    
    def generateTableSQL(self) -> str :
        logger.info(f"Создание таблиц SQL для {self.name}")

        str_result  = f"CREATE TABLE {self.name} (\n"
        str_result += f"\t{ConfigKeywords.id} SERIAL PRIMARY KEY,\n"
        str_result += f"\t{ConfigKeywords.event} INTEGER NOT NULL,\n"
        str_result += f"\t\tCONSTRAINT FK_event_id FOREIGN KEY ({ConfigKeywords.id}) REFERENCES {ConfigKeywords.events}({ConfigKeywords.id}),\n"
        str_result += f"\t{ConfigKeywords.parents} INTEGER ARRAY,\n"
        str_result += f"\t{ConfigKeywords.childs} INTEGER ARRAY,\n"
        str_result += f"\t{ConfigKeywords.prerequisites} INTEGER ARRAY\n"
        str_result += f"); -- таблица связей"

        return str_result
    

    def fillTableSQL(self) -> str :
        """
            Заполнение таблицы
        """
        logger.info(f"Заполнение SQL таблиц для {self.name}")
        result = f"INSERT INTO {self.name} ({ConfigKeywords.event}, {ConfigKeywords.parents}, {ConfigKeywords.childs}, {ConfigKeywords.prerequisites}) VALUES \n"
        ary = []

        for key in self.storage :
            x = self.storage[key]
            if type(x) is Bond :
                str_append  = f"\t( {NOV(x.event)}, {NOV(x.parents)},\n"
                str_append += f"\t  {NOV(x.childs)}, {NOV(x.prerequisites)} )"
                ary.append(str_append)
        result += ",\n".join(ary)
        result += ";"
        return result