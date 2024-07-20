import asyncio
import os
import sys

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "examples",
            "alloptions",
        )
    )
)

import alloptions_nrpc
import alloptions_pb2
import nrpc
import pytest
import pytest_asyncio
from nats.aio.client import Client as NATS


class Server:
    def __init__(self):
        self.cond = asyncio.Condition()
        self.noreply_hit = 0

    async def MtSimpleReply(self, req):
        return alloptions_pb2.SimpleStringReply(reply=req.arg1)

    async def MtVoidReply(self, req):
        if req.arg1 == "please fail":
            raise nrpc.ClientError("failed as requested")
        if req.arg1 == "you are too busy":
            raise nrpc.exc.ServerTooBusy("I am too busy")

    async def MtNoReply(self):
        async with self.cond:
            self.noreply_hit += 1
            await self.cond.notify_all()

    async def wait_for_reply_hit(self, min_hit=1, timeout=1):
        async with self.cond:
            await asyncio.wait_for(
                self.cond.wait_for(
                    lambda: self.noreply_hit >= min_hit and self.noreply_hit
                ),
                timeout,
            )

    async def MtStreamedReply(self, req):
        yield alloptions_pb2.SimpleStringReply(reply=req.arg1)
        print("Sent rep1")
        yield alloptions_pb2.SimpleStringReply(reply=req.arg1)
        print("Sent rep2")


@pytest.fixture(scope="session")
def nats_server():
    import subprocess

    p = subprocess.Popen(
        [
            "nats-server",
            "-p",
            "4242",
        ]
    )
    try:
        yield p
    finally:
        p.terminate()


@pytest_asyncio.fixture
async def nats(nats_server):
    nc = NATS()
    await nc.connect(servers=["nats://localhost:4242/"])
    try:
        yield nc
    finally:
        await nc.close()


@pytest_asyncio.fixture
async def asyncio_debug():
    event_loop = asyncio.get_running_loop()
    oldvalue = event_loop.get_debug()
    event_loop.set_debug(True)
    initial_task_count = len(asyncio.all_tasks(loop=event_loop))
    try:
        yield event_loop
    finally:
        event_loop.set_debug(oldvalue)
        task_count = len(asyncio.all_tasks(loop=event_loop))
        assert initial_task_count == task_count


@pytest_asyncio.fixture
async def server(nats):
    server = Server()
    h1 = alloptions_nrpc.SvcCustomSubjectHandler(nats, server)
    h2 = alloptions_nrpc.SvcSubjectParamsHandler(nats, server)
    s1 = await nats.subscribe(h1.subject(), cb=h1.handler)
    s2 = await nats.subscribe(h2.subject(), cb=h2.handler)
    try:
        yield server
    finally:
        await s1.unsubscribe()
        await s2.unsubscribe()


@pytest.mark.asyncio
async def test_simple_reply(nats, server):
    client = alloptions_nrpc.SvcCustomSubjectClient(nats, "default")
    r = await client.MtSimpleReply(alloptions_pb2.StringArg(arg1="hi"))
    assert r.reply == "hi"


@pytest.mark.asyncio
async def test_void_reply(nats, server):
    client = alloptions_nrpc.SvcCustomSubjectClient(nats, "default")
    r = await client.MtVoidReply(alloptions_pb2.StringArg(arg1="hi"))
    assert r is None

    try:
        r = await client.MtVoidReply(alloptions_pb2.StringArg(arg1="please fail"))
    except nrpc.ClientError as e:
        assert e.message == "failed as requested"
    else:
        assert False, "No error received"


@pytest.mark.asyncio
async def test_server_too_busy(nats, server):
    client = alloptions_nrpc.SvcCustomSubjectClient(nats, "default")

    with pytest.raises(nrpc.exc.ServerTooBusy) as excinfo:
        await client.MtVoidReply(alloptions_pb2.StringArg(arg1="you are too busy"))
    assert excinfo.value.message == "I am too busy"


@pytest.mark.asyncio
async def test_no_reply(nats, server):
    client = alloptions_nrpc.SvcSubjectParamsClient(nats, "default", "me")

    await client.MtNoReply()
    await server.wait_for_reply_hit()


@pytest.mark.asyncio
async def test_streamed_reply(nats, server, asyncio_debug):
    client = alloptions_nrpc.SvcCustomSubjectClient(nats, "default")

    for i in range(500):
        async for r in client.MtStreamedReply(alloptions_pb2.StringArg(arg1="hi")):
            assert r.reply == "hi"
