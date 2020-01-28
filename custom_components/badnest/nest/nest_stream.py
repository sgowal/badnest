"""API that streams the newer protocol buffers from Nest."""

import base64
import collections
import requests
import threading
import uuid

if __package__:
  from .nest_pb2 import (
      StreamBody,
      ObserveResponse,
      ObserveRequest,
      DeviceInfoTrait,
      LocatedAnnotationsTrait,
      DeviceLocatedSettingsTrait,
      TemperatureTrait,
      HumidityTrait,
      TargetTemperatureSettingsTrait,
      EcoModeStateTrait,
  )

  from .nest_thermostat import (
      ThermostatE,
      HeatLink,
  )
else:
  from nest_pb2 import (
      StreamBody,
      ObserveResponse,
      ObserveRequest,
      DeviceInfoTrait,
      LocatedAnnotationsTrait,
      DeviceLocatedSettingsTrait,
      TemperatureTrait,
      HumidityTrait,
      TargetTemperatureSettingsTrait,
      EcoModeStateTrait,
  )

  from nest_thermostat import (
      ThermostatE,
      HeatLink,
  )


_URL = 'https://grpc-web.production.nest.com/nestlabs.gateway.v2.GatewayService/Observe'
_UPDATE_URL = 'https://grpc-web.production.nest.com/nestlabs.gateway.v1.TraitBatchApi/BatchUpdateState'

_TRAITS = {
    'nest.trait.service.DeviceInfoTrait': DeviceInfoTrait,
    'nest.trait.located.LocatedAnnotationsTrait': LocatedAnnotationsTrait,
    'nest.trait.located.DeviceLocatedSettingsTrait': DeviceLocatedSettingsTrait,
    'nest.trait.sensor.TemperatureTrait': TemperatureTrait,
    'nest.trait.sensor.HumidityTrait': HumidityTrait,
    'nest.trait.hvac.TargetTemperatureSettingsTrait': TargetTemperatureSettingsTrait,
    'nest.trait.hvac.EcoModeStateTrait': EcoModeStateTrait,
}

_UPDATE_TRAITS = {
    'nest.trait.sensor.TemperatureTrait': TemperatureTrait,
    'nest.trait.sensor.HumidityTrait': HumidityTrait,
    'nest.trait.hvac.TargetTemperatureSettingsTrait': TargetTemperatureSettingsTrait,
    'nest.trait.hvac.EcoModeStateTrait': EcoModeStateTrait,
}

# Testing.
_ASYNC_UPDATE_TRAITS = {
    'nest.trait.sensor.TemperatureTrait': TemperatureTrait,
    'nest.trait.sensor.HumidityTrait': HumidityTrait,
    'nest.trait.hvac.TargetTemperatureSettingsTrait': TargetTemperatureSettingsTrait,
    'nest.trait.hvac.EcoModeStateTrait': EcoModeStateTrait,
}

_DEVICES = {
    'agateheatlink': HeatLink,
    'agatedisplay': ThermostatE,
}


