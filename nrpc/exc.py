from . import nrpc_pb2


class NrpcError(RuntimeError):
    type_ = None

    def __init__(self, message=None):
        self.message = message

    def as_nrpc_error(self):
        return nrpc_pb2.Error(
            type=self.type_,
            message=str(self),
        )


class ClientError(NrpcError):
    type_ = nrpc_pb2.Error.CLIENT


class ServerError(NrpcError):
    type_ = nrpc_pb2.Error.SERVER


def server_error(e):
    """Convert an exception into a nrpc.Error message"""
    return nrpc_pb2.Error(
        type=nrpc_pb2.Error.SERVER,
        message=str(e),
    )


def from_error(error):
    """Convert a nrpc.Error message into a python exception"""
    if error.type == nrpc_pb2.Error.CLIENT:
        return ClientError(error.message)
    elif error.type == nrpc_pb2.Error.SERVER:
        return ServerError(error.message)
    else:
        raise RuntimeError("Not an error: %s" % error)
