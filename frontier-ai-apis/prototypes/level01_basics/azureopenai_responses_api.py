"""Level 1 — Azure OpenAI Responses API: Single-turn call.

Demonstrates the newer stateful Responses API endpoint.
Env: AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY, AZURE_OPENAI_DEPLOYMENT
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv; load_dotenv()
from openai import AzureOpenAI
from _common.token_utils import print_openai_usage

client = AzureOpenAI(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
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
