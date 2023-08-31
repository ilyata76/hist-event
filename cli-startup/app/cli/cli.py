"""
    Главный файл, отвечающий за поведение CLI-приложения
"""
from pathlib import Path
from plumbum import cli
from loguru import logger

import config
from processes.parse import parse


class StartupCLI(cli.Application):
    """
        CLI-приложение. Задачи: парсить файлы, создавать скрипты SQL
    """



    ## Флаги

    verbose = cli.Flag(["v", "verbose"], 
                       help = "If given, I will be very talkative")
    


    ## Для внутреннего пользования

    def log(self, message : str, *args, **kwargs) :
        """
            Функция пишет лог и пишет в консоль, если есть -v
        """
        logger.info(message, *args, **kwargs)
        if self.verbose:
            print(message.format(*args, **kwargs))



    ## Логика

    def main(self):
        """
            Главный запуск = запуск всех операций
        """
        try :
            path_folder = Path(self.path_folder)
        except AttributeError:
            path_folder = Path(config.yaml_folder)


        print(parse(path_folder.joinpath("test.yaml")))

        self.log("A {x}", x=path_folder)


    @cli.switch("--path-folder", str)
    def setPathFolder(self, path_folder : Path) :
        """
            Установить путь до папки с файлами
        """
        self.path_folder = path_folder

        message = "Установлена папка для всех файлов {path}"

        logger.info(message, path=path_folder)
        if self.verbose :
            print(message.format(path=path_folder))