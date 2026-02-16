from time import perf_counter
from statistics import mean

from agent.agent import CourseLeadAgent
from agent.policy_engine import PolicyEngine
from agent.router import Router
from memory.memory import ConversationMemory
from tts.deepgram_tts import DeepgramTTS
import os

memory = ConversationMemory()
memory.start_session("pipeline_benchmark")   # REQUIRED

agent = CourseLeadAgent(memory, PolicyEngine(), Router())
tts = DeepgramTTS(os.getenv("DEEPGRAM_API_KEY"))

latencies = []

for _ in range(20):
    start = perf_counter()

    reply = agent.handle_input("Yes, I’m interested")
    tts.synthesize(reply)

    latencies.append(perf_counter() - start)

print("\nPipeline Benchmark Results")
print("Mean:", mean(latencies))
print("Min:", min(latencies))
print("Max:", max(latencies))
