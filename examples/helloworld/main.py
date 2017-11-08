import asyncio

from nats.aio.client import Client as NATS

import helloworld_nrpc
import helloworld_pb2


class Server:
    def SayHello(self, req):
        return helloworld_pb2.HelloReply(result="Hello" + req.name)


def run(loop):
    nc = NATS()

    yield from nc.connect(io_loop=loop)

    h = helloworld_nrpc.GreeterHandler(nc, Server())

    yield from nc.subscribe(h.subject, cb=h.handler)

    c = helloworld_nrpc.GreeterClient(nc)

    r = yield from c.SayHello(helloworld_pb2.HelloRequest(name="World"))
    print("Greeting:", r.result)

    yield from nc.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(loop))
    loop.close()
