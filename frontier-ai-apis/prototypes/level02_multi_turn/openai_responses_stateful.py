"""Level 2 — OpenAI Responses API: Stateful multi-turn.

Uses previous_response_id so the server remembers context.
No need to resend history — dramatically reduces per-turn token cost.
Env: OPENAI_API_KEY
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv; load_dotenv()
from openai import OpenAI
from _common.token_utils import print_openai_usage

client = OpenAI()

user_turns = [
    "What is the capital of France?",
    "What is its population?",
    "Name one famous landmark there.",
]

print("=== OpenAI Responses API — Stateful Multi-Turn ===\n")

previous_id = None
for i, user_msg in enumerate(user_turns, 1):
    kwargs = {
        "model": "gpt-4o-mini",
        "instructions": "You are a helpful assistant. Be concise.",
        "input": user_msg,
        "store": True,
    }
    if previous_id:
        kwargs["previous_response_id"] = previous_id

    response = client.responses.create(**kwargs)
    previous_id = response.id

    print(f"--- Turn {i} ---")
    print(f"User: {user_msg}")
    print(f"Assistant: {response.output_text}")
    print_openai_usage(response, label=f"Turn {i}")
    print()
