import sys
from loguru import logger
import config
from cli.cli import StartupCLI

#######################

logger.remove(0)

logger.add(sys.stderr, level="WARNING")

if config.debug : 
    #logger.add(sys.stdout, level="DEBUG")
    logger.add("debug.log", format="{time} {level} {message}", level="DEBUG", rotation="4 MB", compression="zip")
else : 
    #logger.add(sys.stdout, level="INFO")
    logger.add("log.log", format="{time} {level} {message}", level="INFO", rotation="4 MB", compression="zip")

#######################


def main() :
    a = StartupCLI()
    a.run()


if __name__ == "__main__":
    main()