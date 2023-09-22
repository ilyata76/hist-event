import sys
from loguru import logger
import config
from ftp.server import MyFTPServer

logger_configured : bool = False

def configure_logger() : 
    """

    """
    global logger_configured

    if logger_configured :
        return

    logger.remove(0)

    logger.add(sys.stderr, level="WARNING")

    if config.debug : 
        if config.use_console_debug : 
            logger.add(sys.stdout, level="DEBUG")
        logger.add("debug.log", format="{time} {level} {message}", level="DEBUG", rotation="4 MB", compression="zip")
    else : 
        if config.use_console_debug : 
            logger.add(sys.stdout, level="INFO")
        logger.add("log.log", format="{time} {level} {message}", level="INFO", rotation="4 MB", compression="zip")
    
    logger_configured = True


if __name__ == "__main__" :
    configure_logger()
    server = MyFTPServer(config.ftp_host, config.ftp_port)
    server.start()