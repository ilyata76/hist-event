"""
    Схемы, определяющие "ДРУГОЕ" как сущность
"""
from loguru import logger
from schemas.Entity import BaseEntity, BaseStorage
import inspect
from processes.utils import NOV
from config import ConfigKeywords


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
        return inspect.cleandoc( f"""
                                    CREATE TABLE {self.name} (
                                    	{ConfigKeywords.id} INTEGER PRIMARY KEY,
                                    	{ConfigKeywords.name} TEXT NOT NULL,
                                    	{ConfigKeywords.meta} TEXT,
                                    	{ConfigKeywords.description} TEXT,
                                    	{ConfigKeywords.events} INTEGER ARRAY,
                                    	{ConfigKeywords.ex_events} INTEGER ARRAY,
                                    	{ConfigKeywords.dates} INTEGER ARRAY,
                                    	{ConfigKeywords.ex_dates} INTEGER ARRAY,
                                    	{ConfigKeywords.places} INTEGER ARRAY,
                                    	{ConfigKeywords.ex_places} INTEGER ARRAY,
                                    	{ConfigKeywords.persons} INTEGER ARRAY,
                                    	{ConfigKeywords.ex_persons} INTEGER ARRAY,
                                    	{ConfigKeywords.sources} INTEGER ARRAY,
                                    	{ConfigKeywords.ex_sources} INTEGER ARRAY,
                                    	{ConfigKeywords.others} INTEGER ARRAY,
                                    	{ConfigKeywords.ex_others} INTEGER ARRAY,
                                        {ConfigKeywords.source_fragments} INTEGER ARRAY,
                                        {ConfigKeywords.ex_source_fragments} INTEGER ARRAY
                                    );
                                    """ ) + super().generateTableSQL()
    

    def fillTableSQL(self) -> str:
        """
            Заполнение таблицы
        """
        result = f"INSERT INTO {self.name} VALUES \n"
        ary = []

        for key in self.storage :
            x = self.storage[key]
            if type(x) is Other :
                ary.append(inspect.cleandoc(f"""(
                                                    {NOV(x.id)}, {NOV(x.name)}, {NOV(x.meta)}, {NOV(x.description)}, 
                                                    {NOV(x.events)}, {NOV(x.ex_events)}, {NOV(x.dates)}, {NOV(x.ex_dates)},
                                                    {NOV(x.places)}, {NOV(x.ex_places)}, {NOV(x.persons)}, {NOV(x.ex_persons)},
                                                    {NOV(x.sources)}, {NOV(x.ex_sources)}, {NOV(x.others)}, {NOV(x.ex_others)},
                                                    {NOV(x.source_fragments)}, {NOV(x.ex_source_fragments)}
                                                )""") ) 
        result += ",\n".join(ary)
        result += ";"
        return result + super().fillTableSQL()