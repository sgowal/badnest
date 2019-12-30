from enum import Enum

if __package__:
  from .nest_device import Device
else:
  from nest_device import Device


class SmokeAlarmState(Enum):
  UNKNOWN = 0
  OK = 1
  WARNING = 2
  EMERGENCY = 3


class COAlarmState(Enum):
  UNKNOWN = 0
  OK = 1
  WARNING = 2
  EMERGENCY = 3


class HeatAlarmState(Enum):
  UNKNOWN = 0
  OK = 1
  WARNING = 2
  EMERGENCY = 3


class BatteryState(Enum):
  UNKNOWN = 0
  OK = 1
  REPLACE = 2


class SmokeAlarm(Device):

  def __init__(self, serial_number, name, backhand):
    super(SmokeAlarm, self).__init__(serial_number, name, backhand)

    # Properties.
    self._smoke_alarm_state = SmokeAlarmState.UNKNOWN
    self._heat_alarm_state = HeatAlarmState.UNKNOWN
    self._co_alarm_state = COAlarmState.UNKNOWN
    self._battery_health_state = BatteryState.UNKNOWN

  def update_from_json(self, json):
    self._smoke_alarm_state = [SmokeAlarmState.OK, SmokeAlarmState.WARNING, SmokeAlarmState.EMERGENCY][json['smoke_status']]
    self._heat_alarm_state = [HeatAlarmState.OK, HeatAlarmState.WARNING, HeatAlarmState.EMERGENCY][json['heat_status']]
    self._co_alarm_state = [COAlarmState.OK, COAlarmState.WARNING, COAlarmState.EMERGENCY][json['co_status']]
    self._battery_health_state = BatteryState.OK if json['battery_health_state'] == 0 else BatteryState.REPLACE

  @property
  def smoke_alarm_state(self):
    return self._smoke_alarm_state

  @property
  def heat_alarm_state(self):
    return self._heat_alarm_state

  @property
  def co_alarm_state(self):
    return self._co_alarm_state

  @property
  def battery_health_state(self):
    return self._battery_health_state

  def __repr__(self):
    return 'SmokeAlarm [{}, smoke={}, heat={}, co={}, battery={}]'.format(
        self.name, self.smoke_alarm_state, self.heat_alarm_state, self.co_alarm_state, self.battery_health_state)
