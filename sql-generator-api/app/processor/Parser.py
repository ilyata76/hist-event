"""
    Парсинг в NoSQL-схемы
"""
from entity.Storage import StorageManager
from entity.EntityBonds import EntityBonds
from entity.Entity import Entity, Bond
from processor.AbstractProcessor import AbstractProcessor as Processor
from schemas.File import FileBinaryKeyword, FileKeyword, FileBase, FileBinary
from utils.exception import *
from utils.dict_from import dictFromYaml
from utils.config import config, EntityKeyword
from utils.validate import *


class Parser(Processor) :
    """
        Аккумулирующий парсерную функцию приложения класс.
            Работает со Storage, файлами и Entity-классами.
    """

    def __init__(self, storage : StorageManager) :
        self.storage = storage
        super().__init__()


    def __invalidKeyword(self, keyword : str) :
        return keyword not in EntityBonds.keyword_to_keyword.keys() or \
               EntityBonds.keyword_to_keyword[keyword] not in EntityBonds.keyword_to_entity.keys()


    def __checkKeywordIsValid(self, keyword : str) :
        if self.__invalidKeyword(keyword) :
            raise ConfigException(code=ConfigExceptionCode.INVALID_KEYWORD,
                                  detail=f"Такое ключевое слово, {keyword}, не предусмотрено")


    @Processor.methodAsyncDecorator("parser:__appendEntityAndStoreErrors")
    async def __appendEntityAndStoreErrors(self, errors : list , keyword : str, entity : Entity) :
        """Собирает детали исключений в массив, чтобы в любом случае пройти по всем сущностям"""
        try : 
            await self.storage.append(keyword, entity)
        except ParsingException as exc:
            match exc.code :
                case ParsingExceptionCode.FOREIGN_KEY_DOESNT_EXIST | ParsingExceptionCode.ENTITY_TO_LINK_DOESNT_EXIST :
                    errors.append(exc.detail)
                case _ :
                    raise exc


    @Processor.methodAsyncDecorator("parser:__readAndParseFileEntitiesAndSaveInStorage")
    async def readAndParseFileEntitiesAndSaveInStorage(self, file : FileBinaryKeyword) :
        """Поднимает исключение, если произошли ошибки ссылок"""
        self.__checkKeywordIsValid(file.keyword)
        yaml = dictFromYaml(file.file, file.keyword)
        entity_keyword = EntityBonds.keyword_to_keyword[file.keyword]
        errors = [] # массив ошибок, который, если наберётся, будет рэйзить исключение
        for entity_dict in yaml :
            entity = EntityBonds.keyword_to_entity[entity_keyword](**entity_dict)
            await self.__appendEntityAndStoreErrors(errors, file.keyword, entity)
        # если есть ошибки, поднимаем исключение (так нужно, чтобы всё равно пройти все сущности)
        if errors :
            raise ParsingException(code=ParsingExceptionCode.LINKS_ERRORS_WHILE_PARSING,
                                   detail=errors.__str__())


    @Processor.methodAsyncDecorator("parser:parseFilesRecursiveToFillStorage")
    async def parseFilesRecursiveToFillStorage(self, getFile, files : list[FileKeyword], iterator = 0) :
        """Рекурсивно проходит все файлы несколько раз, чтобы добавлять новые сущности разной глубины вложенности"""
        errors = []
        files_with_errors = []

        for file in files :
            file_binary = await getFile(file=FileBase(path=file.path,  
                                                      storage=file.storage)) # некрасиво как-то смотрится, зато инкапсулирована логика
            try : 
                await self.readAndParseFileEntitiesAndSaveInStorage(file=FileBinaryKeyword(**file_binary.model_dump(),
                                                                                             keyword=file.keyword))
            except ParsingException as exc:
                match exc.code : 
                    case ParsingExceptionCode.LINKS_ERRORS_WHILE_PARSING :
                        errors.append(exc.detail)
                        files_with_errors.append(file)
                    case _ :
                        raise exc

        if len(errors) > 0:
            if iterator < config.MAX_ITERATION_PARSE :
                return await self.parseFilesRecursiveToFillStorage(getFile, files_with_errors, iterator + 1)
            else :
                raise ParsingException(code=ParsingExceptionCode.LINKS_ERRORS_WHILE_PARSING,
                                       detail=errors.__str__() + f" (итераций: {iterator + 1})")


    @Processor.methodAsyncDecorator("parser:resolveAllLinksInEntitiesTexts")
    async def resolveAllLinksInEntitiesTexts(self) :
        """
            Функция проверяет все входящие ссылки в текстах (определяемых сущностями), добавляет их в классы сущностей.
            Требуется заполненное внутреннее хранилище!
        """
        return await self.storage.resolveAllLinksInEntitiesTexts()


    @Processor.methodAsyncDecorator("parser:parseAndResolveEventBondsFileToStorage")
    async def parseAndResolveEventBondsFileToStorage(self, getFile, file : FileKeyword) :
        """После всех действий нужно образовать связи между ивентами. Связи отдельно."""
        if file.keyword != EntityKeyword.bonds :
            raise ParsingException(code=ParsingExceptionCode.INVALID_ENTITY_TYPE,
                                   detail=f"Ключевое слово для свящей должно быть {EntityKeyword.bonds}!")
        file_binary = await getFile(file=FileBase(path=file.path, storage=file.storage))
        yaml = dictFromYaml(file_binary.file, file.keyword)

        async def checkEventExist(bond_id: int, event_id : int, busy_events : list[int]) :
            if not await self.storage.getEntityByID(EntityKeyword.events, event_id) :
                raise ParsingException(code=ParsingExceptionCode.ENTITY_TO_LINK_DOESNT_EXIST,
                                       detail=f"Сущность связи {bond_id} ссылается на несуществующее событие {event_id}")
            if event_id in busy_events :
                raise ParsingException(code=ParsingExceptionCode.INVALID_ENTITY_TYPE,
                                       detail=f"Сущность связи {bond_id} имеет неопределённую связь с событием (самоссылка; два или более) - {event_id}")

        for index, dict_bond in enumerate(yaml) :
            bond = Bond(**dict_bond)
            
            await checkEventExist(index, bond.event, [])
            busy_events = [bond.event]
            if bond.parents : 
                for event in bond.parents :
                    await checkEventExist(index, event, busy_events)
            if bond.childs :
                if bond.parents : busy_events.extend(bond.parents)
                for event in bond.childs :
                    await checkEventExist(index, event, busy_events)
            if bond.prerequisites :
                if bond.childs : busy_events.extend(bond.childs)
                if bond.parents and not bond.childs : busy_events.extend(bond.parents)
                for event in bond.prerequisites :
                    await checkEventExist(index, event, busy_events)
            
            await self.storage.appendBond(bond)