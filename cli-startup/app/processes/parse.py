"""
    Файл, отвечающий за работу с YAML-файлами и моделями.
"""
from loguru import logger
from pathlib import Path
import yaml

import pyparsing
import config

from schemas.Entity import BaseStorage
from schemas.Date import DateStorage, Date
from schemas.Person import PersonStorage, Person
from schemas.Place import PlaceStorage, Place
from schemas.Source import SourceStorage, Source
from schemas.Other import OtherStorage, Other


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

    for x in parse_list :
        stroke = x[0]
        result.append( { config.ParseResult.keyword : stroke.split(':')[0].strip(),
                         config.ParseResult.number : stroke.split(':')[1].strip().split('[')[0].strip(),
                         config.ParseResult.name : stroke.split('[')[1].strip() } )
    logger.info("Парсинг строки события res={res}", res=result.__len__())
    return result


############ РАБОТА С ХРАНИЛИЩАМИ

def parseFile(path : Path, keyword : str,
              source_storage : SourceStorage,
              date_storage : DateStorage, 
              place_storage : PlaceStorage,
              person_storage : PersonStorage,
              other_storage : OtherStorage) :
    """
        Парсит файл, изменяет классы Storage во время прохода.
            Регистрирует одни сущности в хранилищах других, если те будут встречены.
            Сохраняет встречаемые для себя в хранилище.

        ВОЗВРАЩАЕТ
            - 0 если всё ок
            - 1 если произошла ошибка
            - 2 если некоторые сущности были ещё не добавлены
    """
    try :
        res_code = 0
        logger.info("Начало операции полного парсинга файла keyword={keyword} path={path}", 
                    path=path, keyword=keyword)
        
        # прочитаем YAML файл, возьмём часть от keyword
        dict_entities = dictFromYaml(path)[keyword]
        # переменная для определения текущего стора для текущей сущности от keyword
        current_storage = BaseStorage()

        if not dict_entities :
            raise Exception(f"{keyword} : {path} : возникла ошибка во время обхода файла (результат None)")
        if type(dict_entities) is dict : 
            # если результат - один словарь, а не много
            dict_entities = [dict_entities]

        for dict_entity in dict_entities :
            # получим по ключевым словам параметры нашей сущности, если те имеются
            name = dict_entity.get(config.ConfigKeywords.name, None)
            id = dict_entity.get(config.ConfigKeywords.id, None)
            description = dict_entity.get(config.ConfigKeywords.description, None)
            link = dict_entity.get(config.ConfigKeywords.link, None)
            author = dict_entity.get(config.ConfigKeywords.author, None)
            date = dict_entity.get(config.ConfigKeywords.date, None)
            person = dict_entity.get(config.ConfigKeywords.person, None)
            geo = dict_entity.get(config.ConfigKeywords.geo, None)
            meta = dict_entity.get(config.ConfigKeywords.meta, None)
            
            match keyword : # добавим в Storage в зависимости от типа читаемого файла

                case config.ConfigKeywords.sources :
                    current_storage = source_storage
                    if not current_storage.get(id) and\
                        not current_storage.append(Source(name=name,
                                                          id=id,
                                                          description=description,
                                                          link=link,
                                                          author=author) ) :
                        raise Exception("Непредвиденная ошибка с добавлением нового источника!")

                case config.ConfigKeywords.dates : 
                    # оставляем так без обобщения на .append(BaseEntity()) для удобства
                    # логов и дебага
                    current_storage = date_storage
                    if not current_storage.get(id) and\
                        not current_storage.append(Date(name=name,
                                                        id=id,
                                                        description=description,
                                                        date=date) ) :
                        raise Exception("Непредвиденная ошибка с добавлением новой даты!")

                case config.ConfigKeywords.places :
                    current_storage = place_storage
                    if not current_storage.get(id) and\
                        not current_storage.append(Place(name=name,
                                                         id=id,
                                                         description=description,
                                                         geo=geo)) :
                        raise Exception("Непредвиденная ошибка с добавлением нового места!")

                case config.ConfigKeywords.persons :
                    current_storage = person_storage
                    if not current_storage.get(id) and\
                        not current_storage.append(Person(name=name,
                                                          id=id,
                                                          description=description,
                                                          person=person)) :
                        raise Exception("Непредвиденная ошибка с добавлением новой персоналии!")

                case config.ConfigKeywords.others :
                    current_storage = other_storage
                    if not current_storage.get(id) and\
                        not current_storage.append(Other(name=name,
                                                         id=id,
                                                         description=description,
                                                         meta=meta)) :
                        raise Exception("Непредвиденная ошибка с добавлением нового 'другого'!")


            def saveAndRegisterEntitites(text, pattern : pyparsing.ParserElement) -> bool :
                """
                    Функция регистрирует и сохраняет сущности: одни при обходе, другие при 
                        определении, что появилась внешняя ссылка
                """
                try :
                    nonlocal res_code
                    register_keyword = None
                    match keyword : # определим тип сущности, которую мы будем регистрировать как внешнюю ссылку
                        # т.е. в словарь ex_dates мы будем класть даты в том случае, когда мы находится
                        # в описании entity DATE, перейдя к ним от keyword => dates <=> ex_dates
                        case config.ConfigKeywords.dates : register_keyword = config.ConfigKeywords.ex_dates
                        case config.ConfigKeywords.places : register_keyword = config.ConfigKeywords.ex_places
                        case config.ConfigKeywords.persons : register_keyword = config.ConfigKeywords.ex_persons
                        case config.ConfigKeywords.sources : register_keyword = config.ConfigKeywords.ex_sources
                        case config.ConfigKeywords.others : register_keyword = config.ConfigKeywords.ex_others
                        case _ : raise Exception("Нет такого типа!")

                    # теперь прочитаем текст на наличие {ссылок:1}[x]
                    entities : list[dict] = parseText(text, pattern)

                    for entity in entities :
                        # {keyword: "date"; number: "1"; name: "ABOBA"}
                        # name - для интерфейсов, нас не интересует
                        entity_id = int(entity[config.ParseResult.number])
                        entity_keyword = entity[config.ParseResult.keyword]

                        # теперь определим словарь для "сохранения"
                        # (в текущую сущность встречаемые в её текстах)
                        save_keyword = None
                        # а также storage, которые будет хранить её как ВНЕШНЮЮ ССЫЛКУ
                        storage = BaseStorage()
                        match entity_keyword :
                            case config.ParseKeywords.date : 
                                storage = date_storage
                                save_keyword = config.ConfigKeywords.dates
                            case config.ParseKeywords.place : 
                                storage = place_storage
                                save_keyword = config.ConfigKeywords.places
                            case config.ParseKeywords.person : 
                                storage = person_storage
                                save_keyword = config.ConfigKeywords.persons
                            case config.ParseKeywords.source :
                                storage = source_storage
                                save_keyword = config.ConfigKeywords.sources
                            case config.ParseKeywords.other :
                                storage = other_storage
                                save_keyword = config.ConfigKeywords.others
                            case _ : raise Exception("Нет такого типа!")

                        # проверить, что сущность-ссылка существует в хранилище
                        if not storage.get(entity_id) :
                            res_code = 2
                            logger.error(f"Сущности {entity_id}[{entity_keyword}] в хранилище ещё не существует!")
                            continue
                            # raise Exception(f"Сущности {entity_id}[{entity_keyword}] в хранилище \
                            #                  ещё не существует!")

                        # сохранить для читаемой сущности ссылку на ту, что встретилась
                        #       в тексте
                        if not current_storage.saveEntity(id, entity_id, save_keyword) :
                            raise Exception(f"Ошибка с сохранением сущности {entity_id}[{entity_keyword}][{save_keyword}] \
                                             для сущности {id}[{keyword}]!")
                            
                        # также зарегистрировать в storage, что появилась внешняя 
                        #       ссылка на сущность-ссылку
                        if not storage.registerEntity(entity_id, id, register_keyword) :
                            raise Exception(f"Ошибка с регистрацией сущности {id}[{keyword}][{register_keyword}] \
                                             для сущности {entity_id}[{entity_keyword}]!")
      
                except Exception as exc :
                    raise exc

            if description :
                saveAndRegisterEntitites(description, patternTextInclusion())

    except Exception as exc :
        res_code = 1
        logger.error("ОШИБКА ВО ВРЕМЯ ПАРСИНГА ФАЙЛА файла keyword={keyword} path={path} exc={exc}", 
                     path=path, keyword=keyword, exc=exc)

    return res_code


