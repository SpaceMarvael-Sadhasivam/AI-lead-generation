import requests
import os
from dotenv import load_dotenv

load_dotenv()

print("ACTIVE KEY:", os.getenv("DEEPGRAM_API_KEY"))



class DeepgramSTT:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.url = "https://api.deepgram.com/v1/listen"

    def transcribe(self, audio_bytes: bytes) -> str:

        headers = {
            "Authorization": f"Token {self.api_key}",
            "Content-Type": "audio/wav"
        }

        params = {
            "model": "nova-2",
            "smart_format": "true",
            "language": "en"
        }

        response = requests.post(
            self.url,
            headers=headers,
            params=params,
            data=audio_bytes
        )

        response.raise_for_status()
        data = response.json()

        return data["results"]["channels"][0]["alternatives"][0]["transcript"]
