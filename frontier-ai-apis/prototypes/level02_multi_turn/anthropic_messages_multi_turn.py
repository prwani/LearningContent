"""Level 2 — Anthropic Messages API: Multi-turn with prompt caching.

Client maintains full history. Uses cache_control on the system prompt
so repeated prefixes are cached server-side (~50% token savings).
Env: ANTHROPIC_API_KEY
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv; load_dotenv()
import anthropic
from _common.token_utils import print_anthropic_usage

client = anthropic.Anthropic()

system_prompt = [
    {
        "type": "text",
        "text": "You are a helpful assistant. Be concise.",
        "cache_control": {"type": "ephemeral"},
    }
]

messages = []

user_turns = [
    "What is the capital of France?",
    "What is its population?",
    "Name one famous landmark there.",
]

print("=== Anthropic Messages API — Multi-Turn with Prompt Caching ===\n")

for i, user_msg in enumerate(user_turns, 1):
    messages.append({"role": "user", "content": user_msg})

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=256,
        system=system_prompt,
        messages=messages,
    )

    assistant_text = response.content[0].text
    messages.append({"role": "assistant", "content": assistant_text})

    print(f"--- Turn {i} ---")
    print(f"User: {user_msg}")
    print(f"Assistant: {assistant_text}")
    print_anthropic_usage(response, label=f"Turn {i}")
    print()
