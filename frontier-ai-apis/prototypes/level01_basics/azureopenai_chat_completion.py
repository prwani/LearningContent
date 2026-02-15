"""Level 1 — Azure OpenAI Chat Completions API: Single-turn call.

Demonstrates the stateless Chat Completions endpoint with system + user messages.
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

response = client.chat.completions.create(
    model=os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini"),
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user",   "content": "Explain what an API is in two sentences."},
    ],
)

print("=== Azure OpenAI Chat Completions — Single Turn ===")
print(f"Response: {response.choices[0].message.content}")
print_openai_usage(response)
