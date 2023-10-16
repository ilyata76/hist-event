"""
    Файл управления базой данных файлов
"""
from database.DBClient import DBClient, MongoDBClient
from database.AbstractDB import AbstractDB, AbstractMongoDB
from schemas.File import File, FileBase
from schemas.Range import Range
from utils.logger import logger
from utils.config import config, FILE_KEY, DATABASE_PATH_PATH,\
      StorageCollection, StorageIdentifier
from utils.exception import DBException, DBExceptionCode


class FileDB(AbstractDB) :
    """
        Абстрактный репозиторий базы данных файлов с CRUD методами.
        
        Мы не храним бинарные файлы, этим занимается ftp-сервер, здесь
            мы храним лишь пути до них и данные им имена.
    """

    def __init__(self, client : DBClient) :
        logger.debug("Создание экземпляра класса FileDB")
        super().__init__(client)

    @AbstractDB.method
    async def appendOne(self, file : File) -> File | None :
        raise DBException(code=DBExceptionCode.METHOD_NOT_REALIZED, detail="FileDB не реализует метод append!")

    @AbstractDB.method
    async def putOne(self, file : File) -> File | None :
        raise DBException(code=DBExceptionCode.METHOD_NOT_REALIZED, detail="FileDB не реализует метод put!")

    @AbstractDB.method
    async def deleteOne(self, file : FileBase) -> File | None :
        raise DBException(code=DBExceptionCode.METHOD_NOT_REALIZED, detail="FileDB не реализует метод delete!")

    @AbstractDB.method
    async def getOne(self, file : FileBase) -> File | None :
        raise DBException(code=DBExceptionCode.METHOD_NOT_REALIZED, detail="FileDB не реализует метод get!")

    @AbstractDB.method
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

    @AbstractMongoDB.method
    async def appendOne(self, file : File) -> File | None :
        """
            Добавить в базу метаинформацию о файле.
            Если файл существует, выбрасывает исключение.
            storage_indentifier - можно отдельно хранить файлы s3 и ftp, например.
        """
        logger.debug(f"Добавление нового файла в базу данных FileMongoDB[{file.storage}]: {file.path}")
        res = None

        async with await self.client.client.start_session() as s :
            exist = await self.db[file.storage].find_one({DATABASE_PATH_PATH: str(file.path)}, session=s)
            if exist :
                raise DBException(code=DBExceptionCode.ENTITY_EXISTS, detail="Такой уже существует!")
            
            added = await self.db[file.storage].insert_one({FILE_KEY: file.model_dump()}, session=s)
            res = await self.db[file.storage].find_one({"_id": added.inserted_id}, session=s)

        logger.info(f"Был добавлен файл {file} в FileMongoDB[{file.storage}]: {res['_id']}")
        return File(**res[FILE_KEY]) if res else res

    @AbstractMongoDB.method
    async def putOne(self, file : File) -> File | None :
        """
            Заменить или создать информацию о файле.
        """
        logger.debug(f"Изменение/добавление файла в базе данных FileMongoDB[{file.storage}]: {file.path}")
        res = None

        async with await self.client.client.start_session() as s :
            res = await self.db[file.storage].find_one_and_replace({DATABASE_PATH_PATH : str(file.path)}, 
                                                                   {FILE_KEY: file.model_dump()}, 
                                                                   session=s)
            if not res : 
                added = await self.db[file.storage].insert_one({FILE_KEY: file.model_dump()}, session=s)
                res = await self.db[file.storage].find_one({"_id": added.inserted_id}, session=s)

        logger.info(f"Был добавлен/заменён файл {file} в FileMongoDB[{file.storage}]: {res['_id']}")
        return File(**res[FILE_KEY]) if res else res
    
    @AbstractMongoDB.method
    async def deleteOne(self, file : FileBase) -> File | None:
        """
            Удалить информацию о файле.
            Если его не существует, поднимается исключение.
        """
        logger.debug(f"Удаление файла из базе данных FileMongoDB[{file.storage}]: {file.path}")
        res = None

        async with await self.client.client.start_session() as s :
            res = await self.db[file.storage].find_one({DATABASE_PATH_PATH : str(file.path)}, session=s)
            if not res :
                raise DBException(code=DBExceptionCode.ENTITY_DONT_EXISTS, detail="Сущности для удаления не существует!")
            await self.db[file.storage].delete_one({"_id": res["_id"]}, session=s)

        file = File(**res[FILE_KEY]) if res else None
        logger.info(f"Был удалён файл {file} в FileMongoDB[{file.storage}]: {res['_id']}")
        return file
    
    @AbstractMongoDB.method
    async def getOne(self, file : FileBase) -> File | None:
        """
            Взять файл, если тот существует.
            Если его не существует, поднимается исключение
        """
        logger.debug(f"Взятие файла из базы данных FileMongoDB[{file.storage}]: {file.path}")
        res = None

        async with await self.client.client.start_session() as s :
            res = await self.db[file.storage].find_one({DATABASE_PATH_PATH : str(file.path)}, session=s)
            if not res :
                raise DBException(code=DBExceptionCode.ENTITY_DONT_EXISTS, detail="Сущности не существует!")

        file = File(**res[FILE_KEY]) if res else None
        logger.info(f"Был возвращёт из базы файл {file} в FileMongoDB[{file.storage}]: {res['_id']}")
        return file
    
    @AbstractMongoDB.method
    async def getMany(self, range : Range, 
                      storage_identifier : str = StorageIdentifier.FTP) -> list[File] | None :
        """
            Вернуть список с start_pos в количестве limit документов-файлов.
        """
        logger.debug(f"Взятие файлов из базы данных FileMongoDB[{StorageCollection.get(storage_identifier)}] с {range.start} до {range.end}")
        res = []
        if not range.end :
            range.end = 10

        async with await self.client.client.start_session() as s :
            collection = self.db[StorageCollection.get(storage_identifier)].find({}, session=s).skip(range.start).limit(range.end-range.start)
            if not collection :
                return DBException(code=DBExceptionCode.ENTITY_DONT_EXISTS, detail="Ни одной сущности не существует!")
            for doc in await collection.to_list(length=range.end-range.start):
                res.append(File(**doc[FILE_KEY]))

        logger.info(f"Было возвращено {len(res) if res else 0} файлов из базы в FileMongoDB[{StorageCollection.get(storage_identifier)}]")
        return res