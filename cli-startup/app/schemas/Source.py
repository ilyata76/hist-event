"""
    Схемы, определяющие исторический источник как сущность
"""
from loguru import logger
from schemas.Entity import BaseEntity, BaseStorage


class Source(BaseEntity) :
    """
        Модель, описывающая сущность исторического источника
    """
    author : str | None = None
    link : str | None = None


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