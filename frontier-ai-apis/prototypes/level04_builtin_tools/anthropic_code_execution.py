"""Level 4 — Anthropic Messages API: Code Execution (built-in tool, 3+ turns).

Multi-turn code execution with iterative tasks.
Env: ANTHROPIC_API_KEY
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv; load_dotenv()
import anthropic
from _common.token_utils import print_anthropic_usage, check_env_keys

check_env_keys()
client = anthropic.Anthropic()

print("=== Anthropic Messages API — Code Execution (3+ turns) ===\n")

queries = [
    "Generate the first 20 Fibonacci numbers using Python.",
    "Now find which of those Fibonacci numbers are also prime.",
    "Calculate the golden ratio approximation using consecutive Fibonacci pairs.",
]

messages = []
for i, query in enumerate(queries, 1):
    messages.append({"role": "user", "content": query})

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        tools=[{"type": "code_execution_20250522"}],
        messages=messages,
    )

    print(f"--- Turn {i} ---")
    print(f"User: {query}")

    # Collect assistant content
    assistant_content = []
    for block in response.content:
        if block.type == "text":
            print(f"Assistant: {block.text[:200]}...")
        elif block.type == "code_execution_tool_use":
            print(f"  Code: {block.code[:100]}...")
        elif block.type == "code_execution_tool_result":
            print(f"  Output: {block.output[:100]}..." if block.output else "  (no output)")
        assistant_content.append(block)

    messages.append({"role": "assistant", "content": assistant_content})
    print_anthropic_usage(response, label=f"Turn {i}")
    print()
