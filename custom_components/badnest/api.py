from .nest import Nest


class NestAPI(object):

  def __init__(self, issue_token, cookie):
    self._api = Nest()
    self._api.login(issue_token, cookie)
    self._devices = self._api.list_devices()

  @property
  def devices(self):
    return self._devices

  @property
  def logging(self):
    return self._api._logging

  def update(self):
    return self._api.update()
