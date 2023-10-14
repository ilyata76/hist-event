"""
    Файл для настройки и конфигурации логгера.
        делает logger
"""
logger_configured = False

if not logger_configured :
    
    import sys

    from app.utils.config import config as _config
    
    first_message = []

    try : 
        from loguru._logger import Logger, Core

        class MyLogger(Logger) :
            pass

        # украдено из loguru.__init__
        logger = MyLogger(core=Core(), exception=None, depth=0,
                          record=False, lazy=False, colors=False, raw=False, 
                          capture=True, patchers=[], extra={})
        first_message.append("Логгер был абстрагирован от библиотеки успешно")

    except BaseException as exc :
        from loguru import logger
        logger.remove(0)
        first_message.append("Логгер не смог быть абстрагированным от библиотеки => был взят библиотечный.")

    # теперь сконфигурируем логгер

    level = "DEBUG" if _config.LOG_DEBUG else "INFO"
    logger.add(_config.LOG_FOLDER.joinpath(_config.LOG_FILENAME), 
                format="{time} {level} {message}", level=level, rotation="4 MB", compression="zip")

    if _config.LOG_CONSOLE :
        logger.add(sys.stdout, level=level)
    else : 
        logger.add(sys.stderr, level="ERROR")

    logger_configured = True
    first_message.append(f"Логгер был сконфигурирован для LOG_DEBUG:{_config.LOG_DEBUG} и LOG_CONSOLE:{_config.LOG_CONSOLE}")

    for msg in first_message :
        logger.debug(msg)