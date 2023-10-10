from utils.logger import logger
from utils.config import config
from ftp.server import MyFTPServer
from ftp.ftp_handler import MyFTPHandlerLoguru


def serve() -> None :
    server = MyFTPServer(config.FTP_HOST, config.FTP_PORT, MyFTPHandlerLoguru)
    server.start()


if __name__ == "__main__" :
    logger.info(f"Параметры запускаемого приложения: \n{config}")

    try : 
        serve()
    except Exception as exc :
        logger.exception(f"Во время работы сервера произошла ошибка [{type(exc)}:{exc}]")