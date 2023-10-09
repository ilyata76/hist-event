"""
    Точка входа
"""
import asyncio

from utils.config import config
from utils.logger import logger
from database.DBClient import MongoDBClient
from database.FileDB import FileMongoDB, FileDB
from schemas.File import File


async def abboa(y : FileDB) :
    # for x in range(0, 100) :
    #     await y.append(File(filename=f"aboba{x}", path=f"./aboba{x}"))
    for x in (await y.getMany(51, 100)) :
        print(x)


if __name__ == "__main__":
    # logger.info(f"Параметры запускаемого приложения: \n{config}")
    
    # x = MongoDBClient()
    # y = FileMongoDB(x)

    # with asyncio.Runner() as runner:
    #     runner.run(abboa(y))

    from grpc_server.NoSQLDatabaseAPIgRPCServer import NoSQLDatabaseAPIgRPCServer

    try : 
        server = NoSQLDatabaseAPIgRPCServer("[::]","50051")
        server.serve()
    except NotImplementedError as exc : # Keyboard
        print("AAA")
        print(type(exc), exc)