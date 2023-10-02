"""
    Схемы, определяющие место как сущность
"""
from loguru import logger
from core.schemas.Entity import BaseEntity, BaseStorage
from config import ConfigKeywords
from core.processes.utils import NOV


class Place(BaseEntity) :
    """
        Модель, описывающая сущность места
    """
    geo : str | None = None


class PlaceStorage(BaseStorage) :
    """
        Класс управления набором мест.
        Используется в первую очередь для лёгкого доступа 
            и регистрации других сущностей.
    """

    def append(self, place : Place) -> bool :
        logger.info(f"Добавление места {place} в {self.name}")
        return super().append(place)

    def get(self, id : int) -> Place | None :
        logger.info(f"Получение места {id} из {self.name}")
        return super().get(id)
    
    def registerEntity(self, id : int, entity_id : int, field : str) -> bool :
        logger.info(f"Регистрация в хранилище мест {self.name} новой сущности {entity_id}[{field}] для {id}")
        return super().registerEntity(id, entity_id, field)
    
    ###################

    def dropTableSQL(self) -> str:
        return super().dropTableSQL() + " -- банк всяческих мест"


    def generateTableSQL(self) -> str:
        """
            Генерация SQL таблицы для даты
        """
        str_include  = f"\t{ConfigKeywords.geo} TEXT"
        return super().generateTableSQL(str_include)
    

    def fillTableSQL(self) -> str:
        """
            Заполнение таблицы
        """
        if not self.storage :
            return ""
        
        result = f"INSERT INTO {self.name} VALUES \n"
        ary = []

        for key in self.storage :
            x = self.storage[key]
            if type(x) is Place :
                str_include  = f"\t  {NOV(x.geo)}"
                str_result = super().fillTableSQL(x, str_include)
                ary.append(str_result)

        result += ",\n".join(ary)
        result += ";"
        return result