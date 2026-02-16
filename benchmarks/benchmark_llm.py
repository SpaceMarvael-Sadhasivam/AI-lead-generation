from time import perf_counter
from statistics import mean
from llm.groq_client import GroqLLM

llm = GroqLLM()

TEST_PROMPTS = [
    "Yes, I am interested in the course",
    "What is the course fee?",
    "I am still a student",
    "Sounds expensive",
    "Can you explain the curriculum?"
]

latencies = []

for _ in range(20):
    start = perf_counter()

    for prompt in TEST_PROMPTS:
        response = llm(prompt)

    latencies.append(perf_counter() - start)

print("\nLLM Benchmark Results (Groq)")
print("Mean:", mean(latencies))
print("Min:", min(latencies))
print("Max:", max(latencies))
print("Last Response:", response)
