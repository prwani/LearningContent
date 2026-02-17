"""Level 2 — Azure OpenAI Responses API: Stateful multi-turn.

Uses previous_response_id so the server remembers context.
No need to resend history — dramatically reduces per-turn token cost.
Env: AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_DEPLOYMENT
Auth: Uses DefaultAzureCredential (Entra ID) — no API key needed.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv; load_dotenv()
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from _common.token_utils import print_openai_usage

credential = DefaultAzureCredential()
token_provider = get_bearer_token_provider(credential, "https://cognitiveservices.azure.com/.default")

client = AzureOpenAI(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    azure_ad_token_provider=token_provider,
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
