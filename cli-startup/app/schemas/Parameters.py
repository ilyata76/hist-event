"""
    Схемы или классы, оперирующими всеми остальными схемами
"""
from schemas.Date import DateStorage
from schemas.Source import SourceStorage
from schemas.Place import PlaceStorage
from schemas.Person import PersonStorage
from schemas.Other import OtherStorage
from schemas.Event import EventStorage


class Storages() :
    """
        Хранилище хранилищей
    """
    
    def __init__(self, 
                 source_storage : SourceStorage,
                 date_storage : DateStorage, 
                 place_storage : PlaceStorage,
                 person_storage : PersonStorage,
                 other_storage : OtherStorage,
                 event_storage : EventStorage ) :
        self.source_storage = source_storage
        self.date_storage = date_storage
        self.place_storage = place_storage
        self.person_storage = person_storage
        self.other_storage = other_storage
        self.event_storage = event_storage


    def __str__(self) -> str:
        """
            Для принтов и логов
        """
        string = "\n" + str(self.source_storage) + "\n"
        string += "\n" + str(self.date_storage) + "\n"
        string += "\n" + str(self.place_storage) + "\n"
        string += "\n" + str(self.person_storage) + "\n"
        string += "\n" + str(self.other_storage) + "\n"
        string += "\n" + str(self.event_storage) + "\n"
        return string