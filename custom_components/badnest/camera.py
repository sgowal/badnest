from homeassistant.components.camera import (
    Camera,
    SUPPORT_ON_OFF,
)

from .const import DOMAIN
from .nest_camera import Camera as LocalCamera


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
  api = hass.data[DOMAIN]['api']
  cameras = []
  for device in api.devices:
    if isinstance(device, LocalCamera):
      api.logging.info('Adding Nest Camera: %s', str(device))
      cameras.append(NestCamera(device))
  async_add_entities(cameras)


class NestCamera(Camera):

  def __init__(self, device):
    self._device = device

  @property
  def device_info(self):
    return {
        'identifiers': {(DOMAIN, self._device.unique_id)},
        'name': self._device.name,
        'manufacturer': 'Nest Labs',
        'model': 'Camera',
    }

  @property
  def unique_id(self):
    return self._device.unique_id + '_camera'

  @property
  def name(self):
    return self._device.name + ' Camera'

  def update(self):
    self._device.update()

  @property
  def is_on(self):
    return self._device.is_online

  @property
  def is_recording(self):
    return self._device.is_streaming

  def turn_off(self):
    self._device.turn_off()

  def turn_on(self):
    self._device.turn_on()

  @property
  def supported_features(self):
    return SUPPORT_ON_OFF

  def camera_image(self):
    return self._device.get_image()
