# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: stockSystem.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11stockSystem.proto\"\x1f\n\tstockName\x12\x12\n\nstock_name\x18\x01 \x01(\t\"8\n\x0bPriceVolume\x12\x13\n\x0bstock_price\x18\x01 \x01(\x05\x12\x14\n\x0cstock_volume\x18\x02 \x01(\x05\"E\n\x0etradingRequest\x12\x12\n\nstock_name\x18\x01 \x01(\t\x12\x0b\n\x03num\x18\x02 \x01(\x05\x12\x12\n\ntrade_type\x18\x03 \x01(\t\"+\n\x0fstatusIndicator\x12\x18\n\x10status_indicator\x18\x01 \x01(\x05\"8\n\rupdateRequest\x12\x12\n\nstock_name\x18\x01 \x01(\t\x12\x13\n\x0bstock_price\x18\x02 \x01(\x05\x32\x8f\x01\n\x0bstockSystem\x12$\n\x06Lookup\x12\n.stockName\x1a\x0c.PriceVolume\"\x00\x12,\n\x05Trade\x12\x0f.tradingRequest\x1a\x10.statusIndicator\"\x00\x12,\n\x06Update\x12\x0e.updateRequest\x1a\x10.statusIndicator\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'stockSystem_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _STOCKNAME._serialized_start=21
  _STOCKNAME._serialized_end=52
  _PRICEVOLUME._serialized_start=54
  _PRICEVOLUME._serialized_end=110
  _TRADINGREQUEST._serialized_start=112
  _TRADINGREQUEST._serialized_end=181
  _STATUSINDICATOR._serialized_start=183
  _STATUSINDICATOR._serialized_end=226
  _UPDATEREQUEST._serialized_start=228
  _UPDATEREQUEST._serialized_end=284
  _STOCKSYSTEM._serialized_start=287
  _STOCKSYSTEM._serialized_end=430
# @@protoc_insertion_point(module_scope)