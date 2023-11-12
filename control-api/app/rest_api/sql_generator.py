"""
    Роутер для работы с генератором SQL
"""
from fastapi import APIRouter, Request

from app.schemas.File import FileBaseKeyword
from app.schemas.StatusIdentifier import Status, StatusIdentifier
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

@sql_generator.put("/parse/{operation}",
                   tags=["process"],
                   name="Парсинг YAML",
                   response_model=StatusIdentifier,
                   description="Пропарсить YAML-файлы с последующим сохранением результатов в NoSQL (файлы должны быть валидны)")
@log_and_except
async def SQLGeneratorParse(request : Request,
                            operation : str) -> StatusIdentifier :
    response = await SQLGeneratorAPIgRPCClient.Parse(operation)
    return StatusIdentifier(**dict_from_message(response))

@sql_generator.put("/generate/{operation}",
                   tags=["process"],
                   name="Генерасия SQL-файла",
                   response_model=StatusIdentifier,
                   description="Сгенерировать SQL-файл из сущностей после /parse/operation")
@log_and_except
async def SQLGeneratorGenerate(request : Request,
                               operation : str) -> StatusIdentifier :
    response = await SQLGeneratorAPIgRPCClient.Generate(operation)
    return StatusIdentifier(**dict_from_message(response))

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

@sql_generator.put("/files/{identifier}")
@log_and_except
async def GetSQLGeneratorFiles(request : Request,
                               identifier : str) -> list[FileBaseKeyword] :
    response = await SQLGeneratorAPIgRPCClient.GetSQLGeneratorFiles(identifier)
    return [FileBaseKeyword(**dict_from_message(file)) for file in response.files]