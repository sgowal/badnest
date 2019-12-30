import logging

from homeassistant.helpers.entity import Entity

from .const import DOMAIN
from .nest_camera import Camera
from .nest_smoke_alarm import SmokeAlarm
from .nest_thermostat import Thermostat


_SENSOR_TYPES = [
    'smoke_alarm_state',
    'heat_alarm_state',
    'co_alarm_state',
    'battery_health_state',
]

_SENSOR_TYPE_NAMES = {
    'smoke_alarm_state': 'Smoke',
    'heat_alarm_state': 'Heat',
    'co_alarm_state': 'CO',
    'battery_health_state': 'Battery',
}


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
  api = hass.data[DOMAIN]['api']
  protect_sensors = []
  for device in api.devices:
    if isinstance(device, SmokeAlarm):
      api.logging.info('Adding Nest Protect sensor: %s', str(device))
      for sensor_type in _SENSOR_TYPES:
        protect_sensors.append(NestProtectSensor(device, sensor_type))
  async_add_entities(protect_sensors)


class NestProtectSensor(Entity):

  def __init__(self, device, sensor_type):
    self._device = device
    self._sensor_type = sensor_type

  @property
  def unique_id(self):
    return self._device.unique_id + '_' + self._sensor_type

  @property
  def name(self):
    return self._device.name + ' ' + _SENSOR_TYPE_NAMES[self._sensor_type]

  @property
  def state(self):
    return getattr(self._device, self._sensor_type).name

  def update(self):
    self._device.update()

  def icon(self):
    return 'mdi:smoke-detector'
