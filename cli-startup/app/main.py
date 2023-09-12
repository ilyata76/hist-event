import sys
from loguru import logger
import config

#######################

def configure_logger() : 
    """

    """
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



def main() :
    configure_logger()
    
    from cli.cli import StartupCLI

    a = StartupCLI()
    a.run()


if __name__ == "__main__":
    main()