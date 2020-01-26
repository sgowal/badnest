from datetime import datetime
from enum import Enum
import threading

if __package__:
  from .nest_device import Device
  from .nest_device import StreamingDevice
  from .nest_pb2 import (
      TargetTemperatureSettingsTrait,
      EcoModeStateTrait,
      SetPointScheduleSettingsTrait,
  )
else:
  from nest_device import Device
  from nest_device import StreamingDevice
  from nest_pb2 import (
      TargetTemperatureSettingsTrait,
      EcoModeStateTrait,
      SetPointScheduleSettingsTrait,
  )


class HVACAction(Enum):
  UNKNOWN = 0
  HEAT = 1
  COOL = 2
  IDLE = 3


class HVACMode(Enum):
  UNKNOWN = 0
  AUTO = 1
  HEAT = 2
  COOL = 3
  OFF = 4


class FanMode(Enum):
  UNKNOWN = 0
  AUTO = 1
  ON = 2


class PresetMode(Enum):
  UNKNOWN = 0
  ECO = 1
  NONE = 2


class TemperatureUnit(Enum):
  UNKNOWN = 0
  C = 1
  F = 2


class Thermostat(Device):

  def __init__(self, serial_number, name, backhand, api_url=None):
    super(Thermostat, self).__init__(serial_number, name, backhand)
    self._api_url = api_url

    # Properties.
    self._properties_lock = threading.Lock()
    self._temperature_unit = TemperatureUnit.UNKNOWN

    self._current_temperature = None
    self._current_humidity = None

    self._target_temperature = None
    self._target_temperature_high = None
    self._target_temperature_low = None

    self._fan_mode = FanMode.UNKNOWN
    self._available_fan_modes = []
    self._hvac_action = HVACAction.UNKNOWN
    self._hvac_mode = HVACMode.UNKNOWN
    self._available_hvac_modes = []
    self._preset_mode = PresetMode.UNKNOWN
    self._available_preset_modes = []

  def update_from_json(self, json):
    with self._properties_lock:
      self._temperature_unit = TemperatureUnit.C if json['temperature_scale'] == 'C' else TemperatureUnit.F
      self._current_temperature = json['current_temperature']
      self._current_humidity = json['current_humidity']

      self._target_temperature = json['target_temperature']
      self._target_temperature_high = json['target_temperature_high']
      self._target_temperature_low = json['target_temperature_low']

      if json['has_fan']:
        if json['fan_timer_timeout'] == 0:
          self._fan_mode = FanMode.AUTO
        else:
          self._fan_mode = FanMode.ON
        self._available_fan_modes = [FanMode.AUTO, FanMode.ON]
      else:
        self._available_fan_modes = []

      if json['hvac_ac_state']:
        self._hvac_action = HVACAction.COOL
      elif json['hvac_heater_state']:
        self._hvac_action = HVACAction.HEAT
      else:
        self._hvac_action = HVACAction.IDLE

      self._available_hvac_modes = []
      if json['can_heat'] and json['can_cool']:
        self._available_hvac_modes.append(HVACMode.AUTO)
      if json['can_heat']:
        self._available_hvac_modes.append(HVACMode.HEAT)
      if json['can_cool']:
        self._available_hvac_modes.append(HVACMode.COOL)
      self._available_hvac_modes.append(HVACMode.OFF)

      if json['target_temperature_type'] == 'heat':
        self._hvac_mode = HVACMode.HEAT
      elif json['target_temperature_type'] == 'cool':
        self._hvac_mode = HVACMode.COOL
      elif json['target_temperature_type'] == 'range':
        self._hvac_mode = HVACMode.AUTO
      elif json['target_temperature_type'] == 'off':
        self._hvac_mode = HVACMode.OFF
      else:
        self.logging.error('Unknown HVAC mode: {}'.format(json['target_temperature_type']))
        self._hvac_mode = HVACMode.OFF

      if json['eco']['mode'] in ('manual-eco', 'auto-eco'):
        self._preset_mode = PresetMode.ECO
      else:
        self._preset_mode = PresetMode.NONE
      self._available_preset_modes = [PresetMode.ECO, PresetMode.NONE]

  def __repr__(self):
    return 'Thermostat [{}, current={:.1f}, target={:.1f}]'.format(
        self.name, self.current_temperature, self.target_temperature)

  @property
  def temperature_unit(self):
    with self._properties_lock:
      return self._temperature_unit

  @property
  def current_temperature(self):
    with self._properties_lock:
      return self._current_temperature

  @property
  def current_humidity(self):
    with self._properties_lock:
      return self._current_humidity

  @property
  def target_temperature(self):
    with self._properties_lock:
      return self._target_temperature

  @property
  def target_temperature_high(self):
    with self._properties_lock:
      return self._target_temperature_high

  @property
  def target_temperature_low(self):
    with self._properties_lock:
      return self._target_temperature_low

  @property
  def hvac_action(self):
    with self._properties_lock:
      return self._hvac_action

  @property
  def hvac_mode(self):
    with self._properties_lock:
      return self._hvac_mode

  @property
  def fan_mode(self):
    with self._properties_lock:
      return self._fan_mode

  @property
  def preset_mode(self):
    with self._properties_lock:
      return self._preset_mode

  @property
  def available_hvac_modes(self):
    with self._properties_lock:
      return self._available_hvac_modes

  @property
  def available_fan_modes(self):
    with self._properties_lock:
      return self._available_fan_modes

  @property
  def available_preset_modes(self):
    with self._properties_lock:
      return self._available_preset_modes

  def _set(self, value, prefix='shared'):
    url = '{}/v5/put'.format(self._api_url)
    headers = self.authorization_headers
    json = {
        'objects': [{
            'object_key': '{}.{}'.format(prefix, self.unique_id),
            'op': 'MERGE',
            'value': value,
        }]
    }
    response = self.fetch_post(url=url, json=json, headers=headers)
    return response is not None

  def set_temperature(self, low, high=None):
    return self._set(({'target_temperature': low} if high is None else
                      {'target_temperature_low': low, 'target_temperature_high': high}))

  def set_hvac_mode(self, mode):
    with self._properties_lock:
      if mode not in self.available_hvac_modes:
        self.logging.warn('Trying to set unavailable HVAC mode: {} (not in {})'.format(mode, str(self.available_hvac_modes)))
        return False
    nest_mode = {
        HVACMode.HEAT: 'heat',
        HVACMode.COOL: 'cool',
        HVACMode.AUTO: 'range',
        HVACMode.OFF: 'off',
    }[mode]
    return self._set({'target_temperature_type': nest_mode})

  def set_preset_mode(self, mode):
    with self._properties_lock:
      if mode not in self.available_preset_modes:
        self.logging.warn('Trying to set unavailable preset mode: {} (not in {})'.format(mode, str(self.available_preset_modes)))
        return False
    return self._set({'eco': {'mode': 'manual-eco' if mode == PresetMode.ECO else 'schedule'}}, prefix='device')

  def set_fan_mode(self, mode):
    with self._properties_lock:
      if mode not in self.available_fan_modes:
        self.logging.warn('Trying to set unavailable fan mode: {} (not in {})'.format(mode, str(self.available_fan_modes)))
        return False
    if mode == FanMode.ON:
      t = int(datetime.now().timestamp() + 60 * 30)  # 30 minutes.
    else:
      t = 0
    return self._set({'fan_timer_timeout': t}, prefix='device')


