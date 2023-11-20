from .config import *
from .Keywords import StorageCollection,\
                      StorageIdentifier


FILE_KEY = "file"
DATABASE_PATH_PATH = f"{FILE_KEY}.path" # для пути {file: {path: }}
DATABASE_IP = f"{config.DATABASE_HOST}:{config.DATABASE_PORT}"