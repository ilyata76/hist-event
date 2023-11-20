"""
    Файл управления базой данных файлов
"""
import pymongo.errors as pyerros

from logger import logger
from utils import cutLog
from utils.exception import *

from .DBClient import DBClient, MongoDBClient


class AbstractDB :
    """
        Абстрактный класс работы с DBClient
    """

    def __init__(self, client : DBClient) :
        logger.debug("Создание экземпляра AbstractDB")
        self.client = client


    async def testConnect(self) :
        if not self.client.connected and not await self.client.testConnection(): 
            raise DBException(code=DBExceptionCode.SERVICE_UNAVAIABLE, 
                              detail="КлиентDB не смог подключиться к базам данных!")


    def methodAsyncDecorator(path : str) : 
        """
            Декоратор для методов работы с базой данных.
        """
        def method(function) :
            async def wrapMethodDatabase(self, *args, **kwargs) :
                try : 
                    await self.testConnect()
                    return await function(self, *args, **kwargs)
                except DBException as exc :
                    logger.error(f"Произошла ошибка, связанная с работой базы данных : {type(exc)}:{exc}")
                    raise exc
                except Exception as exc :
                    logger.error(f"Произошла непредвиденная ошибка : {type(exc)}:{exc}")
                    raise exc
            return wrapMethodDatabase
        return method


class AbstractMongoDB(AbstractDB) :
    """
        Для работы с классами от MongoDB
    """

    def __init__(self, client : MongoDBClient) :
        logger.debug("Создание класса AbstartMongoDB")
        super().__init__(client)


    def methodAsyncDecorator(path : str) : 
        """
            Декоратор для методов работы с файлами.
                Поднимает DBException и другие исключения
        """
        def method(function) :
            async def wrapMethodDatabase(self, *args, **kwargs) :
                prefix = f"[DATABASE] : {path} : {cutLog(args)} : {cutLog(kwargs)}"
                try : 
                    logger.debug(f"{prefix}")
                    await self.testConnect()
                    res = await function(self, *args, **kwargs)
                    logger.info(f"{prefix} : {cutLog(res)}")
                    return res
                except (pyerros.ConnectionFailure, 
                        pyerros.ExecutionTimeout, 
                        pyerros.WTimeoutError, 
                        pyerros.NetworkTimeout, 
                        pyerros.ServerSelectionTimeoutError,
                        pyerros.WaitQueueTimeoutError) as exc:
                    logger.error(f"{prefix} : Клиент не смог подключиться к базам данных!")
                    raise DBException(code=DBExceptionCode.SERVICE_UNAVAIABLE, 
                                    detail=f"Клиент не смог подключиться к базам данных!")
                except (pyerros.CursorNotFound, 
                        pyerros.CollectionInvalid, 
                        pyerros.ConfigurationError, 
                        pyerros.InvalidURI, 
                        pyerros.InvalidName) :
                    logger.error(f"{prefix} : База данных стала недоступна для Клиент")
                    raise DBException(code=DBExceptionCode.INVALIDATED, 
                                      detail=f"База данных стала недоступна для Клиент")
                except pyerros.DocumentTooLarge :
                    logger.error(f"{prefix} : Документ слишком много весит!")
                    raise DBException(code=DBExceptionCode.TOO_LARGE, 
                                      detail=f"Документ слишком много весит!")
                except (pyerros.WriteError, pyerros.EncryptionError, pyerros.DuplicateKeyError, pyerros.OperationFailure) :
                    logger.error(f"{prefix} : Произошла ошибка с операциями MongoDB")
                    raise DBException(code=DBExceptionCode.OPERATION_ERROR, 
                                      detail=f"Произошла ошибка с операциями MongoDB : {exc}")
                except DBException as exc :
                    logger.error(f"{prefix} : Произошла ошибка, связанная с работой базы данных : {exc}")
                    raise exc
                except BaseException as exc :
                    logger.error(f"{prefix} : Произошла непредвиденная ошибка : {type(exc)}:{exc}")
                    raise exc
            return wrapMethodDatabase
        return method