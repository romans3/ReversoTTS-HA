"""Support for the Reverso TTS speech service (API v1)."""
from __future__ import annotations

import logging
import hashlib
import os
from typing import Any, Dict, Optional

import voluptuous as vol
import requests

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
    LANGUAGE_DEFAULT_VOICE,
)
from . import DOMAIN

_LOGGER = logging.getLogger(__name__)

REVERSO_BASE_URL = "https://voice.reverso.net/api/v1/tts"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_LANG, default=DEFAULT_LANG): vol.In(SUPPORT_LANGUAGES),
        vol.Optional(CONF_PITCH, default=DEFAULT_PITCH): str,
        vol.Optional(CONF_BITRATE, default=DEFAULT_BITRATE): str,
    }
)


# ---------------------------------------------------------------------------
# Utility: resolve voice ID
# ---------------------------------------------------------------------------

def _resolve_voice_id(language: str | None, options: Dict[str, Any] | None, default_voice: str) -> str:
    """Determina il voice_id da usare."""
    if options and "voice_id" in options:
        return str(options["voice_id"])

    if language in LANGUAGE_DEFAULT_VOICE:
        return LANGUAGE_DEFAULT_VOICE[language]

    return default_voice


# ---------------------------------------------------------------------------
# Reverso API v1 client + CACHE
# ---------------------------------------------------------------------------

class ReversoTTSClient:
    """Client per Reverso TTS API v1 con caching RAM + disco."""

    def __init__(self, hass: HomeAssistant, speed: float = 1.0, audio_format: str = "mp3") -> None:
        self._speed = speed
        self._format = audio_format
        self._cache = {}  # RAM cache
        self._hass = hass
        self._cache_path = hass.data[DOMAIN]["cache_path"]

    def synthesize(self, text: str, voice_id: str) -> Optional[bytes]:
        # Calcolo chiave basato su voce, velocità e testo
        key = hashlib.sha1(f"{voice_id}|{self._speed}|{text}".encode()).hexdigest()
        cache_file = os.path.join(self._cache_path, f"{key}.mp3")

        # 1) CACHE DISCO
        if os.path.exists(cache_file):
            _LOGGER.debug("ReversoTTS disk cache hit: %s", cache_file)
            with open(cache_file, "rb") as f:
                return f.read()

        # 2) CACHE RAM
        if key in self._cache:
            _LOGGER.debug("ReversoTTS RAM cache hit: %s", key)
            return self._cache[key]

        # 3) API CALL
        url = f"{REVERSO_BASE_URL}/{voice_id}"

        # FIX 400: Velocità come numero (punto decimale)
        try:
            speed_val = float(str(self._speed).replace(",", "."))
            if speed_val < 0.5 or speed_val > 2.0:
                speed_val = 1.0
        except:
            speed_val = 1.0

        # FIX 400: Payload con campi obbligatori
        payload = {
            "text": text,
            "speed": speed_val,
            "voiceName": voice_id,
            "format": self._format
        }

        # 🔥 HEADERS ORIGINALI FUNZIONANTI
        headers = {
            "Content-Type": "application/json",
            "Accept": "*/*",
            "Origin": "https://voice.reverso.net",
            "Referer": "https://voice.reverso.net/text-to-speech",
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.6099.71 Safari/537.36"
            ),
            "apikey": "test-api-key-123456",
        }

        resp = None
        try:
            # Ripristiniamo la chiamata semplice che funzionava
            resp = requests.post(url, json=payload, headers=headers, timeout=15)
            
            # Controllo Cloudflare
            if "Just a moment..." in resp.text:
                _LOGGER.error("ReversoTTS: Bloccato da Cloudflare. Attendi 30 minuti prima di riprovare.")
                return None
                
            resp.raise_for_status()
        except Exception as err:
            _LOGGER.error("Reverso TTS Fallito per voce %s: %s", voice_id, err)
            if resp is not None:
                _LOGGER.error("Dettagli errore API: %s", resp.text[:300])
            return None

        if resp.status_code != 200:
            _LOGGER.error("Reverso TTS HTTP error: %s", resp.status_code)
            return None

        audio = resp.content

        # Salva in RAM
        self._cache[key] = audio

        # Salva su disco
        with open(cache_file, "wb") as f:
            f.write(audio)

        return audio


# ---------------------------------------------------------------------------
# YAML setup
# ---------------------------------------------------------------------------

