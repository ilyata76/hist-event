"""
    Файл, отвечающий за работу с YAML-файлами и моделями.
"""
import datetime
from loguru import logger
from pathlib import Path
from ftplib import FTP

from schemas import BaseEntity, Date, Person, Place, Event, Other,\
                    Source, SourceFragment, Biblio, BiblioFragment,\
                    Storages, Bond, BondStorage, Paths
from processes.utils import patternTextInclusion, dictFromYaml
from config import ConfigKeywords, max_reparse_count as config_max_reparse_count


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

    name = dict_entity.get(ConfigKeywords.name, None)
    description = dict_entity.get(ConfigKeywords.description, None)
    link = dict_entity.get(ConfigKeywords.link, None)
    author = dict_entity.get(ConfigKeywords.author, None)
    date = dict_entity.get(ConfigKeywords.date, None)
    geo = dict_entity.get(ConfigKeywords.geo, None)
    meta = dict_entity.get(ConfigKeywords.meta, None)
    min = dict_entity.get(ConfigKeywords.min, None)
    max = dict_entity.get(ConfigKeywords.max, None)
    level = dict_entity.get(ConfigKeywords.level, None)
    start = dict_entity.get(ConfigKeywords.start, None)
    end = dict_entity.get(ConfigKeywords.end, None)
    source = dict_entity.get(ConfigKeywords.source, None)
    state = dict_entity.get(ConfigKeywords.state, None)
    period = dict_entity.get(ConfigKeywords.period, None)
    biblio = dict_entity.get(ConfigKeywords.biblio, None)
    type = dict_entity.get(ConfigKeywords.type, None)
    subtype = dict_entity.get(ConfigKeywords.subtype, None)
        
    entity_to_append = None # сущность для возвращения

    match keyword : # добавим в Storage в зависимости от типа читаемого файла

        case ConfigKeywords.sources :
            # исторический источник

            if storages.date_storage.get(int(date)) :
                if storages.person_storage.get(int(author)) :
                    entity_to_append = Source( name=name, 
                                               id=id, 
                                               description=description,
                                               link=link, 
                                               author=author, 
                                               date=date,
                                               type=type,
                                               subtype=subtype )
                else :
                    res_code = 2
                    logger.warning(f"Такой персоналии для источника={id} - author={author} - не существует")
                    entity_to_append = None
            else :
                res_code = 2
                logger.warning(f"Такой даты для источника={id} - date={date} - не существует")
                entity_to_append = None

        
        case ConfigKeywords.source_fragments :
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


        case ConfigKeywords.dates : 
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


        case ConfigKeywords.places :
            # место

            entity_to_append = Place( name=name, 
                                      id=id, 
                                      description=description, 
                                      geo=geo )


        case ConfigKeywords.persons :
            # историческая личность

            # Для персоналии должна быть зарегистрирована дата в dates.yaml,
            # т.к. date поле есть ссылка FK
            if storages.date_storage.get(int(date)) :
                entity_to_append = Person( name=name, 
                                           id=id, 
                                           description=description,
                                           date=date )
            else :
                res_code = 2
                logger.warning(f"Такой даты для персоналии={id} - date={date} - не существует")
                entity_to_append = None 


        case ConfigKeywords.others :
            # "Другое"
            entity_to_append = Other( name=name, 
                                      id=id, 
                                      description=description, 
                                      meta=meta )


        case ConfigKeywords.events :
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


        case ConfigKeywords.biblios :
            entity_to_append = Biblio( name=name, 
                                       id=id, 
                                       description=description, 
                                       author=author,
                                       link=link,
                                       state=state,
                                       period=period,
                                       date=date )

        case ConfigKeywords.biblio_fragments :
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
        logger.info("Начало операции полного парсинга файла keyword={keyword} path={path}", 
                    path=path, keyword=keyword)
        
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
        logger.error("ОШИБКА ВО ВРЕМЯ ПАРСИНГА ФАЙЛА файла keyword={keyword} path={path} exc={exc}", 
                     path=path, keyword=keyword, exc=exc)

    finally: 
        logger.info("Конец операции полного парсинга файла keyword={keyword} path={path} res_code={res_code}", 
                        path=path, keyword=keyword, res_code=res_code)

        return res_code

###########

def parseBonds(paths : Paths, storages : Storages, 
               bond_storage: BondStorage, ftp : FTP = FTP()) -> None :
    """
        Связи отдельно парсим, 
            т.к. на них накладываются дополнительные условия
    """
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


        for _ in range(max_reparse) :
            for keyword in list(codes.keys()) :
                checkAndParse(keyword)

            if 1 in list(codes.values()) :
                raise Exception("Непредвиденная ошибка - статус код одной из операций = 1 (см. лог)")

            if 2 not in list(codes.values()) :
                break

        if 2 in list(codes.values()) or 1 in list(codes.values()) :
            raise Exception(f"Программа отработала неправильно codes={codes}")

        ######## ТЕПЕРЬ СВЯЗИ ОТДЕЛЬНО
        parseBonds(paths, storages, bond_storage, ftp)
        
        return storages, bond_storage

    except Exception as exc :
        logger.error("ОШИБКА ВО ВРЕМЯ ОБЩЕГО ПАРСИНГА {t}: exc={exc}", t=type(exc), exc=exc)
        return None, None
