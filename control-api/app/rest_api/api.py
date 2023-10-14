"""
    REST API для интерфейсов
"""
from fastapi import FastAPI

from app.utils.logger import logger
from app.utils.config import config


api = FastAPI()


@api.on_event("startup")
def onStartup() :
    logger.info(f"Параметры запускаемого приложения: \n{config}")


from app.rest_api.ping import ping
api.include_router(router=ping)