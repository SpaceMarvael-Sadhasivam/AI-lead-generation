from time import perf_counter
from statistics import mean
from stt.deepgram_stt import DeepgramSTT
import os

stt = DeepgramSTT(os.getenv("DEEPGRAM_API_KEY"))

with open("sample.wav", "rb") as f:
    AUDIO_BYTES = f.read()

latencies = []

for _ in range(20):
    start = perf_counter()

    transcript = stt.transcribe(AUDIO_BYTES)

    latencies.append(perf_counter() - start)

print("\nSTT Benchmark Results")
print("Mean:", mean(latencies))
print("Min:", min(latencies))
print("Max:", max(latencies))
print("Transcript:", transcript)
