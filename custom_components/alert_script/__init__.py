"""Support for repeating alerts when conditions are met."""
from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant.const import (
    CONF_ENTITY_ID,
    CONF_NAME,
    CONF_REPEAT,
    CONF_STATE,
    CONF_UNIQUE_ID,
    SERVICE_TOGGLE,
    SERVICE_TURN_OFF,
    SERVICE_TURN_ON,
    STATE_ON,
)
from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity_component import EntityComponent
from homeassistant.helpers.typing import ConfigType

from .const import (
    CONF_ALERT_MESSAGE,
    CONF_CAN_ACK,
    CONF_DATA,
    CONF_DONE_MESSAGE,
    CONF_NOTIFIERS,
    CONF_SCRIPT,
    CONF_SKIP_FIRST,
    CONF_TITLE,
    CONF_VARIABLES,
    DEFAULT_CAN_ACK,
    DEFAULT_SKIP_FIRST,
    DOMAIN,
    LOGGER,
)

from .entity import AlertScriptEntity
ALERT_SCRIPT_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_NAME): cv.string,
        vol.Required(CONF_ENTITY_ID): cv.entity_id,
        vol.Optional(CONF_STATE, default=STATE_ON): cv.string,
        vol.Required(CONF_REPEAT): vol.All(
            cv.ensure_list,
            [vol.Coerce(float)],
            # Minimum delay is 1 second = 0.016 minutes
            [vol.Range(min=0.016)],
        ),
        vol.Optional(CONF_CAN_ACK, default=DEFAULT_CAN_ACK): cv.boolean,
        vol.Optional(CONF_SKIP_FIRST, default=DEFAULT_SKIP_FIRST): cv.boolean,
        vol.Optional(CONF_ALERT_MESSAGE): cv.template,
        vol.Optional(CONF_DONE_MESSAGE): cv.template,
        vol.Optional(CONF_TITLE): cv.template,
        vol.Optional(CONF_DATA): vol.Any(
                cv.template, vol.All(dict, cv.template_complex)
            ),
        vol.Optional(CONF_NOTIFIERS, default=list): vol.All(
            cv.ensure_list, [cv.string]
        ),
        vol.Optional(CONF_VARIABLES): vol.Any(
                cv.template, vol.All(dict, cv.template_complex)
            ),
        vol.Optional(CONF_SCRIPT): cv.string,
        vol.Optional(CONF_UNIQUE_ID): cv.string,
    }
)

CONFIG_SCHEMA = vol.Schema(
    {DOMAIN: cv.schema_with_slug_keys(ALERT_SCRIPT_SCHEMA)}, extra=vol.ALLOW_EXTRA
)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Alert component."""
    component = EntityComponent[AlertScriptEntity](LOGGER, DOMAIN, hass)

    entities: list[AlertScriptEntity] = []

    for object_id, cfg in config[DOMAIN].items():
        if not cfg:
            cfg = {}

        name = cfg[CONF_NAME]
        watched_entity_id = cfg[CONF_ENTITY_ID]
        alert_state = cfg[CONF_STATE]
        repeat = cfg[CONF_REPEAT]
        skip_first = cfg[CONF_SKIP_FIRST]
        message_template = cfg.get(CONF_ALERT_MESSAGE)
        done_message_template = cfg.get(CONF_DONE_MESSAGE)
        notifiers = cfg[CONF_NOTIFIERS]
        can_ack = cfg[CONF_CAN_ACK]
        title_template = cfg.get(CONF_TITLE)
        data: dict[str, Any] | None = cfg.get(CONF_DATA)
        variables: dict[str, Any] | None = cfg.get(CONF_VARIABLES)
        script: str | None | None = cfg.get(CONF_SCRIPT)
        unique_id: str | None = cfg.get(CONF_UNIQUE_ID)

        entities.append(
            AlertScriptEntity(
                hass,
                object_id,
                name,
                watched_entity_id,
                alert_state,
                repeat,
                skip_first,
                message_template,
                done_message_template,
                notifiers,
                can_ack,
                title_template,
                data,
                variables,
                script,
                unique_id
            )
        )

    if not entities:
        return False

    component.async_register_entity_service(SERVICE_TURN_OFF, None, "async_turn_off")
    component.async_register_entity_service(SERVICE_TURN_ON, None, "async_turn_on")
    component.async_register_entity_service(SERVICE_TOGGLE, None, "async_toggle")

    await component.async_add_entities(entities)

    return True