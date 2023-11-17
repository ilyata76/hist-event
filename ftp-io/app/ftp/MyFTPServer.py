"""
    Файл с классом управления сервером
"""
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

from logger import logger
from config import config


class MyFTPServer() :
    """
        Класс для управления FTP сервером

        Права от библиотеки:
            "e" = change directory (CWD, CDUP commands)
            "l" = list files (LIST, NLST, STAT, MLSD, MLST, SIZE commands)
            "r" = retrieve file from the server (RETR command)

            "a" = append data to an existing file (APPE command)
            "d" = delete file or directory (DELE, RMD commands)
            "f" = rename file or directory (RNFR, RNTO commands)
            "m" = create directory (MKD command)
            "w" = store a file to the server (STOR, STOU commands)
            "M" = change file mode / permission (SITE CHMOD command) New in 0.7.0
            "T" = change file modification time (SITE MFMT command) New in 1.5.3
    """

    def __init__(self, host : str, port : int, 
                 handler : FTPHandler) :
        logger.debug(f"Создание экземпляра класса MyFTPServer с {host}:{port}")
        self.host = host
        self.port = port
        self._authorizer = DummyAuthorizer()
        self._authorizer.add_user(config.FTP_USERNAME, config.FTP_PASSWORD, 
                                  str(config.FILES_FOLDER), perm="elradfmwMT")
        self._authorizer.add_anonymous(str(config.FILES_FOLDER))
        self._handler = handler
        self._handler.authorizer = self._authorizer


    def start(self) :
        logger.info(f"Старт сервера на {self.host}:{self.port}")
        server = FTPServer((self.host, self.port), self._handler)
        server.serve_forever(handle_exit=True, worker_processes=2, timeout=10)
        logger.info("Остановка сервера")