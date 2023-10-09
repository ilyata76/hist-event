# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: nosql-database-api.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x18nosql-database-api.proto\x12\x03HUY\"\r\n\x0bPingRequest\"\x1c\n\x0cPingResponse\x12\x0c\n\x04pong\x18\x01 \x01(\t\"0\n\x0ePutFileRequest\x12\x10\n\x08\x66ilename\x18\x01 \x01(\t\x12\x0c\n\x04path\x18\x02 \x01(\t\"1\n\x0fPutFileResponse\x12\x10\n\x08\x66ilename\x18\x01 \x01(\t\x12\x0c\n\x04path\x18\x02 \x01(\t\"%\n\x11\x44\x65leteFileRequest\x12\x10\n\x08\x66ilename\x18\x01 \x01(\t\"4\n\x12\x44\x65leteFileResponse\x12\x10\n\x08\x66ilename\x18\x01 \x01(\t\x12\x0c\n\x04path\x18\x02 \x01(\t\"0\n\x0e\x41\x64\x64\x46ileRequest\x12\x10\n\x08\x66ilename\x18\x01 \x01(\t\x12\x0c\n\x04path\x18\x02 \x01(\t\"1\n\x0f\x41\x64\x64\x46ileResponse\x12\x10\n\x08\x66ilename\x18\x01 \x01(\t\x12\x0c\n\x04path\x18\x02 \x01(\t\"\"\n\x0eGetFileRequest\x12\x10\n\x08\x66ilename\x18\x01 \x01(\t\"1\n\x0fGetFileResponse\x12\x10\n\x08\x66ilename\x18\x01 \x01(\t\x12\x0c\n\x04path\x18\x02 \x01(\t\"7\n\x13GetManyFilesRequest\x12\x11\n\tstart_pos\x18\x01 \x01(\x05\x12\r\n\x05limit\x18\x02 \x01(\x05\"$\n\x14GetManyFilesResponse\x12\x0c\n\x04TODO\x18\x01 \x01(\t2\xf1\x02\n\x10NoSQLDatabaseAPI\x12-\n\x04Ping\x12\x10.HUY.PingRequest\x1a\x11.HUY.PingResponse\"\x00\x12\x36\n\x07\x41\x64\x64\x46ile\x12\x13.HUY.AddFileRequest\x1a\x14.HUY.AddFileResponse\"\x00\x12\x36\n\x07PutFile\x12\x13.HUY.PutFileRequest\x1a\x14.HUY.PutFileResponse\"\x00\x12?\n\nDeleteFile\x12\x16.HUY.DeleteFileRequest\x1a\x17.HUY.DeleteFileResponse\"\x00\x12\x36\n\x07GetFile\x12\x13.HUY.GetFileRequest\x1a\x14.HUY.GetFileResponse\"\x00\x12\x45\n\x0cGetManyFiles\x12\x18.HUY.GetManyFilesRequest\x1a\x19.HUY.GetManyFilesResponse\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'nosql_database_api_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_PINGREQUEST']._serialized_start=33
  _globals['_PINGREQUEST']._serialized_end=46
  _globals['_PINGRESPONSE']._serialized_start=48
  _globals['_PINGRESPONSE']._serialized_end=76
  _globals['_PUTFILEREQUEST']._serialized_start=78
  _globals['_PUTFILEREQUEST']._serialized_end=126
  _globals['_PUTFILERESPONSE']._serialized_start=128
  _globals['_PUTFILERESPONSE']._serialized_end=177
  _globals['_DELETEFILEREQUEST']._serialized_start=179
  _globals['_DELETEFILEREQUEST']._serialized_end=216
  _globals['_DELETEFILERESPONSE']._serialized_start=218
  _globals['_DELETEFILERESPONSE']._serialized_end=270
  _globals['_ADDFILEREQUEST']._serialized_start=272
  _globals['_ADDFILEREQUEST']._serialized_end=320
  _globals['_ADDFILERESPONSE']._serialized_start=322
  _globals['_ADDFILERESPONSE']._serialized_end=371
  _globals['_GETFILEREQUEST']._serialized_start=373
  _globals['_GETFILEREQUEST']._serialized_end=407
  _globals['_GETFILERESPONSE']._serialized_start=409
  _globals['_GETFILERESPONSE']._serialized_end=458
  _globals['_GETMANYFILESREQUEST']._serialized_start=460
  _globals['_GETMANYFILESREQUEST']._serialized_end=515
  _globals['_GETMANYFILESRESPONSE']._serialized_start=517
  _globals['_GETMANYFILESRESPONSE']._serialized_end=553
  _globals['_NOSQLDATABASEAPI']._serialized_start=556
  _globals['_NOSQLDATABASEAPI']._serialized_end=925
# @@protoc_insertion_point(module_scope)
