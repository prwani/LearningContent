"""Level 4 — OpenAI Responses API: Code Interpreter (built-in tool, 3+ turns).

Multi-turn code interpreter: build on previous results iteratively.
Env: OPENAI_API_KEY
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv; load_dotenv()
from openai import OpenAI
from _common.token_utils import print_openai_usage, check_env_keys

check_env_keys()
client = OpenAI()

print("=== OpenAI Responses API — Code Interpreter (3+ turns) ===\n")

queries = [
    "Generate a list of the first 20 prime numbers using Python.",
    "Now calculate the sum and average of those primes.",
    "Create a simple ASCII bar chart showing the distribution of those primes by their last digit.",
]

previous_id = None
for i, query in enumerate(queries, 1):
    kwargs = {
        "model": "gpt-4o-mini",
        "tools": [{"type": "code_interpreter"}],
        "input": query,
        "store": True,
    }
    if previous_id:
        kwargs["previous_response_id"] = previous_id

    response = client.responses.create(**kwargs)
    previous_id = response.id

    print(f"--- Turn {i} ---")
    print(f"User: {query}")
    print(f"Assistant: {response.output_text[:300]}...")
    print_openai_usage(response, label=f"Turn {i}")
    print()
