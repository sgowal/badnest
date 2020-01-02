# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: nest_gateway.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='nest_gateway.proto',
  package='nestlabs.gateway.v2',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x12nest_gateway.proto\x12\x13nestlabs.gateway.v2\x1a\x19google/protobuf/any.proto\x1a\x1fgoogle/protobuf/timestamp.proto\"\xd3\x01\n\x0eObserveRequest\x12\x18\n\x10state_types_list\x18\x01 \x03(\x05\x12\x46\n\x11trait_type_params\x18\x03 \x03(\x0b\x32+.nestlabs.gateway.v2.TraitTypeObserveParams\x12N\n\x15trait_instance_params\x18\x04 \x03(\x0b\x32/.nestlabs.gateway.v2.TraitInstanceObserveParams\x12\x0f\n\x07user_id\x18\x05 \x01(\t\"t\n\x1aTraitInstanceObserveParams\x12.\n\x08trait_id\x18\x01 \x01(\x0b\x32\x1c.nestlabs.gateway.v2.TraitId\x12&\n\x1emonotonic_version_filters_list\x18\x02 \x01(\x04\"\x87\x01\n\x16TraitTypeObserveParams\x12\x12\n\ntrait_type\x18\x01 \x01(\t\x12\x38\n\x10state_field_mask\x18\x02 \x01(\x0b\x32\x1e.nestlabs.gateway.v2.FieldMask\x12\x1f\n\x17observer_schema_version\x18\x03 \x01(\r\"\x1a\n\tFieldMask\x12\r\n\x05paths\x18\x01 \x03(\t\"\xa6\x02\n\x0fObserveResponse\x12\x39\n\x0eresource_metas\x18\x01 \x03(\x0b\x32!.nestlabs.gateway.v2.ResourceMeta\x12\'\n\x1finitial_resource_metas_continue\x18\x02 \x01(\x08\x12\x35\n\x0ctrait_states\x18\x03 \x03(\x0b\x32\x1f.nestlabs.gateway.v2.TraitState\x12\x46\n\x15trait_operation_lists\x18\x04 \x03(\x0b\x32\'.nestlabs.gateway.v2.TraitOperationList\x12\x30\n\x0c\x63urrent_time\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\"\x83\x01\n\x12TraitOperationList\x12.\n\x08trait_id\x18\x01 \x01(\x0b\x32\x1c.nestlabs.gateway.v2.TraitId\x12=\n\x10trait_operations\x18\x02 \x03(\x0b\x32#.nestlabs.gateway.v2.TraitOperation\"\x10\n\x0eTraitOperation\"\xb3\x01\n\x0cResourceMeta\x12\x13\n\x0bresource_id\x18\x01 \x01(\t\x12\x0c\n\x04type\x18\x02 \x01(\t\x12\x33\n\x0btrait_metas\x18\x04 \x03(\x0b\x32\x1e.nestlabs.gateway.v2.TraitMeta\x12\x16\n\x0eschema_version\x18\x06 \x01(\r\x12\x33\n\x0biface_metas\x18\x07 \x03(\x0b\x32\x1e.nestlabs.gateway.v2.IfaceMeta\"\x9d\x01\n\nTraitState\x12.\n\x08trait_id\x18\x01 \x01(\x0b\x32\x1c.nestlabs.gateway.v2.TraitId\x12)\n\x05patch\x18\x03 \x01(\x0b\x32\x1a.nestlabs.gateway.v2.Patch\x12\x19\n\x11monotonic_version\x18\x04 \x01(\x04\x12\x19\n\x11publisher_version\x18\x05 \x01(\x04\"j\n\tTraitMeta\x12\x13\n\x0btrait_label\x18\x01 \x01(\t\x12\x0c\n\x04type\x18\x02 \x01(\t\x12:\n\x0eschema_version\x18\x03 \x01(\x0b\x32\".nestlabs.gateway.v2.SchemaVersion\"3\n\x07TraitId\x12\x13\n\x0bresource_id\x18\x01 \x01(\t\x12\x13\n\x0btrait_label\x18\x02 \x01(\t\"\xf8\x01\n\tIfaceMeta\x12\x13\n\x0biface_label\x18\x01 \x01(\t\x12\x0c\n\x04type\x18\x02 \x01(\t\x12R\n\x13trait_label_mapping\x18\x03 \x03(\x0b\x32\x35.nestlabs.gateway.v2.IfaceMeta.TraitLabelMappingEntry\x12:\n\x0eschema_version\x18\x04 \x01(\x0b\x32\".nestlabs.gateway.v2.SchemaVersion\x1a\x38\n\x16TraitLabelMappingEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"-\n\x05Patch\x12$\n\x06values\x18\x01 \x01(\x0b\x32\x14.google.protobuf.Any\"D\n\rSchemaVersion\x12\x17\n\x0f\x63urrent_version\x18\x01 \x01(\r\x12\x1a\n\x12min_compat_version\x18\x02 \x01(\r2h\n\x0eGatewayService\x12V\n\x07Observe\x12#.nestlabs.gateway.v2.ObserveRequest\x1a$.nestlabs.gateway.v2.ObserveResponse0\x01\x62\x06proto3')
  ,
  dependencies=[google_dot_protobuf_dot_any__pb2.DESCRIPTOR,google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR,])




