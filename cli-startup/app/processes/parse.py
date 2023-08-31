"""
    Файл, отвечающий за работу с YAML-файлами и моделями.
"""
from loguru import logger
from pathlib import Path
import yaml

import pyparsing
import config

from schemas.Date import DateStorage, Date, DateConfig
from schemas.Person import PersonStorage, Person, PersonConfig
from schemas.Place import PlaceStorage, Place, PlaceConfig


def dictFromYaml(path : Path) -> dict | list[dict] | None:
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
    name = pyparsing.alphanums + " _-/\\:()" + pyparsing.ppu.Cyrillic.alphanums # TODO to config

    return pyparsing.Combine( pyparsing.Suppress("{") + pyparsing.ZeroOrMore(" ") + pyparsing.Word(keyword) #' { abo'
                                 + pyparsing.Suppress(pyparsing.ZeroOrMore(" ")) + ":" + pyparsing.Suppress(pyparsing.ZeroOrMore(" ")) #' : '
                                 + pyparsing.Word(number) + pyparsing.Suppress(pyparsing.ZeroOrMore(" ")) + pyparsing.Suppress("}") #'1 }'
                                 + pyparsing.Suppress(pyparsing.ZeroOrMore(" ")) # и имя 
                                 + "[" + pyparsing.ZeroOrMore(" ") + pyparsing.Word(name) #'[ NAME'
                                 + pyparsing.Suppress(pyparsing.ZeroOrMore(" ")) + pyparsing.Suppress("]") #' ]'
                                 )


def parseText(string : str, pattern : pyparsing.ParserElement) -> list[dict] :
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


############ РАБОТА С ХРАНИЛИЩАМИ


def parseDatesFile(path : Path) -> DateStorage | None:
    """
        Парсит файл с датами и создаёт список сущностей дат
    """
    try : 
        logger.info("Начало операции полного парсинга файла дат")
        dates = dictFromYaml(path)[config.YamlKeywords.dates]
        date_storage = DateStorage()

        if not dates :
            raise Exception("dates.yaml : error occured")
        if type(dates) is dict : 
            dates = [dates]

        for date in dates :
            date_storage.append(Date(name=date.get(DateConfig.name, None),
                                     id=date.get(DateConfig.id, None),
                                     description=date.get(DateConfig.description, None) ))

        logger.info("Конец операции полного парсинга файла дат res={res}", res=date_storage.storage.__len__())
        return date_storage
    except Exception as exc :
        logger.error("ОШИБКА ВО ВРЕМЯ ПАРСИНГА ФАЙЛА ДАТ exc={exc}", exc=exc)
        return None


def parsePlacesFile(path : Path, date_storage : DateStorage) -> PlaceStorage | None:
    """
        Парсит файл с местами и создаёт список сущностей местами.
        Проверяет существование дат, регистрирует их у местами
            в соответствующее поле.
    """
    try : 
        logger.info("Начало операции полного парсинга файла мест")
        places = dictFromYaml(path)[config.YamlKeywords.places]

        if not places :
            raise Exception("places.yaml : error occured")
        if type(places) is dict : 
            places = [places]

        place_storage = PlaceStorage()

        for place in places :
            
            name = place.get(PlaceConfig.name, None)
            id = place.get(PlaceConfig.id, None)
            description = place.get(PlaceConfig.description, None)
            
            if not place_storage.append(Place(name=name,
                                       id=id,
                                       description=description)) :
                raise Exception("Ошибка с добавлением нового места!")
            
            if description :
                entities : list[dict] = parseText(description, patternTextInclusion())
                
                for entity in entities :

                    if entity[config.ParseResult.keyword] == config.ParseKeywords.date :
                        if not date_storage.get(int(entity[config.ParseResult.number])) :
                            raise Exception(f"Даты {entity[config.ParseResult.number]} не существует!")
                        if not place_storage.registerDate(id, int(entity[config.ParseResult.number])) :
                            raise Exception("Ошибка с регистрацией даты для места!")



        logger.info("Конец операции полного парсинга файла мест res={res}", res=place_storage.storage.__len__())
        return place_storage
    
    except Exception as exc :
        logger.error("ОШИБКА ВО ВРЕМЯ ПАРСИНГА ФАЙЛА МЕСТО exc={exc}", exc=exc)
        return None


def parsePersonsFile(path : Path, date_storage : DateStorage,
                     place_storage : PlaceStorage) -> PersonStorage | None:
    """
        Парсит файл с персонами и создаёт список сущностей персон.
        Проверяет существование дат и мест, регистрирует их у персоны
            в соответствующее поле.
    """
    try : 
        logger.info("Начало операции полного парсинга файла персон")
        persons = dictFromYaml(path)[config.YamlKeywords.persons]

        if not persons :
            raise Exception("persons.yaml : error occured")
        if type(persons) is dict : 
            persons = [persons]

        person_storage = PersonStorage()

        for person in persons :

            name = person.get(PersonConfig.name, None)
            id = person.get(PersonConfig.id, None)
            description = person.get(PersonConfig.description, None)
            
            if not person_storage.append(Person(name=name,
                                                id=id,
                                                description=description)) :
                raise Exception("Ошибка с добавлением новой персоналии!")
            
            if description :
                entities : list[dict] = parseText(description, patternTextInclusion())
                
                for entity in entities :

                    if entity[config.ParseResult.keyword] == config.ParseKeywords.date :
                        if not date_storage.get(int(entity[config.ParseResult.number])) :
                            raise Exception(f"Даты {entity[config.ParseResult.number]} не существует!")
                        if not person_storage.registerDate(id, int(entity[config.ParseResult.number])) :
                            raise Exception(f"Ошибка с регистрацией даты для персоналии!")

                    elif entity[config.ParseResult.keyword] == config.ParseKeywords.place :
                        if not place_storage.get(int(entity[config.ParseResult.number])) :
                            raise Exception(f"Места {entity[config.ParseResult.number]} не существует!")
                        if not person_storage.registerPlace(id, int(entity[config.ParseResult.number])) :
                            raise Exception(f"Ошибка с регистрацией места для персоналии!")
                        
        logger.info("Конец операции полного парсинга файла персон res={res}", res=person_storage.storage.__len__())
        return person_storage
    
    except Exception as exc :
        logger.error("ОШИБКА ВО ВРЕМЯ ПАРСИНГА ФАЙЛА ПЕРСОН exc={exc}", exc=exc)
        return None



################### ГЛАВНЫЙ ПРОЦЕСС

def parse(path : Path, date_path : Path | None = None, persons_path : Path | None = None,
          place_path : Path | None = None):
    """
        Главная функция. Возвращает набор классов, 
            из которых впоследствии будет собран SQL запрос
    """
    try : 
        logger.info("Начало операции ОБЩЕГО парсинга")
        s = "sadgklsad l фывлджа ыфваждл ыфвадлыва {date: 1123   }[ zh-аб об /\\аб  ]  {person :2123} [ии:и]"

        x = parseText(s, patternTextInclusion())
        
        y = parseDatesFile(date_path)
        z = parsePlacesFile(place_path, date_storage=y)
        c = parsePersonsFile(persons_path, date_storage=y, place_storage=z)
        print(y,'\n\n\n',z,'\n\n\n',c)

        logger.info("Конец операции ОБЩЕГО парсинга")
        return 1
    except Exception as exc :
        logger.error("ОШИБКА ВО ВРЕМЯ ОБЩЕГО ПАРСИНГА exc={exc}", exc=exc)
        return None
