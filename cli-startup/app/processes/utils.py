from pathlib import Path
import yaml
import pyparsing
from loguru import logger


def dictFromYaml(path : Path) -> dict | list[dict] | None:
    """
        Открыть файл .yaml по пути path, 
            вернуть результат в виде словаря
    """
    try : 
        logger.info("Чтение {yaml} файла", yaml=path)
        buffer = None
        with open(path, "rb") as file : # encoding="utf-8"
            buffer = file.read()
        return yaml.load(buffer, Loader=yaml.FullLoader)
    except :
        raise Exception(f"Нет такого файла {path}")


def patternTextInclusion() -> pyparsing.ParserElement :
    """
        Для поиска { таких : 1 } [ ИМЯ ] вставок шаблон
    """

    keyword = pyparsing.alphas + "_"
    number = pyparsing.nums
    name = pyparsing.alphanums + " _-/\\:()?!" + pyparsing.ppu.Cyrillic.alphanums # TODO to config

    return pyparsing.Combine( pyparsing.Suppress("{") + pyparsing.ZeroOrMore(" ") + pyparsing.Word(keyword) #' { abo'
                                 + pyparsing.Suppress(pyparsing.ZeroOrMore(" ")) + ":" + pyparsing.Suppress(pyparsing.ZeroOrMore(" ")) #' : '
                                 + pyparsing.Word(number) + pyparsing.Suppress(pyparsing.ZeroOrMore(" ")) + pyparsing.Suppress("}") #'1 }'
                                 + pyparsing.Suppress(pyparsing.ZeroOrMore(" ")) # и имя 
                                 + "[" + pyparsing.ZeroOrMore(" ") + pyparsing.Word(name) #'[ NAME'
                                 + pyparsing.Suppress(pyparsing.ZeroOrMore(" ")) + pyparsing.Suppress("]") #' ]'
                            )


def nullOrValue(value) -> str:
    """
        Функция для создания SQL-параметров при генерации таблиц
    """
    return "null" if not value else str(f"'{value}'")


def NOV(value) -> str :
    """
        Экономия места!
    """
    return nullOrValue(value)