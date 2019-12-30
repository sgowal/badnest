from datetime import datetime
import threading

if __package__:
  from .nest_device import Device
else:
  from nest_device import Device

_TIME_BETWEEN_IMAGES = 10  # in seconds.


class Camera(Device):

  def __init__(self, serial_number, name, backhand, property_url=None, image_url=None):
    super(Camera, self).__init__(serial_number, name, backhand)
    self._image_url = image_url
    self._property_url = property_url

    # Properties.
    self._is_online = None
    self._is_streaming = None

    self._image_lock = threading.Lock()
    self._last_image_capture = 0
    self._last_image = None

  def update_from_json(self, json):
    self._is_online = json['is_online']
    self._is_streaming = json['is_streaming']

  def __repr__(self):
    return 'Camera [{}, online={}, streaming={}]'.format(self.name, self.is_online, self.is_streaming)

  @property
  def is_online(self):
    return self._is_online

  @property
  def is_streaming(self):
    return self._is_streaming

  def _set(self, name, value):
    headers = self.camera_authorization_headers
    data = {'uuid': self.unique_id}
    data[name] = value
    response = self.fetch_post(url=self._property_url, data=data, headers=headers)
    return response is not None

  def turn_off(self):
    return self._set('streaming.enabled', 'false')

  def turn_on(self):
    return self._set('streaming.enabled', 'true')

  def get_image(self):
    with self._image_lock:
      now = datetime.now().timestamp()
      if now - self._last_image_capture < _TIME_BETWEEN_IMAGES and self._last_image is not None:
        return self._last_image
      img = self.fetch_get(url='{}/get_image?uuid={}&cachebuster={}'.format(self._image_url, self.unique_id, int(now)),
                           headers=self.camera_authorization_headers,
                           ignore_status_code=[404])  # 404 means that the camera is offline or not streaming.
      self._last_image = img
      self._last_image_capture = now
      return img
