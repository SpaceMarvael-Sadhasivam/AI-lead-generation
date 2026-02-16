import os
from time import perf_counter
from statistics import mean
from dotenv import load_dotenv
import matplotlib.pyplot as plt
from stt.deepgram_stt import DeepgramSTT
from tts.deepgram_tts import DeepgramTTS
from llm.groq_client import GroqLLM


load_dotenv()

stt = DeepgramSTT(os.getenv("DEEPGRAM_API_KEY"))
tts = DeepgramTTS(os.getenv("DEEPGRAM_API_KEY"))
llm = GroqLLM()

with open("sample.wav", "rb") as f:
    AUDIO_BYTES = f.read()

TEST_PROMPT = "Yes, I am interested in the course"


def percentile(data, p):
    data = sorted(data)
    k = int(len(data) * (p / 100))
    return data[min(k, len(data) - 1)]


stt_lat = []
llm_lat = []
tts_lat = []
pipe_lat = []

ITERATIONS = 10   # increase if needed

for _ in range(ITERATIONS):

    # ---------------- STT ----------------
    start = perf_counter()
    transcript = stt.transcribe(AUDIO_BYTES)
    stt_lat.append(perf_counter() - start)

    # ---------------- LLM ----------------
    start = perf_counter()
    response = llm(TEST_PROMPT)
    llm_lat.append(perf_counter() - start)

    # ---------------- TTS ----------------
    start = perf_counter()
    tts.synthesize(response)
    tts_lat.append(perf_counter() - start)

    # ---------------- PIPELINE ----------------
    start = perf_counter()
    transcript = stt.transcribe(AUDIO_BYTES)
    reply = llm(transcript)
    tts.synthesize(reply)
    pipe_lat.append(perf_counter() - start)


print("\n" + "=" * 60)
print("VOICE AGENT PERFORMANCE COURSE LEAD QUALIFICATION AGENT")
print("=" * 60)

print("\nSTT (Deepgram nova-2)")
print(f"  Mean: {mean(stt_lat):.3f} s")
print(f"  Min : {min(stt_lat):.3f} s")
print(f"  Max : {max(stt_lat):.3f} s")
print(f"  P50 : {percentile(stt_lat, 50):.3f} s")
print(f"  P95 : {percentile(stt_lat, 95):.3f} s")

print("\nLLM (Groq llama-3.1-8b-instant)")
print(f"  Mean: {mean(llm_lat):.3f} s")
print(f"  Min : {min(llm_lat):.3f} s")
print(f"  Max : {max(llm_lat):.3f} s")
print(f"  P50 : {percentile(llm_lat, 50):.3f} s")
print(f"  P95 : {percentile(llm_lat, 95):.3f} s")

print("\nTTS (Deepgram)")
print(f"  Mean: {mean(tts_lat):.3f} s")
print(f"  Min : {min(tts_lat):.3f} s")
print(f"  Max : {max(tts_lat):.3f} s")
print(f"  P50 : {percentile(tts_lat, 50):.3f} s")
print(f"  P95 : {percentile(tts_lat, 95):.3f} s")

print("\nEND-TO-END PIPELINE")
print(f"  Mean: {mean(pipe_lat):.3f} s")
print(f"  Min : {min(pipe_lat):.3f} s")
print(f"  Max : {max(pipe_lat):.3f} s")
print(f"  P50 : {percentile(pipe_lat, 50):.3f} s")
print(f"  P95 : {percentile(pipe_lat, 95):.3f} s")

print("\nGenerating latency graph...")

plt.figure()
plt.plot(stt_lat, label="STT")
plt.plot(llm_lat, label="LLM")
plt.plot(tts_lat, label="TTS")
plt.plot(pipe_lat, label="Pipeline")

plt.xlabel("Iteration")
plt.ylabel("Latency (seconds)")
plt.title("Voice Agent Latency Profile")
plt.legend()
plt.show()

print("=" * 60)
