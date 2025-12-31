protoc \
    --proto_path src \
    --proto_path src/nrpc \
    --python_out src \
    --pyi_out src \
    nrpc/nrpc.proto
