"""Level 1 — OpenAI Responses API: Single-turn call.

Demonstrates the newer stateful Responses API endpoint.
Env: OPENAI_API_KEY
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv; load_dotenv()
from openai import OpenAI
from _common.token_utils import print_openai_usage

client = OpenAI()

response = client.responses.create(
    model="gpt-4o-mini",
    instructions="You are a helpful assistant.",
    input="Explain what an API is in two sentences.",
)

print("=== OpenAI Responses API — Single Turn ===")
print(f"Response: {response.output_text}")
print_openai_usage(response)
