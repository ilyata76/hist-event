# здесь заканчивается абстракция баз данных

from database.DBClient import MongoDBClient
from database.FileDB import FileMongoDB
from database.SQLGeneratorDB import SQLGeneratorMongoDB
from utils.config import config

client = MongoDBClient(uri=config.DATABASE_URI)
files = FileMongoDB(client=client)
sql_gen = SQLGeneratorMongoDB(client=client)