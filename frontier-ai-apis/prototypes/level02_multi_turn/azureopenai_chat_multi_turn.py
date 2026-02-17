"""Level 2 — Azure OpenAI Chat Completions: Multi-turn (stateless).

Client maintains full conversation history and resends it every turn.
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

messages = [
    {"role": "system", "content": "You are a helpful assistant. Be concise."},
]

user_turns = [
    "What is the capital of France?",
    "What is its population?",
    "Name one famous landmark there.",
]

print("=== Azure OpenAI Chat Completions — Multi-Turn (Stateless) ===\n")

for i, user_msg in enumerate(user_turns, 1):
    messages.append({"role": "user", "content": user_msg})
    response = client.chat.completions.create(
        model=os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini"),
        messages=messages,
    )
    assistant_msg = response.choices[0].message.content
    messages.append({"role": "assistant", "content": assistant_msg})

    print(f"--- Turn {i} ---")
    print(f"User: {user_msg}")
    print(f"Assistant: {assistant_msg}")
    print_openai_usage(response, label=f"Turn {i}")
    print()
