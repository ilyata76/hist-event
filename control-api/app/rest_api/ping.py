"""
    Файл с методами пропинговки всех связанных с текущим REST
        сервисами.
"""
from fastapi import APIRouter, Request

from app.schemas.Ping import PongReponse
from app.grpc_client.NoSQLDatabaseAPIgRPCClient import NoSQLDatabaseAPIgRPCClient
from app.grpc_client.FileAPIgRPCCLient import FileAPIgRPCCLient
from app.grpc_client.SQLGeneratorAPIgRPCClient import SQLGeneratorAPIgRPCClient
from app.rest_api.log_and_except import log_and_except


ping = APIRouter(prefix="/ping")

@ping.get("/",
         tags=["ping"],
         name="ping?",
         response_model=PongReponse,
         description="Проверить работоспособность REST")
@log_and_except
async def getPingRoot(request : Request) -> PongReponse:
    return PongReponse(pong="pong", 
                       service="control-api-REST")

@ping.get("/nosql-database-api",
         tags=["ping"],
         name="ping?",
         response_model=PongReponse,
         description="Проверить работоспособность gRPC-сервера с NoSQL базой данных")
@log_and_except
async def getPingNoSQLDatabaseAPI(request : Request) -> PongReponse:
    return PongReponse(pong=(await NoSQLDatabaseAPIgRPCClient.Ping()).pong, 
                       service="nosql-database-api-GRPC")

@ping.get("/file-api",
         tags=["ping"],
         name="ping?",
         response_model=PongReponse,
         description="Проверить работоспособность gRPC-сервера с FileAPI")
@log_and_except
async def getPingFileAPI(request : Request) -> PongReponse:
    return PongReponse(pong=(await FileAPIgRPCCLient.Ping()).pong, 
                       service="file-api-GRPC")

@ping.get("/sql-generator",
         tags=["ping"],
         name="ping?",
         response_model=PongReponse,
         description="Проверить работоспособность gRPC-сервера с SQL Generator")
@log_and_except
async def getPingSQLGeneratorAPI(request : Request) -> PongReponse:
    return PongReponse(pong=(await SQLGeneratorAPIgRPCClient.Ping()).pong, 
                       service="sql-generator-api-GRPC")