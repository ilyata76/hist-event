"""
    Абстрактный процессор
"""
from utils.exception import ConfigException, ConfigExceptionCode
from utils.logger import logger
from utils.config import LogCode


class AbstractProcessor :
    """
    """

    @staticmethod
    def methodDecorator(path : str) :
        """
            Декоратор, который обрабатывает исключения и берёт на себя логирование
                функций главных процессов
        """
        def processorMethod(function) :
            async def wrap(self, *args, **kwargs) :
                try : 
                    logger.debug(f"[PROCESSOR] : {path} : {args} : {kwargs} : {LogCode.PENDING}")
                    res = await function(self, *args, **kwargs)
                    logger.info(f"[PROCESSOR] : {path} : {args} : {kwargs} : {LogCode.SUCCESS}")
                    return res
                except KeyError as exc :
                    raise ConfigException(code=ConfigExceptionCode.INVALID_KEYWORD,
                                          detail=f"Невозможно взять значение по ключу {exc.args}")
                except BaseException as exc :
                    logger.error(f"[PROCESSOR] : {path} : {args} : {kwargs} : {LogCode.ERROR}")
                    raise exc
            return wrap
        return processorMethod