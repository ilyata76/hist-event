"""
    Точка входа
"""
import asyncio

from utils.config import config
from utils.logger import logger

from grpc_server.NoSQLDatabaseAPIgRPCServer import NoSQLDatabaseAPIgRPCServer


async def serve() -> None:
    server = NoSQLDatabaseAPIgRPCServer(config.GRPC_HOST, config.GRPC_PORT)
    await server.serve()


if __name__ == "__main__":
    logger.info(f"ЗАПУС {config}")
    
    try :
        asyncio.run(serve())
    except BaseException as exc :
        logger.exception(f"Произошла непредвиденная ошибка при работе приложения : {type(exc)}:{exc}")