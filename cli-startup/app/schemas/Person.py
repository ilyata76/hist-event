"""
    Схемы, определяющие персоналию как сущность
"""
from loguru import logger
from schemas.Entity import BaseEntity, BaseStorage


class Person(BaseEntity) :
    """
        Модель, описывающая сущность персоналии
    """
    person : str | None = None


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