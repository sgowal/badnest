"""BadNest integration."""

import voluptuous
from homeassistant.helpers import config_validation

from .api import NestAPI
from .const import DOMAIN, CONF_ISSUE_TOKEN, CONF_COOKIE

CONFIG_SCHEMA = voluptuous.Schema({
    DOMAIN: voluptuous.All({
        voluptuous.Required(CONF_ISSUE_TOKEN, default=""): config_validation.string,
        voluptuous.Required(CONF_COOKIE, default=""): config_validation.string,
    })}, extra=voluptuous.ALLOW_EXTRA)


def setup(hass, config):
  """Set up the BadNest component."""
  if config.get(DOMAIN) is not None:
    issue_token = config[DOMAIN].get(CONF_ISSUE_TOKEN)
    cookie = config[DOMAIN].get(CONF_COOKIE)
    api = NestAPI(issue_token, cookie)
    if not api.initial_login():
      return False
    hass.data[DOMAIN] = {
        'api': api,
    }
    return True
  return False
