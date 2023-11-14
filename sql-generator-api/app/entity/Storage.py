"""
    Классы хранилищ для сущностей
"""
from functools import wraps

from utils.logger import logger
from entity.Entity import Entity, Bond
from entity.EntityBonds import EntityBonds
from utils.exception import *
from utils.logger import LogCode
from entity.InclusionParser import InclusionParser


class StorageManager :
    """
        Класс 'управляющего' хранилищами - организация всей работы с сущностями и их хранилищами.
            Создаёт хранилища EntityStorage, хранит их экземпляры, работает с ними.

        Делает всё, что необходимо для корректного добавления сущности (используется InclusionParser, проверяет ссылки и пр.)
    """

    def __init__(self) :
        logger.debug("Создание экземпляра класса Storage")
        self.__storages : dict[str, EntityStorage] = {}
        self.__bonds : dict[int, Bond] = {}


    @staticmethod
    def methodAsyncDecorator(path : str) :
        def method(function) :
            @wraps(function)
            async def wrap(self, *args, **kwargs) :
                try : 
                    logger.debug(f"[STORAGE] : {path} : {args} : {kwargs} : {LogCode.PENDING}")
                    res = await function(self, *args, **kwargs)
                    logger.info(f"[STORAGE] : {path} : {args} : {kwargs} : {res} : {LogCode.SUCCESS}")
                    return res
                except ParsingException as exc :
                    match exc.code :
                        case ParsingExceptionCode.FOREIGN_KEY_DOESNT_EXIST | ParsingExceptionCode.ENTITY_TO_LINK_DOESNT_EXIST :
                            logger.warning(f"[STORAGE] : {path} : {args} : {kwargs} : {exc.detail} : {LogCode.ERROR}")
                        case _ :
                            logger.error(f"[STORAGE] : {path} : {args} : {kwargs} : {exc.detail} : {LogCode.ERROR}")
                    raise exc
                except BaseException as exc :
                    logger.error(f"[STORAGE] : {path} : {args} : {kwargs} : {exc.args} : {LogCode.ERROR}")
                    raise exc
            return wrap
        return method


    def __invalidKeyword(self, keyword : str) :
        return keyword not in EntityBonds.keyword_to_keyword.keys() or \
               EntityBonds.keyword_to_keyword[keyword] not in EntityBonds.keyword_to_entity.keys()


    def __checkKeywordIsValid(self, keyword : str, entity_identifier = "") :
        if self.__invalidKeyword(keyword) :
            raise ConfigException(code=ConfigExceptionCode.INVALID_KEYWORD,
                                  detail=f"Такое ключевое слово, {keyword} ({entity_identifier}), не предусмотрено")

    
    def __checkReversedKeywordIsValid(self, keyword, entity_identifier = "") :
        if keyword not in EntityBonds.keyword_to_keyword_reversed.keys() :
            raise ParsingException(code=ParsingExceptionCode.INVALID_ENTITY_TYPE,
                                   detail=f"Такое ключевое слово, {keyword} ({entity_identifier}), для вставки (сущности) не предусмотрено")


    def __haveNoEntityStorage(self, keyword : str) -> bool :
        return self.__storages.get(keyword, None) is None


    def __createStorageIfNotExist(self, keyword : str) :
        if self.__haveNoEntityStorage(keyword) :
            self.__storages[keyword] = EntityStorage(EntityBonds.keyword_to_keyword[keyword])


    def __getStorageByKeyword(self, keyword : str) :
        self.__createStorageIfNotExist(keyword)
        return self.__storages[keyword]


    @methodAsyncDecorator("storage:getEntityByID")
    async def getEntityByID(self, keyword : str, id : int) -> Entity :
        if (store := self.__storages.get(keyword, None)) is not None : # ура, нашли, где применить :=!
            return store.getByID(id)
        else :
            return None


    @methodAsyncDecorator("storage:__checkForeignKeys")
    async def __checkForeignKeys(self, keyword, entity : Entity) :
        for foreign_key in entity.foreignKeys() :
            if not foreign_key : # некоторые поля могут быть необязательными
                continue
            self.__checkReversedKeywordIsValid(foreign_key.entity, f"{keyword}:{entity.id}") # проверить, что поле проверяемое правильно описано >date<: 1
            if not await self.getEntityByID(EntityBonds.keyword_to_keyword_reversed[foreign_key.entity], foreign_key.id) :
                raise ParsingException(code=ParsingExceptionCode.FOREIGN_KEY_DOESNT_EXIST,
                                       detail=f"Для сущности из {keyword}:{entity.id} ссылка {foreign_key.entity}:{foreign_key.id} ссылается на несуществующую позицию")


    @methodAsyncDecorator("storage:__parseTextForInclusions")
    async def __parseTextForInclusionsToLinks(self, keyword, entity : Entity) :
        for text in entity.textsToParseLinks() :
            if not text :
                continue
            for parse_result in InclusionParser.getEntitiesFromString(text) :
                self.__checkReversedKeywordIsValid(parse_result.keyword, f"{keyword}:{entity.id}")

                #if not self.getEntityByID(EntityBonds.keyword_to_keyword_reversed[parse_result.keyword], parse_result.number) :
                #    raise ParsingException(code=ParsingExceptionCode.ENTITY_TO_LINK_DOESNT_EXIST,
                #                           detail=f"Для сущности из {keyword}:{entity.id} ссылка (внутри текста) {parse_result.keyword}:{parse_result.number} ссылается на несуществующую позицию")

                if self.__storages.get(keyword) : 
                    self.__storages[keyword].addLink(entity.id, 
                                                    parse_result.keyword, 
                                                    parse_result.number)

                external_keyword = EntityBonds.keyword_to_keyword_reversed[parse_result.keyword]
                if self.__storages.get(external_keyword) : 
                    self.__storages[external_keyword].addExternalLink(parse_result.number, 
                                                                    EntityBonds.keyword_to_keyword[keyword],
                                                                    entity.id)


    @methodAsyncDecorator("storage:resolveAllLinksInText")
    async def resolveAllLinksInEntitiesTexts(self) :
        """Функция проверяет все входящие ссылки в текстах (определяемых сущностями), добавляет их в классы сущностей"""
        for storage_key, storage_value in self.__storages.items() :
            for entity in storage_value.entities() :
                await self.__parseTextForInclusionsToLinks(storage_key, entity)


    @methodAsyncDecorator("storage:append")
    async def append(self, keyword : str, entity : Entity) :
        self.__checkKeywordIsValid(keyword, f"{keyword}:{entity.id}")
        current_storage = self.__getStorageByKeyword(keyword)
        await self.__checkForeignKeys(keyword, entity)
        current_storage.append(entity)


    @methodAsyncDecorator("storage:appendBond")
    async def appendBond(self, entity : Bond) :
        if isinstance(entity, Bond):
            self.__bonds.update({entity.event:entity})
            return


    def __str__(self) -> str :
        string = "{|\n\n"
        for v in self.__storages.values() :
            string += v.__str__() + "\n\n"
        return string + "\n\n" + self.__bonds.__str__() + "\n\n" + "|}"


    @methodAsyncDecorator("storage:getStorages")
    async def getStorages(self) :
        return self.__storages


