"""
    Файл логики gRPC-сервера
"""
import grpc
import proto.file_api_pb2 as pb2
import proto.file_api_pb2_grpc as pb2_grpc

from grpc_server.AbstractServicer import AbstractServicer


class FileAPIServicer(pb2_grpc.FileAPIServicer) :
    """
        Логика сервера (сервисер))
    """
    
    @AbstractServicer.method("file-api:/ping")
    async def Ping(self, request : pb2.PingRequest, context : grpc.ServicerContext) :
        return pb2.PingResponse(pong="pong")