_OBSERVEREQUEST = _descriptor.Descriptor(
  name='ObserveRequest',
  full_name='nestlabs.gateway.v2.ObserveRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='state_types_list', full_name='nestlabs.gateway.v2.ObserveRequest.state_types_list', index=0,
      number=1, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='trait_type_params', full_name='nestlabs.gateway.v2.ObserveRequest.trait_type_params', index=1,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='trait_instance_params', full_name='nestlabs.gateway.v2.ObserveRequest.trait_instance_params', index=2,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='user_id', full_name='nestlabs.gateway.v2.ObserveRequest.user_id', index=3,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=104,
  serialized_end=315,
)


_TRAITINSTANCEOBSERVEPARAMS = _descriptor.Descriptor(
  name='TraitInstanceObserveParams',
  full_name='nestlabs.gateway.v2.TraitInstanceObserveParams',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='trait_id', full_name='nestlabs.gateway.v2.TraitInstanceObserveParams.trait_id', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='monotonic_version_filters_list', full_name='nestlabs.gateway.v2.TraitInstanceObserveParams.monotonic_version_filters_list', index=1,
      number=2, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=317,
  serialized_end=433,
)


_TRAITTYPEOBSERVEPARAMS = _descriptor.Descriptor(
  name='TraitTypeObserveParams',
  full_name='nestlabs.gateway.v2.TraitTypeObserveParams',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='trait_type', full_name='nestlabs.gateway.v2.TraitTypeObserveParams.trait_type', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='state_field_mask', full_name='nestlabs.gateway.v2.TraitTypeObserveParams.state_field_mask', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='observer_schema_version', full_name='nestlabs.gateway.v2.TraitTypeObserveParams.observer_schema_version', index=2,
      number=3, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=436,
  serialized_end=571,
)


_FIELDMASK = _descriptor.Descriptor(
  name='FieldMask',
  full_name='nestlabs.gateway.v2.FieldMask',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='paths', full_name='nestlabs.gateway.v2.FieldMask.paths', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=573,
  serialized_end=599,
)


_OBSERVERESPONSE = _descriptor.Descriptor(
  name='ObserveResponse',
  full_name='nestlabs.gateway.v2.ObserveResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='resource_metas', full_name='nestlabs.gateway.v2.ObserveResponse.resource_metas', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='initial_resource_metas_continue', full_name='nestlabs.gateway.v2.ObserveResponse.initial_resource_metas_continue', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='trait_states', full_name='nestlabs.gateway.v2.ObserveResponse.trait_states', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='trait_operation_lists', full_name='nestlabs.gateway.v2.ObserveResponse.trait_operation_lists', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='current_time', full_name='nestlabs.gateway.v2.ObserveResponse.current_time', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=602,
  serialized_end=896,
)


_TRAITOPERATIONLIST = _descriptor.Descriptor(
  name='TraitOperationList',
  full_name='nestlabs.gateway.v2.TraitOperationList',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='trait_id', full_name='nestlabs.gateway.v2.TraitOperationList.trait_id', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='trait_operations', full_name='nestlabs.gateway.v2.TraitOperationList.trait_operations', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=899,
  serialized_end=1030,
)


_TRAITOPERATION = _descriptor.Descriptor(
  name='TraitOperation',
  full_name='nestlabs.gateway.v2.TraitOperation',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
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
  serialized_start=1032,
  serialized_end=1048,
)


_RESOURCEMETA = _descriptor.Descriptor(
  name='ResourceMeta',
  full_name='nestlabs.gateway.v2.ResourceMeta',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='resource_id', full_name='nestlabs.gateway.v2.ResourceMeta.resource_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='type', full_name='nestlabs.gateway.v2.ResourceMeta.type', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='trait_metas', full_name='nestlabs.gateway.v2.ResourceMeta.trait_metas', index=2,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='schema_version', full_name='nestlabs.gateway.v2.ResourceMeta.schema_version', index=3,
      number=6, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='iface_metas', full_name='nestlabs.gateway.v2.ResourceMeta.iface_metas', index=4,
      number=7, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=1051,
  serialized_end=1230,
)


