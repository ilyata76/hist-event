"""
    Файл, отвечающий за работу с YAML-файлами и моделями.
"""
import datetime
from loguru import logger
from pathlib import Path
from ftplib import FTP

from core.schemas.Biblio import Biblio
from core.schemas.BiblioFragment import BiblioFragment
from core.schemas.Date import Date
from core.schemas.Event import Event
from core.schemas.Other import Other
from core.schemas.Person import Person
from core.schemas.Place import Place
from core.schemas.Source import Source
from core.schemas.SourceFragment import SourceFragment
from core.schemas.Storages import Storages
from core.schemas.Bonds import Bond, BondStorage
from core.schemas.Paths import Paths

from core.processes.utils import patternTextInclusion, dictFromYaml

from config import ConfigKeywords, max_reparse_count as config_max_reparse_count
#####################


def sourceIsEntity(dict_entity : dict, id : int,
                   storages : Storages):
    """
        Источник. Зависит от даты и автора-персоналии.
    """
    logger.debug("Сущность для добавления определена - Source")
    res_code, entity = 1, None
    date = dict_entity.get(ConfigKeywords.date, None)
    author = dict_entity.get(ConfigKeywords.author, None)

    if storages.date_storage.get(int(date)) :
        if storages.person_storage.get(int(author)) :
            res_code, entity = 0, Source( name=dict_entity.get(ConfigKeywords.name, None), 
                                          id=id, 
                                          description=dict_entity.get(ConfigKeywords.description, None),
                                          link=dict_entity.get(ConfigKeywords.link, None), 
                                          author=author, 
                                          date=date,
                                          type=dict_entity.get(ConfigKeywords.type, None),
                                          subtype=dict_entity.get(ConfigKeywords.subtype, None) )
        else :
            res_code, entity = 2, None
            logger.warning(f"Такой персоналии для источника={id} - author={author} - не существует")
    else :
        res_code, entity = 2, None
        logger.warning(f"Такой даты для источника={id} - date={date} - не существует")

    return res_code, entity


def sourceFragmentIsEntity(dict_entity : dict, id : int,
                           storages : Storages) :
    """
        Фрагмент от источника. Зависит от самого источника
    """
    logger.debug("Сущность для добавления определена - SourceFragment")
    res_code, entity = 1, None
    source = dict_entity.get(ConfigKeywords.source, None)
    if storages.source_storage.get(int(source)) :
        res_code, entity = 0, SourceFragment( name=dict_entity.get(ConfigKeywords.name, None), 
                                              id=id, 
                                              description=dict_entity.get(ConfigKeywords.description, None),
                                              source=source )
    else :
        res_code, entity = 2, None
        logger.warning(f"Такого источника для фрагмента источника={id} - source={source} - не существует")

    return res_code, entity


def dateIsEntity(dict_entity : dict, id : int):
    """
        Дата. Есть вариации заполнения полей.
    """
    logger.debug("Сущность для добавления определена - Date")
    res_code, entity = 1, None
    start_date, start_time, end_date, end_time, time = None, None, None, None, None

    start = dict_entity.get(ConfigKeywords.start, None)
    end = dict_entity.get(ConfigKeywords.end, None)
    date = dict_entity.get(ConfigKeywords.date, None)


    def datetimeToDateNTime(date_time) :
        """
            Разделить datetime на date и time
        """
        time = None
        temp_time = datetime.datetime.fromisoformat(date_time).time()
        if not (temp_time.hour == temp_time.minute == temp_time.second == temp_time.microsecond == 0) : 
            time = str(temp_time)
        date = str(datetime.datetime.fromisoformat(date_time).date())
        return date, time

    if date : 
        date, time = datetimeToDateNTime(date)
    if start :
        start_date, start_time = datetimeToDateNTime(start)
    if end :
        end_date, end_time = datetimeToDateNTime(end)

    res_code, entity = 0, Date( name=dict_entity.get(ConfigKeywords.name, None), 
                                id=id, 
                                description=dict_entity.get(ConfigKeywords.description, None), 
                                date=date, 
                                time=time, 
                                start_date=start_date, 
                                start_time=start_time,
                                end_date=end_date, 
                                end_time=end_time, 
                                start=start, 
                                end=end )
    
    return res_code, entity


