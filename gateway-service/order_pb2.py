# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: order.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import user_pb2 as user__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0border.proto\x12\x05order\x1a\nuser.proto\"H\n\x05Order\x12\n\n\x02id\x18\x01 \x01(\x05\x12\r\n\x05title\x18\x02 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x03 \x01(\t\x12\x0f\n\x07user_id\x18\x04 \x01(\x05\"\x15\n\x07OrderId\x12\n\n\x02id\x18\x01 \x01(\x05\" \n\rOrderResponse\x12\x0f\n\x07message\x18\x01 \x01(\t2\x9e\x01\n\x0cOrderService\x12\x31\n\x0b\x43reateOrder\x12\x0c.order.Order\x1a\x14.order.OrderResponse\x12(\n\x08GetOrder\x12\x0e.order.OrderId\x1a\x0c.order.Order\x12\x31\n\x0bUpdateOrder\x12\x0c.order.Order\x1a\x14.order.OrderResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'order_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_ORDER']._serialized_start=34
  _globals['_ORDER']._serialized_end=106
  _globals['_ORDERID']._serialized_start=108
  _globals['_ORDERID']._serialized_end=129
  _globals['_ORDERRESPONSE']._serialized_start=131
  _globals['_ORDERRESPONSE']._serialized_end=163
  _globals['_ORDERSERVICE']._serialized_start=166
  _globals['_ORDERSERVICE']._serialized_end=324
# @@protoc_insertion_point(module_scope)
