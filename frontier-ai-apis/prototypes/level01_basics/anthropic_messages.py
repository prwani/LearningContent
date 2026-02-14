"""Level 1 — Anthropic Messages API: Single-turn call.

Demonstrates the stateless Messages endpoint with system + user messages.
Note: max_tokens is REQUIRED for Anthropic.
Env: ANTHROPIC_API_KEY
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv; load_dotenv()
import anthropic
from _common.token_utils import print_anthropic_usage

client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=256,
    system="You are a helpful assistant.",
    messages=[
        {"role": "user", "content": "Explain what an API is in two sentences."},
    ],
)

print("=== Anthropic Messages API — Single Turn ===")
print(f"Response: {response.content[0].text}")
print_anthropic_usage(response)