def placeIsEntity(dict_entity : dict, id : int) :
    """
        Место
    """
    logger.debug("Сущность для добавления определена - Place")
    res_code, entity = 0, Place( name=dict_entity.get(ConfigKeywords.name, None), 
                                 id=id, 
                                 description=dict_entity.get(ConfigKeywords.description, None), 
                                 geo=dict_entity.get(ConfigKeywords.geo, None) )
    
    return res_code, entity


def personIsEntity(dict_entity : dict, id : int,
                   storages : Storages) :
    """
        Зависит от date
    """
    logger.debug("Сущность для добавления определена - Person")
    res_code, entity = 1, None
    date = dict_entity.get(ConfigKeywords.date, None)

    if storages.date_storage.get(int(date)) :
        res_code, entity = 0, Person( name=dict_entity.get(ConfigKeywords.name, None), 
                                      id=id, 
                                      description=dict_entity.get(ConfigKeywords.description, None),
                                      date=date )
    else :
        res_code, entity = 2, None
        logger.warning(f"Такой даты для персоналии={id} - date={date} - не существует")

    return res_code, entity


def otherIsEntity(dict_entity : dict, id : int) :
    """
        "Другое"
    """
    logger.debug("Сущность для добавления определена - Other")
    res_code, entity = 0, Other( name=dict_entity.get(ConfigKeywords.name, None), 
                                 id=id, 
                                 description=dict_entity.get(ConfigKeywords.description, None), 
                                 meta=dict_entity.get(ConfigKeywords.meta, None) )
    return res_code, entity


def eventIsEntity(dict_entity : dict, id : int,
                  storages : Storages) :
    """
        Событие
    """
    logger.debug("Сущность для добавления определена - Event")
    res_code, entity = 1, None
    date = dict_entity.get(ConfigKeywords.date, None)

    if storages.date_storage.get(int(date)) :
        res_code, entity = 0, Event( name=dict_entity.get(ConfigKeywords.name, None), 
                                     id=id, 
                                     min=dict_entity.get(ConfigKeywords.min, None), 
                                     max=dict_entity.get(ConfigKeywords.max, None), 
                                     level=dict_entity.get(ConfigKeywords.level, None), 
                                     date=date )
    else :
        res_code, entity = 2, None
        logger.warning(f"Такой даты для события={id} - date={date} - не существует")
    
    return res_code, entity


def biblioIsEntity(dict_entity : dict, id : int) :
    """
        Книги. Дата здесь - просто строка
    """
    logger.debug("Сущность для добавления определена - Biblio")
    res_code, entity = 0, Biblio( name=dict_entity.get(ConfigKeywords.name, None), 
                                  id=id, 
                                  description=dict_entity.get(ConfigKeywords.description, None), 
                                  author=dict_entity.get(ConfigKeywords.author, None),
                                  link=dict_entity.get(ConfigKeywords.link, None),
                                  state=dict_entity.get(ConfigKeywords.state, None),
                                  period=dict_entity.get(ConfigKeywords.period, None),
                                  date=dict_entity.get(ConfigKeywords.date, None) )
    return res_code, entity


def biblioFragmentIsEntity(dict_entity : dict, id : int,
                           storages : Storages) :
    """
        Зависит от библиографического источника
    """
    logger.debug("Сущность для добавления определена - BiblioFragment")
    res_code, entity = 1, None
    biblio = dict_entity.get(ConfigKeywords.biblio, None)

    if storages.biblio_storage.get(int(biblio)) :
        res_code, entity = 0, BiblioFragment( name=dict_entity.get(ConfigKeywords.name, None), 
                                              id=id, 
                                              description=dict_entity.get(ConfigKeywords.description, None),
                                              biblio=biblio )
    else :
        res_code, entity = 2, None
        logger.warning(f"Такого источника для фрагмента библиографического источника={id} - biblio={biblio} - не существует")

    return res_code, entity

############

