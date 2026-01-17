from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback

from .const import (
    CONF_LANG,
    CONF_PITCH,
    CONF_BITRATE,
    DEFAULT_LANG,
    DEFAULT_PITCH,
    DEFAULT_BITRATE,
)
from .voices import VOICES


class ReversoTTSConfigFlow(config_entries.ConfigFlow, domain="reversotts"):
    """Config flow for Reverso TTS."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="Reverso TTS", data=user_input)

        schema = vol.Schema(
            {
                vol.Required(CONF_LANG, default=DEFAULT_LANG): str,
                vol.Required(CONF_PITCH, default=DEFAULT_PITCH): str,
                vol.Required(CONF_BITRATE, default=DEFAULT_BITRATE): str,
            }
        )

        return self.async_show_form(step_id="user", data_schema=schema)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return ReversoTTSOptionsFlow(config_entry)


class ReversoTTSOptionsFlow(config_entries.OptionsFlow):
    """Options flow for selecting voice."""

    def __init__(self, config_entry):
        # Non assegnare a self.config_entry, che è una property read-only
        self._config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="Opzioni Reverso TTS", data=user_input)

        # Flatten all voices into a single list
        all_voices = []
        for lang_group in VOICES.values():
            all_voices.extend(lang_group)

        # Usa l’attributo interno
        default_voice = self._config_entry.options.get("voice_id", "Vittorio22k_NT")

        schema = vol.Schema(
            {
                vol.Optional(
                    "voice_id",
                    default=default_voice,
                ): vol.In(sorted(all_voices)),
            }
        )

        return self.async_show_form(step_id="init", data_schema=schema)
