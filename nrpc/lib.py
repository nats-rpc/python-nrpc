import asyncio

from nats.aio.client import INBOX_PREFIX

import nrpc.exc
from . import nrpc_pb2


class InvalidSubject(Exception):
    pass


class ClientLost(RuntimeError):
    pass


class CanceledByClient(RuntimeError):
    pass


def parse_subject(
        package_subject,
        package_params_count,
        service_subject,
        service_params_count,
        subject,
):
    package_subject = package_subject.split('.') if package_subject else []
    service_subject = service_subject.split('.')

    minlen = len(package_subject) + package_params_count + \
        len(service_subject) + service_params_count + 1

    tokens = subject.split('.')

    if len(tokens) < minlen:
        raise InvalidSubject(
            "subject must contain %s tokens at least, got %s" % (minlen,
                                                                 subject))

    if tokens[:len(package_subject)] != package_subject:
        raise InvalidSubject(
            "subject should start with %s" % '.'.join(package_subject))

    tokens = tokens[len(package_subject):]

    package_params = tokens[:package_params_count]
    tokens = tokens[package_params_count:]

    if tokens[:len(service_subject)] != service_subject:
        raise InvalidSubject("subject should contain %s, got %s" %
                             ('.'.join(service_subject), subject))

    tokens = tokens[len(service_subject):]

    service_params = tokens[:service_params_count]
    tokens = tokens[service_params_count:]

    name = tokens[0]

    return package_params, service_params, name, tokens[1:]


def parse_subject_tail(method_params_count, tail):
    if len(tail) < method_params_count:
        raise InvalidSubject("subject tail is too short")
    method_params = tail[:method_params_count]
    tail = tail[method_params_count:]
    if len(tail) == 0:
        encoding = "protobuf"
    elif len(tail) == 1:
        encoding = tail[0]
    elif len(tail) > 1:
        raise InvalidSubject("subject tail is too long")
    return method_params, encoding


async def streamed_reply_request(nc, subject, req, timeout):
    if hasattr(nc, 'next_inbox'):
        inbox = nc.next_inbox()
    else:
        next_inbox = INBOX_PREFIX[:]
        next_inbox.extend(nc._nuid.next())
        inbox = next_inbox.decode()

    heartbeat_subject = inbox + ".heartbeat"

    msg_queue = asyncio.Queue(1)

    async def handler(msg):
        await msg_queue.put(msg)

    async def heartbeat():
        while True:
            await asyncio.sleep(1)
            await nc.publish(heartbeat_subject,
                             nrpc_pb2.HeartBeat().SerializeToString())

    heartbeat_task = asyncio.ensure_future(heartbeat())

    sid = await nc.subscribe(inbox, cb=handler)

    try:
        await nc.publish_request(subject, inbox, req)

        while True:
            msg = await asyncio.wait_for(msg_queue.get(), timeout)

            # Is it a keep-alive msg ?
            if len(msg.data) == 1 and msg.data[0] == 0:
                continue

            # Is it an error ?
            if len(msg.data) > 1 and msg.data[0] == 0:
                err = nrpc_pb2.Error.FromString(msg.data[1:])
                if err.type == nrpc_pb2.Error.EOS:
                    return
                raise Error

            yield msg
    finally:
        heartbeat_task.cancel()
        await nc.unsubscribe(sid)


async def heartbeat_listener(nc, subject, oncancel):
    queue = asyncio.Queue(1)

    def handler(msg):
        queue.put(msg)

    sid = await nc.subscribe(nc, subject, handler)

    try:
        while True:
            try:
                msg = await asyncio.wait_for(queue.get(), 2)
                beat = nrpc_pb2.HeartBeat.FromString(msg.data)
                if beat.last:
                    oncancel()
                    return
            except asyncio.TimeoutError as e:
                oncancel()
                return
    finally:
        await nc.unsubscribe(sid)


async def wrap_gen(nc, inbox, async_gen):
    while True:
        try:
            reply = await asyncio.wait_for(async_gen.__anext__(), 1)
            data = reply.SerializeToString()
            await nc.publish(inbox, data)
        except asyncio.TimeoutError:
            # Send a keep-alive message
            await nc.publish(inbox, b'\0')
        except StopAsyncIteration:
            eos = nrpc_pb2.Error()
            eos.type = nrpc_pb2.Error.EOS
            await nc.publish(inbox, b'\0' + eos.SerializeToString())
            return


async def streamed_reply_handler(nc, inbox, async_gen):
    heartbeat_subject = inbox + ".heartbeat"

    err = None

    queue = asyncio.Queue(1)

    EOQ = object()

    async def consume_generator():
        try:
            async for reply in async_gen:
                await queue.put(reply)
        except nrpc.ClientError as e:
            await queue.put(e)
        except asyncio.CancelledError as e:
            await queue.put(e)
        except Exception as e:
            await queue.put(nrpc.exc.server_error(e))

        await queue.put(EOQ)

    task = asyncio.ensure_future(consume_generator())

    heartbeat_task = asyncio.ensure_future(
        heartbeat_listener(nc, heartbeat_subject, task.cancel))

    msgCount = 0

    try:
        while True:
            try:
                reply = await asyncio.wait_for(queue.get(), 1)
                if isinstance(reply, asyncio.CancelledError):
                    return
                if reply is EOQ:
                    reply = nrpc_pb2.Error()
                    reply.type = nrpc_pb2.Error.EOS
                    reply.msgCount = msgCount
                if isinstance(reply, nrpc.exc.NrpcError):
                    reply = reply.as_nrpc_error()
                data = reply.SerializeToString()
                if isinstance(reply, nrpc_pb2.Error):
                    data = b'\x00' + data
                else:
                    msgCount += 1
                await nc.publish(inbox, data)
                if isinstance(reply, nrpc_pb2.Error):
                    return
            except asyncio.TimeoutError:
                await nc.publish(inbox, b'\x00')

    finally:
        task.cancel()
        heartbeat_task.cancel()
