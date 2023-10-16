# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: file-api.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0e\x66ile-api.proto\x12\x08\x66ile_api\"\r\n\x0bPingRequest\"\x1c\n\x0cPingResponse\x12\x0c\n\x04pong\x18\x01 \x01(\t\"O\n\x0e\x41\x64\x64\x46ileRequest\x12\x0f\n\x07storage\x18\x01 \x01(\t\x12\x0c\n\x04path\x18\x02 \x01(\t\x12\x10\n\x08\x66ilename\x18\x03 \x01(\t\x12\x0c\n\x04\x66ile\x18\x04 \x01(\x0c\"B\n\x0f\x41\x64\x64\x46ileResponse\x12\x0f\n\x07storage\x18\x01 \x01(\t\x12\x0c\n\x04path\x18\x02 \x01(\t\x12\x10\n\x08\x66ilename\x18\x03 \x01(\t\"/\n\x0eGetFileRequest\x12\x0f\n\x07storage\x18\x01 \x01(\t\x12\x0c\n\x04path\x18\x02 \x01(\t\"P\n\x0fGetFileResponse\x12\x0f\n\x07storage\x18\x01 \x01(\t\x12\x0c\n\x04path\x18\x02 \x01(\t\x12\x10\n\x08\x66ilename\x18\x03 \x01(\t\x12\x0c\n\x04\x66ile\x18\x04 \x01(\x0c\"7\n\x16GetFileMetaInfoRequest\x12\x0f\n\x07storage\x18\x01 \x01(\t\x12\x0c\n\x04path\x18\x02 \x01(\t\"J\n\x17GetFileMetaInfoResponse\x12\x0f\n\x07storage\x18\x01 \x01(\t\x12\x0c\n\x04path\x18\x02 \x01(\t\x12\x10\n\x08\x66ilename\x18\x03 \x01(\t\"2\n\x11\x44\x65leteFileRequest\x12\x0f\n\x07storage\x18\x01 \x01(\t\x12\x0c\n\x04path\x18\x02 \x01(\t\"E\n\x12\x44\x65leteFileResponse\x12\x0f\n\x07storage\x18\x01 \x01(\t\x12\x0c\n\x04path\x18\x02 \x01(\t\x12\x10\n\x08\x66ilename\x18\x03 \x01(\t\"O\n\x0ePutFileRequest\x12\x0f\n\x07storage\x18\x01 \x01(\t\x12\x0c\n\x04path\x18\x02 \x01(\t\x12\x10\n\x08\x66ilename\x18\x03 \x01(\t\x12\x0c\n\x04\x66ile\x18\x04 \x01(\x0c\"B\n\x0fPutFileResponse\x12\x0f\n\x07storage\x18\x01 \x01(\t\x12\x0c\n\x04path\x18\x02 \x01(\t\x12\x10\n\x08\x66ilename\x18\x03 \x01(\t\"J\n\x1bGetManyFilesMetaInfoRequest\x12\x0f\n\x07storage\x18\x01 \x01(\t\x12\r\n\x05start\x18\x02 \x01(\r\x12\x0b\n\x03\x65nd\x18\x03 \x01(\r\",\n\x1cGetManyFilesMetaInfoResponse\x12\x0c\n\x04TODO\x18\x01 \x01(\t2\x96\x04\n\x07\x46ileAPI\x12\x37\n\x04Ping\x12\x15.file_api.PingRequest\x1a\x16.file_api.PingResponse\"\x00\x12@\n\x07\x41\x64\x64\x46ile\x12\x18.file_api.AddFileRequest\x1a\x19.file_api.AddFileResponse\"\x00\x12@\n\x07GetFile\x12\x18.file_api.GetFileRequest\x1a\x19.file_api.GetFileResponse\"\x00\x12X\n\x0fGetFileMetaInfo\x12 .file_api.GetFileMetaInfoRequest\x1a!.file_api.GetFileMetaInfoResponse\"\x00\x12I\n\nDeleteFile\x12\x1b.file_api.DeleteFileRequest\x1a\x1c.file_api.DeleteFileResponse\"\x00\x12@\n\x07PutFile\x12\x18.file_api.PutFileRequest\x1a\x19.file_api.PutFileResponse\"\x00\x12g\n\x14GetManyFilesMetaInfo\x12%.file_api.GetManyFilesMetaInfoRequest\x1a&.file_api.GetManyFilesMetaInfoResponse\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'file_api_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_PINGREQUEST']._serialized_start=28
  _globals['_PINGREQUEST']._serialized_end=41
  _globals['_PINGRESPONSE']._serialized_start=43
  _globals['_PINGRESPONSE']._serialized_end=71
  _globals['_ADDFILEREQUEST']._serialized_start=73
  _globals['_ADDFILEREQUEST']._serialized_end=152
  _globals['_ADDFILERESPONSE']._serialized_start=154
  _globals['_ADDFILERESPONSE']._serialized_end=220
  _globals['_GETFILEREQUEST']._serialized_start=222
  _globals['_GETFILEREQUEST']._serialized_end=269
  _globals['_GETFILERESPONSE']._serialized_start=271
  _globals['_GETFILERESPONSE']._serialized_end=351
  _globals['_GETFILEMETAINFOREQUEST']._serialized_start=353
  _globals['_GETFILEMETAINFOREQUEST']._serialized_end=408
  _globals['_GETFILEMETAINFORESPONSE']._serialized_start=410
  _globals['_GETFILEMETAINFORESPONSE']._serialized_end=484
  _globals['_DELETEFILEREQUEST']._serialized_start=486
  _globals['_DELETEFILEREQUEST']._serialized_end=536
  _globals['_DELETEFILERESPONSE']._serialized_start=538
  _globals['_DELETEFILERESPONSE']._serialized_end=607
  _globals['_PUTFILEREQUEST']._serialized_start=609
  _globals['_PUTFILEREQUEST']._serialized_end=688
  _globals['_PUTFILERESPONSE']._serialized_start=690
  _globals['_PUTFILERESPONSE']._serialized_end=756
  _globals['_GETMANYFILESMETAINFOREQUEST']._serialized_start=758
  _globals['_GETMANYFILESMETAINFOREQUEST']._serialized_end=832
  _globals['_GETMANYFILESMETAINFORESPONSE']._serialized_start=834
  _globals['_GETMANYFILESMETAINFORESPONSE']._serialized_end=878
  _globals['_FILEAPI']._serialized_start=881
  _globals['_FILEAPI']._serialized_end=1415
# @@protoc_insertion_point(module_scope)
