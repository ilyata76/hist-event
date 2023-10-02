"""
    Схемы, определяющие фрагмент исторического источника как сущность
"""
from loguru import logger
from core.schemas.Entity import BaseEntity, BaseStorage
from config import ConfigKeywords
from core.processes.utils import NOV


class SourceFragment(BaseEntity) :
    """
        Модель, описывающая сущность фрагмента исторического источника
    """
    source : int | None = None


class SourceFragmentStorage(BaseStorage) :
    """
        Класс управления набором фрагментов источников.
        Используется в первую очередь для лёгкого доступа 
            и регистрации других сущностей.
    """

    def append(self, source_fragment : SourceFragment) -> bool :
        logger.info(f"Добавление фрагмента источника {source_fragment} в {self.name}")
        return super().append(source_fragment)
    
    def get(self, id : int) -> SourceFragment | None :
        logger.info(f"Получение фрагмента источника {id} из {self.name}")
        return super().get(id)
    
    def registerEntity(self, id : int, entity_id : int, field : str) -> bool :
        logger.info(f"Регистрация в хранилище фрагментов источников {self.name} новой сущности {entity_id}[{field}] для {id}")
        return super().registerEntity(id, entity_id, field)
    
    ##################

    def dropTableSQL(self) -> str:
        return super().dropTableSQL() + " -- банк ФРАГМЕНТОВ исторических разных источников"


    def generateTableSQL(self) -> str:
        """
            Генерация SQL таблицы для источника
        """
        str_include  = f"\t{ConfigKeywords.source} INTEGER NOT NULL,\n"
        str_include += f"\t\tCONSTRAINT FK_source_id FOREIGN KEY ({ConfigKeywords.source}) REFERENCES {ConfigKeywords.sources}({ConfigKeywords.id})"
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
            if type(x) is SourceFragment :
                str_include = f"\t  {NOV(x.source)}"
                str_result = super().fillTableSQL(x, str_include)
                ary.append(str_result)
        result += ",\n".join(ary)
        result += ";"
        return result