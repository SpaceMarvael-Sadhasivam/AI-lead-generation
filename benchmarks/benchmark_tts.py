from time import perf_counter
from statistics import mean
from tts.deepgram_tts import DeepgramTTS
import os

tts = DeepgramTTS(os.getenv("DEEPGRAM_API_KEY"))

latencies = []

for _ in range(20):
    start = perf_counter()
    tts.synthesize("Latency test")
    latencies.append(perf_counter() - start)

print("\nTTS Benchmark Results")
print("Mean:", mean(latencies))
print("Min:", min(latencies))
print("Max:", max(latencies))
