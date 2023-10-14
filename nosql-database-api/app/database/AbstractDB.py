"""
    Файл управления базой данных файлов
"""
import pymongo.errors as pyerros

from database.DBClient import DBClient, MongoDBClient
from utils.logger import logger
from utils.exception import DBException, DBExceptionCode


class AbstractDB :
    """
        Абстрактный класс работы с DBClient
    """

    def __init__(self, client : DBClient) :
        logger.debug("Создание экземпляра AbstractDB")
        self.client = client

    async def testConnect(self) :
        logger.debug("Клиент DB: тестовое подключение")
        if not self.client.connected and not await self.client.testConnection(): 
            raise DBException(code=DBExceptionCode.SERVICE_UNAVAIABLE, 
                              detail="КлиентDB не смог подключиться к базам данных!")

    def method(function) : 
        """
            Декоратор для методов работы с базой данных.
        """
        async def wrap(self, *args, **kwargs) :
            try : 
                await self.testConnect()
                return await function(self, *args, **kwargs)
            except DBException as exc :
                logger.error(f"Произошла ошибка, связанная с работой базы данных : {type(exc)}:{exc}")
                raise exc
            except Exception as exc :
                logger.error(f"Произошла непредвиденная ошибка : {type(exc)}:{exc}")
                raise exc
        return wrap
    

class AbstractMongoDB(AbstractDB) :
    """
        Для работы с классами от MongoDB
    """
    def __init__(self, client : MongoDBClient) :
        logger.debug("Создание класса AbstartMongoDB")
        super().__init__(client)

    
    def method(function) : 
        """
            Декоратор для методов работы с файлами.
                Поднимает DBException и другие исключения
        """
        async def wrap(self, *args, **kwargs) :
            try : 
                await self.testConnect()
                return await function(self, *args, **kwargs)
            except (pyerros.ConnectionFailure, 
                    pyerros.ExecutionTimeout, 
                    pyerros.WTimeoutError, 
                    pyerros.NetworkTimeout, 
                    pyerros.ServerSelectionTimeoutError,
                    pyerros.WaitQueueTimeoutError) as exc:
                logger.error(f"Клиент не смог подключиться к базам данных! : {type(exc)}:{exc}")
                raise DBException(code=DBExceptionCode.SERVICE_UNAVAIABLE, 
                                  detail=f"Клиент не смог подключиться к базам данных! : {type(exc)}:{exc}")
            except (pyerros.CursorNotFound, 
                    pyerros.CollectionInvalid, 
                    pyerros.ConfigurationError, 
                    pyerros.InvalidURI, 
                    pyerros.InvalidName) :
                logger.error(f"База данных стала недоступна для Клиент : {type(exc)}:{exc}")
                raise DBException(code=DBExceptionCode.INVALIDATED, 
                                  detail=f"База данных стала недоступна для Клиент : {type(exc)}:{exc}")
            except pyerros.DocumentTooLarge :
                logger.error(f"Документ слишком много весит! : {type(exc)}:{exc}")
                raise DBException(code=DBExceptionCode.TOO_LARGE, 
                                  detail=f"Документ слишком много весит! : {type(exc)}:{exc}")
            except (pyerros.WriteError, pyerros.EncryptionError, pyerros.DuplicateKeyError, pyerros.OperationFailure) :
                logger.error("Произошла ошибка с операциями MongoDB")
                raise DBException(code=DBExceptionCode.OPERATION_ERROR, 
                                  detail=f"Произошла ошибка с операциями MongoDB : {type(exc)}:{exc}")
            except DBException as exc :
                logger.error(f"Произошла ошибка, связанная с работой базы данных : {type(exc)}:{exc}")
                raise exc
            except Exception as exc :
                logger.error(f"Произошла непредвиденная ошибка : {type(exc)}:{exc}")
                raise exc
        return wrap