"""Level 4 — OpenAI Responses API: Code Interpreter (built-in tool).

The model writes and executes Python code in a sandbox.
Env: OPENAI_API_KEY
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv; load_dotenv()
from openai import OpenAI
from _common.token_utils import print_openai_usage

client = OpenAI()

print("=== OpenAI Responses API — Code Interpreter (Built-in Tool) ===\n")

response = client.responses.create(
    model="gpt-4o-mini",
    tools=[{"type": "code_interpreter"}],
    input="Calculate the first 20 Fibonacci numbers and show them in a table.",
)

print(f"Response: {response.output_text}")

# Show any code that was executed
for item in response.output:
    if hasattr(item, "type") and item.type == "code_interpreter_call":
        print(f"\n--- Code executed ---")
        print(item.input if hasattr(item, "input") else "(code not available)")

print_openai_usage(response)
