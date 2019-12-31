from homeassistant.components.switch import SwitchDevice

from .const import DOMAIN
from .nest_camera import Camera


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
  api = hass.data[DOMAIN]['api']
  switches = []
  for device in api.devices:
    if isinstance(device, Camera):
      api.logging.info('Adding Nest Camera: %s', str(device))
      switches.append(NestCameraSwitch(device))
  async_add_entities(switches)


class NestCameraSwitch(SwitchDevice):

  def __init__(self, device):
    self._device = device

  @property
  def name(self):
    return self._device.name + ' Camera Switch'

  @property
  def is_on(self):
    return self._device.is_streaming

  def turn_on(self, **kwargs):
    self._device.turn_on()

  def turn_off(self, **kwargs):
    self._device.turn_off()

  @property
  def icon(self):
    if self.is_on:
      return 'mdi:camcorder'
    return 'mdi:camcorder-off'
