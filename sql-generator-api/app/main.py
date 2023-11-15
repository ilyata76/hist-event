"""
    Точка входа
"""
import asyncio

from config import config
from logger import logger

from grpc_server import SQLGeneratorAPIgRPCServer


async def serve() -> None:
    server = SQLGeneratorAPIgRPCServer(config.GRPC_HOST, config.GRPC_PORT)
    await server.serve()


if __name__ == "__main__":
    logger.info(f"ЗАПУС {config}")
    
    try :
        asyncio.run(serve())
    except BaseException as exc :
        logger.exception(f"Произошла непредвиденная ошибка при работе приложения : {type(exc)}:{exc}")