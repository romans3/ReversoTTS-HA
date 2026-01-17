"""Constants for Reverso TTS integration."""

CONF_PITCH = "pitch"        # reinterpretato come "speed"
CONF_BITRATE = "bitrate"    # non usato dall'API moderna
CONF_LANG = "language"

DEFAULT_LANG = "it-IT"
DEFAULT_PITCH = "1.0"
DEFAULT_BITRATE = "128k"

# Opzioni supportate dal servizio TTS
SUPPORT_OPTIONS = ["voice_id", "speed"]

# Lingue supportate (per compatibilità Home Assistant)
SUPPORT_LANGUAGES = [
    "it-IT", "en-US", "en-GB", "fr-FR", "es-ES", "de-DE"
]

# Mappa lingua → voce di default
LANGUAGE_DEFAULT_VOICE = {
    "it-IT": "Vittorio22k_NT",
    "en-US": "Ryan22k_NT",
    "en-GB": "Graham22k_NT",
    "fr-FR": "Bruno22k_NT",
    "es-ES": "Antonio22k_NT",
    "de-DE": "Klaus22k_NT",
}
