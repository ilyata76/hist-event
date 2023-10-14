"""
    Ловит gRPC исключения, поднимает HTTPException
"""
from functools import wraps
from grpc import RpcError, StatusCode

from fastapi import HTTPException, status

from app.utils.logger import logger


def log_and_except(function) :
    """
        Декоратор ловит gRPC исключения, поднимает fastapi.httpexception,
            которые впоследствии будут обработаны FastAPI в коробке
    """
    @wraps(function)
    async def wrap(*args, **kwargs) :
        try : 
            return await function(*args, **kwargs)
        except RpcError as exc :
            logger.error(f"Во время обработки REST-запроса удалённый gRPC-сервер вернул ошибку : {exc.code()}:{exc.details()}")
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
        except BaseException as exc :
            logger.exception(f"Во время обработки REST запроса произошла непредвиденная ошибка : {type(exc)}:{exc}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Во время обработки REST запроса произошла непредвиденная ошибка : {type(exc)}:{exc}")
    return wrap