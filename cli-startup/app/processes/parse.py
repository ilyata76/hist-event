"""
    Файл, отвечающий за работу с YAML-файлами и моделями.
"""
from pathlib import Path
import yaml

import pyparsing
import config


def dictFromYaml(path : Path) :
    """
        Открыть файл .yaml по пути path, 
            вернуть результат в виде словаря
    """
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
    """
    parse_list = pattern.searchString(string).as_list()
    result = []

    for x in parse_list :
        stroke = x[0]
        result.append(
            {
                config.ParseResult.keyword : stroke.split(':')[0].strip(),
                config.ParseResult.number : stroke.split(':')[1].strip().split('[')[0].strip(),
                config.ParseResult.name : stroke.split('[')[1].strip()
            }
        )
    
    return result



################### ГЛАВНЫЙ ПРОЦЕСС

def parse(path : Path) :
    """
        Главная функция. Возвращает набор классов, 
            из которых впоследствии будет собран SQL запрос
    """
    s = "sadgklsad l фывлджа ыфваждл ыфвадлыва {date: 1123   }[ zh-аб об /\\аб  ]  {person :2123} [ии:и]"

    x = parseText(s, patternTextInclusion())
    print(x)

    return dictFromYaml(path)["a"]["x"]
