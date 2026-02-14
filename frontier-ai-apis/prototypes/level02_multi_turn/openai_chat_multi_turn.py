"""Level 2 — OpenAI Chat Completions: Multi-turn (stateless).

Client maintains full conversation history and resends it every turn.
Env: OPENAI_API_KEY
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv; load_dotenv()
from openai import OpenAI
from _common.token_utils import print_openai_usage

client = OpenAI()

messages = [
    {"role": "system", "content": "You are a helpful assistant. Be concise."},
]

user_turns = [
    "What is the capital of France?",
    "What is its population?",
    "Name one famous landmark there.",
]

print("=== OpenAI Chat Completions — Multi-Turn (Stateless) ===\n")

for i, user_msg in enumerate(user_turns, 1):
    messages.append({"role": "user", "content": user_msg})
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
    )
    assistant_msg = response.choices[0].message.content
    messages.append({"role": "assistant", "content": assistant_msg})

    print(f"--- Turn {i} ---")
    print(f"User: {user_msg}")
    print(f"Assistant: {assistant_msg}")
    print_openai_usage(response, label=f"Turn {i}")
    print()
