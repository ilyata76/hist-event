"""
    Валидация полей на правильность их заполнения
"""
from pathlib import Path
from ftplib import FTP
from loguru import logger
from config import ConfigKeywords
from processes.utils import dictFromYaml
from schemas import Paths


errors = []


def memorizeError(message : str) -> None :
    """
        Замыкается на errors
    """
    global errors
    logger.error(message)
    errors.append(message)


def tryToOpen(path : Path, keyword : str, ftp : FTP = FTP()) -> list[dict] | None:
    """
        Попытка открыть файл
    """
    try : 
        res = dictFromYaml(path, ftp)[keyword]
        if type(res) == dict :
            res = [res]
        return res
    except Exception as exc :
        memorizeError(f"Ошибка во время открытия и чтения файла {keyword} по {path} {type(exc)}: exc={exc}")
        return None


def validate(paths : Paths, 
             ftp : FTP = FTP()) -> list:
    """
        Валидация правильности заполненности полей.
        Проверяет ТОЛЬКО правильность заполнения.
    """
    logger.info("Начало процесса валидации")

    global errors

    def openFile(keyword : str) :
        nonlocal paths, ftp
        return tryToOpen(paths.pathByKeyword(keyword), keyword, ftp)

    try :
        ######## DATES 

        if dates := openFile(ConfigKeywords.dates) :
            pass

        ######## SOURCES AND FRAGMENTS

        if sources := openFile(ConfigKeywords.sources) :
            pass

        if source_fragments := openFile(ConfigKeywords.source_fragments) :
            pass

        ######## BIBLIOS AND FRAGMENTS
    
        if biblios := openFile(ConfigKeywords.biblios) :
            pass

        if biblio_fragments := openFile(ConfigKeywords.biblio_fragments) :
            pass

        ######## PLACES

        if places := openFile(ConfigKeywords.places) :
            pass

        ######## PERSONS

        if persons := openFile(ConfigKeywords.persons) :
            pass

        ######## OTHERS

        if others := openFile(ConfigKeywords.others) :
            pass

        ######## EVENTS

        if events := openFile(ConfigKeywords.events) :
            pass

        ######## BONDS

        if bonds := openFile(ConfigKeywords.bonds) :
            pass

        logger.info("УСПЕШНЫЙ конец процесса валидации")

    except Exception as exc:
        logger.info("БЕЗУСПЕШНЫЙ конец процесса валидации")
        memorizeError(f"Непредвиденная ошибка во время исполнения валидации {type(exc)}: exc={exc}")

    finally:    
        return errors