class EntityStorage :
    """
        Класс хранилища для сущности.
            Определяет основные операции с массивом сущностей.
            Логика по keyword заранее определена, требует лишь выбора. 
                (т.к. разные сущности требуют разного подхода, в частности, с PK и FK)
    """

    def __init__(self, keyword) :
        self.keyword = keyword
        self.__checkKeywordIsValid(self.keyword)
        self.type : Entity = EntityBonds.keyword_to_entity[keyword]
        self.store : dict[int, self.type] = {}
        logger.debug("Создание экземпляра класса EntityStorage")


    def __invalidKeyword(self, keyword : str) -> bool :
        return keyword not in EntityBonds.keyword_to_keyword.values() or \
               keyword not in EntityBonds.keyword_to_entity.keys()


    def __checkKeywordIsValid(self, keyword : str) :
        if self.__invalidKeyword(keyword) :
            raise ConfigException(code=ConfigExceptionCode.INVALID_KEYWORD,
                                  detail=f"Такое ключевое слово, {keyword}, для сущности не предусмотрено")


    def __checkEntityIsValidType(self, entity : Entity) :
        if not isinstance(entity, self.type) :
            raise ParsingException(code=ParsingExceptionCode.INVALID_ENTITY_TYPE,
                                   detail=f"Тип сущности {type(entity)} не соответствует типу хранилища {self.type}")


    def append(self, entity : Entity) :
        self.__checkEntityIsValidType(entity)
        self.store[entity.id] = entity


    def getByID(self, id : int) -> Entity | None :
        return self.store.get(id, None)


    def addLink(self, id : int, link_keyword : str, link_id : int) :
        """Для сущности ID добавить, что ОНА ссылается на link_keyword:link_id"""
        entity = self.getByID(id)
        if entity : 
            if entity.links.get(link_keyword) :
                entity.links[link_keyword].add(link_id)
            else :
                entity.links[link_keyword] = set([link_id])


    def addExternalLink(self, id : int, link_keyword : str, link_id : int) :
        """Для сущности ID добавить, что на него ссылается сущность link_keyword:link_id"""
        entity = self.getByID(id)
        if entity : 
            if entity.ex_links.get(link_keyword) :
                entity.ex_links[link_keyword].add(link_id)
            else :
                entity.ex_links[link_keyword] = set([link_id])


    def entities(self) -> list[Entity]:
        return self.store.values()


    def __str__(self) :
        return f"{self.keyword} : [{self.store}]"