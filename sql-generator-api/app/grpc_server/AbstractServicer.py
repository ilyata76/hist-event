"""
    Файл логики gRPC-сервера
"""
import grpc
from functools import partial, wraps

from utils.logger import logger
from utils.config import LogCode
from utils.exception import *


class AbstractServicer :
    """
        храним декоратор
    """

    @staticmethod
    def logPrefix(path : str, peer : str, code : str, request) :
        return f"[SERVER][{peer}] : {path} : " + request.__str__().replace('\n', ' ') + f" : {code}"


    @staticmethod
    def methodAsyncDecorator(path : str) :
        """
            Декоратор, который обрабатывает исключения и берёт на себя логирование
                запросов, приходящих К СЕРВЕРУ
        """
        def servicerMethod(function) :
            @wraps(function)
            async def wrap(self, request, context : grpc.ServicerContext, *args, **kwargs) :
                prefix = partial(AbstractServicer.logPrefix, path=path, peer=context.peer(), request=request)
                try : 
                    logger.debug(f"{prefix(code=LogCode.PENDING)}")
                    res = await function(self, request=request, context=context, *args, **kwargs)
                    logger.info(f"{prefix(code=LogCode.SUCCESS)}")
                    return res
                except grpc.RpcError as exc :
                    logger.error(f"{prefix(code=LogCode.ERROR)} : {exc.code()}:{exc.details()}")
                    await context.abort(exc.code(), exc.details())
                except ConfigException as exc :
                    logger.error(f"{prefix(code=LogCode.ERROR)} : {exc.code}:{exc.detail}")
                    match exc.code : 
                        case ConfigExceptionCode.INVALID_KEYWORD :
                            await context.abort(grpc.StatusCode.INVALID_ARGUMENT, exc.detail)
                        case _ :
                            await context.abort(grpc.StatusCode.UNKNOWN, "Неизвестная ошибка при конфигурации входных данных")
                except (ValidationException, ParsingException) as exc :
                    logger.error(f"{prefix(code=LogCode.ERROR)} : {exc.code}:{exc.detail}")
                    await context.abort(grpc.StatusCode.INVALID_ARGUMENT, exc.detail)
                except BaseException as exc:
                    logger.exception(f"{prefix(code=LogCode.ERROR)} : {type(exc)}:{exc}")
                    await context.abort(grpc.StatusCode.INTERNAL, f"internal server error : {type(exc)}:{exc}")
            return wrap
        return servicerMethod