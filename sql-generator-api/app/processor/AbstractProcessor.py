"""
    Абстрактный процессор
"""
from functools import wraps

from utils.exception import *
from logger import logger


class AbstractProcessor :
    """
        Главные функции приложения
    """

    @staticmethod
    def methodAsyncDecorator(path : str) :
        """
            Декоратор, который обрабатывает исключения и берёт на себя логирование
                функций главных процессов
        """
        def processorMethod(function) :
            @wraps(function)
            async def wrapAbstractProcessorMethod(self, *args, **kwargs) :
                prefix = f"[PROCESSOR] : {path} : {args} : {kwargs}"
                try : 
                    logger.debug(f"{prefix} : START")
                    res = await function(self, *args, **kwargs)
                    logger.info(f"{prefix} : SUCCESS")
                    return res
                except KeyError as exc :
                    logger.error(f"{prefix} : {type(exc)}:{exc.args}")
                    raise ConfigException(code=ConfigExceptionCode.INVALID_KEYWORD,
                                          detail=f"Невозможно взять значение по ключу {exc.args[0]}")
                except ParsingException as exc :
                    prefix = f"{prefix} : {exc.code}:{exc.detail}"
                    match exc.code :
                        case ParsingExceptionCode.LINKS_ERRORS_WHILE_PARSING :
                            logger.warning(prefix)
                        case _ :
                            logger.error(prefix)
                    raise exc
                except BaseException as exc :
                    logger.error(f"{prefix} : {type(exc)}:{exc.args}")
                    raise exc
            return wrapAbstractProcessorMethod
        return processorMethod