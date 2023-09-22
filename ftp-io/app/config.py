"""
    Конфигурирующиеся и постоянные переменные
"""
import os

yaml_folder = str(os.environ.get("YAML_FOLDER", "./files/yamls"))

sql_folder = str(os.environ.get("SQL_FOLDER", "./files/sqls"))

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

use_console_debug = os.environ.get("DEBUG_CONSOLE", "false")
if use_console_debug.lower() == "false" or use_console_debug.lower() == "no" :
    use_console_debug = False
else :
    use_console_debug = True