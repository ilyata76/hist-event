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
from schemas.Storages import Storages, BaseEntity
from schemas.SourceFragment import SourceFragment
from schemas.Biblio import Biblio
from schemas.BiblioFragment import BiblioFragment

from processes.utils import patternTextInclusion, dictFromYaml

import datetime

############

def getEntity(dict_entity : dict, keyword : str, id : int,
              storages : Storages) -> [int, BaseEntity] :
    """
        Подразумевается, что все значения здесь - валидные.
        Вернёт 0, entity, если всё ОК.
        В противном случае - 2, None.
    """

    # определение переменных заранее

    res_code = 0
    start_date, start_time, end_date, end_time = None, None, None, None
    time = None

    name = dict_entity.get(config.ConfigKeywords.name, None)
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
    start = dict_entity.get(config.ConfigKeywords.start, None)
    end = dict_entity.get(config.ConfigKeywords.end, None)
    source = dict_entity.get(config.ConfigKeywords.source, None)
    state = dict_entity.get(config.ConfigKeywords.state, None)
    period = dict_entity.get(config.ConfigKeywords.period, None)
    biblio = dict_entity.get(config.ConfigKeywords.biblio, None)
        
    entity_to_append = None # сущность для возвращения

    match keyword : # добавим в Storage в зависимости от типа читаемого файла

        case config.ConfigKeywords.sources :
            # исторический источник

            if storages.date_storage.get(int(date)) :
                entity_to_append = Source( name=name, 
                                           id=id, 
                                           description=description,
                                           link=link, 
                                           author=author, 
                                           date=date )
            else :
                res_code = 2
                logger.warning(f"Такой даты для источника={id} - date={date} - не существует")
                entity_to_append = None

        
        case config.ConfigKeywords.source_fragments :
            # исторический источник

            if storages.source_storage.get(int(source)) :
                entity_to_append = SourceFragment( name=name, 
                                                   id=id, 
                                                   description=description,
                                                   source=int(source) )
            else :
                res_code = 2
                logger.warning(f"Такого источника для фрагмента источника={id} - source={source} - не существует")
                entity_to_append = None


        case config.ConfigKeywords.dates : 
            # дата (может быть интервалом)

            if date : 
                temp_time = datetime.datetime.fromisoformat(date).time()
                if not (temp_time.hour == temp_time.minute == temp_time.second == temp_time.microsecond == 0) : 
                    time = str(temp_time)
                date = str(datetime.datetime.fromisoformat(date).date())

            if start :
                temp_time = datetime.datetime.fromisoformat(start).time()
                if not (temp_time.hour == temp_time.minute == temp_time.second == temp_time.microsecond == 0) : 
                    start_time = str(temp_time)
                start_date = str(datetime.datetime.fromisoformat(start).date())

            if end :
                temp_time = datetime.datetime.fromisoformat(end).time()
                if not (temp_time.hour == temp_time.minute == temp_time.second == temp_time.microsecond == 0) : 
                    end_time = str(temp_time)
                end_date = str(datetime.datetime.fromisoformat(end).date())

            entity_to_append = Date( name=name, 
                                     id=id, 
                                     description=description, 
                                     date=date, 
                                     time=time, 
                                     start_date=start_date, 
                                     start_time=start_time,
                                     end_date=end_date, 
                                     end_time=end_time, 
                                     start=start, 
                                     end=end )


        case config.ConfigKeywords.places :
            # место

            entity_to_append = Place( name=name, 
                                      id=id, 
                                      description=description, 
                                      geo=geo )


        case config.ConfigKeywords.persons :
            # историческая личность

            # Для персоналии должна быть зарегистрирована дата в dates.yaml,
            # т.к. date поле есть ссылка FK
            if storages.date_storage.get(int(date)) :
                entity_to_append = Person( name=name, 
                                           id=id, 
                                           description=description, 
                                           person=person,
                                           date=date )
            else :
                res_code = 2
                logger.warning(f"Такой даты для персоналии={id} - date={date} - не существует")
                entity_to_append = None 


        case config.ConfigKeywords.others :
            # "Другое"
            entity_to_append = Other( name=name, 
                                      id=id, 
                                      description=description, 
                                      meta=meta )


        case config.ConfigKeywords.events :
            # "Ивент"

            # Для ивента должна быть зарегистрирована дата в dates.yaml,
            # т.к. date поле есть ссылка FK
            if storages.date_storage.get(int(date)) :
                entity_to_append = Event( name=name, 
                                          id=id, 
                                          min=min, 
                                          max=max, 
                                          level=level, 
                                          date=int(date) )
            else :
                res_code = 2
                logger.warning(f"Такой даты для события={id} - date={date} - не существует")
                entity_to_append = None 


        case config.ConfigKeywords.biblios :
            entity_to_append = Biblio( name=name, 
                                       id=id, 
                                       description=description, 
                                       author=author,
                                       link=link,
                                       state=state,
                                       period=period,
                                       date=date )

        case config.ConfigKeywords.biblio_fragments :
            if storages.biblio_storage.get(int(biblio)) :
                entity_to_append = BiblioFragment( name=name, 
                                                   id=id, 
                                                   description=description,
                                                   biblio=biblio )
            else :
                res_code = 2
                logger.warning(f"Такого источника для фрагмента библиографического источника={id} - source={source} - не существует")
                entity_to_append = None



    return res_code, entity_to_append



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

            id = dict_entity.get(config.ConfigKeywords.id, None)

            res_code, entity_to_append = getEntity(dict_entity, keyword, id, storages)

            if not entity_to_append or res_code != 0:
                continue
           
            # прочитаем ещё раз текстовые поля, поддерживающие вставку
            min = dict_entity.get(config.ConfigKeywords.min, None)
            max = dict_entity.get(config.ConfigKeywords.max, None)
            description = dict_entity.get(config.ConfigKeywords.description, None)

            # добавим сущность
            if not storages.append(id, keyword, entity_to_append) :
                raise Exception(f"Не удалость добавить сущность {entity_to_append} по {keyword}")

            # будет регистрировать для добавленной сущности
            # другие, если в текстовых полях есть на них ссылки
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

    finally: 
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
          events_path : Path | None = None,
          biblios_path : Path | None = None):
    """
        Главная функция. Возвращает набор классов, 
            из которых впоследствии будет собран SQL запрос
    """
    try : 
        logger.info("Начало операции ОБЩЕГО парсинга")

        logger.info("СОЗДАНИЕ ХРАНИЛИЩА")

        # если не указаны пути до файлов - будем пробовать брать их из папки
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
        if not biblios_path :
            biblios_path = path_folder.joinpath("biblios.yaml")

        source_code, source_fragment_code, date_code, place_code, person_code,\
              other_code, event_code, biblio_code, biblio_fragment_code = 0, 1, 2, 3, 4, 5, 6, 7, 8

        codes = [2, 2, 2, 2, 2, 2, 2, 2, 2]

        for i in range(config.max_reparse_count) :
            logger.info(f"\n\n\n ПАРСИНГ ФАЙЛОВ - ЦИКЛ ИТЕРАЦИИ {i} \n\n\n")
            print("##"*50 + f"\n\n\t\t ПАРСИНГ ФАЙЛОВ - ЦИКЛ ИТЕРАЦИИ {i}\n\n"+"##"*50)
            # Цикл разрешает некоторое количество взаимных вложенностей
            # , которые не укладываются в иерархию (например, дата ссылается на человека)

            if codes[source_code] == 2 and 1 not in codes:
                codes[source_code] = parseFile(sources_path, config.ConfigKeywords.sources, storages)
            if codes[source_fragment_code] == 2 and 1 not in codes:
                codes[source_fragment_code] = parseFile(sources_path, config.ConfigKeywords.source_fragments, storages)
            if codes[date_code] == 2 and 1 not in codes:
                codes[date_code] = parseFile(dates_path, config.ConfigKeywords.dates, storages)
            if codes[place_code] == 2 and 1 not in codes:
                codes[place_code] = parseFile(places_path, config.ConfigKeywords.places, storages)
            if codes[person_code] == 2 and 1 not in codes:
                codes[person_code] = parseFile(persons_path, config.ConfigKeywords.persons, storages)
            if codes[other_code] == 2 and 1 not in codes:
                codes[other_code] = parseFile(others_path, config.ConfigKeywords.others, storages)
            if codes[event_code] == 2 and 1 not in codes:
                codes[event_code] = parseFile(events_path, config.ConfigKeywords.events, storages)
            if codes[biblio_code] == 2 and 1 not in codes:
                codes[biblio_code] = parseFile(biblios_path, config.ConfigKeywords.biblios, storages)
            if codes[biblio_fragment_code] == 2 and 1 not in codes:
                codes[biblio_fragment_code] = parseFile(biblios_path, config.ConfigKeywords.biblio_fragments, storages)

            if 1 in codes :
                logger.error(f"Ошибка на итерации {i}")
                raise Exception("Непредвиденная ошибка - статус код одной из операций = 1 (см. лог)")

            if 2 not in codes :
                break

        if 2 in codes or 1 in codes :
            print("##"*50 + f"\n\n\t\t БЕЗУСПЕШНО codes={codes}\n\n"+"##"*50)
            logger.error(f"ПРОГРАММА ОТРАБОТАЛА НЕПРАВИЛЬНО codes={codes}")
        else :
            print("##"*50 + f"\n\n\t\t УСПЕХ\n\n"+"##"*50)
            logger.info(f"УСПЕШНЫЙ ПАРСИНГ")

        logger.info("Конец операции ОБЩЕГО парсинга")
        return storages


    except Exception as exc :
        print("##"*50 + f"\n\n\t\t ОШИБКА exc={exc}\n\n"+"##"*50)
        logger.error("ОШИБКА ВО ВРЕМЯ ОБЩЕГО ПАРСИНГА exc={exc}", exc=exc)
        return None
