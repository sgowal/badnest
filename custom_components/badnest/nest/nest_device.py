import abc
import base64
import threading
import six
import uuid

if __package__:
  from .nest_pb2 import (
      BatchUpdateRequest,
      BatchUpdateResponse,
      TargetTemperatureSettingsTrait,
      EcoModeStateTrait,
  )
else:
  from nest_pb2 import (
      BatchUpdateRequest,
      BatchUpdateResponse,
      TargetTemperatureSettingsTrait,
      EcoModeStateTrait,
  )


_UPDATE_STREAM_URL = 'https://grpc-web.production.nest.com/nestlabs.gateway.v1.TraitBatchApi/BatchUpdateState'


@six.add_metaclass(abc.ABCMeta)
class Device(object):

  def __init__(self, serial_number, name, backend):
    self._serial_number = serial_number
    self._name = name
    self._backend = backend

  def update_from_json(self, json):
    return

  def update_from_proto(self, label, proto):
    return

  @property
  def ready(self):
    return True

  @property
  def unique_id(self):
    return self._serial_number

  @property
  def name(self):
    return self._name

  @property
  def logging(self):
    return self._backend._logging

  def fetch_post(self, *args, **kwargs):
    return self._backend._fetch_and_verify(*args, use_get=False, **kwargs)

  def fetch_get(self, *args, **kwargs):
    return self._backend._fetch_and_verify(*args, use_get=True, **kwargs)

  @property
  def authorization_headers(self):
    return self._backend._authorization_headers

  @property
  def camera_authorization_headers(self):
    return self._backend._camera_authorization_headers

  def update(self):
    """Centralized update function."""
    self._backend.update()


@six.add_metaclass(abc.ABCMeta)
class StreamingDevice(Device):
  # We keep track of locations as a last resort.
  _class_lock = threading.Lock()
  _located_annotations = {}

  def __init__(self, serial_number, backend):
    self._backend = backend
    self._serial_number = serial_number

    # Setup properties.
    self._properties_lock = threading.Lock()
    self._name = None
    self._located_annotations_proto = None
    self._device_located_settings_proto = None

  @abc.abstractproperty
  def ready(self):
    pass

  def _fill_name(self):
    if self._located_annotations_proto is None or self._device_located_settings_proto is None:
      return
    if self._name is not None:
      return
    rid = self._device_located_settings_proto.where_annotation_rid.value
    for v in self._located_annotations_proto.predefined_wheres_map.values():
      if v.resource_id.value == rid:
        self._name = v.label.value
        break
    if self._name is None:
      for v in self._located_annotations_proto.custom_wheres_map.values():
        if v.resource_id.value == rid:
          self._name = v.label.value
          break
    print('Found name:', self.unique_id, self._name)

  def fixit(self):
    with self._properties_lock:
      if self._name is not None:
        return
      if self._device_located_settings_proto is None:
        self._name = 'Unknown'
        return
      rid = self._device_located_settings_proto.where_annotation_rid.value
      with self._class_lock:
        if rid in self._located_annotations:
          self._name = self._located_annotations[rid]
        else:
          self._name = 'Unknown'

  def update_from_proto(self, label, proto):
    with self._properties_lock:
      if label == 'located_annotations':
        with self._class_lock:
          for v in proto.predefined_wheres_map.values():
            self._located_annotations[v.resource_id.value] = v.label.value
        self._located_annotations_proto = proto
        self._fill_name()
        return True
      elif label == 'device_located_settings':
        self._device_located_settings_proto = proto
        self._fill_name()
        return True
      return False

  def set(self, label, proto):
    request = BatchUpdateRequest()
    op = request.operations.add()
    op.trait_id.resource_id = 'DEVICE_' + self.unique_id
    op.trait_id.trait_label = label
    if isinstance(proto, TargetTemperatureSettingsTrait):
      op.patch.type_url = 'type.nestlabs.com/nest.trait.hvac.TargetTemperatureSettingsTrait'
    elif isinstance(proto, EcoModeStateTrait):
      op.patch.type_url = 'type.nestlabs.com/nest.trait.hvac.EcoModeStateTrait'
    else:
      return False
    op.patch.value = proto.SerializeToString()

    headers = {
        'Origin': 'https://home.nest.com',
        'Referer': 'https://home.nest.com/',
        'Content-Type': 'application/x-protobuf',
        'X-Accept-Content-Transfer-Encoding': 'base64',
        'X-Accept-Response-Streaming': 'true',
        'request-id': str(uuid.uuid1()),
        'X-nl-webapp-version': 'NlAppSDKVersion/8.15.0 NlSchemaVersion/2.1.20-87-gce5742894',
        'Sec-Fetch-Mode': 'cors',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
    }
    headers.update(self._backend._authorization_headers)
    r = self._backend._stream(
        _UPDATE_STREAM_URL,
        data=request.SerializeToString(),
        headers=headers)
    if r is None:
      return False

    got_ok = False
    for c in r.iter_content(chunk_size=None):
      if not c:
        continue
      decoded_bytes = base64.standard_b64decode(c)
      response = BatchUpdateResponse()
      response.ParseFromString(decoded_bytes)
      if response.HasField('success'):
        got_ok = True
      elif not got_ok and response.HasField('error') and response.error.HasField('message'):
        self._logging.error('Error while setting property of streaming device:', response.error.message)
    return got_ok
