from pathlib import Path
from config import yaml_folder as config_yaml_folder,\
                    sql_folder as config_sql_folder


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
        self.__path_yaml_folder = path_yaml_folder
        self.__path_sql_folder = path_sql_folder
        self.__dates_path = dates_path
        self.__persons_path = persons_path
        self.__places_path = places_path
        self.__sources_path = sources_path
        self.__others_path = others_path
        self.__events_path = events_path
        self.__biblios_path = biblios_path
        self.__bonds_path = bonds_path
        self.__main_sql_path = main_sql_path


    def __returnPath(self, path: Path, str_path: str, sql : bool = False) :
        if sql :
            return path if path else self.__path_sql_folder.joinpath(str_path)
        return path if path else self.__path_yaml_folder.joinpath(str_path)


    @property
    def path_yaml_folder(self):
        return self.__path_yaml_folder
    
    @property 
    def path_sql_folder(self) :
        return self.__path_sql_folder

    @property
    def dates_path(self) :
        return self.__returnPath(self.__dates_path, "dates.yaml")

    @property
    def persons_path(self) :
        return self.__returnPath(self.__persons_path, "persons.yaml")

    @property
    def places_path(self) :
        return self.__returnPath(self.__places_path, "places.yaml")

    @property
    def sources_path(self) :
        return self.__returnPath(self.__sources_path, "sources.yaml")

    @property
    def others_path(self) :
        return self.__returnPath(self.__others_path, "others.yaml")

    @property
    def events_path(self) :
        return self.__returnPath(self.__events_path, "events.yaml")

    @property
    def biblios_path(self) :
        return self.__returnPath(self.__biblios_path, "biblios.yaml")

    @property
    def bonds_path(self) :
        return self.__returnPath(self.__bonds_path, "bonds.yaml")
    
    @property
    def main_sql_path(self) :
        return self.__returnPath(self.__main_sql_path, "main.sql", sql=True)