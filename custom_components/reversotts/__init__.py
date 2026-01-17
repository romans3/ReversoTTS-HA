from __future__ import annotations

import logging
import hashlib
import os
import time

from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.event import async_call_later

from .voices import VOICES

DOMAIN = "reversotts"
_LOGGER = logging.getLogger(__name__)

CACHE_DIR = "reversotts_cache"

# Cache TTL (in giorni)
CACHE_TTL_DAYS = 30
CACHE_TTL_SECONDS = CACHE_TTL_DAYS * 86400


def _cleanup_cache_sync(hass: HomeAssistant):
    """Logica sincrona per la pulizia dei file (eseguita fuori dal loop principale)."""
    cache_path = hass.data[DOMAIN]["cache_path"]
    now = time.time()
    removed = 0

    if not os.path.exists(cache_path):
        return

    for filename in os.listdir(cache_path):
        if not filename.endswith(".mp3"):
            continue

        full_path = os.path.join(cache_path, filename)
        if os.path.isfile(full_path):
            try:
                age = now - os.path.getmtime(full_path)
                if age > CACHE_TTL_SECONDS:
                    os.remove(full_path)
                    removed += 1
            except Exception as e:
                _LOGGER.error("Errore durante la pulizia del file %s: %s", filename, e)

    if removed:
        _LOGGER.info("ReversoTTS cache cleanup: rimossi %s file vecchi", removed)

async def _async_schedule_cleanup(hass: HomeAssistant):
    """Funzione asincrona che avvia la pulizia e schedula la successiva."""
    # Verifica che l'integrazione sia ancora attiva
    if DOMAIN not in hass.data:
        return

    # Esegue la pulizia I/O in un thread separato
    await hass.async_add_executor_job(_cleanup_cache_sync, hass)
    
    # Schedula la prossima pulizia tra 24 ore
    # Passare direttamente la funzione invece di una lambda con async_create_task 
    # è più pulito per il tracker di HA
    async_call_later(hass, 86400, lambda _: hass.async_create_background_task(
        _async_schedule_cleanup(hass), "reversotts_cache_cleanup"
    ))

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up Reverso TTS services."""

    # Costruisce il percorso verso /config/www/reversotts_cache
    # hass.config.path("www") punta direttamente alla cartella www di HA
    cache_path = hass.config.path("www", CACHE_DIR)
    
    # Crea la cartella se non esiste
    if not os.path.exists(cache_path):
        _LOGGER.debug("Creazione cartella cache in: %s", cache_path)
        os.makedirs(cache_path, exist_ok=True)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN]["cache_path"] = cache_path

    #
    # SERVICE: reversotts.list_voices
    #
    async def list_voices(call: ServiceCall):
        flat = []
        for group, voices in VOICES.items():
            for v in voices:
                flat.append({"group": group, "voice_id": v})

        hass.bus.async_fire("reversotts_voices", {"voices": flat})

    hass.services.async_register(DOMAIN, "list_voices", list_voices)

    #
    # SERVICE: reversotts.clear_cache
    #
    async def clear_cache_service(call: ServiceCall):
        """Servizio per forzare la pulizia della cache manualmente."""
        _LOGGER.info("ReversoTTS: Avvio pulizia manuale della cache richiesta dall'utente")
        await _async_schedule_cleanup(hass)

    hass.services.async_register(DOMAIN, "clear_cache", clear_cache_service)

    #
    # SERVICE: reversotts.say
    #
    async def say_with_voice(call: ServiceCall):

        # -----------------------------
        # Normalizzazione del testo
        # -----------------------------
        message = (
            call.data["message"]
                .replace("“", "\"")
                .replace("”", "\"")
                .replace("‘", "'")
                .replace("’", "'")
        )

        # -----------------------------
        # Normalizzazione universale del media_player
        # -----------------------------
        media_player = (
            call.data.get("media_player")
            or call.data.get("entity_id")
            or call.data.get("media_player_entity_id")
            or (call.data.get("target") or {}).get("entity_id")
        )

        # Se è una lista (target multipli), prendi il primo
        if isinstance(media_player, list):
            media_player = media_player[0]

        if not media_player:
            raise ValueError("Nessun media_player specificato per reversotts.say")

        # -----------------------------
        # Normalizzazione voice_id (opzionale)
        # -----------------------------
        DEFAULT_VOICE_ID = "Vittorio22k_HQ"  # default interno

        voice_id = (
            call.data.get("voice_id")
            or hass.data[DOMAIN].get("voice_id")
            or DEFAULT_VOICE_ID
        )

        # gestisci eventuali valori strani da options
        if not voice_id or str(voice_id).lower() == "none":
            voice_id = DEFAULT_VOICE_ID

        # -----------------------------
        # Hash per caching
        # -----------------------------
        key = hashlib.sha1(f"{voice_id}|{message}".encode()).hexdigest()
        cache_file = os.path.join(cache_path, f"{key}.mp3")

        # -----------------------------
        # Cache disco
        # -----------------------------
        if os.path.exists(cache_file):
            _LOGGER.debug("ReversoTTS cache hit: %s", cache_file)
            await hass.services.async_call(
                "media_player",
                "play_media",
                {
                    "entity_id": media_player,
                    "media_content_id": f"/local/{CACHE_DIR}/{key}.mp3", # Rimane così
                    "media_content_type": "music",
                },
                blocking=True,
            )
            return

        # -----------------------------
        # Chiamata TTS engine
        # -----------------------------
        await hass.services.async_call(
            "tts",
            "speak",
            {
                "entity_id": "tts.reverso_tts",
                "message": message,
                "media_player_entity_id": media_player,
                "options": {
                    "voice_id": voice_id,
                    "speed": call.data.get("speed")
                }
            },
            blocking=True,
        )

    hass.services.async_register(
        DOMAIN,
        "say",
        say_with_voice,
        schema=None,
    )

    # Schedule first cleanup 1 minute after startup
    async_call_later(hass, 60, lambda _: hass.async_create_background_task(
        _async_schedule_cleanup(hass), "reversotts_initial_cleanup"
    ))

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    _LOGGER.debug("Setting up Reverso TTS config entry: %s", entry.entry_id)

    hass.data[DOMAIN]["voice_id"] = entry.options.get("voice_id")

    await hass.config_entries.async_forward_entry_setups(entry, ["tts"])
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload Reverso TTS config entry."""
    _LOGGER.debug("Unloading Reverso TTS config entry: %s", entry.entry_id)

    unload_ok = await hass.config_entries.async_unload_platforms(entry, ["tts"])

    return unload_ok
