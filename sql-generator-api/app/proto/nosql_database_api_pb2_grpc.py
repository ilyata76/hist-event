# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import proto.nosql_database_api_pb2 as nosql__database__api__pb2


class NoSQLDatabaseAPIStub(object):
    """сервис работы NoSQL базы данных, используемой различными сервисами, например,
    для запоминания сохранённых файлов на FTP-сервере
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Ping = channel.unary_unary(
                '/nosql_database_api.NoSQLDatabaseAPI/Ping',
                request_serializer=nosql__database__api__pb2.PingR.SerializeToString,
                response_deserializer=nosql__database__api__pb2.PongR.FromString,
                )
        self.AddFileMetaInfo = channel.unary_unary(
                '/nosql_database_api.NoSQLDatabaseAPI/AddFileMetaInfo',
                request_serializer=nosql__database__api__pb2.FileR.SerializeToString,
                response_deserializer=nosql__database__api__pb2.FileR.FromString,
                )
        self.PutFileMetaInfo = channel.unary_unary(
                '/nosql_database_api.NoSQLDatabaseAPI/PutFileMetaInfo',
                request_serializer=nosql__database__api__pb2.FileR.SerializeToString,
                response_deserializer=nosql__database__api__pb2.FileR.FromString,
                )
        self.DeleteFileMetaInfo = channel.unary_unary(
                '/nosql_database_api.NoSQLDatabaseAPI/DeleteFileMetaInfo',
                request_serializer=nosql__database__api__pb2.FileBaseR.SerializeToString,
                response_deserializer=nosql__database__api__pb2.FileR.FromString,
                )
        self.GetFileMetaInfo = channel.unary_unary(
                '/nosql_database_api.NoSQLDatabaseAPI/GetFileMetaInfo',
                request_serializer=nosql__database__api__pb2.FileBaseR.SerializeToString,
                response_deserializer=nosql__database__api__pb2.FileR.FromString,
                )
        self.GetManyFilesMetaInfo = channel.unary_unary(
                '/nosql_database_api.NoSQLDatabaseAPI/GetManyFilesMetaInfo',
                request_serializer=nosql__database__api__pb2.StorageSegmentR.SerializeToString,
                response_deserializer=nosql__database__api__pb2.FileSegmentR.FromString,
                )
        self.PutSQLGeneratorStatus = channel.unary_unary(
                '/nosql_database_api.NoSQLDatabaseAPI/PutSQLGeneratorStatus',
                request_serializer=nosql__database__api__pb2.IdentifierStatusR.SerializeToString,
                response_deserializer=nosql__database__api__pb2.IdentifierStatusR.FromString,
                )
        self.GetSQLGeneratorStatus = channel.unary_unary(
                '/nosql_database_api.NoSQLDatabaseAPI/GetSQLGeneratorStatus',
                request_serializer=nosql__database__api__pb2.IdentifierR.SerializeToString,
                response_deserializer=nosql__database__api__pb2.IdentifierStatusR.FromString,
                )
        self.PutSQLGeneratorFiles = channel.unary_unary(
                '/nosql_database_api.NoSQLDatabaseAPI/PutSQLGeneratorFiles',
                request_serializer=nosql__database__api__pb2.ManyFilesIdentifierR.SerializeToString,
                response_deserializer=nosql__database__api__pb2.IdentifierR.FromString,
                )
        self.GetSQLGeneratorFiles = channel.unary_unary(
                '/nosql_database_api.NoSQLDatabaseAPI/GetSQLGeneratorFiles',
                request_serializer=nosql__database__api__pb2.IdentifierR.SerializeToString,
                response_deserializer=nosql__database__api__pb2.ManyFilesIdentifierR.FromString,
                )


class NoSQLDatabaseAPIServicer(object):
    """сервис работы NoSQL базы данных, используемой различными сервисами, например,
    для запоминания сохранённых файлов на FTP-сервере
    """

    def Ping(self, request, context):
        """проверить работоспособность
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AddFileMetaInfo(self, request, context):
        """сохранить мета-информацию о файле в базе
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def PutFileMetaInfo(self, request, context):
        """сохранить/заменить (запомнить) мета-информацию о файле в базе
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteFileMetaInfo(self, request, context):
        """удалить (забыть) мета-информацию о файле в базе
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetFileMetaInfo(self, request, context):
        """получить мета-информацию файла
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetManyFilesMetaInfo(self, request, context):
        """получить список мета-информацю всех (или отрезком) файлов
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def PutSQLGeneratorStatus(self, request, context):
        """
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetSQLGeneratorStatus(self, request, context):
        """
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def PutSQLGeneratorFiles(self, request, context):
        """
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetSQLGeneratorFiles(self, request, context):
        """
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_NoSQLDatabaseAPIServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Ping': grpc.unary_unary_rpc_method_handler(
                    servicer.Ping,
                    request_deserializer=nosql__database__api__pb2.PingR.FromString,
                    response_serializer=nosql__database__api__pb2.PongR.SerializeToString,
            ),
            'AddFileMetaInfo': grpc.unary_unary_rpc_method_handler(
                    servicer.AddFileMetaInfo,
                    request_deserializer=nosql__database__api__pb2.FileR.FromString,
                    response_serializer=nosql__database__api__pb2.FileR.SerializeToString,
            ),
            'PutFileMetaInfo': grpc.unary_unary_rpc_method_handler(
                    servicer.PutFileMetaInfo,
                    request_deserializer=nosql__database__api__pb2.FileR.FromString,
                    response_serializer=nosql__database__api__pb2.FileR.SerializeToString,
            ),
            'DeleteFileMetaInfo': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteFileMetaInfo,
                    request_deserializer=nosql__database__api__pb2.FileBaseR.FromString,
                    response_serializer=nosql__database__api__pb2.FileR.SerializeToString,
            ),
            'GetFileMetaInfo': grpc.unary_unary_rpc_method_handler(
                    servicer.GetFileMetaInfo,
                    request_deserializer=nosql__database__api__pb2.FileBaseR.FromString,
                    response_serializer=nosql__database__api__pb2.FileR.SerializeToString,
            ),
            'GetManyFilesMetaInfo': grpc.unary_unary_rpc_method_handler(
                    servicer.GetManyFilesMetaInfo,
                    request_deserializer=nosql__database__api__pb2.StorageSegmentR.FromString,
                    response_serializer=nosql__database__api__pb2.FileSegmentR.SerializeToString,
            ),
            'PutSQLGeneratorStatus': grpc.unary_unary_rpc_method_handler(
                    servicer.PutSQLGeneratorStatus,
                    request_deserializer=nosql__database__api__pb2.IdentifierStatusR.FromString,
                    response_serializer=nosql__database__api__pb2.IdentifierStatusR.SerializeToString,
            ),
            'GetSQLGeneratorStatus': grpc.unary_unary_rpc_method_handler(
                    servicer.GetSQLGeneratorStatus,
                    request_deserializer=nosql__database__api__pb2.IdentifierR.FromString,
                    response_serializer=nosql__database__api__pb2.IdentifierStatusR.SerializeToString,
            ),
            'PutSQLGeneratorFiles': grpc.unary_unary_rpc_method_handler(
                    servicer.PutSQLGeneratorFiles,
                    request_deserializer=nosql__database__api__pb2.ManyFilesIdentifierR.FromString,
                    response_serializer=nosql__database__api__pb2.IdentifierR.SerializeToString,
            ),
            'GetSQLGeneratorFiles': grpc.unary_unary_rpc_method_handler(
                    servicer.GetSQLGeneratorFiles,
                    request_deserializer=nosql__database__api__pb2.IdentifierR.FromString,
                    response_serializer=nosql__database__api__pb2.ManyFilesIdentifierR.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'nosql_database_api.NoSQLDatabaseAPI', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class NoSQLDatabaseAPI(object):
    """сервис работы NoSQL базы данных, используемой различными сервисами, например,
    для запоминания сохранённых файлов на FTP-сервере
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
        return grpc.experimental.unary_unary(request, target, '/nosql_database_api.NoSQLDatabaseAPI/Ping',
            nosql__database__api__pb2.PingR.SerializeToString,
            nosql__database__api__pb2.PongR.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def AddFileMetaInfo(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/nosql_database_api.NoSQLDatabaseAPI/AddFileMetaInfo',
            nosql__database__api__pb2.FileR.SerializeToString,
            nosql__database__api__pb2.FileR.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def PutFileMetaInfo(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/nosql_database_api.NoSQLDatabaseAPI/PutFileMetaInfo',
            nosql__database__api__pb2.FileR.SerializeToString,
            nosql__database__api__pb2.FileR.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteFileMetaInfo(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/nosql_database_api.NoSQLDatabaseAPI/DeleteFileMetaInfo',
            nosql__database__api__pb2.FileBaseR.SerializeToString,
            nosql__database__api__pb2.FileR.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetFileMetaInfo(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/nosql_database_api.NoSQLDatabaseAPI/GetFileMetaInfo',
            nosql__database__api__pb2.FileBaseR.SerializeToString,
            nosql__database__api__pb2.FileR.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetManyFilesMetaInfo(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/nosql_database_api.NoSQLDatabaseAPI/GetManyFilesMetaInfo',
            nosql__database__api__pb2.StorageSegmentR.SerializeToString,
            nosql__database__api__pb2.FileSegmentR.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def PutSQLGeneratorStatus(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/nosql_database_api.NoSQLDatabaseAPI/PutSQLGeneratorStatus',
            nosql__database__api__pb2.IdentifierStatusR.SerializeToString,
            nosql__database__api__pb2.IdentifierStatusR.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetSQLGeneratorStatus(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/nosql_database_api.NoSQLDatabaseAPI/GetSQLGeneratorStatus',
            nosql__database__api__pb2.IdentifierR.SerializeToString,
            nosql__database__api__pb2.IdentifierStatusR.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def PutSQLGeneratorFiles(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/nosql_database_api.NoSQLDatabaseAPI/PutSQLGeneratorFiles',
            nosql__database__api__pb2.ManyFilesIdentifierR.SerializeToString,
            nosql__database__api__pb2.IdentifierR.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetSQLGeneratorFiles(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/nosql_database_api.NoSQLDatabaseAPI/GetSQLGeneratorFiles',
            nosql__database__api__pb2.IdentifierR.SerializeToString,
            nosql__database__api__pb2.ManyFilesIdentifierR.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
