from fastapi import FastAPI, HTTPException, status, Depends
from config import configure_logger, logs_folder, latest_stdout_cli_filename,\
      yaml_folder, sql_folder, ConfigPathKeywords
from os import system
from api.schemas import Ping, PostProcess
from functools import wraps
#######################

api = FastAPI()

@api.on_event("startup")
def onStartup() :
    configure_logger()


def getParams(reparse : int = 10,
              yaml_folder : str = yaml_folder,
              sql_folder : str = sql_folder,
              dates_file : str = yaml_folder.joinpath(ConfigPathKeywords.dates_default_path),
              persons_file : str = yaml_folder.joinpath(ConfigPathKeywords.persons_default_path),
              places_file : str = yaml_folder.joinpath(ConfigPathKeywords.places_default_path),
              sources_file : str = yaml_folder.joinpath(ConfigPathKeywords.sources_default_path),
              others_file : str = yaml_folder.joinpath(ConfigPathKeywords.others_default_path),
              events_file : str = yaml_folder.joinpath(ConfigPathKeywords.events_default_path),
              biblios_file : str = yaml_folder.joinpath(ConfigPathKeywords.biblios_default_path),
              bonds_file : str = yaml_folder.joinpath(ConfigPathKeywords.bonds_default_path),
              main_sql_file : str = sql_folder.joinpath(ConfigPathKeywords.main_sql_default_path)) :
    params = " ".join( [f"--reparse {reparse}", f"--main-sql-file {main_sql_file}",
                        f"--sql-folder {sql_folder}", f"--bonds-file {bonds_file}", 
                        f"--biblios-file {biblios_file}", f"--events-file {events_file}",
                        f"--others-file {others_file}", f"--sources-file {sources_file}",
                        f"--places-file {places_file}", f"--persons-file {persons_file}",
                        f"--dates-file {dates_file}", f"--yaml-folder {yaml_folder}"] )
    return params


@api.get("/ping",
         tags=["common"],
         name="ping?",
         response_model=Ping)
async def getRoot() -> Ping:
    """
        Проверить работоспособность сервиса
    """
    return Ping(result="pong!")


@api.post("/process/yaml/validate",
          tags=["process"],
          name="validate-yaml",
          response_model=PostProcess)
async def postValidatorYaml(params = Depends(getParams)) -> PostProcess:
    """
        Запустить процесс валидации yaml-файлов.
            Будет проверять поля на правильность.
    """
    command = ["sql-generate", "validate", params]
    res_code = system(" ".join(command))
    res_stdout = open(logs_folder.joinpath(latest_stdout_cli_filename), "rb").read()
    return PostProcess(result=res_code, stdout=res_stdout)



@api.post("/process/yaml/parse",
          tags=["process"],
          name="parse-yaml",
          response_model=PostProcess)
async def postParserYaml(params = Depends(getParams)) -> PostProcess:
    """
        Запустить процесс парсинга yaml-файлов.
            Входное условие: поля должны быть валидны
    """
    command = ["sql-generate", "parse", params]
    res_code = system(" ".join(command))
    res_stdout = open(logs_folder.joinpath(latest_stdout_cli_filename), "rb").read()
    return PostProcess(result=res_code, stdout=res_stdout)


@api.post("/process/sql/generate",
          tags=["process"],
          name="generate-sql",
          response_model=PostProcess)
async def postGeneratorSQL(params = Depends(getParams),
                           no_validate : bool = False,
                           no_parse : bool = False) -> PostProcess:
    """  
        Запустить полный процесс (валидация->парсинг->генерация) 
            получения SQL-запроса на FTP-сервере
    """
    try : 
        command = ["sql-generate", "full", params]

        if no_validate :
            command.append("--no-validate")
        if no_parse :
            command.append("--no-parse")

        res_code = system(" ".join(command))
        res_stdout = open(logs_folder.joinpath(latest_stdout_cli_filename), "rb").read()

        return PostProcess(result=res_code, stdout=res_stdout)
    
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail=f"Непредвиденная ошибка! [{exc}]")