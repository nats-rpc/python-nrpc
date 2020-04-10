# Python NRPC

A python code generator and lib for Nats RPC.

See https://github.com/nats-rpc/nrpc for more information on NRPC itself.

This package provides a protoc plugin to generate python code from
.proto files, respecting the nrpc specifications.

## Developer notes


For regenerating the nrpc protobuf files, make sure the protobuf is installed.

Copy 'nrpc.proto' from the https://github.com/nats-rpc/nrpc project into the nrpc/ directory.

Then, run the following command:

```bash
python setup.py protoc
```
