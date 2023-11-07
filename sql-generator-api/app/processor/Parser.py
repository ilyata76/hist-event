"""
    Парсинг в NoSQL-схемы
"""
from entity.Storage import Storage
from processor.AbstractProcessor import AbstractProcessor as Processor
from schemas.File import FileBase, FileBinaryKeyword


class Parser(Processor) :
    """
        Аккумулирующий парсерную функцию приложения класс.
            Работает со Storage, файлами и Entity-классами.
    """

    def __init__(self, storage : Storage) :
        self.storage = storage
        super().__init__()


    @Processor.methodDecorator("parser:readAndParseFileEntities")
    async def readAndParseFileEntities(self, file : FileBinaryKeyword) :
        pass
        # for entity in 
            # storage.save()
            # ссылки перекрестные обработка
        # end
        # try except