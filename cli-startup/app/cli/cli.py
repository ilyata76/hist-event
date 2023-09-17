"""
    Главный файл, отвечающий за поведение CLI-приложения
"""
from pathlib import Path
from plumbum import cli
from loguru import logger

from processes import parse, generateSQL, validate
from schemas import Storages, SourceStorage, DateStorage, PlaceStorage, PersonStorage,\
                    PersonStorage, OtherStorage, EventStorage, SourceFragmentStorage,\
                    BiblioStorage, BiblioFragmentStorage, BondStorage, Paths
from config import ConfigKeywords

class StartupCLI(cli.Application):
    """
        CLI-приложение. Задачи: парсить файлы, создавать скрипты SQL
    """

    ## Флаги

    verbose = cli.Flag(["v", "verbose"], 
                       help = "If given, I will be very talkative")
    
    ##

    storages = Storages(
        source_storage=SourceStorage(name=ConfigKeywords.sources), 
        source_fragment_storage=SourceFragmentStorage(name=ConfigKeywords.source_fragments),
        date_storage=DateStorage(ConfigKeywords.dates),
        place_storage=PlaceStorage(ConfigKeywords.places), 
        person_storage=PersonStorage(ConfigKeywords.persons),
        other_storage=OtherStorage(ConfigKeywords.others),
        event_storage=EventStorage(ConfigKeywords.events),
        biblio_storage=BiblioStorage(ConfigKeywords.biblios),
        biblio_fragment_storage=BiblioFragmentStorage(ConfigKeywords.biblio_fragments)
    )

    bond_storage = BondStorage(ConfigKeywords.bonds)

    paths = Paths()


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

            print(self.paths.dates_path)

            self.log("Начинаем валидацию полей")
            errors = validate(self.paths)
            if errors and len(errors) > 0 :
                logger.error(f"Файлы не прошли валидацию на заполнение полей. errors={errors}")
                raise Exception(f"Файлы не прошли валидацию на заполнение полей. errors={errors}")

            ##################

            self.log("Начинаем парсинг")
            self.storages, self.bond_storage = parse(self.paths, self.storages, self.bond_storage)
            if not self.storages or not self.bond_storage :
                logger.error("Произошла ошибка при обработке входных файлов!")
                raise Exception("Произошла ошибка при обработке входных файлов!")
            
            ##################

            self.log("Начинаем генерацию SQL")
            string = generateSQL(self.storages, self.bond_storage)
            if not string :
                logger.error("Произошла ошибка при обработке данных и генерации SQL-запроса")
                raise Exception("Произошла ошибка при обработке данных и генерации SQL-запроса")
            
            with open(self.paths.main_sql_path, "w", encoding="utf-8") as file :
                file.write(string)

            ##################

            self.log("Работа программы завершена корректно")

        except Exception as exc: 
            self.log("Работа программы завершена некорректно exc={exc}", exc=exc)
            logger.error("Программа завершила свою работу некорректно exc={exc}", exc=exc)


    @cli.switch("--yaml-folder", str)
    def setPathYamlFolder(self, path_yaml_folder : Path) :
        """
            Установить путь до папки с YAML файлами
        """
        self.paths.path_yaml_folder = path_yaml_folder
        self.log("Установлена папка для всех YAML файлов {path}", path=self.paths.path_yaml_folder)


    @cli.switch("--sql-folder", str)
    def setPathSQLFolder(self, path_sql_folder : Path) :
        """
            Установить путь до папки с будущими SQL файлами
        """
        self.paths.path_sql_folder = path_sql_folder
        self.log("Установлена папка для всех SQL файлов {path}", path=self.paths.path_sql_folder)

    
    @cli.switch("--main-sql-file", str)
    def setMainSQLFile(self, main_sql_file : Path) :
        """
            Установить путь до главного SQL файла
        """
        self.paths.main_sql_path = main_sql_file
        self.log("Установлена папка для главного выходного SQL файла {path}", path=self.paths.main_sql_path)