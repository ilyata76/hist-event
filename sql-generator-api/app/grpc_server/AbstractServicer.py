"""
    Файл логики gRPC-сервера
"""
import grpc
from functools import wraps

from logger import logger
from utils import cutLog
from utils.exception import *


class AbstractServicer :
    """
        храним декоратор
    """

    @staticmethod
    def methodAsyncDecorator(path : str) :
        """
            Декоратор, который обрабатывает исключения и берёт на себя логирование
                запросов, приходящих К СЕРВЕРУ
        """
        def servicerMethod(function) :
            @wraps(function)
            async def wrapServicerMethod(self, request, context : grpc.ServicerContext, *args, **kwargs) :
                msg = f"[SERVER][{context.peer()}] : {path} : {cutLog(request)} : {cutLog(args)} : {cutLog(kwargs)}"
                code, details = grpc.StatusCode.UNKNOWN, "unknown"
                try : 
                    logger.pendingProcess(msg)
                    res = await function(self, request=request, context=context, *args, **kwargs)
                    logger.successProcess(f"{msg} : {cutLog(res)}")
                    return res
                except grpc.RpcError as exc :
                    code, details = exc.code(), exc.details()
                except ConfigException as exc :
                    match exc.code : 
                        case ConfigExceptionCode.INVALID_KEYWORD :
                            code, details = grpc.StatusCode.INVALID_ARGUMENT, exc.detail
                        case _ :
                            code, details = grpc.StatusCode.UNKNOWN, "Неизвестная ошибка при конфигурации входных данных"
                except (ValidationException, ParsingException) as exc :
                    code, details = grpc.StatusCode.INVALID_ARGUMENT, exc.detail
                except BaseException as exc:
                    code, details = grpc.StatusCode.INTERNAL, f"{type(exc)}:{exc}"
                    logger.critical(f"{msg} : {details}")
                    logger.exception(f"{msg} : {details}")
                logger.errorProcess(f"{msg} : {details}")
                await context.abort(code, details)
            return wrapServicerMethod
        return servicerMethod