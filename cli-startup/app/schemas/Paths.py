from pathlib import Path
from typing import Any
from config import yaml_folder as config_yaml_folder,\
                    sql_folder as config_sql_folder, ConfigPathKeywords, ConfigKeywords


class Paths() :
    """
        Класс с путями
    """

    def __init__(self, path_yaml_folder : Path | None = Path(config_yaml_folder),
                       path_sql_folder : Path | None = Path(config_sql_folder),
                       dates_path : Path | None = None, 
                       persons_path : Path | None = None,
                       places_path : Path | None = None, 
                       sources_path : Path | None = None,
                       others_path : Path | None = None,
                       events_path : Path | None = None,
                       biblios_path : Path | None = None,
                       bonds_path : Path | None = None,
                       main_sql_path : Path | None = None) :
        self.path_yaml_folder = path_yaml_folder
        self.path_sql_folder = path_sql_folder
        self.dates_path = dates_path
        self.persons_path = persons_path
        self.places_path = places_path
        self.sources_path = sources_path
        self.others_path = others_path
        self.events_path = events_path
        self.biblios_path = biblios_path
        self.bonds_path = bonds_path
        self.main_sql_path = main_sql_path



    def __getattribute__(self, __name: str) -> Any:

        # обобщить на property не получилось ((
        # выводит в рекурсию (

        def returnFilePath(str_path: str = "", path: Any = object.__getattribute__(self, __name), sql : bool = False) :
            if path:
                path = Path(path)
            if sql :
                return path if path else self.path_sql_folder.joinpath(str_path)
            return path if path else self.path_yaml_folder.joinpath(str_path)

        match __name :
            case ConfigPathKeywords.path_yaml_folder :
                return Path(object.__getattribute__(self, __name))
            case ConfigPathKeywords.path_sql_folder :
                return Path(object.__getattribute__(self, __name))
            case ConfigPathKeywords.dates_path :
                return returnFilePath(ConfigPathKeywords.dates_default_path)
            case ConfigPathKeywords.persons_path :
                return returnFilePath(ConfigPathKeywords.persons_default_path)
            case ConfigPathKeywords.places_path :
                return returnFilePath(ConfigPathKeywords.places_default_path)
            case ConfigPathKeywords.sources_path :
                return returnFilePath(ConfigPathKeywords.sources_default_path)
            case ConfigPathKeywords.others_path :
                return returnFilePath(ConfigPathKeywords.others_default_path)
            case ConfigPathKeywords.events_path :
                return returnFilePath(ConfigPathKeywords.events_default_path)
            case ConfigPathKeywords.biblios_path :
                return returnFilePath(ConfigPathKeywords.biblios_default_path)
            case ConfigPathKeywords.bonds_path :
                return returnFilePath(ConfigPathKeywords.bonds_default_path)
            case ConfigPathKeywords.main_sql_path :
                return returnFilePath(ConfigPathKeywords.main_sql_default_path, sql = True)
            case _ :
                return object.__getattribute__(self, __name)
    
    def __pathByKeywordDict(self) -> dict[str, Path]:
        return {
            ConfigKeywords.sources : self.sources_path,
            ConfigKeywords.source_fragments : self.sources_path,
            ConfigKeywords.dates : self.dates_path,
            ConfigKeywords.places : self.places_path,
            ConfigKeywords.persons : self.persons_path,
            ConfigKeywords.others : self.others_path,
            ConfigKeywords.events : self.events_path,
            ConfigKeywords.biblios : self.biblios_path,
            ConfigKeywords.biblio_fragments : self.biblios_path,
            ConfigKeywords.bonds : self.bonds_path
        }
    
    def pathByKeyword(self, keyword : str) -> Path :
        return self.__pathByKeywordDict().get(keyword, None)