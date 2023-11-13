"""
    Роутер для работы с генератором SQL
"""
from fastapi import APIRouter, Request

from app.schemas.File import FileBaseKeyword, File
from app.schemas.StatusIdentifier import StatusIdentifier
from app.grpc_client.SQLGeneratorAPIgRPCClient import SQLGeneratorAPIgRPCClient
from app.rest_api.log_and_except import log_and_except
from app.utils.dict_from_message import dict_from_message


sql_generator = APIRouter(prefix="/sql-gen")


@sql_generator.put("/validate",
                   tags=["process"],
                   name="Валидация YAML",
                   response_model=StatusIdentifier,
                   description="Проверить, являюстя ли валидными переданные YAML-файлы")
@log_and_except
async def SQLGeneratorValidate(request : Request,
                               files : list[FileBaseKeyword]) -> StatusIdentifier :
    response = await SQLGeneratorAPIgRPCClient.Validate(files)
    return StatusIdentifier(**dict_from_message(response))


@sql_generator.put("/parse-generate/{operation}",
                   tags=["process"],
                   name="Парсинг YAML и генерация SQL",
                   response_model=StatusIdentifier,
                   description="Пропарсить YAML-файлы и получить SQL-файл")
@log_and_except
async def SQLGeneratorParseAndGenerate(request : Request,
                                       operation : str) -> StatusIdentifier :
    response = await SQLGeneratorAPIgRPCClient.ParseAndGenerate(operation)
    return StatusIdentifier(**dict_from_message(response))


@sql_generator.get("/status/{identifier}")
@log_and_except
async def GetSQLGeneratorStatus(request : Request,
                                identifier : str) -> StatusIdentifier :
    response = await SQLGeneratorAPIgRPCClient.GetSQLGeneratorStatus(identifier)
    return StatusIdentifier(identifier=response.identifier,
                            status=response.status)


@sql_generator.get("/files/{identifier}")
@log_and_except
async def GetSQLGeneratorFiles(request : Request,
                               identifier : str) -> list[FileBaseKeyword] :
    response = await SQLGeneratorAPIgRPCClient.GetSQLGeneratorFiles(identifier)
    return [FileBaseKeyword(**dict_from_message(file)) for file in response.files]


@sql_generator.get("/sql/{identifier}")
@log_and_except
async def GetSQLGeneratorFiles(request : Request,
                               identifier : str) -> File :
    response = await SQLGeneratorAPIgRPCClient.GetSQLGeneratorSQLFile(identifier)
    return File(**dict_from_message(response.file), filename="main.sql")