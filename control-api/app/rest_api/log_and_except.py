"""
    Ловит gRPC исключения, поднимает HTTPException
"""
from functools import wraps
from grpc import RpcError, StatusCode

from fastapi import HTTPException, status, Request

from app.utils.logger import logger
from app.utils.config import LogCode


def log_and_except(#path : str = "not specified"
                   function) :
        """
            Декоратор ловит gRPC исключения, поднимает fastapi.httpexception,
                которые впоследствии будут обработаны FastAPI в коробке
        """
    #def LAE(function) :
        @wraps(function)
        async def wrap(request : Request, *args, **kwargs) :
            log_prefix = f"[SERVER][{request.client.host}:{request.client.port}] : {request.method} {request.url}"
            try : 
                logger.debug(f"{log_prefix} : {LogCode.PENDING}")
                res = await function(request, *args, **kwargs)
                logger.info(f"{log_prefix} : {LogCode.SUCCESS}")
                return res
            except RpcError as exc :
                logger.error(f"{log_prefix} : {LogCode.ERROR} {exc.code()}:{exc.details()}")
                match exc.code() :
                    case StatusCode.NOT_FOUND | StatusCode.UNIMPLEMENTED  :
                        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                            detail=exc.details())
                    case StatusCode.UNAVAILABLE :
                        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                                            detail=exc.details())
                    case StatusCode.ALREADY_EXISTS :
                        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                            detail=exc.details())
                    case StatusCode.INVALID_ARGUMENT | StatusCode.ABORTED |\
                          StatusCode.CANCELLED | StatusCode.RESOURCE_EXHAUSTED :
                        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                            detail=exc.details())
                    case StatusCode.UNAUTHENTICATED :
                        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                            detail=exc.details())
                    case StatusCode.PERMISSION_DENIED :
                        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                            detail=exc.details())
                    case _ :
                        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                            detail=exc.details())
            except HTTPException as exc :
                logger.error(f"{log_prefix} : {LogCode.ERROR} {type(exc)}:{exc}")
                raise exc
            except BaseException as exc :
                logger.exception(f"{log_prefix} : {LogCode.ERROR} : {type(exc)}:{exc}")
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail=f"Во время обработки REST запроса произошла непредвиденная ошибка : {type(exc)}:{exc}")
        return wrap
    #return LAE