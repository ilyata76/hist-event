import sys
from loguru import logger
import config
from fastapi import FastAPI

#######################

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
            
        logger.add(config.logs_folder.joinpath("sql-generator-debug.log"), 
                   format="{time} {level} {message}", level="DEBUG", rotation="4 MB", compression="zip")

    else : 
        if config.use_console_debug : 
            logger.add(sys.stdout, level="INFO")

        logger.add(config.logs_folder.joinpath("/sql-generator.log"), 
                   format="{time} {level} {message}", level="INFO", rotation="4 MB", compression="zip")
    
    logger_configured = True


def main() :
    """
        ЗАпуск CLI
    """
    configure_logger()
    from cli.cli import StartupCLI
    a = StartupCLI()
    a.run()

#######################

api = FastAPI()

@api.get("/")
def getRoot() :
    return "Hello!"


if __name__ == "__main__":
    # from os import system
    # print(system("sql-generate -v"))
    pass