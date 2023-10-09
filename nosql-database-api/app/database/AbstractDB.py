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

    def DBMethodDecorator(function) : 
        """
            Декоратор для методов работы с файлами.
        """
        async def wrap(self, *args, **kwargs) :
            try : 
                if not self.client.connected : 
                    if not await self.client.testConnection() :
                        raise DBException(code=DBExceptionCode.SERVICE_UNAVAIABLE, 
                                          detail="FileDB не смог подключиться к базам данных!")
                return await function(self, *args, **kwargs)
            except DBException as exc :
                logger.error(f"Произошла ошибка, связанная с работой базы данных : {type(exc)}:{exc}")
                raise exc
            except Exception as exc :
                logger.error(f"Произошла непредвиденная ошибка : {type(exc)}:{exc}")
                raise exc
        return wrap
    

class AbstartMongoDB(AbstractDB) :
    """
        Для работы с классами от MongoDB
    """
    def __init__(self, client : MongoDBClient) :
        logger.debug("Создание класса AbstartMongoDB")
        super().__init__(client)

    
    def MongoDBMethodDecorator(function) : 
        """
            Декоратор для методов работы с файлами.
        """
        async def wrap(self, *args, **kwargs) :
            try : 
                if not self.client.connected : 
                    if not await self.client.testConnection() :
                        raise DBException(code=DBExceptionCode.SERVICE_UNAVAIABLE, 
                                          detail="FileDB не смог подключиться к базам данных!")
                return await function(self, *args, **kwargs)
            except (pyerros.ConnectionFailure, 
                    pyerros.ExecutionTimeout, 
                    pyerros.WTimeoutError, 
                    pyerros.NetworkTimeout, 
                    pyerros.ServerSelectionTimeoutError,
                    pyerros.WaitQueueTimeoutError) as exc:
                logger.error(f"FileDB не смог подключиться к базам данных! : {type(exc)}:{exc}")
                raise DBException(code=DBExceptionCode.SERVICE_UNAVAIABLE, 
                                  detail=f"FileDB не смог подключиться к базам данных! : {type(exc)}:{exc}")
            except (pyerros.CursorNotFound, 
                    pyerros.CollectionInvalid, 
                    pyerros.ConfigurationError, 
                    pyerros.InvalidURI, 
                    pyerros.InvalidName) :
                logger.error(f"База данных стала недоступна для FileDB : {type(exc)}:{exc}")
                raise DBException(code=DBExceptionCode.INVALIDATED, 
                                  detail=f"База данных стала недоступна для FileDB : {type(exc)}:{exc}")
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