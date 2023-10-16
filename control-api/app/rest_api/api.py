"""
    REST API для интерфейсов
"""
import time
from fastapi import FastAPI, Request

from app.utils.logger import logger
from app.utils.config import config, LogCode


api = FastAPI()


@api.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@api.middleware("http")
async def add_logging(request: Request, call_next):
    prefix = f"[MIDDLEWARE][{request.client.host}:{request.client.port}] : {request.method} {request.url}"
    logger.debug(f"{prefix} : {LogCode.PENDING}")
    response = await call_next(request)
    status = LogCode.ERROR if response.status_code // 100 != 2 else LogCode.SUCCESS
    logger.info(f"{prefix} : {status} {response.status_code}")
    return response


@api.on_event("startup")
def onStartup() :
    logger.info(f"ЗАПУСК ПРИ {config}")


from app.rest_api.ping import ping
api.include_router(router=ping)


from app.rest_api.file_ftp import file_ftp
api.include_router(router=file_ftp)