"""Level 4 — OpenAI Responses API: Web Search (built-in tool, 3+ turns).

Uses web_search_preview built-in tool with follow-up questions
for a multi-turn research conversation.
Env: OPENAI_API_KEY
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv; load_dotenv()
from openai import OpenAI
from _common.token_utils import print_openai_usage, check_env_keys

check_env_keys()
client = OpenAI()

print("=== OpenAI Responses API — Web Search (3+ turns) ===\n")

queries = [
    "What are the latest breakthroughs in quantum computing this year?",
    "Which companies are leading in quantum computing research?",
    "What are the practical applications expected in the next 5 years?",
]

previous_id = None
for i, query in enumerate(queries, 1):
    kwargs = {
        "model": "gpt-4o-mini",
        "tools": [{"type": "web_search_preview"}],
        "input": query,
        "store": True,
    }
    if previous_id:
        kwargs["previous_response_id"] = previous_id

    response = client.responses.create(**kwargs)
    previous_id = response.id

    print(f"--- Turn {i} ---")
    print(f"User: {query}")
    print(f"Assistant: {response.output_text[:200]}...")
    print_openai_usage(response, label=f"Turn {i}")
    print()
