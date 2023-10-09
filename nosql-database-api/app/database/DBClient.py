"""
    Файл для работы с клиентом базы данных
"""
import motor.motor_asyncio as motor
from datetime import datetime

from utils.logger import logger
from utils.config import config
from utils.exception import DBException, DBExceptionCode


class DBClient() :
    """
        Объект для управления базой данных
    """

    def __init__(self, uri : str = config.DATABASE_URI) :
        logger.debug(f"Создание экземпляра DBClient по {uri}")
        self.uri = uri
        self._previous = datetime(year=2000, month=1, day=1)
        self._connected = False

    async def _testConnection(self) -> bool :
        """
            Проверить, что база данных работает
        """
        logger.error(f"DBClient не реализует метод _testConnection!")
        raise DBException(code=DBExceptionCode.METHOD_NOT_REALIZED, detail=f"DBClient не реализует метод _testConnection!")

    async def testConnection(self) -> bool :
        """
            Провести тестовое подключение, но если только оно не было проведено ранее
        """
        logger.debug(f"Проведение тестового подключения в DBClient к базе по {self.uri}")
        if int((datetime.now() - self._previous).total_seconds()) >= config.DATABASE_RECONNECTION_S :
            self._previous = datetime.now()
            return await self._testConnection()
        return self._connected
    
    @property # getter
    def connected(self) -> bool :
        return self._connected


class MongoDBClient(DBClient) :
    """
        Объект для управления базой данных MongoDB
    """

    def __init__(self, uri : str = config.DATABASE_URI) :
        super().__init__(uri)
        logger.debug(f"Инициализация клиента для базы данных MongoDBClient по {self.uri}")
        self._client = motor.AsyncIOMotorClient(self.uri, 
                                                connectTimeoutMS=config.DATABASE_TIMEOUT_MS, 
                                                timeoutMS=config.DATABASE_TIMEOUT_MS)

    @property
    def client(self) :
        return self._client

    async def _testConnection(self) -> bool :
        """
            Проверить, что MongoDB функционирует
        """
        try :
            await self.client.server_info()
            self._connected = True
        except BaseException :
            self._connected = False
        logger.debug(f"Тестовое подключение к MongoDB: {self._connected}")
        return self.connected