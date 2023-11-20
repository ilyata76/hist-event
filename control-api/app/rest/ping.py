"""
    Файл с методами пропинговки всех связанных с текущим REST
        сервисами.
"""
from fastapi import APIRouter, Request

from app.schemas import PongService
from app.grpc_client import *

from .restMethodAsyncDecorator import restMethodAsyncDecorator


ping = APIRouter(prefix="/ping")


@ping.get("/",
         tags=["ping"], name="ping?",
         response_model=PongService,
         description="Проверить работоспособность REST")
@restMethodAsyncDecorator
async def getPingRoot(request : Request) -> PongService :
    return PongService(pong="pong", service="control-api")


@ping.get("/nosql-database-api",
         tags=["ping"], name="ping?",
         response_model=PongService,
         description="Проверить работоспособность gRPC-сервера с NoSQL базой данных")
@restMethodAsyncDecorator
async def getPingNoSQLDatabaseAPI(request : Request) -> PongService :
    return await NoSQLDatabaseAPIgRPCClient.Ping()


@ping.get("/file-api",
         tags=["ping"], name="ping?",
         response_model=PongService,
         description="Проверить работоспособность gRPC-сервера с FileAPI")
@restMethodAsyncDecorator
async def getPingFileAPI(request : Request) -> PongService :
    return await FileAPIgRPCCLient.Ping()


@ping.get("/sql-generator",
         tags=["ping"], name="ping?",
         response_model=PongService,
         description="Проверить работоспособность gRPC-сервера с SQL Generator")
@restMethodAsyncDecorator
async def getPingSQLGeneratorAPI(request : Request) -> PongService :
    return await SQLGeneratorAPIgRPCClient.Ping()