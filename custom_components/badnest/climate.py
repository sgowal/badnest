from homeassistant.components.climate import ClimateDevice
from homeassistant.components.climate.const import (
    ATTR_TARGET_TEMP_HIGH,
    ATTR_TARGET_TEMP_LOW,
    CURRENT_HVAC_COOL,
    CURRENT_HVAC_HEAT,
    CURRENT_HVAC_IDLE,
    FAN_AUTO,
    FAN_ON,
    HVAC_MODE_AUTO,
    HVAC_MODE_COOL,
    HVAC_MODE_HEAT,
    HVAC_MODE_OFF,
    PRESET_ECO,
    PRESET_NONE,
    SUPPORT_FAN_MODE,
    SUPPORT_PRESET_MODE,
    SUPPORT_TARGET_TEMPERATURE,
    SUPPORT_TARGET_TEMPERATURE_RANGE,
)
from homeassistant.const import (
    ATTR_TEMPERATURE,
    TEMP_CELSIUS,
    TEMP_FAHRENHEIT,
)

from .const import DOMAIN
from .nest import (
    Thermostat,
    ThermostatE,
    HVACAction,
    HVACMode,
    FanMode,
    PresetMode,
    TemperatureUnit,
)

_MODE_HASSIO = {
    HVACMode.UNKNOWN: HVAC_MODE_OFF,
    HVACMode.AUTO: HVAC_MODE_AUTO,
    HVACMode.HEAT: HVAC_MODE_HEAT,
    HVACMode.COOL: HVAC_MODE_COOL,
    HVACMode.OFF: HVAC_MODE_OFF,
}

_MODE_NEST = {
    HVAC_MODE_AUTO: HVACMode.AUTO,
    HVAC_MODE_HEAT: HVACMode.HEAT,
    HVAC_MODE_COOL: HVACMode.COOL,
    HVAC_MODE_OFF: HVACMode.OFF,
}

_ACTION_HASSIO = {
    HVACAction.UNKNOWN: CURRENT_HVAC_IDLE,
    HVACAction.IDLE: CURRENT_HVAC_IDLE,
    HVACAction.HEAT: CURRENT_HVAC_HEAT,
    HVACAction.COOL: CURRENT_HVAC_COOL,
}

_PRESET_HASSIO = {
    PresetMode.UNKNOWN: PRESET_NONE,
    PresetMode.ECO: PRESET_ECO,
    PresetMode.NONE: PRESET_NONE,
}

_PRESET_NEST = {
    PRESET_ECO: PresetMode.ECO,
    PRESET_NONE: PresetMode.NONE,
}

_FAN_HASSIO = {
    FanMode.UNKNOWN: FAN_AUTO,
    FanMode.AUTO: FAN_AUTO,
    FanMode.ON: FAN_ON,
}

_FAN_NEST = {
    FAN_AUTO: FanMode.AUTO,
    FAN_ON: FanMode.ON,
}


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
  api = hass.data[DOMAIN]['api']
  thermostats = []
  for device in api.devices:
    if isinstance(device, (Thermostat, ThermostatE)):
      api.logging.info('Adding Nest Thermostat: %s', str(device))
      thermostats.append(NestClimate(device))
  async_add_entities(thermostats)


class NestClimate(ClimateDevice):

  def __init__(self, device):
    self._device = device

  @property
  def unique_id(self):
    return self._device.unique_id + '_thermostat'

  @property
  def name(self):
    return self._device.name + ' Thermostat'

  def update(self):
    self._device.update()

  @property
  def supported_features(self):
    features = SUPPORT_TARGET_TEMPERATURE | SUPPORT_PRESET_MODE
    if self._device.available_fan_modes:
      features |= SUPPORT_FAN_MODE
    if HVACMode.AUTO in self._device.available_hvac_modes:
      features |= SUPPORT_TARGET_TEMPERATURE_RANGE
    return features

  @property
  def temperature_unit(self):
    return TEMP_CELSIUS if self._device.temperature_unit == TemperatureUnit.C else TEMP_FAHRENHEIT

  @property
  def current_temperature(self):
    return self._device.current_temperature

  @property
  def current_humidity(self):
    return self._device.current_humidity

  @property
  def target_temperature(self):
    if self._device.hvac_mode == HVACMode.AUTO or self._device.preset_mode == PresetMode.ECO:
      return None
    return self._device.target_temperature

  @property
  def target_temperature_high(self):
    if self._device.hvac_mode == HVACMode.AUTO and self._device.preset_mode != PresetMode.ECO:
      return self._device.target_temperature_high
    return None

  @property
  def target_temperature_low(self):
    if self._device.hvac_mode == HVACMode.AUTO and self._device.preset_mode != PresetMode.ECO:
      return self._device.target_temperature_high
    return None

  @property
  def hvac_action(self):
    return _ACTION_HASSIO[self._device.hvac_action]

  @property
  def hvac_mode(self):
    return _MODE_HASSIO[self._device.hvac_mode]

  @property
  def hvac_modes(self):
    return [_MODE_HASSIO[m] for m in self._device.available_hvac_modes]

  @property
  def preset_mode(self):
    return _PRESET_HASSIO[self._device.preset_mode]

  @property
  def preset_modes(self):
    return [_PRESET_HASSIO[m] for m in self._device.available_preset_modes]

  @property
  def fan_mode(self):
    if self._device.available_fan_modes:
      return _FAN_HASSIO[self._device.fan_mode]
    return None

  @property
  def fan_modes(self):
    if self._device.available_fan_modes:
      return [_FAN_HASSIO[m] for m in self._device.available_fan_modes]
    return None

  def set_temperature(self, **kwargs):
    if self._device.hvac_mode == HVACMode.AUTO:
      high = kwargs.get(ATTR_TARGET_TEMP_HIGH)
      low = kwargs.get(ATTR_TARGET_TEMP_LOW)
      if high is not None and low is not None:
        self._device.set_temperature(low, high)
    else:
      temp = kwargs.get(ATTR_TEMPERATURE)
      if temp is not None:
        self._device.set_temperature(temp)

  def set_hvac_mode(self, hvac_mode):
    self._device.set_hvac_mode(_MODE_NEST[hvac_mode])

  def set_fan_mode(self, fan_mode):
    self._device.set_fan_mode(_FAN_NEST[fan_mode])

  def set_preset_mode(self, preset_mode):
    self._device.set_preset_mode(_PRESET_NEST[preset_mode])
