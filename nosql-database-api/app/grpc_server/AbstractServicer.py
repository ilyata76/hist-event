"""
    Файл логики gRPC-сервера
"""
import grpc
from functools import partial

from utils.logger import logger
from utils.config import LogCode
from utils.exception import DBException, DBExceptionCode,\
    ConfigException, ConfigExceptionCode


class AbstractServicer :
    """
        храним декоратор
    """

    @staticmethod
    def logPrefix(path : str, peer : str, code : str) :
        return f"[SERVER][{peer}] : {path} : {code}"

    def method(path : str) :
        """
            Декоратор, который обрабатывает исключения и берёт на себя логирование
                запросов, приходящих К СЕРВЕРУ
        """
        def servicerMethod(function) :
            async def wrap(self, request, context : grpc.ServicerContext, *args, **kwargs) :
                prefix = partial(AbstractServicer.logPrefix, path=path, peer=context.peer())
                try : 
                    logger.debug(f"{prefix(code=LogCode.PENDING)}")
                    res = await function(self, request=request, context=context, *args, **kwargs)
                    logger.info(f"{prefix(code=LogCode.SUCCESS)}")
                    return res
                except grpc.RpcError as exc :
                    logger.error(f"{prefix(code=LogCode.ERROR)} : {exc.code()}:{exc.details()}")
                    await context.abort(exc.code(), exc.details())
                except DBException as exc :
                    logger.error(f"{prefix(code=LogCode.ERROR)} : {exc.code}:{exc.detail}")
                    abort = partial(context.abort, details=exc.detail)
                    match exc.code :
                        case DBExceptionCode.SERVICE_UNAVAIABLE | DBExceptionCode.INVALIDATED :
                            await abort(grpc.StatusCode.UNAVAILABLE)
                        case DBExceptionCode.ENTITY_EXISTS :
                            await abort(grpc.StatusCode.ALREADY_EXISTS)
                        case DBExceptionCode.TOO_LARGE : 
                            await abort(grpc.StatusCode.RESOURCE_EXHAUSTED)
                        case DBExceptionCode.OPERATION_ERROR :
                            await abort(grpc.StatusCode.ABORTED)
                        case DBExceptionCode.METHOD_NOT_REALIZED :
                            await abort(grpc.StatusCode.UNIMPLEMENTED)
                        case DBExceptionCode.ENTITY_DONT_EXISTS :
                            await abort(grpc.StatusCode.NOT_FOUND)
                        case _ :
                            await abort(grpc.StatusCode.UNKNOWN)
                except ConfigException as exc :
                    logger.error(f"{prefix(code=LogCode.ERROR)} : {exc.code}:{exc.detail}")
                    abort = partial(context.abort, details=exc.detail)
                    match exc.code :
                        case ConfigExceptionCode.INVALID_STORAGE_IDENTIFIER :
                            await abort(grpc.StatusCode.INVALID_ARGUMENT)
                        case _ :
                            await abort(grpc.StatusCode.UNKNOWN)
                except BaseException as exc:
                    logger.exception(f"{prefix(code=LogCode.ERROR)} : {type(exc)}:{exc}")
                    await context.abort(grpc.StatusCode.INTERNAL, f"internal server error : {type(exc)}:{exc}")
            return wrap
        return servicerMethod