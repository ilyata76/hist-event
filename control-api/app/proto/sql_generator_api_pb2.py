# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: sql-generator-api.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x17sql-generator-api.proto\x12\x11sql_generator_api\"\x07\n\x05PingR\"\x15\n\x05PongR\x12\x0c\n\x04pong\x18\x01 \x01(\t\"?\n\nManyFilesR\x12\x31\n\x05\x66iles\x18\x01 \x03(\x0b\x32\".sql_generator_api.FileBaseKeyword\"]\n\x14ManyFilesIdentifierR\x12\x31\n\x05\x66iles\x18\x01 \x03(\x0b\x32\".sql_generator_api.FileBaseKeyword\x12\x12\n\nidentifier\x18\x02 \x01(\t\"!\n\x0bIdentifierR\x12\x12\n\nidentifier\x18\x01 \x01(\t\"7\n\x11IdentifierStatusR\x12\x12\n\nidentifier\x18\x01 \x01(\t\x12\x0e\n\x06status\x18\x02 \x01(\t\"A\n\x0f\x46ileBaseKeyword\x12\x0f\n\x07storage\x18\x01 \x01(\t\x12\x0c\n\x04path\x18\x02 \x01(\t\x12\x0f\n\x07keyword\x18\x04 \x01(\t2\x8b\x04\n\x0fSQLGeneratorAPI\x12<\n\x04Ping\x12\x18.sql_generator_api.PingR\x1a\x18.sql_generator_api.PongR\"\x00\x12Q\n\x08Validate\x12\x1d.sql_generator_api.ManyFilesR\x1a$.sql_generator_api.IdentifierStatusR\"\x00\x12O\n\x05Parse\x12\x1e.sql_generator_api.IdentifierR\x1a$.sql_generator_api.IdentifierStatusR\"\x00\x12R\n\x08Generate\x12\x1e.sql_generator_api.IdentifierR\x1a$.sql_generator_api.IdentifierStatusR\"\x00\x12_\n\x15GetSQLGeneratorStatus\x12\x1e.sql_generator_api.IdentifierR\x1a$.sql_generator_api.IdentifierStatusR\"\x00\x12\x61\n\x14GetSQLGeneratorFiles\x12\x1e.sql_generator_api.IdentifierR\x1a\'.sql_generator_api.ManyFilesIdentifierR\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'sql_generator_api_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_PINGR']._serialized_start=46
  _globals['_PINGR']._serialized_end=53
  _globals['_PONGR']._serialized_start=55
  _globals['_PONGR']._serialized_end=76
  _globals['_MANYFILESR']._serialized_start=78
  _globals['_MANYFILESR']._serialized_end=141
  _globals['_MANYFILESIDENTIFIERR']._serialized_start=143
  _globals['_MANYFILESIDENTIFIERR']._serialized_end=236
  _globals['_IDENTIFIERR']._serialized_start=238
  _globals['_IDENTIFIERR']._serialized_end=271
  _globals['_IDENTIFIERSTATUSR']._serialized_start=273
  _globals['_IDENTIFIERSTATUSR']._serialized_end=328
  _globals['_FILEBASEKEYWORD']._serialized_start=330
  _globals['_FILEBASEKEYWORD']._serialized_end=395
  _globals['_SQLGENERATORAPI']._serialized_start=398
  _globals['_SQLGENERATORAPI']._serialized_end=921
# @@protoc_insertion_point(module_scope)
