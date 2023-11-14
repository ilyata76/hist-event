"""
    Файл для настройки и конфигурации логгера.
        делает logger
"""

class LogCode :
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"


logger_configured = False

if not logger_configured :

    import sys

    from utils.config import config as _config

    first_message = []

    try : 
        from loguru._logger import Logger, Core, Level, _defaults

        class MyLogger(Logger) :

            def __init__(self, *args, **kwargs) :
                super().__init__(*args, **kwargs)
                self.level("PENDING_PROCESS", 
                           _defaults.env("LOGURU_PENDING_NO", int, _defaults.LOGURU_DEBUG_NO + 1),
                           _defaults.LOGURU_TRACE_COLOR,
                           _defaults.LOGURU_TRACE_ICON)
                self.level("SUCCESS_PROCESS", 
                           _defaults.env("LOGURU_SUCCESS_NO", int, _defaults.LOGURU_SUCCESS_NO + 1),
                           _defaults.LOGURU_SUCCESS_COLOR,
                           _defaults.LOGURU_SUCCESS_ICON)
                self.level("ERROR_PROCESS", 
                           _defaults.env("LOGURU_ERROR_NO", int, _defaults.LOGURU_ERROR_NO + 1),
                           _defaults.LOGURU_ERROR_COLOR,
                           _defaults.LOGURU_ERROR_ICON)

            def __log(self, level : str, from_decorator : bool, 
                                            options, msg, args, kwargs) :
                msg = msg.__str__().replace("\n", " ")
                return self._log(level, from_decorator, options, msg, args, kwargs)

            def pendingProcess(self, msg, *args, **kwargs) :
                return self.__log("PENDING_PROCESS", False, self._options , msg, args, kwargs)

            def successProcess(self, msg, *args, **kwargs) :
                return self.__log("SUCCESS_PROCESS", False, self._options , msg, args, kwargs)

            def errorProcess(self, msg, *args, **kwargs) :
                return self.__log("ERROR_PROCESS", False, self._options , msg, args, kwargs)


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