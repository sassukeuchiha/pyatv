# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: pyatv/protocols/mrp/protobuf/SetRecordingStateMessage.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from pyatv.protocols.mrp.protobuf import ProtocolMessage_pb2 as pyatv_dot_protocols_dot_mrp_dot_protobuf_dot_ProtocolMessage__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n;pyatv/protocols/mrp/protobuf/SetRecordingStateMessage.proto\x1a\x32pyatv/protocols/mrp/protobuf/ProtocolMessage.proto\"\x93\x01\n\x18SetRecordingStateMessage\x12\x37\n\x05state\x18\x01 \x01(\x0e\x32(.SetRecordingStateMessage.RecordingState\">\n\x0eRecordingState\x12\x0b\n\x07Unknown\x10\x00\x12\r\n\tRecording\x10\x01\x12\x10\n\x0cNotRecording\x10\x02:M\n\x18setRecordingStateMessage\x12\x10.ProtocolMessage\x18# \x01(\x0b\x32\x19.SetRecordingStateMessage')


SETRECORDINGSTATEMESSAGE_FIELD_NUMBER = 35
setRecordingStateMessage = DESCRIPTOR.extensions_by_name['setRecordingStateMessage']

_SETRECORDINGSTATEMESSAGE = DESCRIPTOR.message_types_by_name['SetRecordingStateMessage']
_SETRECORDINGSTATEMESSAGE_RECORDINGSTATE = _SETRECORDINGSTATEMESSAGE.enum_types_by_name['RecordingState']
SetRecordingStateMessage = _reflection.GeneratedProtocolMessageType('SetRecordingStateMessage', (_message.Message,), {
  'DESCRIPTOR' : _SETRECORDINGSTATEMESSAGE,
  '__module__' : 'pyatv.protocols.mrp.protobuf.SetRecordingStateMessage_pb2'
  # @@protoc_insertion_point(class_scope:SetRecordingStateMessage)
  })
_sym_db.RegisterMessage(SetRecordingStateMessage)

if _descriptor._USE_C_DESCRIPTORS == False:
  pyatv_dot_protocols_dot_mrp_dot_protobuf_dot_ProtocolMessage__pb2.ProtocolMessage.RegisterExtension(setRecordingStateMessage)

  DESCRIPTOR._options = None
  _SETRECORDINGSTATEMESSAGE._serialized_start=116
  _SETRECORDINGSTATEMESSAGE._serialized_end=263
  _SETRECORDINGSTATEMESSAGE_RECORDINGSTATE._serialized_start=201
  _SETRECORDINGSTATEMESSAGE_RECORDINGSTATE._serialized_end=263
# @@protoc_insertion_point(module_scope)
