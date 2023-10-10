"""
    Точка входа
"""
import asyncio

from utils.config import config
from utils.logger import logger
from grpc_server.FileAPIgRPCServer import FileAPIgRPCServer


async def serve() -> None :
    server = FileAPIgRPCServer(config.GRPC_HOST, config.GRPC_PORT)
    await server.serve()


if __name__ == "__main__":
    logger.info(f"Параметры запускаемого приложения: \n{config}")

    try : 
        asyncio.run(serve())
    except BaseException as exc :
        logger.exception(f"Произошла непредвиденная ошибка при работе приложения : {type(exc)}:{exc}")