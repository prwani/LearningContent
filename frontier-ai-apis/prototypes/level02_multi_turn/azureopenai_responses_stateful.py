"""Level 2 — Azure OpenAI Responses API: Stateful multi-turn.

Uses previous_response_id so the server remembers context.
No need to resend history — dramatically reduces per-turn token cost.
Env: AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY, AZURE_OPENAI_DEPLOYMENT
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv; load_dotenv()
from openai import AzureOpenAI
from _common.token_utils import print_openai_usage

client = AzureOpenAI(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    api_version="2024-12-01-preview",
)

user_turns = [
    "What is the capital of France?",
    "What is its population?",
    "Name one famous landmark there.",
]

print("=== Azure OpenAI Responses API — Stateful Multi-Turn ===\n")

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