class StreamingAPI(object):

  def __init__(self, backend):
    self._backend = backend
    self._update_lock = threading.Lock()
    self._devices = None

  @property
  def logging(self):
    return self._backend._logging

  def list_devices(self):
    with self._update_lock:
      devices = {}
      unprocessed_protos = collections.defaultdict(list)

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

      request = ObserveRequest()
      request.state_types_list.extend([2, 1])
      for trait_type in _TRAITS:
        params = request.trait_type_params.add()
        params.trait_type = trait_type

      r = self._backend._stream(_URL, data=request.SerializeToString(), headers=headers)
      if r is None:
        self._logging.error('Unable to list streaming devices.')
        return []

      try:
        for c in r.iter_content(chunk_size=None):
          if not c:
            continue
          decoded_bytes = base64.standard_b64decode(c)
          proto = StreamBody()
          proto.ParseFromString(decoded_bytes)
          response = ObserveResponse()
          for message in proto.message:
            response.ParseFromString(message)
            protos = process_response(response)

            for device, label, proto in protos:
              if label == 'device_info' and device not in devices:
                # Potential new device.
                if proto.type in _DEVICES:
                  devices[device] = _DEVICES[proto.type](device.split('_', 1)[-1], self._backend)
                  if device in unprocessed_protos:
                    for l, p in unprocessed_protos[device]:
                      devices[device].update_from_proto(l, p)
                    del unprocessed_protos[device]
              elif device not in devices:
                unprocessed_protos[device].append((label, proto))
              else:
                # New proto for existing device.
                devices[device].update_from_proto(label, proto)
      except requests.exceptions.ConnectionError:
        self.logging.info('Initial bulk of streaming messages received.')

      self._devices = [d for d in devices.values() if d.ready]
      return self._devices

  async def async_update(self):
    # TODO: Provide asynchronous update.
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

    request = ObserveRequest()
    request.state_types_list.extend([2, 1])
    for trait_type in _ASYNC_UPDATE_TRAITS:
      params = request.trait_type_params.add()
      params.trait_type = trait_type

    # Do not timeout.
    r = self._backend._stream(_URL, data=request.SerializeToString(), headers=headers, timeout=None)
    if r is None:
      self._logging.error('Unable to list streaming devices.')
      return

    devices = dict(('DEVICE_' + v.unique_id, v) for v in self._devices)
    try:
      for c in r.iter_content(chunk_size=None):
        if not c:
          continue
        decoded_bytes = base64.standard_b64decode(c)
        proto = StreamBody()
        proto.ParseFromString(decoded_bytes)
        response = ObserveResponse()
        for message in proto.message:
          response.ParseFromString(message)
          protos = process_response(response)

          for device, label, proto in protos:
            if device in devices:
              devices[device].update_from_proto(label, proto)

        self.logging.debug('Async update debug: {}'.format(devices))
    except requests.exceptions.ConnectionError:
      self.logging.info('Communication error.')
    self.logging.info('Async update finished.')

  def update(self):
    with self._update_lock:
      if not self._devices:
        return

      # TODO: Provide asynchronous update.
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

      request = ObserveRequest()
      request.state_types_list.extend([2, 1])
      for trait_type in _UPDATE_TRAITS:
        params = request.trait_type_params.add()
        params.trait_type = trait_type

      r = self._backend._stream(_URL, data=request.SerializeToString(), headers=headers)
      if r is None:
        self._logging.error('Unable to list streaming devices.')
        return False

      devices = dict(('DEVICE_' + v.unique_id, v) for v in self._devices)
      try:
        for c in r.iter_content(chunk_size=None):
          if not c:
            continue
          decoded_bytes = base64.standard_b64decode(c)
          proto = StreamBody()
          proto.ParseFromString(decoded_bytes)
          response = ObserveResponse()
          for message in proto.message:
            response.ParseFromString(message)
            protos = process_response(response)

            for device, label, proto in protos:
              if device in devices:
                devices[device].update_from_proto(label, proto)
      except requests.exceptions.ConnectionError:
        self.logging.info('Bulk of update streaming messages received.')
      return True


def process_trait(trait_type, byte_content):
  if trait_type in _TRAITS and _TRAITS[trait_type] is not None:
    proto = _TRAITS[trait_type]()
    proto.ParseFromString(byte_content)
    return proto
  return None


def process_response(message):
  protos = []
  for trait_state in message.trait_states:
    device = trait_state.trait_id.resource_id
    label = trait_state.trait_id.trait_label
    trait_type = trait_state.patch.values.type_url
    byte_content = trait_state.patch.values.value

    if not trait_type.startswith('type.nestlabs.com/'):
      continue
    trait_type = trait_type.split('/', 1)[1]
    proto = process_trait(trait_type, byte_content)
    if proto is not None:
      protos.append((device, label, proto))
  return protos


if __name__ == '__main__':
  import logging
  logging.basicConfig(level=logging.DEBUG)

  import importlib.util
  spec = importlib.util.spec_from_file_location('module.name', 'secret.py')
  secret = importlib.util.module_from_spec(spec)
  spec.loader.exec_module(secret)

  from nest_api import API
  from nest_thermostat import HVACMode

  api = API(secret.ISSUE_TOKEN, secret.COOKIE)
  api.login()

  stream_api = StreamingAPI(api)
  devices = stream_api.list_devices()
  print('Found devices:', devices)

  thermostat = [d for d in devices if isinstance(d, ThermostatE)][0]
  print(thermostat)

  # if thermostat.set_temperature(19.5):
  #   print('Success changing temperature.')
  # else:
  #   print('Error changing temperature.')

  # if thermostat.set_hvac_mode(HVACMode.HEAT):
  #   print('Success changing mode.')
  # else:
  #   print('Error changing mode.')

  if stream_api.update():
    print('Update successful:', devices)
  else:
    print('Update failed')

  # Testing async updates.
  import asyncio
  asyncio.run(stream_api.async_update())