################### ГЛАВНЫЙ ПРОЦЕСС

def parse(path : Path, dates_path : Path | None = None, persons_path : Path | None = None,
          places_path : Path | None = None, sources_path : Path | None = None,
          others_path : Path | None = None):
    """
        Главная функция. Возвращает набор классов, 
            из которых впоследствии будет собран SQL запрос
    """
    try : 
        logger.info("Начало операции ОБЩЕГО парсинга")

        logger.info("СОЗДАНИЕ ХРАНИЛИЩА")
        s0 = SourceStorage(name="sources")
        s1 = DateStorage(name="dates")
        s2 = PlaceStorage(name="places")
        s3 = PersonStorage(name="persons")
        s4 = OtherStorage(name="others")

        source_code = 2
        date_code = 2
        place_code = 2
        person_code = 2
        other_code = 2

        for i in range(config.max_reparse_count) :
            logger.info(f"ПАРСИНГ ФАЙЛОВ - ЦИКЛ ИТЕРАЦИИ {i}")
            # Цикл разрешает некоторое количество взаимных вложенностей
            # , которые не укладываются в иерархию (например, дата ссылается на человека)
            if source_code == 2 :
                source_code = parseFile(sources_path, config.ConfigKeywords.sources, s0, s1, s2, s3, s4)
            if date_code == 2 :
                date_code = parseFile(dates_path, config.ConfigKeywords.dates, s0, s1, s2, s3, s4)
            if place_code == 2 :
                place_code = parseFile(places_path, config.ConfigKeywords.places, s0, s1, s2, s3, s4)
            if person_code == 2 :
                person_code = parseFile(persons_path, config.ConfigKeywords.persons, s0, s1, s2, s3, s4)
            if other_code == 2 :
                other_code = parseFile(others_path, config.ConfigKeywords.others, s0, s1, s2, s3, s4)

            codes = [source_code, date_code, place_code, person_code, other_code]

            if 1 in codes :
                logger.error(f"Ошибка на итерации {i}")
                raise Exception("Непредвиденная ошибка - статус код одной из операций = 1 (см. лог)")

            if 2 not in codes :
                break

        if 2 in codes or 1 in codes :
            logger.error(f"РАБОТА ОТРАБОТАЛА НЕПРАВИЛЬНО codes={codes}")
        else :
            logger.info(f"УСПЕШНЫЙ ПАРСИНГ")

        print('\n\n\n', s0, '\n\n\n', s1,'\n\n\n', s2,'\n\n\n', s3, '\n\n\n', s4, '\n\n\n')

        logger.info("Конец операции ОБЩЕГО парсинга")
        return 1
    except Exception as exc :
        logger.error("ОШИБКА ВО ВРЕМЯ ОБЩЕГО ПАРСИНГА exc={exc}", exc=exc)
        return None
