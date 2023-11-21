"""
    Файл работы с коллекциями, связанными
        с работой главных функций кластера - генерации SQL-запроса, обработки
        сущностей.
    В частности, хранить сами сущности, хранить статус.
"""
from logger import logger
from config import config
from schemas import *
from utils.exception import *

from .DBClient import DBClient, MongoDBClient
from .AbstractDB import AbstractDB, AbstractMongoDB


class SQLGeneratorDB(AbstractDB) :
    """
        Абстрактный репозиторий базы данных сущностей и всего,
            связанное с sql-generator-api
    """

    def __init__(self, client : DBClient) :
        logger.debug("Создание экземпляра класса SQLGeneratorDB")
        super().__init__(client)
        self.TYPE = "type"
        self.META_TYPE = "meta"
        self.SQL_TYPE = "sql"
        self.FILES_TYPE = "files"


    @AbstractDB.methodAsyncDecorator("SQLGeneratorDB:putMeta")
    async def putMeta(self, identifier : Identifier, meta : Meta) -> Meta | None :
        raise DBException(code=DBExceptionCode.METHOD_NOT_REALIZED, detail="SQLGeneratorDB не реализует метод putMeta!")


    @AbstractDB.methodAsyncDecorator("SQLGeneratorDB:getMeta")
    async def getMeta(self, identifier : Identifier) -> Meta | None :
        raise DBException(code=DBExceptionCode.METHOD_NOT_REALIZED, detail="SQLGeneratorDB не реализует метод getMeta!")


    @AbstractDB.methodAsyncDecorator("SQLGeneratorDB:putFiles")
    async def putFiles(self, identifier : Identifier, files : FileBaseKeywordList) -> FileBaseKeywordList | None :
        raise DBException(code=DBExceptionCode.METHOD_NOT_REALIZED, detail="SQLGeneratorDB не реализует метод putFiles!")


    @AbstractDB.methodAsyncDecorator("SQLGeneratorDB:getFiles")
    async def getFiles(self, identifier : Identifier) -> FileBaseKeywordList | None :
        raise DBException(code=DBExceptionCode.METHOD_NOT_REALIZED, detail="SQLGeneratorDB не реализует метод getFiles!")


    @AbstractDB.methodAsyncDecorator("SQLGeneratorDB:putSQL")
    async def putSQL(self, identifier : Identifier, file : FileBase) -> FileBase | None :
        raise DBException(code=DBExceptionCode.METHOD_NOT_REALIZED, detail="SQLGeneratorDB не реализует метод putSQL!")


    @AbstractDB.methodAsyncDecorator("SQLGeneratorDB:getSQL")
    async def getSQL(self, identifier : Identifier) -> FileBase | None :
        raise DBException(code=DBExceptionCode.METHOD_NOT_REALIZED, detail="SQLGeneratorDB не реализует метод getSQL!")


    @AbstractDB.methodAsyncDecorator("SQLGeneratorDB:getAllSQLIDs")
    async def getAllSQLIDs(self) -> int :
        raise DBException(code=DBExceptionCode.METHOD_NOT_REALIZED, detail="SQLGeneratorDB не реализует метод getAllSQLIDs!")


