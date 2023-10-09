"""
    Файл логики gRPC-сервера
"""
import grpc
import proto.nosql_database_api_pb2 as pb2
import proto.nosql_database_api_pb2_grpc as pb2_grpc

from utils.logger import logger


class NoSQLDatabaseAPIServicer(pb2_grpc.NoSQLDatabaseAPIServicer) :
    """
        Логика сервера (сервисер))
    """
    
    def Ping(self, request : pb2.PingRequest, context : grpc.ServicerContext):
        try : 
            logger.info("[gRPC] | Ping")
            return pb2.PingResponse(pong="Pong!")
        # тест
        except Exception as exc:
            context.set_code(grpc.StatusCode.ABORTED)
            return pb2.PingResponse(pong="Pong!")