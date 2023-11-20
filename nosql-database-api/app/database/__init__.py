# здесь заканчивается абстракция баз данных
from config import DATABASE_IP

from .DBClient import MongoDBClient
from .FileDB import FileMongoDB
from .SQLGeneratorDB import SQLGeneratorMongoDB


client = MongoDBClient(uri=DATABASE_IP)
files = FileMongoDB(client=client)
sql_gen = SQLGeneratorMongoDB(client=client)