from google.protobuf import descriptor_pb2 as _descriptor_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SubjectRule(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    COPY: _ClassVar[SubjectRule]
    TOLOWER: _ClassVar[SubjectRule]
COPY: SubjectRule
TOLOWER: SubjectRule
PACKAGESUBJECT_FIELD_NUMBER: _ClassVar[int]
packageSubject: _descriptor.FieldDescriptor
PACKAGESUBJECTPARAMS_FIELD_NUMBER: _ClassVar[int]
packageSubjectParams: _descriptor.FieldDescriptor
SERVICESUBJECTRULE_FIELD_NUMBER: _ClassVar[int]
serviceSubjectRule: _descriptor.FieldDescriptor
METHODSUBJECTRULE_FIELD_NUMBER: _ClassVar[int]
methodSubjectRule: _descriptor.FieldDescriptor
SERVICESUBJECT_FIELD_NUMBER: _ClassVar[int]
serviceSubject: _descriptor.FieldDescriptor
SERVICESUBJECTPARAMS_FIELD_NUMBER: _ClassVar[int]
serviceSubjectParams: _descriptor.FieldDescriptor
METHODSUBJECT_FIELD_NUMBER: _ClassVar[int]
methodSubject: _descriptor.FieldDescriptor
METHODSUBJECTPARAMS_FIELD_NUMBER: _ClassVar[int]
methodSubjectParams: _descriptor.FieldDescriptor
STREAMEDREPLY_FIELD_NUMBER: _ClassVar[int]
streamedReply: _descriptor.FieldDescriptor

class Error(_message.Message):
    __slots__ = ("type", "message", "msgCount")
    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        CLIENT: _ClassVar[Error.Type]
        SERVER: _ClassVar[Error.Type]
        EOS: _ClassVar[Error.Type]
        SERVERTOOBUSY: _ClassVar[Error.Type]
    CLIENT: Error.Type
    SERVER: Error.Type
    EOS: Error.Type
    SERVERTOOBUSY: Error.Type
    TYPE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    MSGCOUNT_FIELD_NUMBER: _ClassVar[int]
    type: Error.Type
    message: str
    msgCount: int
    def __init__(self, type: _Optional[_Union[Error.Type, str]] = ..., message: _Optional[str] = ..., msgCount: _Optional[int] = ...) -> None: ...

class Void(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class NoRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class NoReply(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class HeartBeat(_message.Message):
    __slots__ = ("lastbeat",)
    LASTBEAT_FIELD_NUMBER: _ClassVar[int]
    lastbeat: bool
    def __init__(self, lastbeat: bool = ...) -> None: ...