class SQLGeneratorMongoDB(SQLGeneratorDB) :
    """
        Реализация базы данных через MongoDB(Client).
        
        Храним документы с типами:
            
            type: status
            status: ""

            type: files
            files: [{}]

            type: sql
            sql: path-to-sql-file
    """

    def __init__(self, client : MongoDBClient) :
        logger.debug("Создание экземпляра класса SQLGeneratorMongoDB")
        super().__init__(client=client)
        self.db = self.client.client[config.DATABASE_SQL_GENERATOR_DB]


    @AbstractMongoDB.methodAsyncDecorator("SQLGeneratorMongoDB:putMeta")
    async def putMeta(self, identifier : Identifier, meta : Meta) -> Meta | None :
        """
            Заменить или внести сведения о статусе для операции по её коллекции-идентификатору
        """
        res = None

        async with await self.client.client.start_session() as s :
            exist = await self.db[identifier].find_one_and_replace({ self.TYPE : self.META_TYPE },
                                                                   { self.TYPE : self.META_TYPE, self.META_TYPE : meta.model_dump() },
                                                                   session=s)    
            if not exist :
                await self.db[identifier].insert_one({ self.TYPE : self.META_TYPE, self.META_TYPE : meta.model_dump() }, 
                                                     session=s)
            res = await self.db[identifier].find_one({ self.TYPE : self.META_TYPE }, 
                                                     session=s)

        return Meta(**res[self.META_TYPE]) if res else res


    @AbstractMongoDB.methodAsyncDecorator("SQLGeneratorMongoDB:getMeta")
    async def getMeta(self, identifier : Identifier) -> Meta | None :
        """
            Получить сведения о статусе для операции по её коллекции-идентификатору.
                Если таковых нет, поднимает исключение
        """
        res = None

        async with await self.client.client.start_session() as s :
            res = await self.db[identifier].find_one({ self.TYPE : self.META_TYPE }, session=s)
            if not res :
                raise DBException(code=DBExceptionCode.ENTITY_DONT_EXISTS,
                                  detail=f"Мета-иноформация для {identifier} не определена")

        return Meta(**res[self.META_TYPE]) if res else res


    @AbstractMongoDB.methodAsyncDecorator("SQLGeneratorMongoDB:putFiles")
    async def putFiles(self, identifier : Identifier, files : FileBaseKeywordList) -> FileBaseKeywordList | None :
        """Файлы, которые связаны с текущей операцией"""
        res = None

        async with await self.client.client.start_session() as s :
            exist = await self.db[identifier].find_one_and_replace({ self.TYPE : self.FILES_TYPE },
                                                                   { self.TYPE : self.FILES_TYPE, self.FILES_TYPE : files.model_dump() },
                                                                   session=s) 
            if not exist :
                await self.db[identifier].insert_one({ self.TYPE : self.FILES_TYPE, self.FILES_TYPE : files.model_dump() },
                                                     session=s)
            res = await self.db[identifier].find_one({ self.TYPE : self.FILES_TYPE},
                                                     session=s)

        return FileBaseKeywordList(**res[self.FILES_TYPE]) if res else res


    @AbstractMongoDB.methodAsyncDecorator("SQLGeneratorMongoDB:getFiles")
    async def getFiles(self, identifier : Identifier) -> FileBaseKeywordList | None :
        """Файлы, которые связны с текущей операцией"""
        res = None

        async with await self.client.client.start_session() as s :
            res = await self.db[identifier].find_one({ self.TYPE : self.FILES_TYPE }, session=s)
            if not res :
                raise DBException(code=DBExceptionCode.ENTITY_DONT_EXISTS,
                                  detail=f"Файлы для {identifier} не определены")

        return FileBaseKeywordList(**res[self.FILES_TYPE]) if res else res


    @AbstractMongoDB.methodAsyncDecorator("SQLGeneratorMongoDB:putSQL")
    async def putSQL(self, identifier : Identifier, file : FileBase) -> FileBase | None :
        """"""
        res = None

        async with await self.client.client.start_session() as s :
            exist = await self.db[identifier].find_one_and_replace({self.TYPE : self.SQL_TYPE},
                                                                   { self.TYPE : self.SQL_TYPE, self.SQL_TYPE : file.model_dump() }, 
                                                                   session=s)
            if not exist :
                await self.db[identifier].insert_one({ self.TYPE : self.SQL_TYPE, self.SQL_TYPE : file.model_dump() },
                                                     session=s)
            res = await self.db[identifier].find_one({ self.TYPE : self.SQL_TYPE},
                                                     session=s)

        return FileBase(**res[self.SQL_TYPE]) if res else res


    @AbstractMongoDB.methodAsyncDecorator("SQLGeneratorMongoDB:getSQL")
    async def getSQL(self, identifier : Identifier) -> FileBase | None :
        """"""
        res = None

        async with await self.client.client.start_session() as s :
            res = await self.db[identifier].find_one({ self.TYPE : self.SQL_TYPE},
                                                     session=s)
            if not res :
                raise DBException(code=DBExceptionCode.ENTITY_DONT_EXISTS,
                                  detail=f"Файл SQL для {identifier} не определён (не сгенерирован)")
        
        return FileBase(**res[self.SQL_TYPE]) if res else res


    async def getAllSQLIDs(self) -> MetaIdentifierList :
        """"""
        res : list[MetaIdentifier] = []

        async with await self.client.client.start_session() as s :
            for id in (await self.db.list_collection_names(session=s)) :
                sql_exist = await self.db[id].find_one({ self.TYPE : self.SQL_TYPE},
                                                       session=s)
                if sql_exist :
                    meta = await self.db[id].find_one({ self.TYPE : self.META_TYPE }, session=s)
                    if meta: 
                        res.append(MetaIdentifier(**meta[self.META_TYPE], identifier=id))

        return MetaIdentifierList(metas=res)