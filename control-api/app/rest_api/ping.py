"""
    Файл с методами пропинговки всех связанных с текущим REST
        сервисами.
"""
from fastapi import APIRouter, Request

from app.schemas.Ping import PongReponse
from app.grpc_client.NoSQLDatabaseAPIgRPCClient import NoSQLDatabaseAPIgRPCClient
from app.grpc_client.FileAPIgRPCCLient import FileAPIgRPCCLient
from app.rest_api.log_and_except import log_and_except


ping = APIRouter(prefix="/ping")

@ping.get("/",
         tags=["ping"],
         name="ping?",
         response_model=PongReponse,
         description="Проверить работоспособность REST")
@log_and_except("/ping")
async def getPingRoot(request : Request) -> PongReponse:
    return PongReponse(pong="pong", 
                       service="control-api-REST")

@ping.get("/nosql-database-api",
         tags=["ping"],
         name="ping?",
         response_model=PongReponse,
         description="Проверить работоспособность gRPC-сервера с NoSQL базой данных")
@log_and_except("/ping/nosql-database-api")
async def getPingNoSQLDatabaseAPI(request : Request) -> PongReponse:
    return PongReponse(pong=(await NoSQLDatabaseAPIgRPCClient.Ping()).pong, 
                       service="nosql-database-api-GRPC")

@ping.get("/file-api",
         tags=["ping"],
         name="ping?",
         response_model=PongReponse,
         description="Проверить работоспособность gRPC-сервера с FileAPI")
@log_and_except("/ping/file-api")
async def getPingFileAPI(request : Request) -> PongReponse:
    return PongReponse(pong=(await FileAPIgRPCCLient.Ping()).pong, 
                       service="file-api-GRPC")