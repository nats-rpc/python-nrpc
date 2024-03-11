# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: helloworld.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from nrpc import nrpc_pb2 as nrpc_dot_nrpc__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='helloworld.proto',
  package='helloworld',
  syntax='proto3',
  serialized_options=b'\n\033io.grpc.examples.helloworldB\017HelloWorldProtoP\001',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x10helloworld.proto\x12\nhelloworld\x1a\x0fnrpc/nrpc.proto\"\x1c\n\x0cHelloRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\"E\n\nHelloReply\x12\x10\n\x06result\x18\x01 \x01(\tH\x00\x12\x1c\n\x05\x65rror\x18\x02 \x01(\x0b\x32\x0b.nrpc.ErrorH\x00\x42\x07\n\x05reply2I\n\x07Greeter\x12>\n\x08SayHello\x12\x18.helloworld.HelloRequest\x1a\x16.helloworld.HelloReply\"\x00\x42\x30\n\x1bio.grpc.examples.helloworldB\x0fHelloWorldProtoP\x01\x62\x06proto3'
  ,
  dependencies=[nrpc_dot_nrpc__pb2.DESCRIPTOR,])




_HELLOREQUEST = _descriptor.Descriptor(
  name='HelloRequest',
  full_name='helloworld.HelloRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='helloworld.HelloRequest.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=49,
  serialized_end=77,
)


_HELLOREPLY = _descriptor.Descriptor(
  name='HelloReply',
  full_name='helloworld.HelloReply',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='result', full_name='helloworld.HelloReply.result', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='error', full_name='helloworld.HelloReply.error', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='reply', full_name='helloworld.HelloReply.reply',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=79,
  serialized_end=148,
)

_HELLOREPLY.fields_by_name['error'].message_type = nrpc_dot_nrpc__pb2._ERROR
_HELLOREPLY.oneofs_by_name['reply'].fields.append(
  _HELLOREPLY.fields_by_name['result'])
_HELLOREPLY.fields_by_name['result'].containing_oneof = _HELLOREPLY.oneofs_by_name['reply']
_HELLOREPLY.oneofs_by_name['reply'].fields.append(
  _HELLOREPLY.fields_by_name['error'])
_HELLOREPLY.fields_by_name['error'].containing_oneof = _HELLOREPLY.oneofs_by_name['reply']
DESCRIPTOR.message_types_by_name['HelloRequest'] = _HELLOREQUEST
DESCRIPTOR.message_types_by_name['HelloReply'] = _HELLOREPLY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

HelloRequest = _reflection.GeneratedProtocolMessageType('HelloRequest', (_message.Message,), {
  'DESCRIPTOR' : _HELLOREQUEST,
  '__module__' : 'helloworld_pb2'
  # @@protoc_insertion_point(class_scope:helloworld.HelloRequest)
  })
_sym_db.RegisterMessage(HelloRequest)

HelloReply = _reflection.GeneratedProtocolMessageType('HelloReply', (_message.Message,), {
  'DESCRIPTOR' : _HELLOREPLY,
  '__module__' : 'helloworld_pb2'
  # @@protoc_insertion_point(class_scope:helloworld.HelloReply)
  })
_sym_db.RegisterMessage(HelloReply)


DESCRIPTOR._options = None

_GREETER = _descriptor.ServiceDescriptor(
  name='Greeter',
  full_name='helloworld.Greeter',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=150,
  serialized_end=223,
  methods=[
  _descriptor.MethodDescriptor(
    name='SayHello',
    full_name='helloworld.Greeter.SayHello',
    index=0,
    containing_service=None,
    input_type=_HELLOREQUEST,
    output_type=_HELLOREPLY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_GREETER)

DESCRIPTOR.services_by_name['Greeter'] = _GREETER

# @@protoc_insertion_point(module_scope)
