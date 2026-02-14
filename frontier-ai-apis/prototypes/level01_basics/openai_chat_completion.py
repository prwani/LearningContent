"""Level 1 — OpenAI Chat Completions API: Single-turn call.

Demonstrates the stateless Chat Completions endpoint with system + user messages.
Env: OPENAI_API_KEY
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv; load_dotenv()
from openai import OpenAI
from _common.token_utils import print_openai_usage

client = OpenAI()  # reads OPENAI_API_KEY

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user",   "content": "Explain what an API is in two sentences."},
    ],
)

print("=== OpenAI Chat Completions — Single Turn ===")
print(f"Response: {response.choices[0].message.content}")
print_openai_usage(response)
