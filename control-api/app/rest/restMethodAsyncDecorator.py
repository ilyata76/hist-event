"""
    Ловит gRPC исключения, поднимает HTTPException
"""
from functools import wraps
from grpc import RpcError, StatusCode

from fastapi import HTTPException, status, Request

from app.logger import logger


def restMethodAsyncDecorator(function) :
    """
        Декоратор ловит gRPC исключения, поднимает fastapi.httpexception,
            которые впоследствии будут обработаны FastAPI в коробке
    """
    @wraps(function)
    async def methodRest(request : Request, *args, **kwargs) :
        msg = f"[SERVER][{request.client.host}:{request.client.port}] : {request.method} {request.url}"
        code, details = status.HTTP_500_INTERNAL_SERVER_ERROR, "Неизвестная ошибка!!!"
        try : 
            logger.pendingProcess(f"{msg}")
            res = await function(request, *args, **kwargs)
            logger.successProcess(f"{msg} : {res}")
            return res
        except RpcError as exc :
            details = exc.details()
            match exc.code() :
                case StatusCode.NOT_FOUND | StatusCode.UNIMPLEMENTED  :
                    code = status.HTTP_404_NOT_FOUND
                case StatusCode.UNAVAILABLE :
                    code = status.HTTP_503_SERVICE_UNAVAILABLE
                case StatusCode.ALREADY_EXISTS :
                    code = status.HTTP_409_CONFLICT
                case StatusCode.INVALID_ARGUMENT | StatusCode.ABORTED | StatusCode.CANCELLED | StatusCode.RESOURCE_EXHAUSTED :
                    code = status.HTTP_400_BAD_REQUEST
                case StatusCode.UNAUTHENTICATED :
                    code = status.HTTP_401_UNAUTHORIZED
                case StatusCode.PERMISSION_DENIED :
                    code = status.HTTP_403_FORBIDDEN
                case _ :
                    code = status.HTTP_500_INTERNAL_SERVER_ERROR
        except HTTPException as exc :
            code, details = exc.status_code, exc.detail
        except BaseException as exc :
            code, details = status.HTTP_500_INTERNAL_SERVER_ERROR, f"{type(exc)}:{exc}"
            logger.critical(f"{msg} : {details}")
            logger.exception(f"{msg} : {details}")
        logger.errorProcess(f"{msg} : {details}")
        raise HTTPException(status_code=code, detail=details)
    return methodRest