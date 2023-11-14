"""
    Файл клиента для gRPC
"""
from functools import partial, wraps
import grpc

from utils.logger import logger
from utils.logger import LogCode


class AbstractgRPCClient :
    """
        храним декоратор
    """

    @staticmethod
    def logPrefix(path : str, code : str, args : list, kwargs : dict) :
        return f"[CLIENT] : {path} : {args} : {kwargs} : {code}"


    @staticmethod
    def methodAsyncDecorator(path : str, ip : str) :
        """
            Декоратор, который обрабатывает исключения и берёт на себя логирование
                запросов, исходящих ОТ КЛИЕНТА.
        """
        def gRPCMethod(function) :
            @wraps(function)
            async def wrap(*args, channel = None, **kwargs) :
                prefix = partial(AbstractgRPCClient.logPrefix, path=path, args=args, kwargs=kwargs)
                try : 
                    logger.debug(f"{prefix(code=LogCode.PENDING)}")
                    if not channel : 
                        with grpc.insecure_channel(ip) as channel :
                            result = await function(*args, channel=channel, **kwargs)
                    else :
                        result = await function(*args, channel=channel, **kwargs)
                    logger.info(f"{prefix(code=LogCode.SUCCESS)} : {result}")
                    return result
                except grpc.RpcError as exc:
                    logger.error(f"{prefix(code=LogCode.ERROR)} : {exc.code()}:{exc.details()}")
                    raise exc
                except BaseException as exc:
                    logger.exception(f"{prefix(code=LogCode.ERROR)} : {type(exc)}:{exc}")
                    raise RuntimeError(f"При обработке запроса произошла непредвиденная ошибка : {type(exc)}:{exc}")
            return wrap
        return gRPCMethod