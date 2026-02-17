"""Level 1 — Azure OpenAI Responses API: Single-turn call.

Demonstrates the newer stateful Responses API endpoint.
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

response = client.responses.create(
    model=os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini"),
    instructions="You are a helpful assistant.",
    input="Explain what an API is in two sentences.",
)

print("=== Azure OpenAI Responses API — Single Turn ===")
print(f"Response: {response.output_text}")
print_openai_usage(response)
