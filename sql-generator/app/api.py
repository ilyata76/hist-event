from fastapi import FastAPI
from config import configure_logger
#######################

api = FastAPI()

@api.on_event("startup")
def onStartup() :
    configure_logger()


@api.get("/")
def getRoot() :
    return "Hello!"