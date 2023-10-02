"""
    Валидация полей на правильность их заполнения
"""
from pathlib import Path
from ftplib import FTP
from loguru import logger
from config import ConfigKeywords
from core.processes.utils import dictFromYaml
from core.schemas.Paths import Paths


errors = []


def memorizeError(message : str) -> None :
    """
        Замыкается на errors
    """
    global errors
    errors.append(message)


def tryToOpen(path : Path, 
              keyword : str, 
              ftp : FTP = FTP()) -> list[dict] | None:
    """
        Попытка открыть файл
    """
    try : 
        logger.debug(f"Открытие файла {path}")
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
    logger.info("Процесс валидации: начало")

    global errors

    def openFile(keyword : str) :
        nonlocal paths, ftp
        return tryToOpen(paths.pathByKeyword(keyword), keyword, ftp)

    try :
        ######## DATES 

        logger.info("Начинается валидация полей файла DATES")
        if dates := openFile(ConfigKeywords.dates) :
            pass
        logger.info("Закончена валидация полей файла DATES")

        ######## SOURCES AND FRAGMENTS

        logger.info("Начинается валидация полей файла SOURCES")
        if sources := openFile(ConfigKeywords.sources) :
            pass
        logger.info("Закончена валидация полей файла SOURCES")

        logger.info("Начинается валидация полей файла SOURCE_FRAGMENTS")
        if source_fragments := openFile(ConfigKeywords.source_fragments) :
            pass
        logger.info("Закончена валидация полей файла SOURCE_FRAGMENTS")

        ######## BIBLIOS AND FRAGMENTS

        logger.info("Начинается валидация полей файла BIBLIOS")
        if biblios := openFile(ConfigKeywords.biblios) :
            pass
        logger.info("Закончена валидация полей файла BIBLIOS")

        logger.info("Начинается валидация полей файла BIBLIO_FRAGMENTS")
        if biblio_fragments := openFile(ConfigKeywords.biblio_fragments) :
            pass
        logger.info("Закончена валидация полей файла BIBLIO_FRAGMENTS")

        ######## PLACES

        logger.info("Начинается валидация полей файла PLACES")
        if places := openFile(ConfigKeywords.places) :
            pass
        logger.info("Закончена валидация полей файла PLACES")

        ######## PERSONS

        logger.info("Начинается валидация полей файла PERSONS")
        if persons := openFile(ConfigKeywords.persons) :
            pass
        logger.info("Закончена валидация полей файла PERSONS")

        ######## OTHERS

        logger.info("Начинается валидация полей файла OTHERS")
        if others := openFile(ConfigKeywords.others) :
            pass
        logger.info("Закончена валидация полей файла OTHERS")

        ######## EVENTS

        logger.info("Начинается валидация полей файла EVENTS")
        if events := openFile(ConfigKeywords.events) :
            pass
        logger.info("Закончена валидация полей файла EVENTS")

        ######## BONDS

        logger.info("Начинается валидация полей файла BONDS")
        if bonds := openFile(ConfigKeywords.bonds) :
            pass
        logger.info("Закончена валидация полей файла BONDS")

        if errors.__len__() == 0 :
            logger.info("Процесс валидации: успешное завершение")
        else :
            logger.info("Процесс валидации: безуспешное завершение")

    except Exception as exc:
        logger.info(f"Безуспешный конец процесса валидации в силу ошибки во время исполнения [{exc}]", level="exception")
        memorizeError(f"Непредвиденная ошибка во время исполнения валидации {type(exc)} [{exc}]")

    finally:    
        return tuple(errors)