"""
    Роутер для работы с генератором SQL
"""
from fastapi import APIRouter, Request

from app.schemas import *
from app.grpc_client import SQLGeneratorAPIgRPCClient
from app.utils import dictFromGoogleMessage

from .restMethodAsyncDecorator import restMethodAsyncDecorator


sql_generator = APIRouter(prefix="/sql-gen")


@sql_generator.put("/validate",
                   tags=["process"], name="Валидация YAML",
                   response_model=StatusIdentifier,
                   description="Проверить, являюстя ли валидными переданные YAML-файлы")
@restMethodAsyncDecorator
async def SQLGeneratorValidate(request : Request,
                               files : FileBaseKeywordList) -> StatusIdentifier :
    return await SQLGeneratorAPIgRPCClient.Validate(files)


@sql_generator.put("/parse-generate/{operation}",
                   tags=["process"], name="Парсинг YAML и генерация SQL",
                   response_model=StatusIdentifier,
                   description="Пропарсить YAML-файлы и получить SQL-файл")
@restMethodAsyncDecorator
async def SQLGeneratorParseAndGenerate(request : Request,
                                       operation : str) -> StatusIdentifier :
    return await SQLGeneratorAPIgRPCClient.ParseAndGenerate(Identifier(operation))


@sql_generator.get("/status/{operation}")
@restMethodAsyncDecorator
async def GetSQLGeneratorStatus(request : Request,
                                operation : str) -> StatusIdentifier :
    return await SQLGeneratorAPIgRPCClient.GetSQLGeneratorStatus(Identifier(operation))


@sql_generator.get("/files/{operation}")
@restMethodAsyncDecorator
async def GetSQLGeneratorFiles(request : Request,
                               operation : str) -> FileBaseKeywordList :
    return await SQLGeneratorAPIgRPCClient.GetSQLGeneratorFiles(Identifier(operation))


@sql_generator.get("/sql/{operation}")
@restMethodAsyncDecorator
async def GetSQLGeneratorFiles(request : Request,
                               operation : str) -> File :
    file_base = await SQLGeneratorAPIgRPCClient.GetSQLGeneratorSQLFile(Identifier(operation))
    return File(**file_base.model_dump(), filename="main.sql")