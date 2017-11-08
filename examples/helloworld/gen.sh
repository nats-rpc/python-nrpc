protoc -I. -I../.. --python_out . ../../nrpc.proto
protoc -I. -I../.. --python_out . --pynrpc_out . helloworld.proto
