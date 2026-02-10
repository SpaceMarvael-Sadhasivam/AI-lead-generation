import requests
from tts.tts_adapter import TTSAdapter


class DeepgramTTS(TTSAdapter):
    """
    Deepgram Cloud TTS implementation
    """

    def __init__(self, api_key: str, voice: str = "aura-asteria-en"):
        self.api_key = api_key
        self.voice = voice
        self.url = "https://api.deepgram.com/v1/speak"

    def synthesize(self, text: str) -> bytes:
        headers = {
            "Authorization": f"Token {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "text": text
        }

        params = {
            "model": self.voice,
            "encoding": "linear16",
            "sample_rate": 24000
        }

        response = requests.post(
            self.url,
            headers=headers,
            params=params,
            json=payload
        )

        response.raise_for_status()
        return response.content