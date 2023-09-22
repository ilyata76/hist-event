"""
    Главный файл, отвечающий за поведение CLI-приложения
"""
from pathlib import Path
from plumbum import cli
from loguru import logger
from ftplib import FTP
from io import BytesIO

from processes import parse, generateSQL, validate
from schemas import Storages, SourceStorage, DateStorage, PlaceStorage, PersonStorage,\
                    PersonStorage, OtherStorage, EventStorage, SourceFragmentStorage,\
                    BiblioStorage, BiblioFragmentStorage, BondStorage, Paths
from config import ConfigKeywords, max_reparse_count as config_max_reparse_count,\
                        ftp_host, ftp_port, ftp_password, ftp_username


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

    reparse_count = config_max_reparse_count

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
        ftp = FTP()

        try : 

            ####

            ftp.connect(ftp_host, ftp_port)
            ftp.login(ftp_username, ftp_password)

            ###

            self.log("Начинаем валидацию полей")
            errors = validate(self.paths, ftp)
            if errors and len(errors) > 0 :
                logger.error(f"Файлы не прошли валидацию на заполнение полей. errors={errors}")
                raise Exception(f"Файлы не прошли валидацию на заполнение полей. errors={errors}")

            ##################

            self.log("Начинаем парсинг")
            self.storages, self.bond_storage = parse(self.paths, self.storages, self.bond_storage, 
                                                     self.reparse_count, ftp)
            if not self.storages or not self.bond_storage :
                logger.error("Произошла ошибка при обработке входных файлов!")
                raise Exception("Произошла ошибка при обработке входных файлов!")
            
            ##################

            self.log("Начинаем генерацию SQL")
            string = generateSQL(self.storages, self.bond_storage)
            if not string :
                logger.error("Произошла ошибка при обработке данных и генерации SQL-запроса")
                raise Exception("Произошла ошибка при обработке данных и генерации SQL-запроса")
            
            byts = BytesIO(bytes(string, encoding="utf-8"))

            try :
                ftp.storbinary(f"STOR {self.paths.main_sql_path}", byts)
            except Exception :
                ftp.connect(ftp_host, ftp_port)
                ftp.login(ftp_username, ftp_password)
                ftp.storbinary(f"STOR {self.paths.main_sql_path}", byts)

            ##################

            self.log("Работа программы завершена корректно")

        except Exception as exc: 
            self.log("Работа программы завершена некорректно exc={exc}", exc=exc)
            logger.error("Программа завершила свою работу некорректно exc={exc}", exc=exc)
        finally :
            ftp.close()


    #########
    # ПУТИ ДО ПАПОК И ФАЙЛОВ БУДУТ УСТАНАВЛИВАТЬСЯ ДЛЯ FTP-ХРАНИЛИЩА
    #########

    @cli.switch("--yaml-folder", str)
    def setPathYamlFolder(self, path_yaml_folder : Path) :
        """
            Установить путь до папки с YAML файлами
        """
        self.paths.path_yaml_folder = path_yaml_folder
        self.log("Установлена папка для всех YAML файлов {path}", path=self.paths.path_yaml_folder)


    @cli.switch("--dates-file", str)
    def setPathDatesFile(self, dates_path : Path) :
        """
            Установить путь до YAML файла с датами
        """
        self.paths.dates_path = dates_path
        self.log("Установлена папка для YAML файла с датами {path}", path=self.paths.dates_path)


    @cli.switch("--persons-file", str)
    def setPathPersonsFile(self, persons_path : Path) :
        """
            Установить путь до YAML файла с персоналиями
        """
        self.paths.persons_path = persons_path
        self.log("Установлена папка для YAML файла с персоналиями {path}", path=self.paths.persons_path)


    @cli.switch("--places-file", str)
    def setPathPlacesFile(self, places_path : Path) :
        """
            Установить путь до YAML файла с местами
        """
        self.paths.places_path = places_path
        self.log("Установлена папка для YAML файла с местами {path}", path=self.paths.places_path)


    @cli.switch("--sources-file", str)
    def setPathSourcesFile(self, sources_path : Path) :
        """
            Установить путь до YAML файла с ист. источниками
        """
        self.paths.sources_path = sources_path
        self.log("Установлена папка для YAML файла с ист. источниками {path}", path=self.paths.sources_path)


    @cli.switch("--others-file", str)
    def setPathOthersFile(self, others_path : Path) :
        """
            Установить путь до YAML файла с "другим"
        """
        self.paths.others_path = others_path
        self.log("Установлена папка для YAML файла с \"другим\" {path}", path=self.paths.others_path)


    @cli.switch("--events-file", str)
    def setPathEventsFile(self, events_path : Path) :
        """
            Установить путь до YAML файла с событиями
        """
        self.paths.events_path = events_path
        self.log("Установлена папка для YAML файла с событиями {path}", path=self.paths.events_path)


    @cli.switch("--biblios-file", str)
    def setPathBibliosFile(self, biblios_path : Path) :
        """
            Установить путь до YAML файла с библиографией
        """
        self.paths.biblios_path = biblios_path
        self.log("Установлена папка для YAML файла с библиографией {path}", path=self.paths.biblios_path)


    @cli.switch("--bonds-file", str)
    def setPathBondsFile(self, bonds_path : Path) :
        """
            Установить путь до YAML файла со связями событий
        """
        self.paths.bonds_path = bonds_path
        self.log("Установлена папка для YAML файла со связями событий  {path}", path=self.paths.bonds_path)


    @cli.switch("--sql-folder", str)
    def setPathSQLFolder(self, path_sql_folder : Path) :
        """
            Установить путь до папки с будущими SQL файлами
        """
        self.paths.path_sql_folder = path_sql_folder
        self.log("Установлена папка для всех SQL файлов {path}", path=self.paths.path_sql_folder)

    
    @cli.switch("--main-sql-file", str)
    def setMainSQLFile(self, main_sql_path : Path) :
        """
            Установить путь до SQL файла с главным выводом
        """
        self.paths.main_sql_path = main_sql_path
        self.log("Установлена папка для главного выходного SQL файла {path}", path=self.paths.main_sql_path)


    @cli.switch("--reparse", int)
    def setReparseCount(self, value : int) :
        """
            Установить максимальное количество обходов файлов
        """
        self.reparse_count = value
        self.log("Максимальное количество обходов - {value}", value=self.reparse_count)