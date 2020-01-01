"""API that streams the newer protocol buffers from Nest."""

import uuid

from proto.nest_gateway_pb2 import ObserveRequest


_URL = 'https://grpc-web.production.nest.com/nestlabs.gateway.v2.GatewayService/Observe'

_TRAITS = [
    'nest.trait.hvac.EcoModeTrait',
    'nest.trait.hvac.TargetTemperatureSettingsTrait',
]


def run(api):
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
  headers.update(api._authorization_headers)
  print(headers)

  request = ObserveRequest()
  request.state_types_list.extend([2, 1])
  for trait_type in _TRAITS:
    params = request.trait_type_params.add()
    params.trait_type = trait_type
  print(request, request.SerializeToString())

  r = api._session.post(
      _URL,
      data=request.SerializeToString(),
      stream=True)
  for line in r.iter_lines():
    if not line:
      continue
    print(line)


if __name__ == '__main__':
  import logging
  logging.basicConfig(level=logging.INFO)

  import importlib.util
  spec = importlib.util.spec_from_file_location('module.name', 'secret.py')
  secret = importlib.util.module_from_spec(spec)
  spec.loader.exec_module(secret)

  from nest import Nest
  nest = Nest()
  nest.login(secret.ISSUE_TOKEN, secret.COOKIE)

  run(nest)
