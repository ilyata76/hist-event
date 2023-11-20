from .config import *
from .Keywords import *


NOSQL_IP = f"{config.NOSQL_DATABASE_GRPC_HOST}:{config.NOSQL_DATABASE_GRPC_PORT}"
FILE_IP = f"{config.FILE_API_GRPC_HOST}:{config.FILE_API_GRPC_PORT}"
SQL_PATH = lambda filename_without_extention : f"sql/{filename_without_extention}.sql/"