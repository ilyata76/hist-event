import grpc
import proto.nosql_database_api_pb2
import proto.nosql_database_api_pb2_grpc

import proto.file_api_pb2
import proto.file_api_pb2_grpc

print("ABOBA")

try : 
    with grpc.insecure_channel("localhost:50051") as channel :
        stub = proto.nosql_database_api_pb2_grpc.NoSQLDatabaseAPIStub(channel)
        response = stub.Ping(proto.nosql_database_api_pb2.PingRequest())
    print("Greeter client received: " + response.pong)
except grpc.RpcError as exc :
    print(type(exc), exc.args[0])
    print(exc.code())
    print(exc.details())


try : 
    with grpc.insecure_channel("localhost:50052") as channel :
        stub = proto.file_api_pb2_grpc.FileAPIStub(channel)
        response = stub.Ping(proto.file_api_pb2.PingRequest())
    print("Greeter client received: " + response.pong)
except grpc.RpcError as exc :
    print(type(exc), exc.args[0])
    print(exc.code())
    print(exc.details())
    