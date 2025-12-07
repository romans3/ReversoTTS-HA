import aiohttp
from homeassistant.components.tts import TextToSpeechEntity

DOMAIN = "reversotts"

async def call_reverso_api(message: str, language: str):
    url = f"https://voice.reverso.net/RestPronunciation.svc/v1/output=json/GetVoiceStream/{language}/{message}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.read()

class ReversoTTSEntity(TextToSpeechEntity):
    def __init__(self, hass, language="it"):
        self._language = language

    @property
    def supported_languages(self):
        return ["it", "en", "fr", "de", "es"]

    async def async_get_tts_audio(self, message, language, options=None):
        audio = await call_reverso_api(message, language or self._language)
        return "mp3", audio
