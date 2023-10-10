```bash
python -m grpc_tools.protoc -I./proto --python_out=./app/proto --pyi_out=./app/proto --grpc_python_out=./app/proto ./proto/helloworld.proto
```
