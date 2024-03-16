# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: alloptions.proto
# Protobuf Python Version: 5.26.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from nrpc import nrpc_pb2 as nrpc_dot_nrpc__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x10\x61lloptions.proto\x12\x04main\x1a\x0fnrpc/nrpc.proto\"\x19\n\tStringArg\x12\x0c\n\x04\x61rg1\x18\x01 \x01(\t\"\"\n\x11SimpleStringReply\x12\r\n\x05reply\x18\x01 \x01(\t2\xe7\x02\n\x10SvcCustomSubject\x12N\n\rMtSimpleReply\x12\x0f.main.StringArg\x1a\x17.main.SimpleStringReply\"\x13\x82\xb2\x19\x0fmt_simple_reply\x12,\n\x0bMtVoidReply\x12\x0f.main.StringArg\x1a\n.nrpc.Void\"\x00\x12\x39\n\x0bMtNoRequest\x12\x0f.nrpc.NoRequest\x1a\x17.main.SimpleStringReply\"\x00\x12\x41\n\x0fMtStreamedReply\x12\x0f.main.StringArg\x1a\x17.main.SimpleStringReply\"\x04\x90\xb2\x19\x01\x12\x43\n\x16MtVoidReqStreamedReply\x12\n.nrpc.Void\x1a\x17.main.SimpleStringReply\"\x04\x90\xb2\x19\x01\x1a\x12\xc2\xf3\x18\x0e\x63ustom_subject2\xdf\x01\n\x10SvcSubjectParams\x12J\n\x13MtWithSubjectParams\x12\n.nrpc.Void\x1a\x17.main.SimpleStringReply\"\x0e\x8a\xb2\x19\x03mp1\x8a\xb2\x19\x03mp2\x12(\n\tMtNoReply\x12\n.nrpc.Void\x1a\r.nrpc.NoReply\"\x00\x12G\n\x12MtNoRequestWParams\x12\x0f.nrpc.NoRequest\x1a\x17.main.SimpleStringReply\"\x07\x8a\xb2\x19\x03mp1\x1a\x0c\xca\xf3\x18\x08\x63lientid2M\n\x10NoRequestService\x12\x39\n\x0bMtNoRequest\x12\x0f.nrpc.NoRequest\x1a\x17.main.SimpleStringReply\"\x00\x42\x1c\x82\xb5\x18\x04root\x8a\xb5\x18\x08instance\x90\xb5\x18\x01\x98\xb5\x18\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'alloptions_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'\202\265\030\004root\212\265\030\010instance\220\265\030\001\230\265\030\001'
  _globals['_SVCCUSTOMSUBJECT']._loaded_options = None
  _globals['_SVCCUSTOMSUBJECT']._serialized_options = b'\302\363\030\016custom_subject'
  _globals['_SVCCUSTOMSUBJECT'].methods_by_name['MtSimpleReply']._loaded_options = None
  _globals['_SVCCUSTOMSUBJECT'].methods_by_name['MtSimpleReply']._serialized_options = b'\202\262\031\017mt_simple_reply'
  _globals['_SVCCUSTOMSUBJECT'].methods_by_name['MtStreamedReply']._loaded_options = None
  _globals['_SVCCUSTOMSUBJECT'].methods_by_name['MtStreamedReply']._serialized_options = b'\220\262\031\001'
  _globals['_SVCCUSTOMSUBJECT'].methods_by_name['MtVoidReqStreamedReply']._loaded_options = None
  _globals['_SVCCUSTOMSUBJECT'].methods_by_name['MtVoidReqStreamedReply']._serialized_options = b'\220\262\031\001'
  _globals['_SVCSUBJECTPARAMS']._loaded_options = None
  _globals['_SVCSUBJECTPARAMS']._serialized_options = b'\312\363\030\010clientid'
  _globals['_SVCSUBJECTPARAMS'].methods_by_name['MtWithSubjectParams']._loaded_options = None
  _globals['_SVCSUBJECTPARAMS'].methods_by_name['MtWithSubjectParams']._serialized_options = b'\212\262\031\003mp1\212\262\031\003mp2'
  _globals['_SVCSUBJECTPARAMS'].methods_by_name['MtNoRequestWParams']._loaded_options = None
  _globals['_SVCSUBJECTPARAMS'].methods_by_name['MtNoRequestWParams']._serialized_options = b'\212\262\031\003mp1'
  _globals['_STRINGARG']._serialized_start=43
  _globals['_STRINGARG']._serialized_end=68
  _globals['_SIMPLESTRINGREPLY']._serialized_start=70
  _globals['_SIMPLESTRINGREPLY']._serialized_end=104
  _globals['_SVCCUSTOMSUBJECT']._serialized_start=107
  _globals['_SVCCUSTOMSUBJECT']._serialized_end=466
  _globals['_SVCSUBJECTPARAMS']._serialized_start=469
  _globals['_SVCSUBJECTPARAMS']._serialized_end=692
  _globals['_NOREQUESTSERVICE']._serialized_start=694
  _globals['_NOREQUESTSERVICE']._serialized_end=771
# @@protoc_insertion_point(module_scope)
