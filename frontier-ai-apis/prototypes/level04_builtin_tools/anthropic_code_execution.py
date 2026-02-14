"""Level 4 — Anthropic Messages API: Code Execution (built-in tool).

Uses the code_execution tool type for server-side Python sandbox.
Env: ANTHROPIC_API_KEY
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv; load_dotenv()
import anthropic
from _common.token_utils import print_anthropic_usage

client = anthropic.Anthropic()

print("=== Anthropic Messages API — Code Execution (Built-in Tool) ===\n")

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=4096,
    tools=[{"type": "code_execution_20250522"}],
    messages=[
        {"role": "user", "content": "Calculate the first 20 Fibonacci numbers and print them."},
    ],
)

# Extract text and code results from content blocks
for block in response.content:
    if block.type == "text":
        print(f"Response: {block.text}")
    elif block.type == "code_execution_tool_use":
        print(f"\n--- Code executed ---\n{block.code}")
    elif block.type == "code_execution_tool_result":
        print(f"\n--- Output ---\n{block.output}")

print_anthropic_usage(response)
