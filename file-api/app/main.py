"""
    Точка входа
"""
import asyncio

from config import config
from logger import logger
from grpc_server import FileAPIgRPCServer


async def serve() -> None :
    server = FileAPIgRPCServer(config.GRPC_HOST, config.GRPC_PORT)
    await server.serve()


if __name__ == "__main__" :
    logger.info(f"Запуск {config}")

    try : 
        asyncio.run(serve())
    except BaseException as exc :
        logger.critical(f"Произошла непредвиденная ошибка при работе приложения : {type(exc)}:{exc}")
        logger.exception(f"Произошла непредвиденная ошибка при работе приложения : {type(exc)}:{exc}")