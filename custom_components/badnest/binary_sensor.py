from homeassistant.components.binary_sensor import (
    BinarySensorDevice,
    DEVICE_CLASS_BATTERY,
    DEVICE_CLASS_CONNECTIVITY,
    DEVICE_CLASS_GAS,
    DEVICE_CLASS_HEAT,
    DEVICE_CLASS_SMOKE,
)

from .const import DOMAIN
from .nest_smoke_alarm import (
    SmokeAlarm,
    COAlarmState,
    HeatAlarmState,
    SmokeAlarmState,
    BatteryState,
)


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

_SENSOR_TYPES = {
    'smoke_alarm_state': DEVICE_CLASS_SMOKE,
    'heat_alarm_state': DEVICE_CLASS_HEAT,
    'co_alarm_state': DEVICE_CLASS_GAS,
    'battery_health_state': DEVICE_CLASS_BATTERY,
}


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
  api = hass.data[DOMAIN]['api']
  sensors = []
  for device in api.devices:
    if isinstance(device, SmokeAlarm):
      api.logging.info('Adding Nest Protect sensor: %s', str(device))
      for sensor_type in _SENSOR_TYPES:
        sensors.append(NestProtectSensor(device, sensor_type))
  sensors.append(NestUpdateSensor(api))
  async_add_entities(sensors)


class NestProtectSensor(BinarySensorDevice):

  def __init__(self, device, sensor_type):
    self._device = device
    self._sensor_type = sensor_type

  @property
  def unique_id(self):
    return self._device.unique_id + '_' + self._sensor_type

  @property
  def name(self):
    return self._device.name + ' Protect ' + _SENSOR_TYPE_NAMES[self._sensor_type]

  def update(self):
    self._device.update()

  @property
  def is_on(self):
    if self._sensor_type == 'smoke_alarm_state':
      return self._device.smoke_alarm_state in (SmokeAlarmState.WARNING, SmokeAlarmState.EMERGENCY)
    elif self._sensor_type == 'heat_alarm_state':
      return self._device.heat_alarm_state in (HeatAlarmState.WARNING, HeatAlarmState.EMERGENCY)
    elif self._sensor_type == 'co_alarm_state':
      return self._device.co_alarm_state in (COAlarmState.WARNING, COAlarmState.EMERGENCY)
    elif self._sensor_type == 'battery_health_state':
      return self._device.smoke_alarm_state == BatteryState.REPLACE
    else:
      return None

  @property
  def device_class(self):
    return _SENSOR_TYPES[self._sensor_type]


class NestUpdateSensor(BinarySensorDevice):

  def __init__(self, api):
    self._api = api
    self._value = True

  @property
  def unique_id(self):
    return DOMAIN + '_update_success'

  @property
  def name(self):
    return DOMAIN + ' Successful Update'

  def update(self):
    self._value = self._api.update()

  @property
  def is_on(self):
    return self._value

  @property
  def device_class(self):
    return DEVICE_CLASS_CONNECTIVITY
