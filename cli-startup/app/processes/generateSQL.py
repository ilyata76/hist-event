"""
    Файл, отвечающий за генерацию SQL-файла или запроса
        для базы данных, её генерации
"""
from loguru import logger
from schemas import Storages

################### ГЛАВНЫЙ ПРОЦЕСС

def generateSQL(storages : Storages) -> str | None:
    """
        Главная функция процесса создания SQL-запроса
    """
    try : 
        logger.info("\n\nНАЧАЛО ГЕНЕРАЦИИ SQL (УДАЛЕНИЕ ТАБЛИЦ)\n\n")
        result = "\n-- УДАЛИТЬ ТАБЛИЦЫ, если те существуют\n\n"
        result += "BEGIN;\n\n"
        result += storages.dropTablesSQL() + "\n\n"
        result += "COMMIT;\n\n"
        result += "\n-- СОЗДАТЬ ТАБЛИЦЫ \n\n"
        logger.info("СОЗДАНИЕ ТАБЛИЦ SQL")
        result += "BEGIN;\n\n"
        result += storages.generateTablesSQL() + "\n\n"
        result += "COMMIT;\n\n"
        result += "\n-- ЗАПОЛНИТЬ ТАБЛИЦЫ \n\n"
        logger.info("ЗАПОЛНЕНИЕ ТАБЛИЦ SQL")
        result += "BEGIN;\n\n"
        result += storages.fillTablesSQL() + "\n\n"
        result += "COMMIT;\n\n"
        logger.info("КОНЕЦ ГЕНЕРАЦИИ SQL")
        return result
    except Exception as exc:
        logger.error("При генерации SQL произошла ошибка exc={exc}", exc=exc)
        return None