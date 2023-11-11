"""
    Генерация SQL
"""
from processor.AbstractProcessor import AbstractProcessor as Processor
from entity.Storage import StorageManager


class Generator(Processor) :
    """
        Аккумулирующий генераторную функцию приложения класс.
            Работает со Storage, файлами и Entity-классами.
    """

    def __init__(self, storage : StorageManager) :
        self.storage = storage
        super().__init__()


    @Processor.methodAsyncDecorator("generator:readAndGenerateSQLFromStorage")
    async def readAndGenerateSQLFromStorage(self) :
        pass