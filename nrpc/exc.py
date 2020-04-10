from . import nrpc_pb2


class NrpcError(RuntimeError):
    type_ = None

    def __init__(self, message=None):
        self.message = message

    def as_nrpc_error(self):
        return nrpc_pb2.Error(type=self.type_, message=str(self))


class ClientError(NrpcError):
    type_ = nrpc_pb2.Error.CLIENT


class ServerError(NrpcError):
    type_ = nrpc_pb2.Error.SERVER


class EOS(NrpcError):
    type_ = nrpc_pb2.Error.EOS

    def __init__(self):
        self.message = None


class ServerTooBusy(NrpcError):
    type_ = nrpc_pb2.Error.SERVERTOOBUSY


def server_error(e):
    """Convert an exception into a nrpc.Error message"""
    return nrpc_pb2.Error(type=nrpc_pb2.Error.SERVER, message=str(e))


def from_error(error):
    """Convert a nrpc.Error message into a python exception"""
    if error.type == nrpc_pb2.Error.CLIENT:
        return ClientError(error.message)
    elif error.type == nrpc_pb2.Error.SERVER:
        return ServerError(error.message)
    elif error.type == nrpc_pb2.Error.EOS:
        return EOS()
    elif error.type == nrpc_pb2.Error.SERVERTOOBUSY:
        return ServerTooBusy(error.message)
    else:
        raise RuntimeError("Not an error: %s" % error)
