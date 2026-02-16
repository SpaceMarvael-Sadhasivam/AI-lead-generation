from time import perf_counter
from statistics import mean

from agent.agent import CourseLeadAgent
from agent.policy_engine import PolicyEngine
from agent.router import Router
from memory.memory import ConversationMemory

memory = ConversationMemory()
memory.start_session("benchmark_session")    # REQUIRED

agent = CourseLeadAgent(memory, PolicyEngine(), Router())

TEST_TRANSCRIPTS = [
    "Yes, I’m interested",
    "Can you explain pricing?",
    "Sounds expensive",
    "I’m a student",
]

latencies = []

for _ in range(50):
    start = perf_counter()

    for text in TEST_TRANSCRIPTS:
        agent.handle_input(text)

    latencies.append(perf_counter() - start)

print("\nAgent Benchmark Results")
print("Mean:", mean(latencies))
print("Min:", min(latencies))
print("Max:", max(latencies))