def get_engine(config: ConfigType, discovery_info=None) -> Provider:
    lang = config[CONF_LANG]
    pitch_str = config[CONF_PITCH]

    try:
        speed = float(pitch_str)
    except Exception:
        speed = 1.0

    client = ReversoTTSClient(speed=speed)
    return ReversoProvider(lang, speed, client)


# ---------------------------------------------------------------------------
# Config Entry setup
# ---------------------------------------------------------------------------

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:

    lang = config_entry.data[CONF_LANG]
    pitch_str = config_entry.data[CONF_PITCH]

    try:
        speed = float(pitch_str)
    except Exception:
        speed = 1.0

    client = ReversoTTSClient(hass, speed=speed)

    async_add_entities([
        ReversoTTSEntity(lang, speed, client, config_entry)
    ])


# ---------------------------------------------------------------------------
# Entity
# ---------------------------------------------------------------------------

class ReversoTTSEntity(TextToSpeechEntity):

    _attr_name = "Reverso TTS"

    def __init__(self, lang: str, speed: float, client: ReversoTTSClient, config_entry: ConfigEntry):
        self._lang = lang
        self._speed = speed
        self._client = client
        self._config_entry = config_entry

        self._attr_unique_id = f"reversotts_{config_entry.entry_id}"

    @property
    def default_language(self):
        return self._lang

    @property
    def supported_languages(self):
        return SUPPORT_LANGUAGES

    @property
    def supported_options(self):
        return SUPPORT_OPTIONS

    def get_tts_audio(self, message, language, options=None) -> TtsAudioType:
        lang = language or self._lang

        voice_id = _resolve_voice_id(
            lang,
            options,
            self._config_entry.options.get("voice_id", "Vittorio22k_NT")
        )

        # -------------------------------------------------------------------
        # 🎚️ OVERRIDE DINAMICO SPEED
        # -------------------------------------------------------------------
        speed = self._speed

        if options and "speed" in options:
            raw_speed = options.get("speed")

            if raw_speed is None or raw_speed == "":
                # Nessuna velocità specificata → usa quella di default
                pass
            else:
                try:
                    speed = float(raw_speed)
                except Exception:
                    _LOGGER.warning("ReversoTTS: valore speed non valido (%s), uso %s", raw_speed, speed)

        # PATCH: aggiorna correttamente la velocità nel client
        self._client._speed = speed

        # Normalizza virgolette tipografiche
        message = (
            message.replace("“", "\"")
                   .replace("”", "\"")
                   .replace("‘", "'")
                   .replace("’", "'")
        )

        # -------------------------------------------------------------------
        # 🔊 GENERAZIONE AUDIO
        # -------------------------------------------------------------------
        audio = self._client.synthesize(message, voice_id)

        # -------------------------------------------------------------------
        # 🔄 FALLBACK AUTOMATICO
        # -------------------------------------------------------------------
        if not audio:
            fallback_voice = "Chiara22k_NT"
            _LOGGER.warning("ReversoTTS: fallback attivato → %s", fallback_voice)
            audio = self._client.synthesize(message, fallback_voice)

        if not audio:
            return (None, None)

        return ("mp3", audio)


# ---------------------------------------------------------------------------
# Provider legacy (YAML)
# ---------------------------------------------------------------------------

class ReversoProvider(Provider):

    def __init__(self, lang: str, speed: float, client: ReversoTTSClient):
        self._lang = lang
        self._speed = speed
        self._client = client
        self.name = "Reverso TTS"

    @property
    def default_language(self):
        return self._lang

    @property
    def supported_languages(self):
        return SUPPORT_LANGUAGES

    @property
    def supported_options(self):
        return SUPPORT_OPTIONS

    def get_tts_audio(self, message, language, options=None) -> TtsAudioType:
        lang = language or self._lang

        voice_id = _resolve_voice_id(
            lang,
            options,
            LANGUAGE_DEFAULT_VOICE.get(lang, "Vittorio22k_NT")
        )

        # Normalizza virgolette tipografiche
        message = (
            message.replace("“", "\"")
                   .replace("”", "\"")
                   .replace("‘", "'")
                   .replace("’", "'")
        )

        audio = self._client.synthesize(message, voice_id)

        if not audio:
            fallback_voice = "Chiara22k_NT"
            _LOGGER.warning("ReversoTTS (YAML): fallback attivato → %s", fallback_voice)
            audio = self._client.synthesize(message, fallback_voice)

        if not audio:
            return (None, None)

        return ("mp3", audio)
