"""
    Файл, отвечающий за генерацию SQL-файла или запроса
        для базы данных, её генерации
"""
from loguru import logger
from schemas.Storages import Storages

################### ГЛАВНЫЙ ПРОЦЕСС

def generateSQL(storages : Storages) -> str | None:
    """
        Главная функция процесса создания SQL-запроса
    """
    try : 
        logger.info("\n\nНАЧАЛО ГЕНЕРАЦИИ SQL (УДАЛЕНИЕ ТАБЛИЦ)\n\n")
        result = "-- УДАЛИТЬ ТАБЛИЦЫ, если те существуют\n\n"
        result += storages.dropTablesSQL() + "\n\n"
        result += "-- СОЗДАТЬ ТАБЛИЦЫ \n\n"
        logger.info("СОЗДАНИЕ ТАБЛИЦ SQL")
        result += storages.generateTablesSQL() + "\n\n"
        result += "-- ЗАПОЛНИТЬ ТАБЛИЦЫ \n\n"
        logger.info("ЗАПОЛНЕНИЕ ТАБЛИЦ SQL")
        result += storages.fillTablesSQL() + "\n\n"
        logger.info("КОНЕЦ ГЕНЕРАЦИИ SQL")
        return result
    except :
        return None