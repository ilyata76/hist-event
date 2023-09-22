"""
    Схемы или классы, оперирующими всеми остальными схемами
"""
from pyparsing import ParserElement 
from loguru import logger
from schemas import BaseEntity, BaseStorage,\
                    SourceStorage, DateStorage, PlaceStorage, PersonStorage, OtherStorage,\
                    EventStorage, SourceFragmentStorage, BiblioStorage, BiblioFragmentStorage
from config import ConfigKeywords, ParseResult, ParseKeywords



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
                 event_storage : EventStorage,
                 source_fragment_storage : SourceFragmentStorage,
                 biblio_storage : BiblioStorage,
                 biblio_fragment_storage : BiblioFragmentStorage ) :
        self.source_storage = source_storage
        self.date_storage = date_storage
        self.place_storage = place_storage
        self.person_storage = person_storage
        self.other_storage = other_storage
        self.event_storage = event_storage
        self.source_fragment_storage = source_fragment_storage
        self.biblio_storage = biblio_storage
        self.biblio_fragment_storage = biblio_fragment_storage


    def append(self, id : int , keyword : str, 
               entity : BaseEntity) -> bool :
        """
            Добавить ENTITY по KEYWORD в подходящее хранилище
        """
        match keyword : # добавим в Storage в зависимости от типа читаемого файла
            case ConfigKeywords.sources :
                self.current_storage = self.source_storage
            case ConfigKeywords.dates : 
                self.current_storage = self.date_storage
            case ConfigKeywords.places :
                self.current_storage = self.place_storage
            case ConfigKeywords.persons :
                self.current_storage = self.person_storage
            case ConfigKeywords.others :
                self.current_storage = self.other_storage
            case ConfigKeywords.events :
                self.current_storage = self.event_storage
            case ConfigKeywords.source_fragments :
                self.current_storage = self.source_fragment_storage
            case ConfigKeywords.biblios :
                self.current_storage = self.biblio_storage
            case ConfigKeywords.biblio_fragments :
                self.current_storage = self.biblio_fragment_storage
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
                    pattern : ParserElement) -> list[dict] :
        """
            Возвращает список словарей - результата парсинга по паттерну
            Используется для парсинга текста события и регистрации их ID в моделях
        """
        logger.debug("Начало парсинга текста")
        parse_list = pattern.searchString(string).as_list()
        result = []

        for x in parse_list :
            stroke = x[0]
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
            res_code = 0
            register_keyword = None
            match keyword : # определим тип сущности, которую мы будем регистрировать как внешнюю ссылку
                # т.е. в словарь ex_dates мы будем класть даты в том случае, когда мы находится
                # в описании entity DATE, перейдя к ним от keyword => dates <=> ex_dates
                case ConfigKeywords.dates : 
                    register_keyword = ConfigKeywords.ex_dates
                case ConfigKeywords.places : 
                    register_keyword = ConfigKeywords.ex_places
                case ConfigKeywords.persons : 
                    register_keyword = ConfigKeywords.ex_persons
                case ConfigKeywords.sources : 
                    register_keyword = ConfigKeywords.ex_sources
                case ConfigKeywords.others : 
                    register_keyword = ConfigKeywords.ex_others
                case ConfigKeywords.events : 
                    register_keyword = ConfigKeywords.ex_events
                case ConfigKeywords.source_fragments :
                    register_keyword = ConfigKeywords.ex_source_fragments
                case ConfigKeywords.biblios :
                    register_keyword = ConfigKeywords.ex_biblios
                case ConfigKeywords.biblio_fragments :
                    register_keyword = ConfigKeywords.ex_biblio_fragments
                case _ : raise Exception(f"Нет такого типа! {keyword}")

            # теперь прочитаем текст на наличие {ссылок:1}[x]
            entities : list[dict] = self.__parseText(text, pattern)

            for entity in entities :
                # {keyword: "date"; number: "1"; name: "ABOBA"}
                # name - для интерфейсов, нас не интересует
                entity_id = int(entity[ParseResult.number])
                entity_keyword = entity[ParseResult.keyword]

                # теперь определим словарь для "сохранения"
                # (в текущую сущность встречаемые в её текстах)
                save_keyword = None
                # а также storage, которые будет хранить её как ВНЕШНЮЮ ССЫЛКУ
                storage = BaseStorage()
                
                match entity_keyword :
                    case ParseKeywords.date : 
                        storage = self.date_storage
                        save_keyword = ConfigKeywords.dates
                    case ParseKeywords.place : 
                        storage = self.place_storage
                        save_keyword = ConfigKeywords.places
                    case ParseKeywords.person : 
                        storage = self.person_storage
                        save_keyword = ConfigKeywords.persons
                    case ParseKeywords.source :
                        storage = self.source_storage
                        save_keyword = ConfigKeywords.sources
                    case ParseKeywords.other :
                        storage = self.other_storage
                        save_keyword = ConfigKeywords.others
                    case ParseKeywords.event :
                        storage = self.event_storage
                        save_keyword = ConfigKeywords.events
                    case ParseKeywords.source_fragment :
                        storage = self.source_fragment_storage
                        save_keyword = ConfigKeywords.source_fragments
                    case ParseKeywords.biblio :
                        storage = self.biblio_storage
                        save_keyword = ConfigKeywords.biblios
                    case ParseKeywords.biblio_fragment :
                        storage = self.biblio_fragment_storage
                        save_keyword = ConfigKeywords.biblio_fragments
                    case _ : raise Exception("Нет такого типа!")

                # проверить, что сущность-ссылка существует в хранилище
                if not storage.get(entity_id) :
                    res_code = 2
                    logger.warning(f"Сущности {entity_id}[{entity_keyword}] в хранилище ещё не существует! для добавления {keyword}")
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