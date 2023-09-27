"""
    Схемы, определяющие "ДРУГОЕ" как сущность
"""
from loguru import logger
from core.schemas.Entity import BaseEntity, BaseStorage
from config import ConfigKeywords
from core.processes.utils import NOV


class Other(BaseEntity) :
    """
        Модель, описывающая сущность "другого"
    """
    meta : str | None = None


class OtherStorage(BaseStorage) :
    """
        Класс управления набором "другого".
        Используется в первую очередь для лёгкого доступа 
            и регистрации других сущностей.
    """

    def append(self, other : Other) -> bool :
        logger.info(f"Добавление 'другого' {other} в {self.name}")
        return super().append(other)
    
    def get(self, id : int) -> Other | None :
        logger.info(f"Получение 'другого' {id} из {self.name}")
        return super().get(id)
    
    def registerEntity(self, id : int, entity_id : int, field : str) -> bool :
        logger.info(f"Регистрация в хранилище 'другого' {self.name} новой сущности {entity_id}[{field}] для {id}")
        return super().registerEntity(id, entity_id, field)
    
    ###################

    def dropTableSQL(self) -> str:
        return super().dropTableSQL() + " -- банк всего остального, что не попало ни в какую из категорий"


    def generateTableSQL(self) -> str:
        """
            Генерация SQL таблицы для даты
        """
        str_include  = f"\t{ConfigKeywords.meta} TEXT"
        return super().generateTableSQL(str_include)
    

    def fillTableSQL(self) -> str:
        """
            Заполнение таблицы
        """
        result = f"INSERT INTO {self.name} VALUES \n"
        ary = []

        for key in self.storage :
            x = self.storage[key]
            if type(x) is Other :
                str_include  = f"\t  {NOV(x.meta)}"
                str_result = super().fillTableSQL(x, str_include)
                ary.append(str_result)
                
        result += ",\n".join(ary)
        result += ";"
        return result