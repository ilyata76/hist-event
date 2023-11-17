from loguru._logger import Logger, _defaults


class MyLogger(Logger) :

    def __init__(self, *args, **kwargs) :
        super().__init__(*args, **kwargs)
        self.level("PENDING", 
                   _defaults.env("LOGURU_PENDING_NO", int, _defaults.LOGURU_DEBUG_NO + 1),
                   _defaults.LOGURU_TRACE_COLOR,
                   _defaults.LOGURU_DEBUG_ICON)
        self.level("PENDING_PROCESS", 
                   _defaults.env("LOGURU_PENDING_PROCESS_NO", int, _defaults.LOGURU_DEBUG_NO + 2),
                   _defaults.LOGURU_TRACE_COLOR,
                   _defaults.LOGURU_TRACE_ICON)
        self.level("SUCCESS_PROCESS", 
                   _defaults.env("LOGURU_SUCCESS_PROCESS_NO", int, _defaults.LOGURU_SUCCESS_NO + 1),
                   _defaults.LOGURU_SUCCESS_COLOR,
                   _defaults.LOGURU_SUCCESS_ICON)
        self.level("ERROR_PROCESS", 
                   _defaults.env("LOGURU_ERROR_PROCESS_NO", int, _defaults.LOGURU_ERROR_NO + 1),
                   _defaults.LOGURU_ERROR_COLOR,
                   _defaults.LOGURU_ERROR_ICON)


    def __log(self, level : str, from_decorator : bool, options, msg, args, kwargs) :
        msg = msg.__str__().replace("\n", " ")
        return self._log(level, from_decorator, options, msg, args, kwargs)


    def pending(self, msg, *args, **kwargs) :
        return self.__log("PENDING", False, self._options , msg, args, kwargs)

    def success(self, msg, *args, **kwargs):
        return self.__log("SUCCESS", False, self._options, msg, args, kwargs)

    def pendingProcess(self, msg, *args, **kwargs) :
        return self.__log("PENDING_PROCESS", False, self._options , msg, args, kwargs)

    def successProcess(self, msg, *args, **kwargs) :
        return self.__log("SUCCESS_PROCESS", False, self._options , msg, args, kwargs)

    def errorProcess(self, msg, *args, **kwargs) :
        return self.__log("ERROR_PROCESS", False, self._options , msg, args, kwargs)
