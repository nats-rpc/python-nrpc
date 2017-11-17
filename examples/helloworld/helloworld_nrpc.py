# This file is automatically generated from helloworld.proto, DO NOT EDIT!

import asyncio
import nats.aio

import nrpc

import helloworld_pb2 as helloworld__pb2


PKG_SUBJECT = 'helloworld'
PKG_SUBJECT_PARAMS = []
PKG_SUBJECT_PARAMS_COUNT = 0


Greeter_SUBJECT = 'Greeter'
Greeter_SUBJECT_PARAMS = []
Greeter_SUBJECT_PARAMS_COUNT = 0


class GreeterHandler:
    methods = {
        'SayHello': ('SayHello', 0, helloworld__pb2.HelloRequest),
    }

    def __init__(self, nc, server):
        self.nc = nc
        self.subject = (
            (PKG_SUBJECT + '.' if PKG_SUBJECT else '') +
            '*.' * PKG_SUBJECT_PARAMS_COUNT +
            Greeter_SUBJECT + '.' +
            '*.' * Greeter_SUBJECT_PARAMS_COUNT +
            '>'
        )
        self.server = server

    @asyncio.coroutine
    def handler(self, msg):
        try:
            pkg_params, svc_params, mt_subject, tail = nrpc.parse_subject(
                PKG_SUBJECT, PKG_SUBJECT_PARAMS_COUNT,
                Greeter_SUBJECT, Greeter_SUBJECT_PARAMS_COUNT,
                msg.subject)

            mname, params_count, input_type = self.methods[mt_subject]
            mt_params, count = nrpc.parse_subject_tail(params_count, tail)

            req = input_type.FromString(msg.data)
            method = getattr(self.server, mname)
            mt_params.append(req)
            rep = method(*mt_params)
            rawRep = rep.SerializeToString()
            yield from self.nc.publish(msg.reply, rawRep)
        except Exception as e:
            print("Error in handler:", e)


class GreeterClient:
    def __init__(
        self, nc,
    ):
        self.nc = nc

    @asyncio.coroutine
    def SayHello(
        self,
        req,
    ):
        subject = PKG_SUBJECT + '.' + Greeter_SUBJECT + '.' + 'SayHello'
        rawReq = req.SerializeToString()
        rawRep = yield from self.nc.timed_request(subject, rawReq, 5)
        if rawRep.data[0] == 0:
            return nrpc_pb2.Error.FromString(rawRep.data[1:])
        return helloworld__pb2.HelloReply.FromString(rawRep.data)
