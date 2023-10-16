"""
    Файл логики gRPC-сервера
"""
import grpc
from functools import partial

from utils.logger import logger
from utils.config import LogCode
from utils.exception import ConfigException, ConfigExceptionCode,\
                            StorageException, StorageExceptionCode


class AbstractServicer :
    """
        храним декоратор
    """

    @staticmethod
    def logPrefix(path : str, peer : str, code : str) :
        return f"[SERVER][{peer}] : {path} : {code}"

    @staticmethod
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
                except StorageException as exc :
                    logger.error(f"{prefix(code=LogCode.ERROR)} : {exc.code}:{exc.detail}")
                    abort = partial(context.abort, details=exc.detail)
                    match exc.code :
                        case StorageExceptionCode.METHOD_NOT_REALIZED :
                            await abort(grpc.StatusCode.UNIMPLEMENTED)
                        case StorageExceptionCode.ALREADY_EXISTS :
                            await abort(grpc.StatusCode.ALREADY_EXISTS)
                        case StorageExceptionCode.ENTITY_DOESNT_EXISTS :
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