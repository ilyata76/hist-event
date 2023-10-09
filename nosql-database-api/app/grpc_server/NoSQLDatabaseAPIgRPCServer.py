"""
    Файл управления самим gRPC сервером
"""
from concurrent import futures
from grpc import server

import proto.nosql_database_api_pb2_grpc as pb2_grpc
from grpc_server.NoSQLDatabaseAPIServicer import NoSQLDatabaseAPIServicer
from utils.logger import logger


class NoSQLDatabaseAPIgRPCServer :
    """
        Управление сервером
    """
    
    def __init__(self, ip : str, port : str): # conf
        logger.debug("Создание экземпляра класса управления gRPC сервером")
        self._server = server(futures.ThreadPoolExecutor(max_workers=10)) # c
        logger.info("Привязка к gRPC серверу сервиса NoSQLDatabaseAPIservicer")
        pb2_grpc.add_NoSQLDatabaseAPIServicer_to_server(NoSQLDatabaseAPIServicer(), self._server)
        self._port = port
        self._ip = ip
        self._server.add_insecure_port(self._ip + ":" + self._port)

    def serve(self) :
        """
            Запустить сервер
        """
        try : 
            self._server.start()
            logger.info(f"Сервер был запущен на {self._ip}:{self._port}")
            self._server.wait_for_termination()
        except KeyboardInterrupt as exc:
            logger.info("Сервер был принудительно остановлен")