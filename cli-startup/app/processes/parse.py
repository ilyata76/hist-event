"""
    Файл, отвечающий за работу с YAML-файлами и моделями.
"""
from loguru import logger
from pathlib import Path
import yaml

import pyparsing
import config

from schemas.Date import DateStorage, Date


def dictFromYaml(path : Path) :
    """
        Открыть файл .yaml по пути path, 
            вернуть результат в виде словаря
    """
    logger.info("Чтение {yaml} файла", yaml=path)
    buffer = None
    with open(path, "rb") as file : # encoding="utf-8"
        buffer = file.read()
    return yaml.load(buffer, Loader=yaml.FullLoader)


def patternTextInclusion() -> pyparsing.ParserElement :
    """
        Для поиска { таких : 1 } [ ИМЯ ] вставок шаблон
    """

    keyword = pyparsing.alphas
    number = pyparsing.nums
    name = pyparsing.alphanums + " _-/\\:" + pyparsing.ppu.Cyrillic.alphanums # TODO to config

    return pyparsing.Combine( pyparsing.Suppress("{") + pyparsing.ZeroOrMore(" ") + pyparsing.Word(keyword) #' { abo'
                                 + pyparsing.Suppress(pyparsing.ZeroOrMore(" ")) + ":" + pyparsing.Suppress(pyparsing.ZeroOrMore(" ")) #' : '
                                 + pyparsing.Word(number) + pyparsing.Suppress(pyparsing.ZeroOrMore(" ")) + pyparsing.Suppress("}") #'1 }'
                                 + pyparsing.Suppress(pyparsing.ZeroOrMore(" ")) # и имя 
                                 + "[" + pyparsing.ZeroOrMore(" ") + pyparsing.Word(name) #'[ NAME'
                                 + pyparsing.Suppress(pyparsing.ZeroOrMore(" ")) + pyparsing.Suppress("]") #' ]'
                                 )


def parseText(string : str, pattern : pyparsing.ParserElement) -> dict :
    """
        Возвращает список словарей - результата парсинга по паттерну
        Используется для парсинга текста события и регистрации их ID в моделях
    """
    logger.debug("Начало парсинга текста события")
    parse_list = pattern.searchString(string).as_list()
    result = []

    # ВОЗМОЖНО, нужно сразу здесь определять и конфигурировать модели
    for x in parse_list :
        stroke = x[0]
        result.append(
            {
                config.ParseResult.keyword : stroke.split(':')[0].strip(),
                config.ParseResult.number : stroke.split(':')[1].strip().split('[')[0].strip(),
                config.ParseResult.name : stroke.split('[')[1].strip()
            }
        )
    logger.info("Парсинг строки события res={res}", res=result.__len__())
    return result


def parseDatesFile(path : Path) -> DateStorage | None:
    """
        Парсит файл с датами и создаёт список сущностей дат
    """
    try : 
        logger.info("Начало операции полного парсинга файла дат")
        dates = dictFromYaml(path)["dates"]
        date_storage = DateStorage()

        for date in dates :
            date_storage.append(Date(name=date.get("name", None),
                                     id=date.get("id", None),
                                     description=date.get("description", None) ))

        logger.info("Конец операции полного парсинга файла дат res={res}", res=date_storage.storage.__len__())
        return date_storage
    except Exception as exc :
        logger.error("ОШИБКА ВО ВРЕМЯ ПАРСИНГА ФАЙЛА ДАТ exc={exc}", exc=exc)
        return None



################### ГЛАВНЫЙ ПРОЦЕСС

def parse(path : Path, date_path : Path | None = None):
    """
        Главная функция. Возвращает набор классов, 
            из которых впоследствии будет собран SQL запрос
    """
    try : 
        logger.info("Начало операции ОБЩЕГО парсинга")
        s = "sadgklsad l фывлджа ыфваждл ыфвадлыва {date: 1123   }[ zh-аб об /\\аб  ]  {person :2123} [ии:и]"

        x = parseText(s, patternTextInclusion())
        

        y = parseDatesFile(date_path)
        print(y)
        y.registerEvent(1, 2)
        y.registerEvent(1, 2)
        y.registerEvent(1, 2)
        y.registerEvent(3, 2)
        print(y)

        logger.info("Конец операции ОБЩЕГО парсинга")
        return 1
    except Exception as exc :
        logger.error("ОШИБКА ВО ВРЕМЯ ОБЩЕГО ПАРСИНГА exc={exc}", exc=exc)
        return None
