"""
    Главный файл, отвечающий за поведение CLI-приложения
"""
from pathlib import Path
from plumbum import cli
from loguru import logger

import config
from processes.parse import parse
from processes.generateSQL import generateSQL
from schemas.Storages import Storages, SourceStorage, DateStorage, PlaceStorage, PersonStorage,\
                                PersonStorage, OtherStorage, EventStorage, SourceFragmentStorage,\
                                BiblioStorage, BiblioFragmentStorage


class StartupCLI(cli.Application):
    """
        CLI-приложение. Задачи: парсить файлы, создавать скрипты SQL
    """



    ## Флаги

    verbose = cli.Flag(["v", "verbose"], 
                       help = "If given, I will be very talkative")
    

    storages = Storages(
        source_storage=SourceStorage(name=config.ConfigKeywords.sources), 
        source_fragment_storage=SourceFragmentStorage(name=config.ConfigKeywords.source_fragments),
        date_storage=DateStorage(config.ConfigKeywords.dates),
        place_storage=PlaceStorage(config.ConfigKeywords.places), 
        person_storage=PersonStorage(config.ConfigKeywords.persons),
        other_storage=OtherStorage(config.ConfigKeywords.others),
        event_storage=EventStorage(config.ConfigKeywords.events),
        biblio_storage=BiblioStorage(config.ConfigKeywords.biblios),
        biblio_fragment_storage=BiblioFragmentStorage(config.ConfigKeywords.biblio_fragments)
    )


    ## Для внутреннего пользования

    def log(self, message : str, *args, **kwargs) :
        """
            Функция пишет лог и пишет в консоль, если есть -v
        """
        logger.info(message, *args, **kwargs)
        if self.verbose:
            print(message.format(*args, **kwargs))



    ## Логика

    def main(self) :
        """
            Главный запуск = запуск всех операций
        """
        try :
            path_yaml_folder = Path(self.path_yaml_folder)
        except AttributeError:
            path_yaml_folder = Path(config.yaml_folder)

        try :
            path_sql_folder = Path(self.path_sql_folder)
        except AttributeError:
            path_sql_folder = Path(config.sql_folder)

        try : 
            self.log("Начинаем парсинг")
            self.storages = parse(path_yaml_folder, self.storages)
            if not self.storages :
                logger.error("Произошла ошибка при обработке входных файлов!")
                raise Exception("Произошла ошибка при обработке входных файлов!")
            #self.log("Теперь хранилища storages []->:\n\n{stor}\n\n", stor=self.storages)


            self.log("Начинаем генерацию SQL")
            string = generateSQL(self.storages)
            if not string :
                logger.error("Произошла ошибка при обработке данных и генерации SQL-запроса")
                raise Exception("Произошла ошибка при обработке данных и генерации SQL-запроса")
            
            with open(path_sql_folder.joinpath("main.sql"), "w", encoding="utf-8") as file :
                file.write(string)

            self.log("Работа программы завершена корректно")

        except Exception as exc: 
            self.log("Работа программы завершена некорректно exc={exc}", exc=exc)
            logger.error("Программа завершила свою работу некорректно exc={exc}", exc=exc)


    @cli.switch("--yaml-folder", str)
    def setPathYamlFolder(self, path_yaml_folder : Path) :
        """
            Установить путь до папки с YAML файлами
        """
        self.path_yaml_folder = path_yaml_folder
        self.log("Установлена папка для всех YAML файлов {path}", path=self.path_yaml_folder)


    @cli.switch("--sql-folder", str)
    def setPathSQLFolder(self, path_sql_folder : Path) :
        """
            Установить путь до папки с будущими SQL файлами
        """
        self.path_sql_folder = path_sql_folder
        self.log("Установлена папка для всех SQL файлов {path}", path=self.path_sql_folder)