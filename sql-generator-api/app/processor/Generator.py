"""
    Генерация SQL
"""
from processor.AbstractProcessor import AbstractProcessor as Processor
from entity.Storage import StorageManager, EntityStorage
from entity.Entity import *
from entity.EntityBonds import EntityBonds


class Generator(Processor) :
    """
        Аккумулирующий генераторную функцию приложения класс.
            Работает со Storage, файлами и Entity-классами.
    """

    def __init__(self, storage : StorageManager) :
        self.storage = storage
        super().__init__()


    def __getEntityByCommonKeyword(self, keyword : str) :
        keyword = EntityBonds.keyword_to_keyword[keyword]
        return EntityBonds.keyword_to_entity[keyword]


    def __dropTableIfExists(self, keyword : str) :
        return self.__getEntityByCommonKeyword(keyword).dropTableIfExists()


    def __createTable(self, keyword : str) :
        return self.__getEntityByCommonKeyword(keyword).createTable()


    def __fillTable(self, keyword : str, storage : EntityStorage) :
        string = self.__getEntityByCommonKeyword(keyword).insertIntoTableHead() + "\n"
        values = []
        for entity in storage.entities() :
            values.append(entity.insertIntoTableValue())
        string += ",\n".join(values) + ";\n"
        return string


    @Processor.methodAsyncDecorator("generator:readAndGenerateSQLFromStorage")
    async def readAndGenerateSQLFromStorage(self) -> str :
        string = "BEGIN;\n"
        for keyword, storage in (await self.storage.getStorages()).items() :
            string += self.__dropTableIfExists(keyword) + "\n"
            string += self.__createTable(keyword) + "\n"
            string += self.__fillTable(keyword, storage)
        return string + "COMMIT;"