class ThermostatE(StreamingDevice):

  def __init__(self, serial_number, backend):
    super(ThermostatE, self).__init__(serial_number, backend)

    # Properties.
    self._properties_lock = threading.Lock()
    self._temperature_unit = TemperatureUnit.UNKNOWN

    self._current_temperature = None
    self._current_humidity = None

    self._target_temperature = None

    self._hvac_action = HVACAction.UNKNOWN
    self._hvac_mode = HVACMode.UNKNOWN
    self._preset_mode = PresetMode.UNKNOWN

    # Can always heat (but never cool).
    self._available_hvac_modes = [HVACMode.HEAT, HVACMode.OFF]

    # ECO mode is available.
    self._available_preset_modes = [PresetMode.ECO, PresetMode.NONE]

    # The Thermostat E in Europe doesn't control cooling or fans.
    self._target_temperature_high = 24.  # Nest defaults
    self._target_temperature_low = 20.  # Nest defaults
    self._fan_mode = FanMode.UNKNOWN
    self._available_fan_modes = []

  @property
  def ready(self):
    self.fixit()
    if not self.name:
      return False
    with self._properties_lock:
      return (self._current_temperature is not None and
              self._current_humidity is not None and
              self._hvac_action is not None and
              self._hvac_mode is not None and
              self._preset_mode is not None)

  def _update_action(self):
    if self._target_temperature is None or self._current_temperature is None:
      return
    # Allow a little offset.
    if self._target_temperature > self._current_temperature + .2 and self._hvac_mode == HVACMode.HEAT:
      self._hvac_action = HVACAction.HEAT
    else:
      self._hvac_action = HVACAction.IDLE

  def update_from_proto(self, label, proto):
    if super(ThermostatE, self).update_from_proto(label, proto):
      return
    with self._properties_lock:
      if label == 'current_temperature':
        self._temperature_unit = TemperatureUnit.C
        self._current_temperature = proto.temperature_value.temperature.value
        self._update_action()
      elif label == 'current_humidity':
        self._current_humidity = proto.humidity_value.humidity.value
      elif label == 'target_temperature_settings':
        self._target_temperature = proto.target_temperature.heating_target.value
        self._hvac_mode = HVACMode.HEAT if proto.enabled.value else HVACMode.OFF
        self._update_action()
      elif label == 'eco_mode_state':
        self._preset_mode = (PresetMode.ECO if proto.eco_mode in (EcoModeStateTrait.ECO_MODE_MANUAL_ECO, EcoModeStateTrait.ECO_MODE_AUTO_ECO)
                             else PresetMode.NONE)
      else:
        self.logging.info('Unprocessed ThermostatE update: {} {}'.format(label, proto))

  def __repr__(self):
    if self.ready:
      return 'ThermostatE [{}, current={:.1f}, target={:.1f}]'.format(
          self.name, self.current_temperature, self.target_temperature)
    return 'ThermostatE [{}]'.format(self.name or self.unique_id)

  @property
  def temperature_unit(self):
    with self._properties_lock:
      return self._temperature_unit

  @property
  def current_temperature(self):
    with self._properties_lock:
      return self._current_temperature

  @property
  def current_humidity(self):
    with self._properties_lock:
      return self._current_humidity

  @property
  def target_temperature(self):
    with self._properties_lock:
      return self._target_temperature

  @property
  def target_temperature_high(self):
    with self._properties_lock:
      return self._target_temperature_high

  @property
  def target_temperature_low(self):
    with self._properties_lock:
      return self._target_temperature_low

  @property
  def hvac_action(self):
    with self._properties_lock:
      return self._hvac_action

  @property
  def hvac_mode(self):
    with self._properties_lock:
      return self._hvac_mode

  @property
  def fan_mode(self):
    with self._properties_lock:
      return self._fan_mode

  @property
  def preset_mode(self):
    with self._properties_lock:
      return self._preset_mode

  @property
  def available_hvac_modes(self):
    with self._properties_lock:
      return self._available_hvac_modes

  @property
  def available_fan_modes(self):
    with self._properties_lock:
      return self._available_fan_modes

  @property
  def available_preset_modes(self):
    with self._properties_lock:
      return self._available_preset_modes

  def _set_temperature_and_mode(self, value, enabled):
    trait = TargetTemperatureSettingsTrait()
    trait.enabled.value = enabled
    trait.target_temperature.setpoint_type = SetPointScheduleSettingsTrait.SET_POINT_SCHEDULE_TYPE_HEAT
    trait.target_temperature.heating_target.value = value
    return self.set('target_temperature_settings', trait)

  def set_temperature(self, low, high=None):
    if high is not None:
      return False
    with self._properties_lock:
      enabled = self._hvac_mode == HVACMode.HEAT  # Keep current mode.
      if self._set_temperature_and_mode(low, enabled):
        self._target_temperature = low
        return True
    return False

  def set_hvac_mode(self, mode):
    with self._properties_lock:
      if mode not in self._available_hvac_modes:
        self.logging.warn('Trying to set unavailable HVAC mode: {} (not in {})'.format(mode, str(self.available_hvac_modes)))
        return False
      temperature = self._target_temperature  # Keep current temperature.
      if self._set_temperature_and_mode(temperature, enabled=(mode == HVACMode.HEAT)):
        self._hvac_mode = mode
        return True
    return False

  def set_preset_mode(self, mode):
    trait = EcoModeStateTrait()
    enabled = mode == PresetMode.ECO
    trait.eco_mode = EcoModeStateTrait.ECO_MODE_MANUAL_ECO if enabled else EcoModeStateTrait.ECO_MODE_INACTIVE
    trait.eco_mode = EcoModeStateTrait.ECO_MODE_CHANGE_REASON_STRUCTURE_MODE if enabled else EcoModeStateTrait.ECO_MODE_CHANGE_REASON_MANUAL
    with self._properties_lock:
      if self.set('eco_mode_state', trait):
        self._preset_mode = mode
    return False

  def set_fan_mode(self, mode):
    return False


class HeatLink(StreamingDevice):

  def __init__(self, serial_number, backend):
    super(HeatLink, self).__init__(serial_number, backend)

    # Properties.
    self._properties_lock = threading.Lock()
    self._temperature_unit = TemperatureUnit.UNKNOWN
    self._current_temperature = None

  @property
  def ready(self):
    self.fixit()
    if not self.name:
      return False
    with self._properties_lock:
      return self._current_temperature is not None

  def update_from_proto(self, label, proto):
    if super(HeatLink, self).update_from_proto(label, proto):
      return
    with self._properties_lock:
      if label == 'temperature':
        self._temperature_unit = TemperatureUnit.C
        self._current_temperature = proto.temperature_value.temperature.value
      else:
        self.logging.info('Unprocessed HeatLink update: {} {}'.format(label, proto))

  def __repr__(self):
    if self.ready:
      return 'HeatLink [{}, current={:.1f}]'.format(
          self.name, self.current_temperature)
    return 'HeatLink [{}]'.format(self.name or self.unique_id)

  @property
  def temperature_unit(self):
    with self._properties_lock:
      return self._temperature_unit

  @property
  def current_temperature(self):
    with self._properties_lock:
      return self._current_temperature
