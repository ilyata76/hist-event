"""
    Файл работы с коллекциями, связанными
        с работой главных функций кластера - генерации SQL-запроса, обработки
        сущностей.
    В частности, хранить сами сущности, хранить статус.
"""

from database.DBClient import DBClient, MongoDBClient
from database.AbstractDB import AbstractDB, AbstractMongoDB
from utils.logger import logger
from utils.config import config
from utils.exception import DBException, DBExceptionCode
from schemas.StatusIdentifier import StatusIdentifier, Identifier
from schemas.File import FileBaseKeywordList, FileBase


class SQLGeneratorDB(AbstractDB) :
    """
        Абстрактный репозиторий базы данных сущностей и всего,
            связанное с sql-generator-api
    """

    def __init__(self, client : DBClient) :
        logger.debug("Создание экземпляра класса SQLGeneratorDB")
        super().__init__(client)
        self.TYPE = "type"
        self.STATUS_TYPE = "status"
        self.SQL_TYPE = "sql"
        self.FILES_TYPE = "files"

    @AbstractDB.method("SQLGeneratorDB:putStatus")
    async def putStatus(self, status_identifier : StatusIdentifier) -> StatusIdentifier | None :
        raise DBException(code=DBExceptionCode.METHOD_NOT_REALIZED, detail="SQLGeneratorDB не реализует метод putStatus!")

    @AbstractDB.method("SQLGeneratorDB:getStatus")
    async def getStatus(self, identifier : Identifier) -> StatusIdentifier | None :
        raise DBException(code=DBExceptionCode.METHOD_NOT_REALIZED, detail="SQLGeneratorDB не реализует метод getStatus!")

    @AbstractDB.method("SQLGeneratorDB:putFiles")
    async def putFiles(self, identifier : Identifier, files : FileBaseKeywordList) -> Identifier | None :
        raise DBException(code=DBExceptionCode.METHOD_NOT_REALIZED, detail="SQLGeneratorDB не реализует метод putFiles!")

    @AbstractDB.method("SQLGeneratorDB:getFiles")
    async def getFiles(self, identifier : Identifier) -> FileBaseKeywordList | None :
        raise DBException(code=DBExceptionCode.METHOD_NOT_REALIZED, detail="SQLGeneratorDB не реализует метод getFiles!")

    @AbstractDB.method("SQLGeneratorDB:putSQL")
    async def putSQL(self, identifier : Identifier, file : FileBase) -> FileBase | None :
        raise DBException(code=DBExceptionCode.METHOD_NOT_REALIZED, detail="SQLGeneratorDB не реализует метод putSQL!")

    @AbstractDB.method("SQLGeneratorDB:getSQL")
    async def getSQL(self, identifier : Identifier) -> FileBase | None :
        raise DBException(code=DBExceptionCode.METHOD_NOT_REALIZED, detail="SQLGeneratorDB не реализует метод getSQL!")


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


    def prefix(self) :
        return f"[DATABASE][MONGODB][SQLGENERATOR]"


    @AbstractMongoDB.method("SQLGeneratorMongoDB:putStatus")
    async def putStatus(self, status_identifier : StatusIdentifier) -> StatusIdentifier | None :
        """
            Заменить или внести сведения о статусе для операции по её коллекции-идентификатору
        """
        res = None

        async with await self.client.client.start_session() as s :
            exist = await self.db[status_identifier.identifier].find_one_and_replace({ self.TYPE : self.STATUS_TYPE },
                                                                                     { self.TYPE : self.STATUS_TYPE, self.STATUS_TYPE : status_identifier.status },
                                                                                     session=s)    
            if not exist :
                await self.db[status_identifier.identifier].insert_one({ self.TYPE : self.STATUS_TYPE, self.STATUS_TYPE : status_identifier.status })
            res = await self.db[status_identifier.identifier].find_one({ self.TYPE : self.STATUS_TYPE }, session=s)

        return StatusIdentifier(identifier=status_identifier.identifier,
                                status=res[self.STATUS_TYPE]) if res else res


    @AbstractMongoDB.method("SQLGeneratorMongoDB:getStatus")
    async def getStatus(self, identifier : Identifier) -> StatusIdentifier | None :
        """
            Получить сведения о статусе для операции по её коллекции-идентификатору.
                Если таковых нет, поднимает исключение
        """
        res = None

        async with await self.client.client.start_session() as s :
            res = await self.db[identifier.identifier].find_one({ self.TYPE : self.STATUS_TYPE }, session=s)
            if not res :
                raise DBException(code=DBExceptionCode.ENTITY_DONT_EXISTS,
                                  detail=f"Статус для {identifier.identifier} не определён")
        
        return StatusIdentifier(identifier=identifier.identifier,
                                status=res[self.STATUS_TYPE]) if res else res


    @AbstractMongoDB.method("SQLGeneratorMongoDB:putFiles")
    async def putFiles(self, identifier : Identifier, files : FileBaseKeywordList) -> Identifier | None :
        """Файлы, которые связаны с текущей операцией"""
        res = None

        async with await self.client.client.start_session() as s :
            exist = await self.db[identifier.identifier].find_one_and_replace({ self.TYPE : self.FILES_TYPE },
                                                                              { self.TYPE : self.FILES_TYPE, self.FILES_TYPE : files.model_dump() },
                                                                              session=s) 
            if not exist :
                await self.db[identifier.identifier].insert_one({ self.TYPE : self.FILES_TYPE, self.FILES_TYPE : files.model_dump() })
            res = await self.db[identifier.identifier].find_one({ self.TYPE : self.FILES_TYPE})

        return Identifier(identifier=identifier.identifier) if res else res


    @AbstractMongoDB.method("SQLGeneratorMongoDB:getFiles")
    async def getFiles(self, identifier : Identifier) -> FileBaseKeywordList | None :
        """Файлы, которые связны с текущей операцией"""
        res = None

        async with await self.client.client.start_session() as s :
            res = await self.db[identifier.identifier].find_one({ self.TYPE : self.FILES_TYPE }, session=s)
            if not res :
                raise DBException(code=DBExceptionCode.ENTITY_DONT_EXISTS,
                                  detail=f"Файлы для {identifier.identifier} не определены")

        return FileBaseKeywordList(**res[self.FILES_TYPE]) if res else res


    @AbstractMongoDB.method("SQLGeneratorMongoDB:putSQL")
    async def putSQL(self, identifier : Identifier, file : FileBase) -> FileBase | None :
        """"""
        res = None

        async with await self.client.client.start_session() as s :
            exist = await self.db[identifier.identifier].find_one_and_replace({self.TYPE : self.SQL_TYPE},
                                                                              { self.TYPE : self.SQL_TYPE, self.SQL_TYPE : file.model_dump() }, 
                                                                              session=s)
            if not exist :
                await self.db[identifier.identifier].insert_one({ self.TYPE : self.SQL_TYPE, self.SQL_TYPE : file.model_dump() })
            res = await self.db[identifier.identifier].find_one({ self.TYPE : self.SQL_TYPE})

        return FileBase(**res[self.SQL_TYPE]) if res else res


    @AbstractMongoDB.method("SQLGeneratorMongoDB:getSQL")
    async def getSQL(self, identifier : Identifier) -> FileBase | None :
        """"""
        res = None

        async with await self.client.client.start_session() as s :
            res = await self.db[identifier.identifier].find_one({ self.TYPE : self.SQL_TYPE})
            if not res :
                raise DBException(code=DBExceptionCode.ENTITY_DONT_EXISTS,
                                  detail=f"Статус для {identifier.identifier} не определён")
        
        return FileBase(**res[self.SQL_TYPE]) if res else res