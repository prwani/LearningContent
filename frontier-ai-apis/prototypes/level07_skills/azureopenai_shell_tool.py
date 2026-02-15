"""Level 7 — Azure OpenAI Responses API: Shell Tool.

Demonstrates the built-in shell tool that provides a full
Debian 12 Linux container for code execution.
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

print("=== Azure OpenAI Responses API — Shell Tool ===\n")

response = client.responses.create(
    model=os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini"),
    tools=[{
        "type": "container",
        "container": {
            "image": "python:3.11-slim",
            "environment": {},
        },
    }],
    input="Write a Python script that prints system info (OS, Python version, CPU count) and run it.",
)

print(f"Response: {response.output_text}")

# Show any container/shell executions
for item in response.output:
    item_type = getattr(item, "type", "")
    if "container" in item_type or "shell" in item_type:
        print(f"\n--- Shell execution ---")
        print(f"Type: {item_type}")
        if hasattr(item, "output"):
            print(f"Output: {item.output}")

print_openai_usage(response)
