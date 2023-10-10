"""
    Файл с описанием хендлеров для MyFTPServer.
    MyFTPHandlerLoguru делает логирование запросов
"""
from pyftpdlib.handlers import FTPHandler

from utils.logger import logger


class MyFTPHandler(FTPHandler) :

    @property
    def prefix(self) :
        return f"[FTP][{self.remote_ip}:{self.remote_port}][{self.username}]"


class MyFTPHandlerLoguru(MyFTPHandler) :
    """
        Хендлер сохраняет логи через loguru
    """

    def on_connect(self):
        logger.info(f"{self.prefix} Подключен клиент")
        return super().on_connect()

    def on_disconnect(self):
        logger.info(f"{self.prefix} Клиент отключен")
        return super().on_disconnect()

    def on_login(self, username):
        logger.info(f"{self.prefix} Пользователь {username} авторизован")
        return super().on_login(username)

    def on_login_failed(self, username):
        logger.info(f"{self.prefix} Пользователь {username} не может быть авторизован")
        return super().on_login_failed(username)

    def on_logout(self, username):
        logger.info(f"{self.prefix} Пользователь {username} деавторизован")
        return super().on_logout(username)

    def on_file_sent(self, file):
        logger.info(f"{self.prefix} Отправлен файл {file}")
        return super().on_file_sent(file)

    def on_file_received(self, file):
        logger.info(f"{self.prefix} Получен файл {file}")
        return super().on_file_received(file)

    def on_incomplete_file_sent(self, file):
        logger.info(f"{self.prefix} Файл {file} не может быть отправлен")
        return super().on_incomplete_file_sent(file)

    def on_incomplete_file_received(self, file):
        logger.info(f"{self.prefix} Файл {file} не может быть получен")
        return super().on_incomplete_file_received(file)