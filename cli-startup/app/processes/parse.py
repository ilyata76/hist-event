"""
    Файл, отвечающий за работу с YAML-файлами и моделями.
"""
from loguru import logger
from pathlib import Path

import config

from schemas.Date import Date
from schemas.Person import Person
from schemas.Place import Place
from schemas.Source import Source
from schemas.Other import Other
from schemas.Event import Event
from schemas.Storages import Storages

from processes.utils import patternTextInclusion, dictFromYaml

import datetime


############ РАБОТА С ХРАНИЛИЩАМИ

def parseFile(path : Path, keyword : str, storages : Storages) :
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
            min = dict_entity.get(config.ConfigKeywords.min, None)
            max = dict_entity.get(config.ConfigKeywords.max, None)
            level = dict_entity.get(config.ConfigKeywords.level, None)
            time = dict_entity.get(config.ConfigKeywords.time, None)
            
            entity_to_append = None

            match keyword : # добавим в Storage в зависимости от типа читаемого файла
                case config.ConfigKeywords.sources :
                    entity_to_append = Source(name=name, id=id, description=description,
                                               link=link, author=author, date=date)
                case config.ConfigKeywords.dates : 
                    if date : date = str(datetime.date.fromisoformat(date))
                    if time : time = str(datetime.time.fromisoformat(time))
                    entity_to_append = Date(name=name, id=id, description=description, 
                                            date=date, time=time)
                case config.ConfigKeywords.places :
                    entity_to_append = Place(name=name, id=id, description=description, 
                                             geo=geo)
                case config.ConfigKeywords.persons :
                    entity_to_append = Person(name=name, id=id, description=description, 
                                              person=person)
                case config.ConfigKeywords.others :
                    entity_to_append = Other(name=name, id=id, description=description, 
                                             meta=meta)
                case config.ConfigKeywords.events :
                    if storages.date_storage.get(int(date)) :
                        entity_to_append = Event(name=name, id=id, min=min,
                                                max=max, level=level, date=int(date))
                    else :
                        res_code = 2
                        logger.error(f"Такой даты для события - date={date} - не существует")
                        continue 

            if not storages.append(id, keyword, entity_to_append) :
                raise Exception(f"Не удалость добавить сущность {entity_to_append} по {keyword}")

            if description :
                if storages.saveAndRegisterEntitites(description, patternTextInclusion(), keyword, id) == 2 :
                    res_code = 2
            if min :
                if storages.saveAndRegisterEntitites(min, patternTextInclusion(), keyword, id) == 2:
                    res_code = 2
            if max :
                if storages.saveAndRegisterEntitites(max, patternTextInclusion(), keyword, id) == 2 :
                    res_code = 2

    except Exception as exc :
        res_code = 1
        logger.error("ОШИБКА ВО ВРЕМЯ ПАРСИНГА ФАЙЛА файла keyword={keyword} path={path} exc={exc}", 
                     path=path, keyword=keyword, exc=exc)

    logger.info("Начало операции полного парсинга файла keyword={keyword} path={path} res_code={res_code}", 
                    path=path, keyword=keyword, res_code=res_code)

    return res_code


################### ГЛАВНЫЙ ПРОЦЕСС

def parse(path_folder : Path,
          storages : Storages,
          dates_path : Path | None = None, 
          persons_path : Path | None = None,
          places_path : Path | None = None, 
          sources_path : Path | None = None,
          others_path : Path | None = None,
          events_path : Path | None = None):
    """
        Главная функция. Возвращает набор классов, 
            из которых впоследствии будет собран SQL запрос
    """
    try : 
        logger.info("Начало операции ОБЩЕГО парсинга")

        logger.info("СОЗДАНИЕ ХРАНИЛИЩА")

        if not dates_path :
            dates_path = path_folder.joinpath("dates.yaml")
        if not persons_path :
            persons_path = path_folder.joinpath("persons.yaml")
        if not places_path :
            places_path = path_folder.joinpath("places.yaml")
        if not sources_path :
            sources_path = path_folder.joinpath("sources.yaml")
        if not others_path :
            others_path = path_folder.joinpath("others.yaml")
        if not events_path :
            events_path = path_folder.joinpath("events.yaml")

        source_code, date_code, place_code, person_code, other_code,event_code = 2, 2, 2, 2, 2, 2

        for i in range(config.max_reparse_count) :
            logger.info(f"\n\n\n ПАРСИНГ ФАЙЛОВ - ЦИКЛ ИТЕРАЦИИ {i} \n\n\n")
            # Цикл разрешает некоторое количество взаимных вложенностей
            # , которые не укладываются в иерархию (например, дата ссылается на человека)
            codes = [source_code, date_code, place_code, person_code, other_code, event_code]

            if source_code == 2 :
                source_code = parseFile(sources_path, config.ConfigKeywords.sources, storages)
                codes[0] = source_code
            if date_code == 2 and 1 not in codes:
                date_code = parseFile(dates_path, config.ConfigKeywords.dates, storages)
                codes[1] = date_code
            if place_code == 2 and 1 not in codes:
                place_code = parseFile(places_path, config.ConfigKeywords.places, storages)
                codes[2] = place_code
            if person_code == 2 and 1 not in codes:
                person_code = parseFile(persons_path, config.ConfigKeywords.persons, storages)
                codes[3] = person_code
            if other_code == 2 and 1 not in codes:
                other_code = parseFile(others_path, config.ConfigKeywords.others, storages)
                codes[4] = other_code
            if event_code == 2 and 1 not in codes:
                event_code = parseFile(events_path, config.ConfigKeywords.events, storages)
                codes[5] = event_code

            if 1 in codes :
                logger.error(f"Ошибка на итерации {i}")
                raise Exception("Непредвиденная ошибка - статус код одной из операций = 1 (см. лог)")

            if 2 not in codes :
                break

        if 2 in codes or 1 in codes :
            logger.error(f"РАБОТА ОТРАБОТАЛА НЕПРАВИЛЬНО codes={codes}")
        else :
            logger.info(f"УСПЕШНЫЙ ПАРСИНГ")

        logger.info("Конец операции ОБЩЕГО парсинга")
        return storages
    except Exception as exc :
        logger.error("ОШИБКА ВО ВРЕМЯ ОБЩЕГО ПАРСИНГА exc={exc}", exc=exc)
        return None
