"""Level 10 — Unified API Demo: Same prompt to OpenAI, Azure OpenAI, and Anthropic.

Sends identical prompts to all providers and compares responses + token usage.
Env: OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY, AZURE_OPENAI_DEPLOYMENT, ANTHROPIC_API_KEY
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv; load_dotenv()
from openai import OpenAI, AzureOpenAI
import anthropic
from _common.token_utils import print_openai_usage, print_anthropic_usage, check_env_keys

check_env_keys()

openai_client = OpenAI()
anthropic_client = anthropic.Anthropic()

# Azure OpenAI client (optional — skipped if env vars not set)
azure_client = None
azure_deployment = os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini")
if os.environ.get("AZURE_OPENAI_ENDPOINT") and os.environ.get("AZURE_OPENAI_API_KEY"):
    azure_client = AzureOpenAI(
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
        api_version="2024-12-01-preview",
    )

PROMPT = "Explain the difference between REST and GraphQL APIs in 3 bullet points."
SYSTEM = "You are a helpful technical assistant. Be concise."

print("=" * 60)
print("  Unified API Demo — Same Prompt, All Providers")
print("=" * 60)

results = []

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
results.append(("OpenAI Chat Completions", oai_response.usage.prompt_tokens, oai_response.usage.completion_tokens, oai_response.usage.total_tokens))

# --- OpenAI Responses API ---
print("\n--- OpenAI Responses API ---")
oai_resp = openai_client.responses.create(
    model="gpt-4o-mini",
    instructions=SYSTEM,
    input=PROMPT,
)
print(f"Response:\n{oai_resp.output_text}")
print_openai_usage(oai_resp, label="Responses API")
results.append(("OpenAI Responses API", oai_resp.usage.prompt_tokens, oai_resp.usage.completion_tokens, oai_resp.usage.total_tokens))

# --- Azure OpenAI Chat Completions ---
if azure_client:
    print("\n--- Azure OpenAI Chat Completions ---")
    azure_response = azure_client.chat.completions.create(
        model=azure_deployment,
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": PROMPT},
        ],
    )
    print(f"Response:\n{azure_response.choices[0].message.content}")
    print_openai_usage(azure_response, label="Azure OpenAI")
    results.append(("Azure OpenAI Chat", azure_response.usage.prompt_tokens, azure_response.usage.completion_tokens, azure_response.usage.total_tokens))

    # --- Azure OpenAI Responses API ---
    print("\n--- Azure OpenAI Responses API ---")
    azure_resp = azure_client.responses.create(
        model=azure_deployment,
        instructions=SYSTEM,
        input=PROMPT,
    )
    print(f"Response:\n{azure_resp.output_text}")
    print_openai_usage(azure_resp, label="Azure Responses API")
    results.append(("Azure OpenAI Responses", azure_resp.usage.prompt_tokens, azure_resp.usage.completion_tokens, azure_resp.usage.total_tokens))
else:
    print("\n--- Azure OpenAI: SKIPPED (AZURE_OPENAI_ENDPOINT not set) ---")

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
results.append(("Anthropic Messages", ant_response.usage.input_tokens, ant_response.usage.output_tokens, ant_response.usage.input_tokens + ant_response.usage.output_tokens))

# --- Comparison summary ---
print("\n" + "=" * 60)
print("  Token Usage Comparison")
print("=" * 60)
print(f"  {'Provider':<28} {'Input':>8} {'Output':>8} {'Total':>8}")
print(f"  {'-'*28} {'-'*8} {'-'*8} {'-'*8}")
for name, inp, out, total in results:
    print(f"  {name:<28} {inp:>8} {out:>8} {total:>8}")
