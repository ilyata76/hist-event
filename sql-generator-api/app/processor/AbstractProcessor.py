"""
    Абстрактный процессор
"""
from entity.Entity import Entity, Date
from utils.logger import logger
from utils.config import LogCode, EntityKeyword


class AbstractProcessor :

    keyword_to_keyword : dict[str, str] = {
        EntityKeyword.dates : EntityKeyword.DATE
    } # словарь соответствия: какая сущность будет описываться внутри тэга ключа (dates: - ожидается DATE)
    keyword_to_entity : dict[str, Entity] = {
        EntityKeyword.DATE : Date
    } # словарь соответствия между keyword и классом сущности.


    @staticmethod
    def method(path : str) :
        """
            Декоратор, который обрабатывает исключения и берёт на себя логирование
                функций главных процессов
        """
        def processorMethod(function) :
            async def wrap(self, *args, **kwargs) :
                try : 
                    logger.debug(f"[PROCESSOR] : {path} : {args} : {kwargs} : {LogCode.PENDING}")
                    res = await function(self, *args, **kwargs)
                    logger.info(f"[PROCESSOR] : {path} : {args} : {kwargs} : {LogCode.SUCCESS}")
                    return res
                except BaseException as exc :
                    logger.error(f"[PROCESSOR] : {path} : {args} : {kwargs} : {LogCode.ERROR}")
                    raise exc
            return wrap
        return processorMethod