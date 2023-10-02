"""
    Конфигурирующиеся и постоянные переменные
"""
import os, sys
from pathlib import Path
from loguru import logger


files_folder = str(os.environ.get("FILES_FOLDER", "./files"))

ftp_admin_username = str(os.environ.get("FTP_ADMIN_USERNAME", "admin"))
ftp_admin_password = str(os.environ.get("FTP_ADMIN_PASSWORD", "admin"))

ftp_host = str(os.environ.get("FTP_HOST", "0.0.0.0"))
ftp_port = int(os.environ.get("FTP_PORT", 21))

debug = os.environ.get("DEBUG_MODE", "false")
if debug.lower() == "false" or debug.lower() == "no" :
    debug = False
else :
    debug = True

use_log_console= os.environ.get("LOG_CONSOLE", "false")
if use_log_console.lower() == "false" or use_log_console.lower() == "no" :
    use_log_console = False
else :
    use_log_console = True

logs_folder = Path(str(os.environ.get("LOGS_FOLDER", "./logs")))
logs_filename = str(os.environ.get("LOGS_FILENAME", "ftp-io.log"))
logger_configured : bool = False


def configure_logger() : 
    """
    """
    global logger_configured
    if logger_configured :
        return
    
    logger.remove(0)
    logger.add(sys.stderr, level="WARNING")

    level = "DEBUG" if debug else "INFO"

    logger.add(logs_folder.joinpath(logs_filename), 
                   format="{time} {level} {message}", level=level, rotation="4 MB", compression="zip")
    
    if use_log_console :
        logger.add(sys.stdout, level=level)
    
    logger_configured = True

    logger.debug("Логгер был сконфигурирован")