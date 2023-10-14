"""
    Файл логики gRPC-сервера
"""
import grpc
from functools import partial

from utils.logger import logger
from utils.config import LogCode


class AbstractServicer :
    """
        храним декоратор
    """

    @staticmethod
    def logPrefix(path : str, peer : str, code : str) :
        return f"[SERVER][{path}][{code}][{peer}]"

    def method(path : str) :
        """
            Декоратор, который обрабатывает исключения и берёт на себя логирование
                запросов, приходящих К СЕРВЕРУ
        """
        def servicerMethod(function) :
            async def wrap(self, request, context : grpc.ServicerContext, *args, **kwargs) :
                prefix = partial(AbstractServicer.logPrefix, path=path, peer=context.peer())
                try : 
                    logger.debug(f"{prefix(code=LogCode.PENDING)} Получен запрос от удаленного gRPC-сервера")
                    res = await function(self, request=request, context=context, *args, **kwargs)
                    logger.info(f"{prefix(code=LogCode.SUCCESS)} Запрос от удаленного gRPC был обработан")
                    return res
                except grpc.RpcError as exc :
                    logger.error(f"{prefix(code=LogCode.ERROR)} Ошибка gRPC-сервера : {exc.code()}:{exc.details()}")
                    await context.abort(exc.code(), exc.details())
                except BaseException as exc:
                    logger.exception(f"{prefix(code=LogCode.ERROR)} Во время обработки запроса произошла ошибка : {type(exc)}:{exc}")
                    await context.abort(grpc.StatusCode.INTERNAL, f"internal server error : {type(exc)}:{exc}")
            return wrap
        return servicerMethod