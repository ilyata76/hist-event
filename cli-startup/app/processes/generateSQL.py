"""
    Файл, отвечающий за генерацию SQL-файла или запроса
        для базы данных, её генерации
"""
from inspect import cleandoc
from loguru import logger
from schemas import Storages, BondStorage
from config import ConfigKeywords



def eventsAndBonds() :
    """
        Создать представление, в котором будут события с их связями
    """
    return cleandoc(f"""
    DROP VIEW IF EXISTS {ConfigKeywords.eventsbonds} CASCADE;
    DROP VIEW IF EXISTS {ConfigKeywords.bondswithoutid} CASCADE;

    CREATE OR REPLACE VIEW {ConfigKeywords.bondswithoutid}
        AS SELECT {ConfigKeywords.event}, {ConfigKeywords.parents}, {ConfigKeywords.childs}, {ConfigKeywords.prerequisites}
            FROM {ConfigKeywords.bonds}
    ;

    CREATE OR REPLACE VIEW {ConfigKeywords.eventsbonds} 
        AS SELECT * 
            FROM {ConfigKeywords.events} as e
            JOIN {ConfigKeywords.bondswithoutid} as b
                ON e.{ConfigKeywords.id} = b.{ConfigKeywords.event}
    ;
    """)




################### ГЛАВНЫЙ ПРОЦЕСС

def generateSQL(storages : Storages, bond_storage : BondStorage) -> str | None:
    """
        Главная функция процесса создания SQL-запроса
    """
    try : 
        logger.info("\n\nНАЧАЛО ГЕНЕРАЦИИ SQL (УДАЛЕНИЕ ТАБЛИЦ)\n\n")
        result = "\n-- УДАЛИТЬ ТАБЛИЦЫ, если те существуют\n\n"
        result += "BEGIN;\n\n"
        result += storages.dropTablesSQL() + "\n\n"
        result += bond_storage.dropTableSQL() + "\n\n"
        result += "\n-- СОЗДАТЬ ТАБЛИЦЫ \n\n"
        logger.info("СОЗДАНИЕ ТАБЛИЦ SQL")
        result += storages.generateTablesSQL() + "\n\n"
        result += bond_storage.generateTableSQL() + "\n\n"
        result += "\n-- ЗАПОЛНИТЬ ТАБЛИЦЫ \n\n"
        logger.info("ЗАПОЛНЕНИЕ ТАБЛИЦ SQL")
        result += storages.fillTablesSQL() + "\n\n"
        result += bond_storage.fillTableSQL() + "\n\n"
        result += eventsAndBonds() + "\n\n"
        result += "COMMIT;\n\n"
        logger.info("КОНЕЦ ГЕНЕРАЦИИ SQL")
        return result
    except Exception as exc:
        logger.error("При генерации SQL произошла ошибка {t} exc={exc}", t=type(exc), exc=exc)
        return None