"""Constants for the Alert Script integration."""

import logging
from typing import Final

DOMAIN: Final = "alert_script"

LOGGER = logging.getLogger(__package__)

CONF_CAN_ACK = "can_acknowledge"
CONF_NOTIFIERS = "notifiers"
CONF_SKIP_FIRST = "skip_first"
CONF_ALERT_MESSAGE = "message"
CONF_DONE_MESSAGE = "done_message"
CONF_TITLE = "title"
CONF_DATA = "data"
CONF_DATA_TEMPLATE = "data_template"
CONF_VARIABLES = "variables"
CONF_SCRIPT = "script"

DEFAULT_CAN_ACK = True
DEFAULT_SKIP_FIRST = False
