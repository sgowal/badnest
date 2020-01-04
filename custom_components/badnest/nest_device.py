class Device(object):

  def __init__(self, serial_number, name, backend):
    self._serial_number = serial_number
    self._name = name
    self._backend = backend

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
