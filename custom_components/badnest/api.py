from .nest import Nest


class NestAPI(object):

  def __init__(self):
    self._api = Nest()

  def initial_login(self, issue_token, cookie):
    # Try to logging a few times before giving up.
    for _ in range(5):
      if self._api.login(issue_token, cookie):
        break
    else:
      return False
    self._devices = self._api.list_devices()
    self._api._logging.warn('Devices: %s', str(self._devices))
    return True

  @property
  def devices(self):
    return self._devices

  @property
  def logging(self):
    return self._api._logging

  def update(self):
    return self._api.update()
