from concurrent import futures

import grpc
import proto.helloworld_pb2
import proto.helloworld_pb2_grpc as pb_grpc

print("ABOBA")
class Greeter(pb_grpc.GreeterServicer):
    # def SayHello(self, request, context):
    #    print("ABOBA", request, context, "aboba", sep="\n")
    #    return pb.HelloReply(message="Hello, %s!" % request.name)
    pass

def serve():
    try : 
        port = "50051"
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        pb_grpc.add_GreeterServicer_to_server(Greeter(), server)
        server.add_insecure_port("[::]:" + port)
        server.start()
        print("Server started, listening on " + port)
        server.wait_for_termination()
    except BaseException as exc :
        print("AAA")
        print(type(exc), exc)

try : 
    serve()    
except NotImplementedError as exc : # Keyboard
    print("AAA")
    print(type(exc), exc)