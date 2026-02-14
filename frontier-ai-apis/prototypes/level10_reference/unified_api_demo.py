"""Level 10 — Unified API Demo: Same prompt to OpenAI and Anthropic side-by-side.

Sends identical prompts to both providers and compares responses + token usage.
Env: OPENAI_API_KEY, ANTHROPIC_API_KEY
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv; load_dotenv()
from openai import OpenAI
import anthropic
from _common.token_utils import print_openai_usage, print_anthropic_usage

openai_client = OpenAI()
anthropic_client = anthropic.Anthropic()

PROMPT = "Explain the difference between REST and GraphQL APIs in 3 bullet points."
SYSTEM = "You are a helpful technical assistant. Be concise."

print("=" * 60)
print("  Unified API Demo — Same Prompt, Both Providers")
print("=" * 60)

# --- OpenAI Chat Completions ---
print("\n--- OpenAI Chat Completions ---")
oai_response = openai_client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": PROMPT},
    ],
)
print(f"Response:\n{oai_response.choices[0].message.content}")
print_openai_usage(oai_response, label="OpenAI")

# --- OpenAI Responses API ---
print("\n--- OpenAI Responses API ---")
oai_resp = openai_client.responses.create(
    model="gpt-4o-mini",
    instructions=SYSTEM,
    input=PROMPT,
)
print(f"Response:\n{oai_resp.output_text}")
print_openai_usage(oai_resp, label="Responses API")

# --- Anthropic Messages API ---
print("\n--- Anthropic Messages API ---")
ant_response = anthropic_client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=512,
    system=SYSTEM,
    messages=[
        {"role": "user", "content": PROMPT},
    ],
)
print(f"Response:\n{ant_response.content[0].text}")
print_anthropic_usage(ant_response, label="Anthropic")

# --- Comparison summary ---
print("\n" + "=" * 60)
print("  Token Usage Comparison")
print("=" * 60)
print(f"  {'Provider':<25} {'Input':>8} {'Output':>8} {'Total':>8}")
print(f"  {'-'*25} {'-'*8} {'-'*8} {'-'*8}")
print(f"  {'OpenAI Chat Completions':<25} {oai_response.usage.prompt_tokens:>8} {oai_response.usage.completion_tokens:>8} {oai_response.usage.total_tokens:>8}")
print(f"  {'OpenAI Responses API':<25} {oai_resp.usage.prompt_tokens:>8} {oai_resp.usage.completion_tokens:>8} {oai_resp.usage.total_tokens:>8}")
print(f"  {'Anthropic Messages':<25} {ant_response.usage.input_tokens:>8} {ant_response.usage.output_tokens:>8} {ant_response.usage.input_tokens + ant_response.usage.output_tokens:>8}")
