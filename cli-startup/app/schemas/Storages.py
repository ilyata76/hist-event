"""
    Схемы или классы, оперирующими всеми остальными схемами
"""
from loguru import logger

from schemas.Entity import BaseEntity, BaseStorage
from schemas.Date import DateStorage
from schemas.Source import SourceStorage
from schemas.Place import PlaceStorage
from schemas.Person import PersonStorage
from schemas.Other import OtherStorage
from schemas.Event import EventStorage

import config
import pyparsing


class Storages() :
    """
        Хранилище хранилищей
    """
    
    def __init__(self, 
                 source_storage : SourceStorage,
                 date_storage : DateStorage, 
                 place_storage : PlaceStorage,
                 person_storage : PersonStorage,
                 other_storage : OtherStorage,
                 event_storage : EventStorage ) :
        self.source_storage = source_storage
        self.date_storage = date_storage
        self.place_storage = place_storage
        self.person_storage = person_storage
        self.other_storage = other_storage
        self.event_storage = event_storage


    def append(self, id : int , keyword : str, 
               entity : BaseEntity) -> bool :
        """
            Добавить ENTITY по KEYWORD в подходящее хранилище
        """
        match keyword : # добавим в Storage в зависимости от типа читаемого файла
            case config.ConfigKeywords.sources :
                self.current_storage = self.source_storage
            case config.ConfigKeywords.dates : 
                self.current_storage = self.date_storage
            case config.ConfigKeywords.places :
                self.current_storage = self.place_storage
            case config.ConfigKeywords.persons :
                self.current_storage = self.person_storage
            case config.ConfigKeywords.others :
                self.current_storage = self.other_storage
            case config.ConfigKeywords.events :
                self.current_storage = self.event_storage
            case _ :
                logger.error(f"Такого keyword={keyword} не существует!")
                return False
        
        result = False
        if self.current_storage.get(id) is None and\
             not (result := self.current_storage.append(entity)) :
            logger.error(f"Ошибка с добавлением новой сущности для {keyword}")
            raise Exception(f"Непредвиденная ошибка с добавлением новой сущности для {keyword}!!!")
        else :
            result = True
        return result


    def __parseText(self, string : str, 
                    pattern : pyparsing.ParserElement) -> list[dict] :
        """
            Возвращает список словарей - результата парсинга по паттерну
            Используется для парсинга текста события и регистрации их ID в моделях
        """
        logger.debug("Начало парсинга текста")
        parse_list = pattern.searchString(string).as_list()
        result = []

        for x in parse_list :
            stroke = x[0]
            result.append( { config.ParseResult.keyword : stroke.split(':')[0].strip(),
                            config.ParseResult.number : stroke.split(':')[1].strip().split('[')[0].strip(),
                            config.ParseResult.name : stroke.split('[')[1].strip() } )
        logger.info("Парсинг строки res={res}", res=result.__len__())
        return result


    def saveAndRegisterEntitites(self, text : str, 
                                 pattern : pyparsing.ParserElement, keyword : str, id: int) -> int :
        """
            Функция регистрирует и сохраняет сущности: одни при обходе, другие при 
                определении, что появилась внешняя ссылка

            Возвращает
                - 0 если всё ок
                - 1 если что-то плохо
                - 2 если нарушение цепочки
        """
        try :
            res_code = 0
            register_keyword = None
            match keyword : # определим тип сущности, которую мы будем регистрировать как внешнюю ссылку
                # т.е. в словарь ex_dates мы будем класть даты в том случае, когда мы находится
                # в описании entity DATE, перейдя к ним от keyword => dates <=> ex_dates
                case config.ConfigKeywords.dates : 
                    register_keyword = config.ConfigKeywords.ex_dates
                case config.ConfigKeywords.places : 
                    register_keyword = config.ConfigKeywords.ex_places
                case config.ConfigKeywords.persons : 
                    register_keyword = config.ConfigKeywords.ex_persons
                case config.ConfigKeywords.sources : 
                    register_keyword = config.ConfigKeywords.ex_sources
                case config.ConfigKeywords.others : 
                    register_keyword = config.ConfigKeywords.ex_others
                case config.ConfigKeywords.events : 
                    register_keyword = config.ConfigKeywords.ex_events
                case _ : raise Exception("Нет такого типа!")

            # теперь прочитаем текст на наличие {ссылок:1}[x]
            entities : list[dict] = self.__parseText(text, pattern)

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
                        storage = self.date_storage
                        save_keyword = config.ConfigKeywords.dates
                    case config.ParseKeywords.place : 
                        storage = self.place_storage
                        save_keyword = config.ConfigKeywords.places
                    case config.ParseKeywords.person : 
                        storage = self.person_storage
                        save_keyword = config.ConfigKeywords.persons
                    case config.ParseKeywords.source :
                        storage = self.source_storage
                        save_keyword = config.ConfigKeywords.sources
                    case config.ParseKeywords.other :
                        storage = self.other_storage
                        save_keyword = config.ConfigKeywords.others
                    case config.ParseKeywords.event :
                        storage = self.event_storage
                        save_keyword = config.ConfigKeywords.events
                    case _ : raise Exception("Нет такого типа!")

                # проверить, что сущность-ссылка существует в хранилище
                if not storage.get(entity_id) :
                    res_code = 2
                    logger.warning(f"Сущности {entity_id}[{entity_keyword}] в хранилище ещё не существует!")
                    continue
                    # raise Exception(f"Сущности {entity_id}[{entity_keyword}] в хранилище \
                    #                  ещё не существует!")

                # сохранить для читаемой сущности ссылку на ту, что встретилась
                #       в тексте
                if not self.current_storage.saveEntity(id, entity_id, save_keyword) :
                    res_code = 1
                    raise Exception(f"Ошибка с сохранением сущности {entity_id}[{entity_keyword}][{save_keyword}] \
                                     для сущности {id}[{keyword}]!")
                    
                # также зарегистрировать в storage, что появилась внешняя 
                #       ссылка на сущность-ссылку
                if not storage.registerEntity(entity_id, id, register_keyword) :
                    res_code = 1
                    raise Exception(f"Ошибка с регистрацией сущности {id}[{keyword}][{register_keyword}] \
                                     для сущности {entity_id}[{entity_keyword}]!")
    
        except Exception as exc :
            res_code = 1
            raise exc
    
        return res_code


    def __str__(self) -> str:
        """
            Для принтов и логов
        """
        string = "\n" + str(self.source_storage) + "\n"
        string += "\n" + str(self.date_storage) + "\n"
        string += "\n" + str(self.place_storage) + "\n"
        string += "\n" + str(self.person_storage) + "\n"
        string += "\n" + str(self.other_storage) + "\n"
        string += "\n" + str(self.event_storage) + "\n"
        return string


    def dropTablesSQL(self) -> str :
        """
            Удалить таблиц, если те существуют
        """
        logger.debug("Удаление таблиц SQL через Storages")
        return "\n\n".join([x.dropTableSQL() for x in [self.source_storage, self.date_storage,
                                                       self.place_storage, self.person_storage, 
                                                       self.other_storage, self.event_storage]])
    

    def generateTablesSQL(self) -> str :
        """
            Генерация таблиц
        """
        logger.debug("Генерация таблиц SQL через Storages")
        return "\n\n".join([self.source_storage.generateTableSQL(),
                            self.date_storage.generateTableSQL(),
                            self.place_storage.generateTableSQL(),
                            self.person_storage.generateTableSQL(),
                            self.other_storage.generateTableSQL(),
                            self.event_storage.generateTableSQL()])
    

    def fillTablesSQL(self) -> str :
        """
            Наполнение таблиц
        """
        logger.debug("Заполнение таблиц SQL через Storages")
        return "\n\n".join([self.source_storage.fillTableSQL(),
                            self.date_storage.fillTableSQL(),
                            self.place_storage.fillTableSQL(),
                            self.person_storage.fillTableSQL(),
                            self.other_storage.fillTableSQL(),
                            self.event_storage.fillTableSQL()])