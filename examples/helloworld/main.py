import asyncio

from nats.aio.client import Client as NATS

import helloworld_nrpc
import helloworld_pb2


class Server:
    async def SayHello(self, req):
        return helloworld_pb2.HelloReply(result="Hello" + req.name)


async def run():
    nc = NATS()
    
    await nc.connect('nats://localhost:4222')

    h = helloworld_nrpc.GreeterHandler(nc, Server())

    await nc.subscribe(h.subject(), cb=h.handler)

    c = helloworld_nrpc.GreeterClient(nc)

    r = await c.SayHello(helloworld_pb2.HelloRequest(name="World"))
    print("Greeting:", r.result)

    await nc.close()


if __name__ == "__main__":
    asyncio.run(run())
