"""
    Файл управления базой данных файлов
"""
from logger import logger
from config import *
from schemas import *
from utils.exception import *

from .DBClient import DBClient, MongoDBClient
from .AbstractDB import AbstractDB, AbstractMongoDB


class FileDB(AbstractDB) :
    """
        Абстрактный репозиторий базы данных файлов с CRUD методами.
        
        Мы не храним бинарные файлы, этим занимается ftp-сервер, здесь
            мы храним лишь пути до них и данные им имена.
    """

    def __init__(self, client : DBClient) :
        logger.debug("Создание экземпляра класса FileDB")
        super().__init__(client)


    @AbstractDB.methodAsyncDecorator("fileDB:appendOne")
    async def appendOne(self, file : File) -> File | None :
        raise DBException(code=DBExceptionCode.METHOD_NOT_REALIZED, detail="FileDB не реализует метод append!")


    @AbstractDB.methodAsyncDecorator("fileDB:putOne")
    async def putOne(self, file : File) -> File | None :
        raise DBException(code=DBExceptionCode.METHOD_NOT_REALIZED, detail="FileDB не реализует метод put!")


    @AbstractDB.methodAsyncDecorator("fileDB:deleteOne")
    async def deleteOne(self, file : FileBase) -> File | None :
        raise DBException(code=DBExceptionCode.METHOD_NOT_REALIZED, detail="FileDB не реализует метод delete!")


    @AbstractDB.methodAsyncDecorator("fileDB:getOne")
    async def getOne(self, file : FileBase) -> File | None :
        raise DBException(code=DBExceptionCode.METHOD_NOT_REALIZED, detail="FileDB не реализует метод get!")


    @AbstractDB.methodAsyncDecorator("fileDB:getMany")
    async def getMany(self, range : Range, storage_identifier : str) -> list[File] | None :
        raise DBException(code=DBExceptionCode.METHOD_NOT_REALIZED, detail="FileDB не реализует метод getAll!")


class FileMongoDB(FileDB) :
    """
        Реализация базы данных файлов через MongoDB(Client).
        Каждый метод независим от других (т.е. не использует ничего, кроме методов работы с MongoDB)
    """

    def __init__(self, client : MongoDBClient) :
        logger.debug("Создание экземпляра класса FileMongoDB")
        super().__init__(client=client)
        self.db = self.client.client[config.DATABASE_FILES_DB]


    @AbstractMongoDB.methodAsyncDecorator("fileMongoDB:appendOne")
    async def appendOne(self, file : File) -> File | None :
        """
            Добавить в базу метаинформацию о файле.
            Если файл существует, выбрасывает исключение.
            storage_indentifier - можно отдельно хранить файлы s3 и ftp, например.
        """
        res = None

        async with await self.client.client.start_session() as s :
            exist = await self.db[file.storage].find_one({DATABASE_PATH_PATH: file.path.as_posix()}, session=s)
            if exist :
                raise DBException(code=DBExceptionCode.ENTITY_EXISTS, 
                                  detail=f"Такой уже, {file.path.as_posix()}, существует!")
            
            added = await self.db[file.storage].insert_one({FILE_KEY: file.model_dump()}, session=s)
            res = await self.db[file.storage].find_one({"_id": added.inserted_id}, session=s)

        return File(**res[FILE_KEY]) if res else res


    @AbstractMongoDB.methodAsyncDecorator("fileMongoDB:putOne")
    async def putOne(self, file : File) -> File | None :
        """
            Заменить или создать информацию о файле.
        """
        res = None

        async with await self.client.client.start_session() as s :
            res = await self.db[file.storage].find_one_and_replace({DATABASE_PATH_PATH : file.path.as_posix()}, 
                                                                   {FILE_KEY: file.model_dump()}, 
                                                                   session=s)
            if not res : 
                added = await self.db[file.storage].insert_one({FILE_KEY: file.model_dump()}, session=s)
                res = await self.db[file.storage].find_one({"_id": added.inserted_id}, session=s)

        return File(**res[FILE_KEY]) if res else res


    @AbstractMongoDB.methodAsyncDecorator("fileMongoDB:deleteOne")
    async def deleteOne(self, file : FileBase) -> File | None:
        """
            Удалить информацию о файле.
            Если его не существует, поднимается исключение.
        """
        res = None

        async with await self.client.client.start_session() as s :
            res = await self.db[file.storage].find_one({DATABASE_PATH_PATH : file.path.as_posix()}, session=s)
            if not res :
                raise DBException(code=DBExceptionCode.ENTITY_DONT_EXISTS, detail=
                                  f"Сущности для удаления {file.path.as_posix()} не существует!")
            await self.db[file.storage].delete_one({"_id": res["_id"]}, session=s)

        return File(**res[FILE_KEY]) if res else None


    @AbstractMongoDB.methodAsyncDecorator("fileMongoDB:getOne")
    async def getOne(self, file : FileBase) -> File | None:
        """
            Взять файл, если тот существует.
            Если его не существует, поднимается исключение
        """
        res = None

        async with await self.client.client.start_session() as s :
            res = await self.db[file.storage].find_one({DATABASE_PATH_PATH : file.path.as_posix()}, session=s)
            if not res :
                raise DBException(code=DBExceptionCode.ENTITY_DONT_EXISTS, 
                                  detail=f"Сущности {file.path.as_posix()} не существует!")

        return File(**res[FILE_KEY]) if res else None


    @AbstractMongoDB.methodAsyncDecorator("fileMongoDB:getMany")
    async def getMany(self, range : Range, storage : Identifier = StorageIdentifier.FTP) -> list[File] | None :
        """
            Вернуть список с start_pos в количестве limit документов-файлов.
        """
        res = []
        if not range.end :
            range.end = 10

        async with await self.client.client.start_session() as s :
            collection = self.db[storage].find({}, session=s).skip(range.start).limit(range.end-range.start)
            if not collection :
                return DBException(code=DBExceptionCode.ENTITY_DONT_EXISTS, detail="Ни одной сущности не существует!")
            for doc in await collection.to_list(length=range.end-range.start):
                res.append(File(**doc[FILE_KEY]))

        return res