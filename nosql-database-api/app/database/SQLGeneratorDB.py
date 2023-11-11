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


class SQLGeneratorDB(AbstractDB) :
    """
        Абстрактный репозиторий базы данных сущностей и всего,
            связанное с sql-generator-api
    """

    def __init__(self, client : DBClient) :
        logger.debug("Создание экземпляра класса SQLGeneratorDB")
        super().__init__(client)
        self.TYPE = "type"
        self.ENTITY_TYPE = "entity"
        self.STATUS_TYPE = "status"
        self.SQL_TYPE = "sql"


    @AbstractDB.method("SQLGeneratorDB:putStatus")
    async def putStatus(self, status_identifier : StatusIdentifier) -> StatusIdentifier | None :
        raise DBException(code=DBExceptionCode.METHOD_NOT_REALIZED, detail="SQLGeneratorDB не реализует метод putStatus!")


    @AbstractDB.method("SQLGeneratorDB:getStatus")
    async def getStatus(self, identifier : Identifier) -> StatusIdentifier | None :
        raise DBException(code=DBExceptionCode.METHOD_NOT_REALIZED, detail="SQLGeneratorDB не реализует метод getStatus!")


    @AbstractDB.method("SQLGeneratorDB:putOneEntity")
    async def putOneEntity(self, identifier : Identifier, entity : dict) -> dict | None : # TODO Entity schema (dynamic)
        raise DBException(code=DBExceptionCode.METHOD_NOT_REALIZED, detail="SQLGeneratorDB не реализует метод putOneEntity!")


    @AbstractDB.method("SQLGeneratorDB:clearAllEntities")
    async def clearAllEntities(self, identifier : Identifier) -> list[dict] | None : # TODO Entity schema (dynamic)
        raise DBException(code=DBExceptionCode.METHOD_NOT_REALIZED, detail="SQLGeneratorDB не реализует метод clearAllEntities!")


    @AbstractDB.method("SQLGeneratorDB:getManyEntities")
    async def getAllEntities(self, identifier : Identifier) -> list[dict] | None : # TODO Entity schema (dynamic)
        raise DBException(code=DBExceptionCode.METHOD_NOT_REALIZED, detail="SQLGeneratorDB не реализует метод getAllEntities!")


class SQLGeneratorMongoDB(SQLGeneratorDB) :
    """
        Реализация базы данных через MongoDB(Client).
        
        Храним документы с типами:
            
            type: status
            status: ""

            type: entity
            entity: {}

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