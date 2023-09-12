"""
    Схемы, определяющие исторический источник как сущность
"""
from loguru import logger
from schemas.Entity import BaseEntity, BaseStorage
import inspect
from config import ConfigKeywords
from processes.utils import NOV


class Source(BaseEntity) :
    """
        Модель, описывающая сущность исторического источника
    """
    author : str | None = None
    link : str | None = None
    date : int | None = None # ссылка на date FK


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
        return inspect.cleandoc( f"""
                                    CREATE TABLE {self.name} (
                                    	{ConfigKeywords.id} INTEGER PRIMARY KEY,
                                    	{ConfigKeywords.name} TEXT NOT NULL,
                                    	{ConfigKeywords.date} INTEGER NOT NULL,
                                    	{ConfigKeywords.description} TEXT,
                                        {ConfigKeywords.author} TEXT NOT NULL,
                                        {ConfigKeywords.link} TEXT,
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

                                            CONSTRAINT FK_date_id FOREIGN KEY (date) REFERENCES dates(id)
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
            if type(x) is Source :
                ary.append(inspect.cleandoc(f"""(
                                                    {NOV(x.id)}, {NOV(x.name)}, {NOV(x.date)}, {NOV(x.description)}, {NOV(x.author)}, {NOV(x.link)},
                                                    {NOV(x.events)}, {NOV(x.ex_events)}, {NOV(x.dates)}, {NOV(x.ex_dates)},
                                                    {NOV(x.places)}, {NOV(x.ex_places)}, {NOV(x.persons)}, {NOV(x.ex_persons)},
                                                    {NOV(x.sources)}, {NOV(x.ex_sources)}, {NOV(x.others)}, {NOV(x.ex_others)}
                                                )""") )
        result += ",\n".join(ary)
        result += ";"
        return result  + super().fillTableSQL()