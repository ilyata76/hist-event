import sys
from loguru import logger
import config

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
            
        logger.add(config.logs_folder + "./cli-startup-debug.log", 
                   format="{time} {level} {message}", level="DEBUG", rotation="4 MB", compression="zip")

    else : 
        if config.use_console_debug : 
            logger.add(sys.stdout, level="INFO")

        logger.add(config.logs_folder + "./cli-startup.log", 
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


if __name__ == "__main__":
    main()