_TRAITSTATE = _descriptor.Descriptor(
  name='TraitState',
  full_name='nestlabs.gateway.v2.TraitState',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='trait_id', full_name='nestlabs.gateway.v2.TraitState.trait_id', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='patch', full_name='nestlabs.gateway.v2.TraitState.patch', index=1,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='monotonic_version', full_name='nestlabs.gateway.v2.TraitState.monotonic_version', index=2,
      number=4, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='publisher_version', full_name='nestlabs.gateway.v2.TraitState.publisher_version', index=3,
      number=5, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=1233,
  serialized_end=1390,
)


_TRAITMETA = _descriptor.Descriptor(
  name='TraitMeta',
  full_name='nestlabs.gateway.v2.TraitMeta',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='trait_label', full_name='nestlabs.gateway.v2.TraitMeta.trait_label', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='type', full_name='nestlabs.gateway.v2.TraitMeta.type', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='schema_version', full_name='nestlabs.gateway.v2.TraitMeta.schema_version', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=1392,
  serialized_end=1498,
)


_TRAITID = _descriptor.Descriptor(
  name='TraitId',
  full_name='nestlabs.gateway.v2.TraitId',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='resource_id', full_name='nestlabs.gateway.v2.TraitId.resource_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='trait_label', full_name='nestlabs.gateway.v2.TraitId.trait_label', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=1500,
  serialized_end=1551,
)


_IFACEMETA_TRAITLABELMAPPINGENTRY = _descriptor.Descriptor(
  name='TraitLabelMappingEntry',
  full_name='nestlabs.gateway.v2.IfaceMeta.TraitLabelMappingEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='nestlabs.gateway.v2.IfaceMeta.TraitLabelMappingEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='nestlabs.gateway.v2.IfaceMeta.TraitLabelMappingEntry.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=_b('8\001'),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1746,
  serialized_end=1802,
)

_IFACEMETA = _descriptor.Descriptor(
  name='IfaceMeta',
  full_name='nestlabs.gateway.v2.IfaceMeta',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='iface_label', full_name='nestlabs.gateway.v2.IfaceMeta.iface_label', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='type', full_name='nestlabs.gateway.v2.IfaceMeta.type', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='trait_label_mapping', full_name='nestlabs.gateway.v2.IfaceMeta.trait_label_mapping', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='schema_version', full_name='nestlabs.gateway.v2.IfaceMeta.schema_version', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_IFACEMETA_TRAITLABELMAPPINGENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1554,
  serialized_end=1802,
)


_PATCH = _descriptor.Descriptor(
  name='Patch',
  full_name='nestlabs.gateway.v2.Patch',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='values', full_name='nestlabs.gateway.v2.Patch.values', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=1804,
  serialized_end=1849,
)


_SCHEMAVERSION = _descriptor.Descriptor(
  name='SchemaVersion',
  full_name='nestlabs.gateway.v2.SchemaVersion',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='current_version', full_name='nestlabs.gateway.v2.SchemaVersion.current_version', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='min_compat_version', full_name='nestlabs.gateway.v2.SchemaVersion.min_compat_version', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=1851,
  serialized_end=1919,
)

