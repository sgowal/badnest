from datetime import datetime

from homeassistant.const import (
    DEVICE_CLASS_HUMIDITY,
    DEVICE_CLASS_TEMPERATURE,
    TEMP_CELSIUS,
    TEMP_FAHRENHEIT,
)

from homeassistant.helpers.entity import Entity

from .const import DOMAIN
from .nest import (
    Thermostat,
    ThermostatE,
    HeatLink,
    TemperatureUnit,
)

_SENSOR_TYPE_NAMES = {
    'current_temperature': 'Temperature',
    'current_humidity': 'Humidity',
}

_SENSOR_TYPES = {
    'current_temperature': DEVICE_CLASS_TEMPERATURE,
    'current_humidity': DEVICE_CLASS_HUMIDITY,
}


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
  api = hass.data[DOMAIN]['api']
  sensors = []
  for device in api.devices:
    if isinstance(device, (Thermostat, ThermostatE)):
      api.logging.info('Adding Nest Thermostat sensor: %s', str(device))
      for sensor_type in _SENSOR_TYPES:
        sensors.append(ThermostatSensor(device, sensor_type))
    elif isinstance(device, HeatLink):
      sensors.append(HeatLinkSensor(device))
  async_add_entities(sensors)


class ThermostatSensor(Entity):

  def __init__(self, device, sensor_type):
    self._device = device
    self._sensor_type = sensor_type

  @property
  def unique_id(self):
    return self._device.unique_id + '_' + self._sensor_type

  @property
  def name(self):
    return self._device.name + ' Thermostat ' + _SENSOR_TYPE_NAMES[self._sensor_type]

  def update(self):
    self._device.update()

  @property
  def state(self):
    return getattr(self._device, self._sensor_type)

  @property
  def unit_of_measurement(self):
    if self._sensor_type == 'current_humidity':
      return '%'
    elif self._sensor_type == 'current_temperature':
      return TEMP_CELSIUS if self._device.temperature_unit == TemperatureUnit.C else TEMP_FAHRENHEIT
    else:
      return None

  @property
  def device_class(self):
    return _SENSOR_TYPES[self._sensor_type]


class HeatLinkSensor(ThermostatSensor):

  def __init__(self, device):
    super(HeatLinkSensor, self).__init__(device, 'current_temperature')
    self._device = device

  @property
  def name(self):
    return self._device.name + ' HeatLink ' + _SENSOR_TYPE_NAMES[self._sensor_type]
