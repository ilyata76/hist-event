"""
    Файл управления самим gRPC сервером
"""
from concurrent import futures
from asyncio import CancelledError

import grpc
import proto.nosql_database_api_pb2_grpc as pb2_grpc

from logger import logger
from config import config

from .NoSQLDatabaseAPIServicer import NoSQLDatabaseAPIServicer


class NoSQLDatabaseAPIgRPCServer :
    """
        Управление сервером
    """
    
    def __init__(self, ip : str = config.GRPC_HOST, port : str = config.GRPC_PORT):
        logger.debug("Создание экземпляра класса управления gRPC сервером")
        self._server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=config.GRPC_MAX_WORKERS))
        logger.info("Привязка к gRPC серверу сервиса NoSQLDatabaseAPIservicer")
        pb2_grpc.add_NoSQLDatabaseAPIServicer_to_server(NoSQLDatabaseAPIServicer(), self._server)
        self._port = port
        self._ip = ip
        self._server.add_insecure_port(self._ip + ":" + self._port)


    async def serve(self) :
        """
            Запустить сервер
        """
        try : 
            await self._server.start()
            logger.info(f"Сервер был запущен на {self._ip}:{self._port}")
            await self._server.wait_for_termination()
        except (KeyboardInterrupt, CancelledError) :
            logger.info("Сервер был принудительно остановлен")
        except BaseException as exc :
            logger.critical(f"Произошла непредвиденная ошибка с сервером : {type(exc)}:{exc}")
            logger.exception(f"Произошла непредвиденная ошибка с сервером : {type(exc)}:{exc}")