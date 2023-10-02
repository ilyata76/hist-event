from config import ftp_host, ftp_port, configure_logger, logger
from ftp.server import MyFTPServer
from ftp.ftp_handler import MyFTPHandlerLoguru


if __name__ == "__main__" :
    try : 
        configure_logger()
        server = MyFTPServer(ftp_host, ftp_port, MyFTPHandlerLoguru)
        server.start()
    except Exception as exc :
        logger.exception(f"Во время работы сервера произошла ошибка [{type(exc)}:{exc}]")