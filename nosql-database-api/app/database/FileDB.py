"""
    Файл управления базой данных файлов
"""
from database.DBClient import DBClient, MongoDBClient
from database.AbstractDB import AbstractDB, AbstartMongoDB
from schemas.File import File
from utils.logger import logger
from utils.config import config, FILE_KEY, DATABASE_FILENAME_PATH
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

    @AbstractDB.DBMethodDecorator
    async def appendOne(self, file : File, storage_identifier : str) -> File | None :
        logger.error("FileDB не реализует метод append!")
        raise DBException(code=DBExceptionCode.METHOD_NOT_REALIZED, detail="FileDB не реализует метод append!")

    @AbstractDB.DBMethodDecorator
    async def putOne(self, filename : str, file : File, storage_identifier : str) -> File | None :
        logger.error("FileDB не реализует метод put!")
        raise DBException(code=DBExceptionCode.METHOD_NOT_REALIZED, detail="FileDB не реализует метод put!")

    @AbstractDB.DBMethodDecorator
    async def deleteOne(self, filename : str, storage_identifier : str) -> File | None :
        logger.error("FileDB не реализует метод delete!")
        raise DBException(code=DBExceptionCode.METHOD_NOT_REALIZED, detail="FileDB не реализует метод delete!")

    @AbstractDB.DBMethodDecorator
    async def getOne(self, filename : str, storage_identifier : str) -> File | None :
        logger.error("FileDB не реализует метод get!")
        raise DBException(code=DBExceptionCode.METHOD_NOT_REALIZED, detail="FileDB не реализует метод get!")

    @AbstractDB.DBMethodDecorator
    async def getMany(self, start_pos : int, length : int, storage_identifier : str) -> list[File] | None :
        logger.error("FileDB не реализует метод getAll!")
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

    @AbstartMongoDB.MongoDBMethodDecorator
    async def appendOne(self, file : File, 
                        storage_identifier : str = config.DATABASE_FTP_FILES_COLLECTION) -> File | None :
        """
            Добавить в базу метаинформацию о файле.
            Если файл существует, выбрасывает исключение.
            storage_indentifier - можно отдельно хранить файлы s3 и ftp, например.
        """
        logger.debug(f"Добавление нового файла в базу данных FileMongoDB[{storage_identifier}]: {file.filename}")
        res = None

        async with await self.client.client.start_session() as s :
            exist = await self.db[storage_identifier].find_one({DATABASE_FILENAME_PATH: file.filename}, session=s)
            if exist :
                raise DBException(code=DBExceptionCode.ENTITY_EXISTS, detail="Такой уже существует!")
            
            added = await self.db[storage_identifier].insert_one({FILE_KEY: file.model_dump()}, session=s)
            res = await self.db[storage_identifier].find_one({"_id": added.inserted_id}, session=s)

        logger.info(f"Был добавлен файл {file} в FileMongoDB[{storage_identifier}]: {res['_id']}")
        return File(**res[FILE_KEY]) if res else res

    @AbstartMongoDB.MongoDBMethodDecorator
    async def putOne(self, filename : str, file : File, 
                     storage_identifier : str = config.DATABASE_FTP_FILES_COLLECTION) -> File | None :
        """
            Заменить или создать информацию о файле.
        """
        logger.debug(f"Изменение/добавление файла в базе данных FileMongoDB[{storage_identifier}]: {filename}")
        res = None

        async with await self.client.client.start_session() as s :
            res = await self.db[storage_identifier].find_one_and_replace({DATABASE_FILENAME_PATH : filename}, 
                                                                                      {FILE_KEY: file.model_dump()}, 
                                                                                      session=s)
            if not res : 
                added = await self.db[storage_identifier].insert_one({FILE_KEY: file.model_dump()}, session=s)
                res = await self.db[storage_identifier].find_one({"_id": added.inserted_id}, session=s)

        logger.info(f"Был добавлен/заменён файл {file} в FileMongoDB[{storage_identifier}]: {res['_id']}")
        return File(**res[FILE_KEY]) if res else res
    
    @AbstartMongoDB.MongoDBMethodDecorator
    async def deleteOne(self, filename: str, 
                        storage_identifier : str = config.DATABASE_FTP_FILES_COLLECTION) -> File | None:
        """
            Удалить информацию о файле.
            Если его не существует, поднимается исключение.
        """
        logger.debug(f"Удаление файла из базе данных FileMongoDB[{storage_identifier}]: {filename}")
        res = None

        async with await self.client.client.start_session() as s :
            res = await self.db[storage_identifier].find_one({DATABASE_FILENAME_PATH : filename}, session=s)
            if not res :
                raise DBException(code=DBExceptionCode.ENTITY_DONT_EXISTS, detail="Сущности для удаления не существует!")
            await self.db[storage_identifier].delete_one({"_id": res["_id"]}, session=s)

        file = File(**res[FILE_KEY]) if res else None
        logger.info(f"Был удалён файл {file} в FileMongoDB[{storage_identifier}]: {res['_id']}")
        return file
    
    @AbstartMongoDB.MongoDBMethodDecorator
    async def getOne(self, filename: str, 
                     storage_identifier : str = config.DATABASE_FTP_FILES_COLLECTION) -> File | None:
        """
            Взять файл, если тот существует.
            Если его не существует, поднимается исключение
        """
        logger.debug(f"Взятие файла из базы данных FileMongoDB[{storage_identifier}]: {filename}")
        res = None

        async with await self.client.client.start_session() as s :
            res = await self.db[storage_identifier].find_one({DATABASE_FILENAME_PATH : filename}, session=s)
            if not res :
                raise DBException(code=DBExceptionCode.ENTITY_DONT_EXISTS, detail="Сущности не существует!")

        file = File(**res[FILE_KEY]) if res else None
        logger.info(f"Был возвращёт из базы файл {file} в FileMongoDB[{storage_identifier}]: {res['_id']}")
        return file
    
    @AbstartMongoDB.MongoDBMethodDecorator
    async def getMany(self, start_pos : int, limit: int, 
                      storage_identifier : str = config.DATABASE_FTP_FILES_COLLECTION) -> list[File] | None :
        """
            Вернуть список с start_pos в количестве limit документов-файлов.
        """
        logger.debug(f"Взятие файлов из базы данных FileMongoDB[{storage_identifier}] с {start_pos} в количестве до {limit}")
        res = []

        async with await self.client.client.start_session() as s :
            collection = self.db[storage_identifier].find({}, session=s).skip(start_pos)
            if limit :
                collection = collection.limit(limit)
            if not collection :
                return DBException(code=DBExceptionCode.ENTITY_DONT_EXISTS, detail="Ни одной сущности не существует!")
            for doc in await collection.to_list(length=limit):
                res.append(File(**doc[FILE_KEY]))

        logger.info(f"Было возвращено {len(res) if res else 0} файлов из базы в FileMongoDB[{storage_identifier}]")
        return res