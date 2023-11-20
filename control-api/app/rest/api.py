"""
    REST API для интерфейсов
"""
import time
from fastapi import FastAPI, Request

from app.logger import logger
from app.config import config


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
    logger.debug(f"{prefix}")
    response = await call_next(request)
    logger.info(f"{prefix} : {response.status_code}")
    return response


@api.on_event("startup")
def onStartup() :
    logger.info(f"ЗАПУСК ПРИ {config}")


from .ping import ping
api.include_router(router=ping)


from .file import file
api.include_router(router=file)


from .sql_generator import sql_generator
api.include_router(router=sql_generator)