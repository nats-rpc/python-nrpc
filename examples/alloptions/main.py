import asyncio

from nats.aio.client import Client as NATS

import nrpc
import alloptions_nrpc
import alloptions_pb2


class Server:
    def __init__(self):
        self.noreply_hit = 0

    @asyncio.coroutine
    def MtSimpleReply(self, req):
        return alloptions_pb2.SimpleStringReply(reply=req.arg1)

    @asyncio.coroutine
    def MtVoidReply(self, req):
        if req.arg1 == "please fail":
            raise nrpc.ClientError("failed as requested")

    @asyncio.coroutine
    def MtNoReply(self):
        self.noreply_hit += 1


def run(loop):
    nc = NATS()

    yield from nc.connect(io_loop=loop)

    server = Server()
    h1 = alloptions_nrpc.SvcCustomSubjectHandler(nc, server)
    h2 = alloptions_nrpc.SvcSubjectParamsHandler(nc, server)

    yield from nc.subscribe(h1.subject(), cb=h1.handler)
    yield from nc.subscribe(h2.subject(), cb=h2.handler)

    c1 = alloptions_nrpc.SvcCustomSubjectClient(nc, "default")
    c2 = alloptions_nrpc.SvcSubjectParamsClient(nc, "default", "me")

    r = yield from c1.MtSimpleReply(
        alloptions_pb2.StringArg(arg1="hi"))
    assert r.reply == "hi"

    r = yield from c1.MtVoidReply(
        alloptions_pb2.StringArg(arg1="hi"))
    assert r is None

    try:
        r = yield from c1.MtVoidReply(
            alloptions_pb2.StringArg(arg1="please fail"))
    except nrpc.ClientError as e:
        assert e.message == "failed as requested"
    else:
        assert False, "No error received"

    yield from c2.MtNoReply()
    yield from asyncio.sleep(0.2)
    assert server.noreply_hit == 1

    yield from nc.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(loop))
    loop.close()
