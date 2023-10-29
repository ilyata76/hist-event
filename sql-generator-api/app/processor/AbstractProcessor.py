"""
    Абстрактный процессор
"""
from entity.Entity import Entity, Date, Person, Place, Biblio, BiblioFragment,\
                        Source, SourceFragment, Event, Other
from utils.logger import logger
from utils.config import LogCode, EntityKeyword


class AbstractProcessor :

    # для добавления новых сущностей - достаточно после их описания
    # добавить сюда, в словари, связанные с ними соотношения

    keyword_to_keyword : dict[str, str] = {
        EntityKeyword.dates : EntityKeyword.DATE,
        EntityKeyword.persons : EntityKeyword.PERSON,
        EntityKeyword.places : EntityKeyword.PLACE,
        EntityKeyword.biblios : EntityKeyword.BIBLIO,
        EntityKeyword.biblio_fragments : EntityKeyword.BIBLIO_FRAGMENT,
        EntityKeyword.sources : EntityKeyword.SOURCE,
        EntityKeyword.source_fragments : EntityKeyword.SOURCE_FRAGMENT,
        EntityKeyword.events : EntityKeyword.EVENT,
        EntityKeyword.others : EntityKeyword.OTHER
    } # словарь соответствия: какая сущность будет описываться внутри тэга ключа (dates: - ожидается DATE)
    keyword_to_entity : dict[str, Entity] = {
        EntityKeyword.DATE : Date,
        EntityKeyword.PERSON : Person,
        EntityKeyword.PLACE : Place,
        EntityKeyword.BIBLIO : Biblio,
        EntityKeyword.BIBLIO_FRAGMENT : BiblioFragment,
        EntityKeyword.SOURCE : Source,
        EntityKeyword.SOURCE_FRAGMENT : SourceFragment,
        EntityKeyword.EVENT : Event,
        EntityKeyword.OTHER : Other
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