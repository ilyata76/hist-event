# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import app.proto.sql_generator_api_pb2 as sql__generator__api__pb2


class SQLGeneratorAPIStub(object):
    """долгий синхронный процесс (последовательный обход сущностей),
    выделенный в отдельный сервис
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Ping = channel.unary_unary(
                '/sql_generator_api.SQLGeneratorAPI/Ping',
                request_serializer=sql__generator__api__pb2.PingR.SerializeToString,
                response_deserializer=sql__generator__api__pb2.PongR.FromString,
                )
        self.Validate = channel.unary_unary(
                '/sql_generator_api.SQLGeneratorAPI/Validate',
                request_serializer=sql__generator__api__pb2.ManyFilesR.SerializeToString,
                response_deserializer=sql__generator__api__pb2.Status.FromString,
                )
        self.Parse = channel.unary_unary(
                '/sql_generator_api.SQLGeneratorAPI/Parse',
                request_serializer=sql__generator__api__pb2.ManyFilesR.SerializeToString,
                response_deserializer=sql__generator__api__pb2.Status.FromString,
                )
        self.Generate = channel.unary_unary(
                '/sql_generator_api.SQLGeneratorAPI/Generate',
                request_serializer=sql__generator__api__pb2.ManyFilesR.SerializeToString,
                response_deserializer=sql__generator__api__pb2.Status.FromString,
                )


class SQLGeneratorAPIServicer(object):
    """долгий синхронный процесс (последовательный обход сущностей),
    выделенный в отдельный сервис
    """

    def Ping(self, request, context):
        """проверить работоспособность
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Validate(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Parse(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Generate(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_SQLGeneratorAPIServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Ping': grpc.unary_unary_rpc_method_handler(
                    servicer.Ping,
                    request_deserializer=sql__generator__api__pb2.PingR.FromString,
                    response_serializer=sql__generator__api__pb2.PongR.SerializeToString,
            ),
            'Validate': grpc.unary_unary_rpc_method_handler(
                    servicer.Validate,
                    request_deserializer=sql__generator__api__pb2.ManyFilesR.FromString,
                    response_serializer=sql__generator__api__pb2.Status.SerializeToString,
            ),
            'Parse': grpc.unary_unary_rpc_method_handler(
                    servicer.Parse,
                    request_deserializer=sql__generator__api__pb2.ManyFilesR.FromString,
                    response_serializer=sql__generator__api__pb2.Status.SerializeToString,
            ),
            'Generate': grpc.unary_unary_rpc_method_handler(
                    servicer.Generate,
                    request_deserializer=sql__generator__api__pb2.ManyFilesR.FromString,
                    response_serializer=sql__generator__api__pb2.Status.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'sql_generator_api.SQLGeneratorAPI', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class SQLGeneratorAPI(object):
    """долгий синхронный процесс (последовательный обход сущностей),
    выделенный в отдельный сервис
    """

    @staticmethod
    def Ping(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/sql_generator_api.SQLGeneratorAPI/Ping',
            sql__generator__api__pb2.PingR.SerializeToString,
            sql__generator__api__pb2.PongR.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Validate(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/sql_generator_api.SQLGeneratorAPI/Validate',
            sql__generator__api__pb2.ManyFilesR.SerializeToString,
            sql__generator__api__pb2.Status.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Parse(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/sql_generator_api.SQLGeneratorAPI/Parse',
            sql__generator__api__pb2.ManyFilesR.SerializeToString,
            sql__generator__api__pb2.Status.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Generate(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/sql_generator_api.SQLGeneratorAPI/Generate',
            sql__generator__api__pb2.ManyFilesR.SerializeToString,
            sql__generator__api__pb2.Status.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
