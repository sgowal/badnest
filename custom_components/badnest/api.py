from .nest import API


class NestAPI(object):

  def __init__(self, issue_token, cookie):
    self._api = API(issue_token, cookie)

  def initial_login(self):
    # Try to logging a few times before giving up.
    for _ in range(5):
      if self._api.login():
        break
    else:
      return False
    self._devices = self._api.list_devices()
    self._api._logging.info('Devices: %s', str(self._devices))
    return True

  @property
  def devices(self):
    return self._devices

  @property
  def logging(self):
    return self._api._logging

  def update(self):
    return self._api.update()
