"""
    Валидация полей на правильность их заполнения
"""
from pathlib import Path
from loguru import logger
from config import ConfigKeywords
from processes.utils import dictFromYaml
from schemas import Paths


def validate(paths : Paths) -> list:
    """
        Валидация правильности заполненности полей.
        Проверяет ТОЛЬКО правильность заполнения.
    """

    errors = []

    def memorizeError(message : str) -> None :
        """Замыкается на errors"""
        logger.error(message)
        errors.append(message)


    try :

        def tryToOpen(path : Path, keyword : str) -> dict | list[dict] | None:
            """
                Замыкается на memorizeError. errors.append
            """
            try : 
                return dictFromYaml(path)[keyword]
            except Exception as exc :
                memorizeError(f"Ошибка во время открытия и чтения файла {keyword} по {path} {type(exc)}: exc={exc}")
                return None


        ######## DATES 

        if dates := tryToOpen(paths.dates_path, ConfigKeywords.dates) :
            pass

        ######## SOURCES AND FRAGMENTS

        if sources := tryToOpen(paths.sources_path, ConfigKeywords.sources) :
            pass

        if source_fragments := tryToOpen(paths.sources_path, ConfigKeywords.source_fragments) :
            pass

        ######## BIBLIOS AND FRAGMENTS
    
        if biblios := tryToOpen(paths.biblios_path, ConfigKeywords.biblios) :
            pass

        if biblio_fragments := tryToOpen(paths.biblios_path, ConfigKeywords.biblio_fragments) :
            pass

        ######## PLACES

        if places := tryToOpen(paths.places_path, ConfigKeywords.places) :
            pass

        ######## PERSONS

        if persons := tryToOpen(paths.persons_path, ConfigKeywords.persons) :
            pass

        ######## OTHERS

        if others := tryToOpen(paths.others_path, ConfigKeywords.others) :
            pass

        ######## EVENTS

        if events := tryToOpen(paths.events_path, ConfigKeywords.events) :
            pass

        ######## BONDS

        if bonds := tryToOpen(paths.bonds_path, ConfigKeywords.bonds) :
            pass


    except Exception as exc:
        memorizeError(f"Непредвиденная ошибка во время исполнения валидации {type(exc)}: exc={exc}")


    finally:    
        return errors