"""
    Точка входа
"""
from logger import logger
from config import config
from ftp import MyFTPServer, MyFTPHandlerLoguru


def serve() -> None :
    server = MyFTPServer(config.FTP_HOST, config.FTP_PORT, MyFTPHandlerLoguru)
    server.start()


if __name__ == "__main__" :
    logger.info(f"Запуск {config}")

    try : 
        serve()
    except Exception as exc :
        logger.critical(f"Во время работы сервера произошла ошибка : {type(exc)}:{exc}")
        logger.exception(f"Во время работы сервера произошла ошибка : {type(exc)}:{exc}")