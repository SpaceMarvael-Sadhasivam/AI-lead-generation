import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("DEEPGRAM_API_KEY")

headers = {
    "Authorization": f"Token {API_KEY}",
    "Content-Type": "audio/wav"
}

params = {
    "model": "nova-2"
}

response = requests.post(
    "https://api.deepgram.com/v1/listen",
    headers=headers,
    params=params,
    data=b"RIFF"   # minimal dummy payload
)

print("Status:", response.status_code)
print("Response:", response.text)
