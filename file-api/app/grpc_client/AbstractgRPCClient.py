"""
    Файл клиента для gRPC
"""
from functools import partial
from grpc import RpcError

from utils.logger import logger
from utils.config import LogCode


class AbstractgRPCClient :
    """
        храним декоратор
    """

    @staticmethod
    def logPrefix(path : str, code : str) :
        return f"[CLIENT][{path}][{code}]"

    def method(path : str) :
        """
            Декоратор, который обрабатывает исключения и берёт на себя логирование
                запросов, исходящих ОТ КЛИЕНТА
        """
        def gRPCMethod(function) :
            async def wrap(*args, **kwargs) :
                prefix = partial(AbstractgRPCClient.logPrefix, path=path)
                try : 
                    logger.debug(f"{prefix(code=LogCode.PENDING)} Отправлен запрос к удаленному gRPC-серверу")
                    result = await function(*args, **kwargs)
                    logger.info(f"{prefix(code=LogCode.SUCCESS)} Получен ответ от удаленного gRPC-сервера")
                    return result
                except RpcError as exc:
                    logger.info(f"{prefix(code=LogCode.ERROR)} Удаленный сервер вернул ошибку : {exc.code()}:{exc.details()}")
                    raise exc
                except BaseException as exc:
                    logger.error(f"{prefix(code=LogCode.ERROR)} При обработке запроса произошла непредвиденная ошибка : {type(exc)}:{exc}")
                    raise RuntimeError(f"При обработке запроса произошла непредвиденная ошибка : {type(exc)}:{exc}")
            return wrap
        return gRPCMethod