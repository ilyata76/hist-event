"""
    Валидация входных сущностей на правильность заполнения
"""
from utils.logger import logger
from schemas.File import FileBase, FileKeywordList, FileBinaryKeyword
from entity.Entity import Entity
from utils.dict_from import dictFromYaml
from utils.exception import ConfigException, ConfigExceptionCode
from processor.AbstractProcessor import AbstractProcessor
from grpc_client.FileAPIgRPCCLient import FileAPIgRPCCLient


class Validator :
    """
        Аккумулирующий валидирующую функцию приложения класс.
            Работает со Storage, файлами и Entity-классами.
    """

    def __init__(self) :
        logger.debug("Создание экземпляра класса Validator")
        self.keyword_to_keyword : dict[str, str] = AbstractProcessor.keyword_to_keyword
        self.keyword_to_entity : dict[str, Entity] = AbstractProcessor.keyword_to_entity


    @AbstractProcessor.method("validator:__validateEntity")
    async def __validateEntity(self, dict_entity : dict, keyword : str, entity_index : int) :
        """
            Валидация конкретной сущности.
            Выбрасывает исключение, если какая-то сущность не может быть провалидирована.
        """
        self.keyword_to_entity[keyword].validate(f"{keyword}:{entity_index+1}", dict_entity)


    @AbstractProcessor.method("validator:__validateFile")
    async def __validateFile(self, file : FileBinaryKeyword) :
        """
            Валидация всех сущностей входящих в файл по keyword.
            Выбрасывает исключение, если какая-то сущность не может быть провалидирована.
        """
        if file.keyword not in self.keyword_to_keyword.keys() or \
           self.keyword_to_keyword[file.keyword] not in self.keyword_to_entity.keys() :
            raise ConfigException(code=ConfigExceptionCode.INVALID_KEYWORD,
                                  detail=f"Такое ключевое слово, {file.keyword}, не предусмотрено")
        try : 
            yaml = dictFromYaml(file.file, file.keyword)
            for index, entity in enumerate(yaml) :
                await self.__validateEntity(entity, self.keyword_to_keyword[file.keyword], index)
        except KeyError as exc :
            raise ConfigException(code=ConfigExceptionCode.INVALID_KEYWORD,
                                  detail=f"Невозможно взять значение по ключу {exc.args}")


    @AbstractProcessor.method("validator:validateFiles")
    async def validateFiles(self, files : FileKeywordList) :
        """
            Валидация входящих файлов сущностей по их ключевым словам.
            Выбрасывает исключение, если какая-то сущность не может быть провалидирована.
        """
        for file in files.files :
            file_binary = await FileAPIgRPCCLient.GetFile(file=FileBase(path=file.path, 
                                                                        storage=file.storage))
            await self.__validateFile(file=FileBinaryKeyword(**file_binary.model_dump(),
                                                             keyword=file.keyword))