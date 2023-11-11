"""
    Роутер для работы с генератором SQL
"""
from fastapi import APIRouter, Request

from app.schemas.File import FileKeyword
from app.schemas.StatusIdentifier import Status, StatusIdentifier
from app.grpc_client.SQLGeneratorAPIgRPCClient import SQLGeneratorAPIgRPCClient
from app.rest_api.log_and_except import log_and_except


sql_generator = APIRouter(prefix="/sql-gen")

@sql_generator.put("/validate/{operation}",
                   tags=["process"],
                   name="Валидация YAML",
                   response_model=str,
                   description="Проверить, являюстя ли валидными переданные YAML-файлы")
@log_and_except
async def SQLGeneratorValidate(request : Request,
                               operation : str,
                               files : list[FileKeyword]) -> str :
    response = await SQLGeneratorAPIgRPCClient.Validate(files, operation)
    return response.status

@sql_generator.put("/parse/{operation}",
                   tags=["process"],
                   name="Парсинг YAML",
                   response_model=str,
                   description="Пропарсить YAML-файлы с последующим сохранением результатов в NoSQL (файлы должны быть валидны)")
@log_and_except
async def SQLGeneratorParse(request : Request,
                            operation : str,
                            files : list[FileKeyword]) -> str :
    response = await SQLGeneratorAPIgRPCClient.Parse(files, operation)
    return response.status

@sql_generator.put("/generate/{operation}",
                   tags=["process"],
                   name="Генерасия SQL-файла",
                   response_model=str,
                   description="Сгенерировать SQL-файл из сущностей после /parse/operation")
@log_and_except
async def SQLGeneratorGenerate(request : Request,
                               operation : str,
                               files : list[FileKeyword]) -> str :
    response = await SQLGeneratorAPIgRPCClient.Generate(files, operation)
    return response.status

@sql_generator.get("/status/{identifier}")
@log_and_except
async def GetSQLGeneratorStatus(request : Request,
                                identifier : str) -> StatusIdentifier :
    response = await SQLGeneratorAPIgRPCClient.GetSQLGeneratorStatus(identifier)
    return StatusIdentifier(identifier=response.identifier,
                            status=response.status)

@sql_generator.put("/status/{identifier}")
@log_and_except
async def PutSQLGeneratorStatus(request : Request,
                                identifier : str,
                                status : Status) -> StatusIdentifier :
    response = await SQLGeneratorAPIgRPCClient.PutSQLGeneratorStatus(identifier, status.status)
    return StatusIdentifier(identifier=response.identifier,
                            status=response.status)