_OBSERVEREQUEST.fields_by_name['trait_type_params'].message_type = _TRAITTYPEOBSERVEPARAMS
_OBSERVEREQUEST.fields_by_name['trait_instance_params'].message_type = _TRAITINSTANCEOBSERVEPARAMS
_TRAITINSTANCEOBSERVEPARAMS.fields_by_name['trait_id'].message_type = _TRAITID
_TRAITTYPEOBSERVEPARAMS.fields_by_name['state_field_mask'].message_type = _FIELDMASK
_OBSERVERESPONSE.fields_by_name['resource_metas'].message_type = _RESOURCEMETA
_OBSERVERESPONSE.fields_by_name['trait_states'].message_type = _TRAITSTATE
_OBSERVERESPONSE.fields_by_name['trait_operation_lists'].message_type = _TRAITOPERATIONLIST
_OBSERVERESPONSE.fields_by_name['current_time'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_TRAITOPERATIONLIST.fields_by_name['trait_id'].message_type = _TRAITID
_TRAITOPERATIONLIST.fields_by_name['trait_operations'].message_type = _TRAITOPERATION
_RESOURCEMETA.fields_by_name['trait_metas'].message_type = _TRAITMETA
_RESOURCEMETA.fields_by_name['iface_metas'].message_type = _IFACEMETA
_TRAITSTATE.fields_by_name['trait_id'].message_type = _TRAITID
_TRAITSTATE.fields_by_name['patch'].message_type = _PATCH
_TRAITMETA.fields_by_name['schema_version'].message_type = _SCHEMAVERSION
_IFACEMETA_TRAITLABELMAPPINGENTRY.containing_type = _IFACEMETA
_IFACEMETA.fields_by_name['trait_label_mapping'].message_type = _IFACEMETA_TRAITLABELMAPPINGENTRY
_IFACEMETA.fields_by_name['schema_version'].message_type = _SCHEMAVERSION
_PATCH.fields_by_name['values'].message_type = google_dot_protobuf_dot_any__pb2._ANY
DESCRIPTOR.message_types_by_name['ObserveRequest'] = _OBSERVEREQUEST
DESCRIPTOR.message_types_by_name['TraitInstanceObserveParams'] = _TRAITINSTANCEOBSERVEPARAMS
DESCRIPTOR.message_types_by_name['TraitTypeObserveParams'] = _TRAITTYPEOBSERVEPARAMS
DESCRIPTOR.message_types_by_name['FieldMask'] = _FIELDMASK
DESCRIPTOR.message_types_by_name['ObserveResponse'] = _OBSERVERESPONSE
DESCRIPTOR.message_types_by_name['TraitOperationList'] = _TRAITOPERATIONLIST
DESCRIPTOR.message_types_by_name['TraitOperation'] = _TRAITOPERATION
DESCRIPTOR.message_types_by_name['ResourceMeta'] = _RESOURCEMETA
DESCRIPTOR.message_types_by_name['TraitState'] = _TRAITSTATE
DESCRIPTOR.message_types_by_name['TraitMeta'] = _TRAITMETA
DESCRIPTOR.message_types_by_name['TraitId'] = _TRAITID
DESCRIPTOR.message_types_by_name['IfaceMeta'] = _IFACEMETA
DESCRIPTOR.message_types_by_name['Patch'] = _PATCH
DESCRIPTOR.message_types_by_name['SchemaVersion'] = _SCHEMAVERSION
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ObserveRequest = _reflection.GeneratedProtocolMessageType('ObserveRequest', (_message.Message,), dict(
  DESCRIPTOR = _OBSERVEREQUEST,
  __module__ = 'nest_gateway_pb2'
  # @@protoc_insertion_point(class_scope:nestlabs.gateway.v2.ObserveRequest)
  ))
_sym_db.RegisterMessage(ObserveRequest)

TraitInstanceObserveParams = _reflection.GeneratedProtocolMessageType('TraitInstanceObserveParams', (_message.Message,), dict(
  DESCRIPTOR = _TRAITINSTANCEOBSERVEPARAMS,
  __module__ = 'nest_gateway_pb2'
  # @@protoc_insertion_point(class_scope:nestlabs.gateway.v2.TraitInstanceObserveParams)
  ))
_sym_db.RegisterMessage(TraitInstanceObserveParams)

TraitTypeObserveParams = _reflection.GeneratedProtocolMessageType('TraitTypeObserveParams', (_message.Message,), dict(
  DESCRIPTOR = _TRAITTYPEOBSERVEPARAMS,
  __module__ = 'nest_gateway_pb2'
  # @@protoc_insertion_point(class_scope:nestlabs.gateway.v2.TraitTypeObserveParams)
  ))
_sym_db.RegisterMessage(TraitTypeObserveParams)

FieldMask = _reflection.GeneratedProtocolMessageType('FieldMask', (_message.Message,), dict(
  DESCRIPTOR = _FIELDMASK,
  __module__ = 'nest_gateway_pb2'
  # @@protoc_insertion_point(class_scope:nestlabs.gateway.v2.FieldMask)
  ))
_sym_db.RegisterMessage(FieldMask)

ObserveResponse = _reflection.GeneratedProtocolMessageType('ObserveResponse', (_message.Message,), dict(
  DESCRIPTOR = _OBSERVERESPONSE,
  __module__ = 'nest_gateway_pb2'
  # @@protoc_insertion_point(class_scope:nestlabs.gateway.v2.ObserveResponse)
  ))
_sym_db.RegisterMessage(ObserveResponse)

TraitOperationList = _reflection.GeneratedProtocolMessageType('TraitOperationList', (_message.Message,), dict(
  DESCRIPTOR = _TRAITOPERATIONLIST,
  __module__ = 'nest_gateway_pb2'
  # @@protoc_insertion_point(class_scope:nestlabs.gateway.v2.TraitOperationList)
  ))
_sym_db.RegisterMessage(TraitOperationList)

TraitOperation = _reflection.GeneratedProtocolMessageType('TraitOperation', (_message.Message,), dict(
  DESCRIPTOR = _TRAITOPERATION,
  __module__ = 'nest_gateway_pb2'
  # @@protoc_insertion_point(class_scope:nestlabs.gateway.v2.TraitOperation)
  ))
_sym_db.RegisterMessage(TraitOperation)

ResourceMeta = _reflection.GeneratedProtocolMessageType('ResourceMeta', (_message.Message,), dict(
  DESCRIPTOR = _RESOURCEMETA,
  __module__ = 'nest_gateway_pb2'
  # @@protoc_insertion_point(class_scope:nestlabs.gateway.v2.ResourceMeta)
  ))
_sym_db.RegisterMessage(ResourceMeta)

TraitState = _reflection.GeneratedProtocolMessageType('TraitState', (_message.Message,), dict(
  DESCRIPTOR = _TRAITSTATE,
  __module__ = 'nest_gateway_pb2'
  # @@protoc_insertion_point(class_scope:nestlabs.gateway.v2.TraitState)
  ))
_sym_db.RegisterMessage(TraitState)

TraitMeta = _reflection.GeneratedProtocolMessageType('TraitMeta', (_message.Message,), dict(
  DESCRIPTOR = _TRAITMETA,
  __module__ = 'nest_gateway_pb2'
  # @@protoc_insertion_point(class_scope:nestlabs.gateway.v2.TraitMeta)
  ))
_sym_db.RegisterMessage(TraitMeta)

TraitId = _reflection.GeneratedProtocolMessageType('TraitId', (_message.Message,), dict(
  DESCRIPTOR = _TRAITID,
  __module__ = 'nest_gateway_pb2'
  # @@protoc_insertion_point(class_scope:nestlabs.gateway.v2.TraitId)
  ))
_sym_db.RegisterMessage(TraitId)

IfaceMeta = _reflection.GeneratedProtocolMessageType('IfaceMeta', (_message.Message,), dict(

  TraitLabelMappingEntry = _reflection.GeneratedProtocolMessageType('TraitLabelMappingEntry', (_message.Message,), dict(
    DESCRIPTOR = _IFACEMETA_TRAITLABELMAPPINGENTRY,
    __module__ = 'nest_gateway_pb2'
    # @@protoc_insertion_point(class_scope:nestlabs.gateway.v2.IfaceMeta.TraitLabelMappingEntry)
    ))
  ,
  DESCRIPTOR = _IFACEMETA,
  __module__ = 'nest_gateway_pb2'
  # @@protoc_insertion_point(class_scope:nestlabs.gateway.v2.IfaceMeta)
  ))
_sym_db.RegisterMessage(IfaceMeta)
_sym_db.RegisterMessage(IfaceMeta.TraitLabelMappingEntry)

Patch = _reflection.GeneratedProtocolMessageType('Patch', (_message.Message,), dict(
  DESCRIPTOR = _PATCH,
  __module__ = 'nest_gateway_pb2'
  # @@protoc_insertion_point(class_scope:nestlabs.gateway.v2.Patch)
  ))
_sym_db.RegisterMessage(Patch)

SchemaVersion = _reflection.GeneratedProtocolMessageType('SchemaVersion', (_message.Message,), dict(
  DESCRIPTOR = _SCHEMAVERSION,
  __module__ = 'nest_gateway_pb2'
  # @@protoc_insertion_point(class_scope:nestlabs.gateway.v2.SchemaVersion)
  ))
_sym_db.RegisterMessage(SchemaVersion)


_IFACEMETA_TRAITLABELMAPPINGENTRY._options = None

_GATEWAYSERVICE = _descriptor.ServiceDescriptor(
  name='GatewayService',
  full_name='nestlabs.gateway.v2.GatewayService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=1921,
  serialized_end=2025,
  methods=[
  _descriptor.MethodDescriptor(
    name='Observe',
    full_name='nestlabs.gateway.v2.GatewayService.Observe',
    index=0,
    containing_service=None,
    input_type=_OBSERVEREQUEST,
    output_type=_OBSERVERESPONSE,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_GATEWAYSERVICE)

DESCRIPTOR.services_by_name['GatewayService'] = _GATEWAYSERVICE

# @@protoc_insertion_point(module_scope)
