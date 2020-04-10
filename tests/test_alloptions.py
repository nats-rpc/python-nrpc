import asyncio
import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "examples",
            "alloptions",
        )))

from nats.aio.client import Client as NATS
import pytest

import nrpc

import alloptions_nrpc
import alloptions_pb2


class Server:
    def __init__(self):
        self.cond = asyncio.Condition()
        self.noreply_hit = 0

    @asyncio.coroutine
    def MtSimpleReply(self, req):
        return alloptions_pb2.SimpleStringReply(reply=req.arg1)

    @asyncio.coroutine
    def MtVoidReply(self, req):
        if req.arg1 == "please fail":
            raise nrpc.ClientError("failed as requested")
        if req.arg1 == "you are too busy":
            raise nrpc.exc.ServerTooBusy("I am too busy")

    async def MtNoReply(self):
        with await self.cond:
            self.noreply_hit += 1
            await self.cond.notify_all()

    async def wait_for_reply_hit(self, min_hit=1, timeout=1):
        with await self.cond:
            await asyncio.wait_for(
                self.cond.wait_for(
                    lambda: self.noreply_hit >= min_hit and self.noreply_hit),
                timeout,
            )

    async def MtStreamedReply(self, req):
        yield alloptions_pb2.SimpleStringReply(reply=req.arg1)
        yield alloptions_pb2.SimpleStringReply(reply=req.arg1)


@pytest.fixture(scope="session")
def nats_server():
    import subprocess
    p = subprocess.Popen([
        "nats-server",
        "-p",
        "4242",
    ])
    try:
        yield p
    finally:
        p.terminate()


@pytest.fixture
async def nats(nats_server, event_loop):
    nc = NATS()
    await nc.connect(servers=["nats://localhost:4242/"], io_loop=event_loop)
    try:
        yield nc
    finally:
        await nc.close()


@pytest.fixture
async def server(nats):
    server = Server()
    h1 = alloptions_nrpc.SvcCustomSubjectHandler(nats, server)
    h2 = alloptions_nrpc.SvcSubjectParamsHandler(nats, server)
    s1 = await nats.subscribe(h1.subject(), cb=h1.handler)
    s2 = await nats.subscribe(h2.subject(), cb=h2.handler)
    try:
        yield server
    finally:
        await nats.unsubscribe(s2)
        await nats.unsubscribe(s1)


@pytest.mark.asyncio
async def test_simple_reply(event_loop, nats, server):
    client = alloptions_nrpc.SvcCustomSubjectClient(nats, "default")
    r = await client.MtSimpleReply(alloptions_pb2.StringArg(arg1="hi"))
    assert r.reply == "hi"


@pytest.mark.asyncio
async def test_void_reply(event_loop, nats, server):
    client = alloptions_nrpc.SvcCustomSubjectClient(nats, "default")
    r = await client.MtVoidReply(alloptions_pb2.StringArg(arg1="hi"))
    assert r is None

    try:
        r = await client.MtVoidReply(
            alloptions_pb2.StringArg(arg1="please fail"))
    except nrpc.ClientError as e:
        assert e.message == "failed as requested"
    else:
        assert False, "No error received"


@pytest.mark.asyncio
async def test_server_too_busy(event_loop, nats, server):
    client = alloptions_nrpc.SvcCustomSubjectClient(nats, "default")

    with pytest.raises(nrpc.exc.ServerTooBusy) as excinfo:
        await client.MtVoidReply(
            alloptions_pb2.StringArg(arg1="you are too busy"))
    assert excinfo.value.message == "I am too busy"


@pytest.mark.asyncio
async def test_no_reply(event_loop, nats, server):
    client = alloptions_nrpc.SvcSubjectParamsClient(nats, "default", "me")

    await client.MtNoReply()
    await server.wait_for_reply_hit()


@pytest.mark.asyncio
async def test_streamed_reply(event_loop, nats, server):
    client = alloptions_nrpc.SvcCustomSubjectClient(nats, "default")
    async for r in client.MtStreamedReply(alloptions_pb2.StringArg(arg1="hi")):
        assert r.reply == "hi"
