from datetime import datetime
from enum import Enum

if __package__:
  from .nest_device import Device
else:
  from nest_device import Device


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
    self._temperature_unit = json['temperature_scale']
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
    return 'Thermostat [{}, current={:.1f}, target={:1f}]'.format(
        self.name, self.current_temperature, self.target_temperature)

  @property
  def temperature_unit(self):
    return self._temperature_unit

  @property
  def current_temperature(self):
    return self._current_temperature

  @property
  def current_humidity(self):
    return self._current_humidity

  @property
  def target_temperature(self):
    return self._target_temperature

  @property
  def target_temperature_high(self):
    return self._target_temperature_high

  @property
  def target_temperature_low(self):
    return self._target_temperature_low

  @property
  def hvac_action(self):
    return self._hvac_action

  @property
  def hvac_mode(self):
    return self._hvac_mode

  @property
  def fan_mode(self):
    return self._fan_mode

  @property
  def preset_mode(self):
    return self._preset_mode

  @property
  def available_hvac_modes(self):
    return self._available_hvac_modes

  @property
  def available_fan_modes(self):
    return self._available_fan_modes

  @property
  def available_preset_modes(self):
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
    if mode not in self.available_preset_modes:
      self.logging.warn('Trying to set unavailable preset mode: {} (not in {})'.format(mode, str(self.available_preset_modes)))
      return False
    return self._set({'eco': {'mode': 'manual-eco' if mode == PresetMode.ECO else 'schedule'}}, prefix='device')

  def set_fan_mode(self, mode):
    if mode not in self.available_fan_modes:
      self.logging.warn('Trying to set unavailable fan mode: {} (not in {})'.format(mode, str(self.available_fan_modes)))
      return False
    if mode == FanMode.ON:
      t = int(datetime.now().timestamp() + 60 * 30)  # 30 minutes.
    else:
      t = 0
    return self._set({'fan_timer_timeout': t}, prefix='device')
