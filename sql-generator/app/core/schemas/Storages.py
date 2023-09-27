"""
    Схемы или классы, оперирующими всеми остальными схемами
"""
from pyparsing import ParserElement 
from loguru import logger

from core.schemas.Entity import BaseEntity, BaseStorage
from core.schemas.Biblio import BiblioStorage
from core.schemas.BiblioFragment import BiblioFragmentStorage
from core.schemas.Date import DateStorage
from core.schemas.Event import EventStorage
from core.schemas.Other import OtherStorage
from core.schemas.Person import PersonStorage
from core.schemas.Place import PlaceStorage
from core.schemas.Source import SourceStorage
from core.schemas.SourceFragment import SourceFragmentStorage

from config import ConfigKeywords, ParseResult, ParseKeywords



class Storages() :
    """
        Хранилище хранилищей
    """
    
    def __init__(self, 
                 source_storage : SourceStorage | None
                    = SourceStorage(ConfigKeywords.sources),
                 date_storage : DateStorage | None 
                    = DateStorage(ConfigKeywords.dates), 
                 place_storage : PlaceStorage| None 
                    = PlaceStorage(ConfigKeywords.places),
                 person_storage : PersonStorage | None 
                    = PersonStorage(ConfigKeywords.persons),
                 other_storage : OtherStorage | None 
                    = OtherStorage(ConfigKeywords.others),
                 event_storage : EventStorage | None 
                    = EventStorage(ConfigKeywords.events),
                 source_fragment_storage : SourceFragmentStorage | None 
                    = SourceFragmentStorage(ConfigKeywords.source_fragments),
                 biblio_storage : BiblioStorage | None 
                    = BiblioStorage(ConfigKeywords.biblios),
                 biblio_fragment_storage : BiblioFragmentStorage | None 
                    = BiblioFragmentStorage(ConfigKeywords.biblio_fragments)) :
        self.source_storage = source_storage
        self.date_storage = date_storage
        self.place_storage = place_storage
        self.person_storage = person_storage
        self.other_storage = other_storage
        self.event_storage = event_storage
        self.source_fragment_storage = source_fragment_storage
        self.biblio_storage = biblio_storage
        self.biblio_fragment_storage = biblio_fragment_storage


    def __getKeywordStorageDict(self) -> dict[str, BaseStorage]:
        """
            Вернуть словарь тогда, когда по ключу-ХРАНИЛИЩУ выбирается того же
                типа хранилище
        """
        return {
            ConfigKeywords.sources          : self.source_storage,
            ConfigKeywords.source_fragments : self.source_fragment_storage,
            ConfigKeywords.dates            : self.date_storage,
            ConfigKeywords.biblios          : self.biblio_storage,
            ConfigKeywords.biblio_fragments : self.biblio_fragment_storage,
            ConfigKeywords.persons          : self.person_storage,
            ConfigKeywords.places           : self.place_storage,
            ConfigKeywords.others           : self.other_storage,
            ConfigKeywords.events           : self.event_storage
        }


    def __getParseKeywordKeywordDict(self) :
        """
            Вернуть словарь тогда, когда по ключу-СУЩНОСТИ выбирается 
                ключ для хранения ВНУТРЕННЕЙ ссылки у ТЕКУЩЕЙ сущности.

            Например, для СОХРАНЕНИЯ при обходе текста со {вставками:?}[?]
        """
        return {
            ParseKeywords.source            : ConfigKeywords.sources,
            ParseKeywords.source_fragment   : ConfigKeywords.source_fragments,
            ParseKeywords.date              : ConfigKeywords.dates,
            ParseKeywords.biblio            : ConfigKeywords.biblios,
            ParseKeywords.biblio_fragment   : ConfigKeywords.biblio_fragments,
            ParseKeywords.person            : ConfigKeywords.persons,
            ParseKeywords.place             : ConfigKeywords.places,
            ParseKeywords.other             : ConfigKeywords.others,
            ParseKeywords.event             : ConfigKeywords.events
        }


    def __getReversedKeywordKeywordDict(self) :
        """
            Вернуть словарь тогда, когда по ключу-ХРАНИЛИЩУ выбирается 
                ключ для хранения ВНЕШНЕЙ ссылки у ДРУГОЙ сущности.

            Например, для РЕГИСТРАЦИИ.
        """
        return {
            ConfigKeywords.sources          : ConfigKeywords.ex_sources,
            ConfigKeywords.source_fragments : ConfigKeywords.ex_source_fragments,
            ConfigKeywords.dates            : ConfigKeywords.ex_dates,
            ConfigKeywords.biblios          : ConfigKeywords.ex_biblios,
            ConfigKeywords.biblio_fragments : ConfigKeywords.ex_biblio_fragments,
            ConfigKeywords.persons          : ConfigKeywords.ex_persons,
            ConfigKeywords.places           : ConfigKeywords.ex_places,
            ConfigKeywords.others           : ConfigKeywords.ex_others,
            ConfigKeywords.events           : ConfigKeywords.ex_events
        }
    

    def __specifyCurrentSaveStorage(self, keyword : str) -> BaseStorage | None :
        """
            Определить текущее хранилище __current_storage,
                в который будет сохраняться сущность (или в котором она будет изменяться)
        """
        return ((self.__getKeywordStorageDict()).get(keyword, None))


    def append(self, id : int , keyword : str, 
               entity : BaseEntity) -> bool :
        """
            Добавить ENTITY по KEYWORD в подходящее хранилище
        """
        result = False
        if current_storage := self.__specifyCurrentSaveStorage(keyword) :
            if current_storage.get(id) is None and\
                not (result := current_storage.append(entity)) :
                logger.error(f"Ошибка с добавлением новой сущности для {keyword}")
                raise Exception(f"Непредвиденная ошибка с добавлением новой сущности для {keyword}!!!")
            else :
                result = True
        else :
            logger.error(f"Такого keyword={keyword} не существует!")
        return result


    def __parseText(self, string : str, 
                    pattern : ParserElement) -> list[dict] :
        """
            Возвращает список словарей - результата парсинга по паттерну
            Используется для парсинга текста события и регистрации их ID в моделях
        """
        logger.debug("Начало парсинга текста")
        parse_list : list = pattern.searchString(string).as_list()
        result : list = []

        for x in parse_list :
            stroke : str = x[0]
            result.append( { ParseResult.keyword : stroke.split(':')[0].strip(),
                            ParseResult.number : stroke.split(':')[1].strip().split('[')[0].strip(),
                            ParseResult.name : stroke.split('[')[1].strip() } )
        logger.info("Парсинг строки res={res}", res=result.__len__())
        return result


    def saveAndRegisterEntitites(self, text : str, 
                                 pattern : ParserElement, keyword : str, id: int) -> int :
        """
            Функция регистрирует и сохраняет сущности: одни при обходе, другие при 
                определении, что появилась внешняя ссылка

            keyword - сущность, поля text которого будут читаться на предмет {вставок:id}[?]
            id - идентификатор текущей сущности

            Возвращает
                - 0 если всё ок
                - 1 если что-то плохо
                - 2 если нарушение цепочки
        """
        try :

            if not (current_save_storage := self.__specifyCurrentSaveStorage(keyword)) :
                logger.error(f"Такого keyword={keyword} не существует!")
                return False

            res_code = 0
            # определим тип сущности, которую мы будем регистрировать как внешнюю ссылку
            # т.е. в словарь ex_dates мы будем класть даты в том случае, когда мы находится
            # в описании entity DATE, перейдя к ним от keyword => dates <=> ex_dates
            if not (register_keyword := self.__getReversedKeywordKeywordDict().get(keyword)) :
                raise Exception(f"Нет такого типа! {keyword}")
            
            # теперь прочитаем текст на наличие {ссылок:1}[x]
            entities : list[dict] = self.__parseText(text, pattern)

            for entity in entities :
                # {keyword: "date"; number: "1"; name: "ABOBA"} name - для интерфейсов, нас не интересует
                entity_id, entity_keyword = int(entity[ParseResult.number]), entity[ParseResult.keyword]

                # определить ключевое слово, по которому будет "сохранение" встречаемых сущностей у текущей
                if not (save_keyword := self.__getParseKeywordKeywordDict().get(entity_keyword)) :
                    raise Exception(f"Нет такого типа, {entity_keyword}!")
                # а также ex_storage, который будет "сохранять" текущую сущность как ВНЕШНЮЮ ССЫЛКУ
                if not (ex_storage := self.__getKeywordStorageDict().get(save_keyword)) :
                    raise Exception(f"Нет такого типа, {save_keyword}!")

                # проверить, что сущность-ссылка существует в хранилище
                if not ex_storage.get(entity_id) :
                    res_code = 2
                    logger.warning(f"Сущности {entity_id}[{entity_keyword}] в хранилище ещё не существует! для добавления {keyword}")
                    continue

                # сохранить для читаемой сущности ссылку на ту, что встретилась
                #       в тексте
                if not current_save_storage.saveEntity(id, entity_id, save_keyword) :
                    res_code = 1
                    raise Exception(f"Ошибка с сохранением сущности {entity_id}[{entity_keyword}][{save_keyword}] \
                                     для сущности {id}[{keyword}]!")
                    
                # также зарегистрировать в storage, что появилась внешняя 
                #       ссылка на сущность-ссылку
                if not ex_storage.registerEntity(entity_id, id, register_keyword) :
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
        string += "\n" + str(self.source_fragment_storage) + "\n"
        string += "\n" + str(self.biblio_storage) + "\n"
        string += "\n" + str(self.biblio_fragment_storage) + "\n"
        return string


    def __get_array(self) -> list[BaseStorage] :
        """
            для внутреннего пользования функций для SQL-генерации
        """
        return [ self.date_storage, 
                 self.person_storage, 
                 self.source_storage, 
                 self.source_fragment_storage,
                 self.biblio_storage, 
                 self.biblio_fragment_storage,
                 self.place_storage, 
                 self.other_storage, 
                 self.event_storage ]


    def dropTablesSQL(self) -> str :
        """
            Удалить таблиц, если те существуют
        """
        logger.debug("Удаление таблиц SQL через Storages")
        return "\n\n".join([x.dropTableSQL() for x in self.__get_array()])
    

    def generateTablesSQL(self) -> str :
        """
            Генерация таблиц
        """
        logger.debug("Генерация таблиц SQL через Storages")
        return "\n\n".join([x.generateTableSQL() for x in self.__get_array()])
    

    def fillTablesSQL(self) -> str :
        """
            Наполнение таблиц
        """
        logger.debug("Заполнение таблиц SQL через Storages")
        return "\n\n".join([x.fillTableSQL() for x in self.__get_array()])