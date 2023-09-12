"""
    Схемы, определяющие фрагмент библиографического источника как сущность
"""
from loguru import logger
from schemas.Entity import BaseEntity, BaseStorage
import inspect
from config import ConfigKeywords
from processes.utils import NOV


class BiblioFragment(BaseEntity) :
    """
        Модель, описывающая сущность фрагмента библиографического источника
    """
    biblio : int | None = None


class BiblioFragmentStorage(BaseStorage) :
    """
        Класс управления набором фрагментов библиографических источников.
        Используется в первую очередь для лёгкого доступа 
            и регистрации других сущностей.
    """

    def append(self, biblio_fragment : BiblioFragment) -> bool :
        logger.info(f"Добавление фрагмента библиографического источника {biblio_fragment} в {self.name}")
        return super().append(biblio_fragment)
    
    def get(self, id : int) -> BiblioFragment | None :
        logger.info(f"Получение фрагмента библиографического источника {id} из {self.name}")
        return super().get(id)
    
    def registerEntity(self, id : int, entity_id : int, field : str) -> bool :
        logger.info(f"Регистрация в хранилище фрагментов библиографических источников {self.name} новой сущности {entity_id}[{field}] для {id}")
        return super().registerEntity(id, entity_id, field)
    
    ##################

    def dropTableSQL(self) -> str:
        return super().dropTableSQL() + " -- банк ФРАГМЕНТОВ Библиографических источников"


    def generateTableSQL(self) -> str:
        """
            Генерация SQL таблицы для б. источника
        """
        str_include  = f"\t{ConfigKeywords.biblio} INTEGER NOT NULL,\n"
        str_include += f"\t\tCONSTRAINT FK_biblio_id FOREIGN KEY ({ConfigKeywords.biblio}) REFERENCES {ConfigKeywords.biblios}({ConfigKeywords.id})"
        return super().generateTableSQL(str_include)
    

    def fillTableSQL(self) -> str:
        """
            Заполнение таблицы
        """
        result = f"INSERT INTO {self.name} VALUES \n"
        ary = []

        for key in self.storage :
            x = self.storage[key]
            if type(x) is BiblioFragment :
                str_include = f"\t  {NOV(x.biblio)}"
                str_result = super().fillTableSQL(x, str_include)
                ary.append(str_result)
        result += ",\n".join(ary)
        result += ";"
        return result