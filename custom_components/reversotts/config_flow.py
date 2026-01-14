"""Config flow for Reverso TTS integration."""
from __future__ import annotations

from typing import Any
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.components.tts import CONF_LANG
from homeassistant.data_entry_flow import FlowResult

from .const import (
    CONF_BITRATE,
    CONF_PITCH,
    DEFAULT_BITRATE,
    DEFAULT_LANG,
    DEFAULT_PITCH,
    DOMAIN,
    SUPPORT_LANGUAGES,
)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Optional(CONF_LANG, default=DEFAULT_LANG): vol.In(SUPPORT_LANGUAGES),
        vol.Optional(CONF_PITCH, default=DEFAULT_PITCH): str,
        vol.Optional(CONF_BITRATE, default=DEFAULT_BITRATE): vol.In(
            ["22k", "96k", "128k", "192k", "320k"]
        ),
    }
)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Reverso TTS."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is not None:
            self._async_abort_entries_match(
                {
                    CONF_LANG: user_input[CONF_LANG],
                    CONF_PITCH: user_input[CONF_PITCH],
                    CONF_BITRATE: user_input[CONF_BITRATE],
                }
            )
            return self.async_create_entry(title="Reverso TTS", data=user_input)

        return self.async_show_form(step_id="user", data_schema=STEP_USER_DATA_SCHEMA)

    async def async_step_onboarding(
        self, data: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle a flow initialized by onboarding."""
        return await self.async_step_user(
            {
                CONF_LANG: DEFAULT_LANG,
                CONF_PITCH: DEFAULT_PITCH,
                CONF_BITRATE: DEFAULT_BITRATE,
            }
        )
