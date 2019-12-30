from datetime import datetime
import logging
import requests
import threading

if __package__:
  from .nest_camera import Camera
  from .nest_smoke_alarm import SmokeAlarm
  from .nest_thermostat import Thermostat
else:
  from nest_camera import Camera
  from nest_smoke_alarm import SmokeAlarm
  from nest_thermostat import Thermostat

_USER_AGENT = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) '
               'AppleWebKit/537.36 (KHTML, like Gecko) '
               'Chrome/75.0.3770.100 Safari/537.36')
_URL_JWT = "https://nestauthproxyservice-pa.googleapis.com/v1/issue_jwt"
# Nest public API key.
_NEST_API_ROOT_URL = 'https://home.nest.com'
_CAMERA_API_ROOT_URL = 'https://webapi.camera.home.nest.com'
_NEST_API_KEY = 'AIzaSyAdkSIMNc51XGNEAYWasX9UOWkS5P6sZE4'
_TIME_BETWEEN_UPDATE = 60


class Nest(object):

  def __init__(self):
    self._logging = logging.getLogger(__name__)

    self._session = requests.Session()
    self._user_id = None  # Populated after login.
    self._access_token = None  # Populated after login.

    self._request_lock = threading.Lock()
    self._devices = None

    self._update_lock = threading.Lock()
    self._last_update = None

  def _fetch_and_verify(self, url, headers, data=None, json=None, params=None, use_get=True, ignore_status_code=()):
    try:
      if use_get:
        with self._request_lock:
          response = self._session.get(url=url, headers=headers, data=data, json=json, params=params)
      else:
        with self._request_lock:
          response = self._session.post(url=url, headers=headers, data=data, json=json, params=params)
    except requests.exceptions.RequestException as e:
      self._logging.error('Invalid request: %s', str(e))
      return None
    if response.status_code == 200:
      if response.headers['content-type'].startswith('application/json'):
        return response.json()
      else:
        return response.content
    if response.status_code not in ignore_status_code:
      self._logging.error('Invalid response status: %d (%s)', response.status_code, response.text)
    return None

  def _get_login_access_token(self, issue_token, cookie):
    headers = {
        'User-Agent': _USER_AGENT,
        'Sec-Fetch-Mode': 'cors',
        'X-Requested-With': 'XmlHttpRequest',
        'Referer': 'https://accounts.google.com/o/oauth2/iframe',
        'cookie': cookie,
    }
    response = self._fetch_and_verify(url=issue_token, headers=headers, use_get=True)
    if response:
      return response['access_token']
    return None

  def _get_login_information(self, access_token):
    headers = {
        'User-Agent': _USER_AGENT,
        'Authorization': 'Bearer ' + access_token,
        'x-goog-api-key': _NEST_API_KEY,
        'Referer': 'https://home.nest.com'
    }
    params = {
        'embed_google_oauth_access_token': True,
        'expire_after': '3600s',
        'google_oauth_access_token': access_token,
        'policy_id': 'authproxy-oauth-policy'
    }
    return self._fetch_and_verify(url=_URL_JWT, headers=headers, params=params, use_get=False)

  def login(self, issue_token, cookie):
    access_token = self._get_login_access_token(issue_token, cookie)
    info = self._get_login_information(access_token)
    if not info:
      self._logging.warning('Login failed.')
      return False
    self._user_id = info['claims']['subject']['nestId']['id']
    self._access_token = info['jwt']
    self._logging.info('Login successful.')
    return True

  @property
  def _status_url(self):
    if self._user_id is None:
      raise RuntimeError('Not logged in.')
    return '{}/api/0.1/user/{}/app_launch'.format(_NEST_API_ROOT_URL, self._user_id)

  @property
  def _authorization_headers(self):
    if self._access_token is None:
      raise RuntimeError('Not logged in.')
    return {'Authorization': 'Basic {}'.format(self._access_token)}

  @property
  def _camera_authorization_headers(self):
    if self._access_token is None:
      raise RuntimeError('Not logged in.')
    return {
        'User-Agent': _USER_AGENT,
        'X-Requested-With': 'XmlHttpRequest',
        'Referer': 'https://home.nest.com/',
        'cookie': 'user_token={}'.format(self._access_token)
    }

  def list_devices(self):
    response = self._fetch_and_verify(
        url=self._status_url,
        json={
            'known_bucket_types': ['where', 'device', 'shared', 'topaz'],
            'known_bucket_versions': [],
        },
        headers=self._authorization_headers,
        use_get=False)
    if not response:
      self._logging.error('Unable to list devices.')
      return []

    # Get location names.
    rooms = {}
    for bucket in response['updated_buckets']:
      if not bucket['object_key'].startswith('where'):
        continue
      for room in bucket['value']['wheres']:
        rooms[room['where_id']] = room['name']

    # Create all devices.
    thermostats_url = response['service_urls']['urls']['czfe_url']
    devices = []
    for bucket in response['updated_buckets']:
      if bucket['object_key'].startswith('shared'):
        serial_number = bucket['object_key'].split('.', 1)[1]
        values = bucket['value']
        # Thermostats are split in two buckets.
        for bucket2 in response['updated_buckets']:
          if bucket2['object_key'] == 'device.' + serial_number:
            values.update(bucket2['value'])
            break
        name = rooms[values['where_id']]
        description = values.get('description', None)
        if description:
           name += ' ({})'.format(description)
        device = Thermostat(serial_number, name, self, thermostats_url)
        device.update_from_json(values)
        devices.append(device)

      elif bucket['object_key'].startswith('topaz'):
        serial_number = bucket['object_key'].split('.', 1)[1]
        values = bucket['value']
        name = rooms[values['where_id']]
        description = values.get('description', None)
        if description:
           name += ' ({})'.format(description)
        device = SmokeAlarm(serial_number, name, self)
        device.update_from_json(values)
        devices.append(device)

    # Cameras are handled separately.
    response = self._fetch_and_verify(
        url='{}/api/cameras.get_owned_and_member_of_with_properties'.format(_CAMERA_API_ROOT_URL),
        headers=self._camera_authorization_headers,
        use_get=True)
    if not response:
      self._logging.error('Unable to find cameras.')
      return devices
    for values in response['items']:
      serial_number = values['uuid']
      name = values['name']
      image_url = 'https://' + values['nexus_api_nest_domain_host']
      property_url = '{}/api/dropcams.set_properties'.format(_CAMERA_API_ROOT_URL)
      device = Camera(serial_number, name, self, property_url, image_url)
      device.update_from_json(values)
      devices.append(device)

    self._devices = devices
    self._logging.info('Devices listed and updated.')
    return devices

  def update(self, reload_devices=False):
    now = datetime.now().timestamp()
    self._update_lock.acquire()
    if not reload_devices and self._last_update is not None and now - self._last_update < _TIME_BETWEEN_UPDATE:
      self._update_lock.release()
      self._logging.info('Devices updated (from cache).')
      return
    self._last_update = now
    self._update_lock.release()

    if self._devices is None or reload_devices:
      self.list_devices()
      return

    response = self._fetch_and_verify(
        url=self._status_url,
        json={
            'known_bucket_types': ['device', 'shared', 'topaz'],
            'known_bucket_versions': [],
        },
        headers=self._authorization_headers,
        use_get=False)
    if not response:
      self._logging.error('Unable to update devices.')
      return False

    devices = dict((d.unique_id, d) for d in self._devices)
    for bucket in response['updated_buckets']:
      if bucket['object_key'].startswith('shared'):
        serial_number = bucket['object_key'].split('.', 1)[1]
        values = bucket['value']
        # Thermostats are split in two buckets.
        for bucket2 in response['updated_buckets']:
          if bucket2['object_key'] == 'device.' + serial_number:
            values.update(bucket2['value'])
            break
      elif bucket['object_key'].startswith('topaz'):
        serial_number = bucket['object_key'].split('.', 1)[1]
        values = bucket['value']
      else:
        continue
      if serial_number not in devices:
        self._logging.warn('New devices found (but not updated, restart is needed).')
        continue
      devices[serial_number].update_from_json(values)

    # Cameras are handled separately.
    response = self._fetch_and_verify(
        url='{}/api/cameras.get_owned_and_member_of_with_properties'.format(_CAMERA_API_ROOT_URL),
        headers=self._camera_authorization_headers,
        use_get=True)
    if not response:
      self._logging.error('Unable to update cameras.')
      return False
    for values in response['items']:
      serial_number = values['uuid']
      if serial_number not in devices:
        self._logging.warn('New devices found (but not updated, restart is needed).')
        continue
      devices[serial_number].update_from_json(values)

    self._logging.info('Devices updated.')
    return True


if __name__ == '__main__':
  logging.basicConfig(level=logging.INFO)

  import importlib.util
  spec = importlib.util.spec_from_file_location('module.name', 'secret.py')
  secret = importlib.util.module_from_spec(spec)
  spec.loader.exec_module(secret)

  nest = Nest()
  nest.login(secret.ISSUE_TOKEN, secret.COOKIE)
  devices = nest.list_devices()
  print(devices)

  nest.update()
  print(devices)

  nest.update()
  print(devices)
