"""
    Валидация входных сущностей на правильность заполнения
"""
from utils.logger import logger
from schemas.File import FileBinaryKeyword
from utils.dict_from import dictFromYaml
from utils.exception import ConfigException, ConfigExceptionCode
from processor.AbstractProcessor import AbstractProcessor as Processor
from entity.EntityBonds import EntityBonds


class Validator(Processor) :
    """
        Аккумулирующий валидирующую функцию приложения класс.
            Работает со Storage, файлами и Entity-классами.
    """

    def __init__(self) :
        logger.debug("Создание экземпляра класса Validator")
        super().__init__()


    def __invalidKeyword(self, keyword : str) :
        return keyword not in EntityBonds.keyword_to_keyword.keys() or \
               EntityBonds.keyword_to_keyword[keyword] not in EntityBonds.keyword_to_entity.keys()


    def __checkKeywordIsValid(self, keyword : str) :
        if self.__invalidKeyword(keyword) :
            raise ConfigException(code=ConfigExceptionCode.INVALID_KEYWORD,
                                  detail=f"Такое ключевое слово, {keyword}, не предусмотрено")


    @Processor.methodDecorator("validator:__validateEntity")
    async def __validateEntity(self, dict_entity : dict, keyword : str, entity_index : int) :
        """
            Валидация конкретной сущности.
            Выбрасывает исключение, если какая-то сущность не может быть провалидирована.
        """
        entity = EntityBonds.keyword_to_entity[keyword]
        entity.validate(f"{keyword}:{entity_index+1}", dict_entity)


    @Processor.methodDecorator("validator:readAndValidateFileEntities")
    async def readAndValidateFileEntities(self, file : FileBinaryKeyword) :
        """
            Валидация всех сущностей входящих в файл по keyword.
            Выбрасывает исключение, если какая-то сущность не может быть провалидирована.
        """
        self.__checkKeywordIsValid(file.keyword)
        
        yaml = dictFromYaml(file.file, file.keyword)
        for index, entity in enumerate(yaml) :
            await self.__validateEntity(entity, EntityBonds.keyword_to_keyword[file.keyword], index)