def getEntity(dict_entity : dict, keyword : str, 
              id : int, storages : Storages):
    """
        Подразумевается, что все значения здесь - валидные.
        Вернёт 0, entity, если всё ОК.
        В противном случае - 2, None.
    """
    logger.debug("Взятие сущности из словаря после парсинга, {e}", e=dict_entity)
    res_code, entity_to_append = 0, None

    match keyword : # добавим в Storage в зависимости от типа читаемого файла
        case ConfigKeywords.sources :
            res_code, entity_to_append = sourceIsEntity(dict_entity, 
                                                        id, storages)
        case ConfigKeywords.source_fragments :
            res_code, entity_to_append = sourceFragmentIsEntity(dict_entity,
                                                                id, storages)
        case ConfigKeywords.dates : 
            res_code, entity_to_append = dateIsEntity(dict_entity, id)
        case ConfigKeywords.places :
            res_code, entity_to_append = placeIsEntity(dict_entity, id)
        case ConfigKeywords.persons :
            res_code, entity_to_append = personIsEntity(dict_entity, 
                                                        id, storages)
        case ConfigKeywords.others :
            res_code, entity_to_append = otherIsEntity(dict_entity, id)
        case ConfigKeywords.events :
            res_code, entity_to_append = eventIsEntity(dict_entity, 
                                                       id, storages)
        case ConfigKeywords.biblios :
            res_code, entity_to_append = biblioIsEntity(dict_entity, id)
        case ConfigKeywords.biblio_fragments :
            res_code, entity_to_append = biblioFragmentIsEntity(dict_entity,
                                                                id, storages)
        case _ :
            raise Exception(f"Нет такой сущности, {keyword}!")

    return res_code, entity_to_append


############ РАБОТА С ХРАНИЛИЩАМИ

def parseFile(path : Path, keyword : str, 
              storages : Storages, ftp : FTP = FTP()) :
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
        logger.info(f"Начало операции полного парсинга файла keyword={keyword} path={path}")
        
        # прочитаем YAML файл, возьмём часть от keyword
        dict_entities = dictFromYaml(path, ftp)[keyword]

        if not dict_entities :
            raise Exception(f"{keyword} : {path} : возникла ошибка во время обхода файла (результат None)")
        if type(dict_entities) is dict or type(dict_entities) == dict: 
            # если результат - один словарь, а не много
            dict_entities = [dict_entities]

        # цикл по сущностям в файле
        for dict_entity in dict_entities :
            # получим по ключевым словам параметры нашей сущности, если те имеются

            id = dict_entity.get(ConfigKeywords.id, None)
            res_code, entity_to_append = getEntity(dict_entity, keyword, id, storages)

            if not entity_to_append or res_code != 0:
                continue

            # res_code == 0 V V V
            # добавим сущность
            if not storages.append(id, keyword, entity_to_append) :
                raise Exception(f"Не удалость добавить сущность {entity_to_append} по {keyword}")

            # прочитаем ещё раз текстовые поля, поддерживающие вставку
            min = dict_entity.get(ConfigKeywords.min, None)
            max = dict_entity.get(ConfigKeywords.max, None)
            description = dict_entity.get(ConfigKeywords.description, None)

            # будет регистрировать для добавленной сущности
            # другие, если в текстовых полях есть на них ссылки
            if description :
                res_code = storages.saveAndRegisterEntitites(description, patternTextInclusion(), keyword, id)
            if min :
                res_code = storages.saveAndRegisterEntitites(min, patternTextInclusion(), keyword, id)
            if max :
                res_code = storages.saveAndRegisterEntitites(max, patternTextInclusion(), keyword, id)

    except Exception as exc :
        res_code = 1
        logger.error(f"Ошибка во время парсинга файла {keyword} по пути {path} [{exc}]")
        raise Exception(f"Ошибка во время парсинга файла {keyword} по пути {path} [{exc}]")

    logger.info(f"Конец операции полного парсинга файла keyword={keyword} path={path} res_code={res_code}")
    return res_code

###########

