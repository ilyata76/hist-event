"""
    Файл клиента для gRPC
"""
from functools import wraps
import grpc

from utils import cutLog
from logger import logger


class AbstractgRPCClient :
    """
        храним декоратор
    """

    @staticmethod
    def methodAsyncDecorator(path : str, ip : str) :
        """
            Декоратор, который обрабатывает исключения и берёт на себя логирование
                запросов, исходящих ОТ КЛИЕНТА.
        """
        def gRPCMethod(function) :
            @wraps(function)
            async def wrapClientMethod(*args, channel = None, **kwargs) :
                msg = f"[CLIENT] : {path} : {cutLog(args)} : {cutLog(kwargs)}"
                try : 
                    logger.pending(msg)
                    if not channel : 
                        with grpc.insecure_channel(ip) as channel :
                            result = await function(*args, channel=channel, **kwargs)
                    else :
                        result = await function(*args, channel=channel, **kwargs)
                    logger.success(f"{msg} : {cutLog(result)}")
                    return result
                except grpc.RpcError as exc:
                    logger.error(f"{msg} : {exc.code()}:{exc.details()}")
                    raise exc
                except BaseException as exc:
                    logger.exception(f"{msg} : {type(exc)}:{exc}")
                    raise RuntimeError(f"При обработке запроса произошла непредвиденная ошибка : {type(exc)}:{exc}")
            return wrapClientMethod
        return gRPCMethod