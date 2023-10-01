from fastapi import FastAPI, HTTPException, status
from config import configure_logger
from os import system
from api.schemas import Ping, PostSQL
#######################

api = FastAPI()

@api.on_event("startup")
def onStartup() :
    configure_logger()


# TODO: пути до файлов, конфигурации (репарса например) и пр. в query
# TODO: ручки для проверки доступности других серверов

@api.get("/ping",
         tags=["common"],
         name="ping?",
         response_model=Ping)
async def getRoot() -> Ping:
    """
        Проверить работоспособность сервиса
    """
    return Ping(result="pong!")


@api.post("process/yaml/validate",
          tags=["TODO"],
          name="validate-yaml",
          response_model=Ping)
async def postValidatorYaml() -> Ping:
    """
        Запустить процесс валидации yaml-файлов.
            Будет проверять поля на правильность.
    """
    return Ping(result="pong!") # TODO


@api.post("process/yaml/parse",
          tags=["TODO"],
          name="parse-yaml",
          response_model=Ping)
async def postParserYaml() -> Ping:
    """
        Запустить процесс парсинга yaml-файлов.
            Входное условие: поля должны быть валидны
    """
    return Ping(result="pong!") # TODO



@api.post("process/sql/generate",
          tags=["TODO"],
          name="generate-sql",
          response_model=PostSQL)
async def postGeneratorSQL() -> PostSQL:
    """  
        Запустить полный процесс (валидация->парсинг->генерация) 
            получения SQL-запроса на FTP-сервере
    """
    try : 
        res = PostSQL(result=system("sql-generate -v"))
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Непредвиденная ошибка! exc={exc}")
    if res.result != 0 :
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Непредвиденная ошибка! Статус-кол {res.result}")
    return res