def parseBonds(paths : Paths, storages : Storages, 
               bond_storage: BondStorage, ftp : FTP = FTP()) -> None :
    """
        Связи отдельно парсим, 
            т.к. на них накладываются дополнительные условия
    """
    logger.info(f"Парсинг связей из {paths.bonds_path}")
    bonds = dictFromYaml(paths.bonds_path, ftp)[ConfigKeywords.bonds]

    if type(bonds) == dict or type(bonds) is dict:
        bonds = [bonds]

    toList = lambda x : list[x] if type(x) != list and x is not None else x
    checkEvents = lambda lst : [storages.event_storage.get(x) is not None for x in lst]
    printMessage = lambda msg : {"log": logger.error(msg), "exc": Exception(msg)}
    
    for dict_bond in bonds :
        event = dict_bond.get(ConfigKeywords.event, None)
        parents = dict_bond.get(ConfigKeywords.parents, None)
        childs = dict_bond.get(ConfigKeywords.childs, None)
        prerequisites = dict_bond.get(ConfigKeywords.prerequisites, None)

        if parents and event in parents :
            raise printMessage(f"Попытка прописать к событию={event} родителя в виде себя")["exc"]
        if childs and event in childs :
            raise printMessage(f"Попытка прописать к событию={event} ребёнка в виде себя")["exc"]
        if prerequisites and event in prerequisites :
            raise printMessage(f"Попытка прописать к событию={event} предпосылку в виде себя")["exc"]

        parents, childs, prerequisites = toList(parents), toList(childs), toList(prerequisites)

        if storages.event_storage.get(event) :
            if parents and False in checkEvents(parents): 
                raise printMessage(f"Попытка прописать к событию={event} несуществующего родителя")["exc"]
            if childs and False in checkEvents(childs) :
                raise printMessage(f"Попытка прописать к событию={event} несуществующего ребёнка")["exc"]
            if prerequisites and False in checkEvents(prerequisites) :
                raise printMessage(f"Попытка прописать к событию={event} несуществующую предпосылку")["exc"]
            
            bond_storage.append(Bond(event=event,
                                     parents=parents,
                                     childs=childs,
                                     prerequisites=prerequisites))
        else :
            raise printMessage(f"Попытка прописать связи к несуществующему событию={event}")["exc"]    

    return None

################### ГЛАВНЫЙ ПРОЦЕСС

def parse(paths : Paths,
          storages : Storages,
          bond_storage : BondStorage,
          max_reparse : int = config_max_reparse_count,
          ftp : FTP = FTP()):
    """
        Главная функция. Возвращает набор классов, 
            из которых впоследствии будет собран SQL запрос
    """
    try : 
        logger.info("Операция общего парсинга: начало")
        #########

        codes = {
            ConfigKeywords.sources : 2,
            ConfigKeywords.source_fragments : 2,
            ConfigKeywords.dates : 2,
            ConfigKeywords.places : 2,
            ConfigKeywords.persons : 2,
            ConfigKeywords.others : 2,
            ConfigKeywords.events : 2,
            ConfigKeywords.biblios : 2,
            ConfigKeywords.biblio_fragments : 2
        }

        #########

        def checkCodesOn2(code : int) -> bool :
            """
                Замыкается на codes, возвращает True, если нужно
                    пропарсить файл ещё раз
            """
            nonlocal codes
            return codes[code] == 2 and 1 not in list(codes.values())

        def parseF(path : str, keyword : str) -> None :
            """
                Замыкается на codes,
                    вызывает функцию парсинга и обновляет код-результат в codes
            """
            nonlocal codes, storages, ftp
            codes[keyword] = parseFile(path, keyword, storages, ftp)
            return None
        
        def checkAndParse(keyword : str) -> None :
            """
                Функция, объединяющая две сверху
            """
            if checkCodesOn2(keyword) : 
                parseF(paths.pathByKeyword(keyword), keyword)
            return None

        #########

        for _ in range(max_reparse) :
            for keyword in list(codes.keys()) :
                checkAndParse(keyword)
            if 1 in list(codes.values()) :
                raise Exception("Непредвиденная ошибка - статус код одной из операций = 1")
            if 2 not in list(codes.values()) :
                break

        if 2 in list(codes.values()) or 1 in list(codes.values()) :
            raise Exception(f"Программа отработала неправильно коды возврата - {codes}")

        ######## ТЕПЕРЬ СВЯЗИ ОТДЕЛЬНО
        parseBonds(paths, storages, bond_storage, ftp)

        logger.info("Операция общего парсинга: успешное завершение")
        return storages, bond_storage

    except Exception as exc :
        logger.error(f"Ошибка во время операции общего парсинга [{exc}]")
        raise Exception(f"Ошибка во время операции общего парсинга [{exc}]")
