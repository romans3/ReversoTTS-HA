"""Support for the Reverso TTS speech service."""
import logging

from pyttsreverso import pyttsreverso
import voluptuous as vol

from homeassistant.components.tts import (
    CONF_LANG,
    PLATFORM_SCHEMA,
    Provider,
    TextToSpeechEntity,
    TtsAudioType,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType

from .const import (
    CONF_BITRATE,
    CONF_PITCH,
    DEFAULT_BITRATE,
    DEFAULT_LANG,
    DEFAULT_PITCH,
    SUPPORT_LANGUAGES,
    SUPPORT_OPTIONS,
)

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_LANG, default=DEFAULT_LANG): vol.In(SUPPORT_LANGUAGES),
        vol.Optional(CONF_PITCH, default=DEFAULT_PITCH): str,
        vol.Optional(CONF_BITRATE, default=DEFAULT_BITRATE): str,
    }
)


def get_engine(config: ConfigType, discovery_info=None):
    """Set up Reverso speech component."""
    return ReversoProvider(
        config[CONF_LANG],
        config[CONF_PITCH],
        config[CONF_BITRATE],
    )


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Reverso speech platform via config entry."""
    default_language = config_entry.data[CONF_LANG]
    default_pitch = config_entry.data[CONF_PITCH]
    default_bitrate = config_entry.data[CONF_BITRATE]
    async_add_entities(
        [ReversoTTSEntity(default_language, default_pitch, default_bitrate)]
    )


class ReversoTTSEntity(TextToSpeechEntity):
    """The Reverso TTS API provider."""

    def __init__(self, lang: str, pitch: int, bitrate: str):
        """Initialize Reverso TTS provider."""
        self._lang = lang
        self._pitch = pitch
        self._bitrate = bitrate
        self.name = "Reverso TTS"

    @property
    def default_language(self):
        """Return the default language."""
        return self._lang

    @property
    def supported_languages(self):
        """Return list of supported languages."""
        return SUPPORT_LANGUAGES

    def get_tts_audio(self, message, language, options=None):
        """Load TTS using pyttsreverso."""
        if language is None:
            language = self._lang
        try:
            convert = pyttsreverso.ReversoTTS()
            data = convert.convert_text(
                voice=language, pitch=self._pitch, bitrate=self._bitrate, msg=message
            )
        except Exception as e:
            _LOGGER.error("Error while to convert: %s", str(e))
            return (None, None)
        return ("mp3", data)


class ReversoProvider(Provider):
    """The Reverso TTS API provider."""

    def __init__(self, lang: str, pitch: int, bitrate) -> None:
        """Initialize Reverso TTS provider."""
        self._lang = lang
        self._pitch = pitch
        self._bitrate = bitrate
        self.name = "Reverso TTS"

    @property
    def default_language(self):
        """Return the default language."""
        return self._lang

    @property
    def supported_languages(self):
        """Return list of supported languages."""
        return SUPPORT_LANGUAGES

    @property
    def supported_options(self) -> list[str]:
        """Return a list of supported options."""
        return SUPPORT_OPTIONS

    def get_tts_audio(self, message, language, options=None) -> TtsAudioType:
        """Load TTS using pyttsreverso."""
        if language is None:
            language = self._lang
        try:
            convert = pyttsreverso.ReversoTTS()
            data = convert.convert_text(
                voice=language, pitch=self._pitch, bitrate=self._bitrate, msg=message
            )
        except Exception as e:
            _LOGGER.error("Error while to convert: %s", str(e))
            return (None, None)
        return ("mp3", data)
