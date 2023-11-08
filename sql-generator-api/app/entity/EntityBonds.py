"""
    Связи между ключевыми словами, сущностями и пр.
"""
from entity.Entity import *
from utils.config import EntityKeyword as EK


class EntityBonds :

    keyword_to_keyword : dict[str, str] = {
        EK.dates : EK.DATE,
        EK.persons : EK.PERSON,
        EK.places : EK.PLACE,
        EK.biblios : EK.BIBLIO,
        EK.biblio_fragments : EK.BIBLIO_FRAGMENT,
        EK.sources : EK.SOURCE,
        EK.source_fragments : EK.SOURCE_FRAGMENT,
        EK.events : EK.EVENT,
        EK.others : EK.OTHER
    } # словарь соответствия: какая сущность будет описываться внутри тэга ключа (dates: - ожидается DATE)

    keyword_to_keyword_reversed : dict[str, str] = { v:k for k,v in keyword_to_keyword.items() }
    keyword_to_keyword_reversed.update({EK.AUTHOR : EK.persons})

    keyword_to_entity : dict[str, Entity] = {
        EK.DATE : Date,
        EK.PERSON : Person,
        EK.PLACE : Place,
        EK.BIBLIO : Biblio,
        EK.BIBLIO_FRAGMENT : BiblioFragment,
        EK.SOURCE : Source,
        EK.SOURCE_FRAGMENT : SourceFragment,
        EK.EVENT : Event,
        EK.OTHER : Other
    } # словарь соответствия между keyword и классом сущности.