"""
    Главный файл, отвечающий за поведение CLI-приложения
"""
from pathlib import Path
from plumbum import cli
from loguru import logger
from ftplib import FTP, error_perm
from io import BytesIO

from core.processes.parse import parse
from core.processes.generateSQL import generateSQL 
from core.processes.validate import validate
from core.processes.utils import msgFormat
from core.schemas.Storages import Storages
from core.schemas.Bonds import BondStorage
from core.schemas.Paths import Paths
from config import ConfigKeywords, max_reparse_count as config_max_reparse_count,\
                        ftp_host, ftp_port, ftp_password, ftp_username, ConfigCLICommands


class StartupCLI(cli.Application):
    """
        CLI-приложение. Задачи: парсить файлы, создавать скрипты SQL
    """

    VERSION = "0.1.0"

    ## Флаги
    
    no_validate = cli.Flag(["no-validate"],
                           help = "Не проводить валидацию в главном процессе")

    no_parse = cli.Flag(["no-parse"],
                        help = "Не проводить парсинг в главном процессе")

    ##

    storages : Storages | None = None
    bond_storage : BondStorage | None = None
    ftp : FTP | None = None
    errors : list | None = None
    sql_string : str | None = None

    reparse_count = config_max_reparse_count
    paths = Paths()

    ## Для внутреннего пользования

    def log(self, message : str, level = "info", *args, **kwargs) -> None:
        """
            Функция пишет лог и пишет в консоль, 
                также сохраняет в stdout на FTP
        """
        try : 
            print(message.format(*args, **kwargs))
            getattr(logger, level)(message, *args, **kwargs)
        except Exception as exc :
            logger.exception(f"Выполнение команды логирования завершилось с ошибкой! Последнее сообщение=[{message}] Ошибка=[{exc}]")
            print(msgFormat(f"Работа программы завершена некорректно! Последнее сообщение=[{message}] Ошибка=[{exc}]"))


    def validate(self) :
        """
            Запустить функцию валидации вводимых файлов
                и их полей.
        """
        try : 
            self.errors = validate(self.paths, self.ftp)
            if self.errors and len(self.errors) > 0 :
                raise Exception(f"Некоторые файлы не прошли валидацию! [{self.errors}]")
        except Exception as exc :
            raise Exception(f"Процесс валидации завершился с ошибкой! [{exc}]")
        # finally :
        #     return self.errors


    def parse(self) :
        """
            Запустить фунцию
        """
        try : 
            self.storages = Storages()
            self.bond_storage = BondStorage(ConfigKeywords.bonds)
            self.storages, self.bond_storage = parse(self.paths, self.storages, self.bond_storage, 
                                                    self.reparse_count, self.ftp)
            if not self.storages :
                raise Exception("Файлы основных сущностей не прошли проверку при парсинге!")
            if not self.bond_storage :
                raise Exception("Файлы связей, bonds, не прошли проверку при парсинге!")
        except Exception as exc :
            raise Exception(f"Процесс парсинга завершился с ошибкой! [{exc}]")
        # finally :
        #     return self.storages, self.bond_storage


    def generate(self) :
        """
            Запустить функцию генерации SQL-запроса
        """
        try : 
            if not self.storages or not self.bond_storage :
                raise Exception("Для генерации нужны заполненные Storages!")
            self.sql_string = generateSQL(self.storages, self.bond_storage)
            if not self.sql_string :
                raise Exception("Файл SQL не может быть сгенерирован!")
            try : 
                byts = BytesIO(bytes(self.sql_string, encoding="utf-8"))
                try :
                    self.ftp.storbinary(f"STOR {self.paths.main_sql_path}", byts)
                except error_perm as exc :
                    if exc.args[0] == "550 No such file or directory." :
                        self.ftp.mkd(self.paths.path_sql_folder.__str__())
                    self.ftp.connect(ftp_host, ftp_port)
                    self.ftp.login(ftp_username, ftp_password)
                    self.ftp.storbinary(f"STOR {self.paths.main_sql_path}", byts)
            except Exception as exc :
                raise Exception(f"Ошибка с отправкой sql-файла на FTP-сервер! [{exc}]")
        except Exception as exc :
            raise Exception(f"Процесс генерации завершился с ошибкой! [{exc}]")
        # finally :
        #     return self.sql_string

    ## Логика

    def main(self, proccess : str = ConfigCLICommands.full) -> int :
        """
            Главный запуск = запуск всех операций, 
                если нет флагов
        """
        try : 
            if not (proccess in [ConfigCLICommands.full, 
                                 ConfigCLICommands.validate, 
                                 ConfigCLICommands.parse]) :
                raise Exception(f"Неверная команда, {proccess}")

            try : 
                self.ftp = FTP()
                self.ftp.connect(ftp_host, ftp_port)
                self.ftp.login(ftp_username, ftp_password)
                self.log("Успешное подключение к FTP-серверу!")
            except Exception as exc:
                raise Exception(f"Не удалось подключиться к FTP-серверу [{exc}]")

            if proccess in [ConfigCLICommands.full, ConfigCLICommands.validate]\
             and not self.no_validate :
                self.log("Выполнение функции валидации YAML-файлов...")
                self.validate()
            if proccess in [ConfigCLICommands.full, ConfigCLICommands.parse]\
             and not self.no_parse :
                self.log("Выполнение функции парсинга YAML-файлов и сохранения их в Storages...")
                self.parse()
            if proccess in [ConfigCLICommands.full] :
                self.log("Выполнение функции генерации SQL-запроса...")
                self.generate()

            self.log("Работа программы завершена корректно")
            return 0

        except Exception as exc: 
            self.log(f"Работа программы завершена некорректно! [{exc}]", "exception")
            return 1

        finally :
            if self.ftp : 
                self.ftp.close()


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