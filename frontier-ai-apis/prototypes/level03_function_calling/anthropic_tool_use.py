"""Level 3 — Anthropic Messages API: Tool Use.

Defines get_weather with input_schema (flat, no wrapper).
Anthropic returns tool_use blocks with parsed objects (no JSON string parsing).
Results go back as tool_result content blocks.
Env: ANTHROPIC_API_KEY
"""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv; load_dotenv()
import anthropic
from _common.token_utils import print_anthropic_usage

client = anthropic.Anthropic()

# --- Anthropic uses flat tool definitions with input_schema ---
tools = [
    {
        "name": "get_weather",
        "description": "Get current weather for a location.",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "City name"},
            },
            "required": ["location"],
        },
    }
]

def get_weather(location: str) -> str:
    return json.dumps({"location": location, "condition": "rainy", "temp_c": 15})

print("=== Anthropic Messages API — Tool Use ===\n")

messages = [
    {"role": "user", "content": "What's the weather in Paris?"},
]

# Step 1: Model decides to use a tool
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=256,
    tools=tools,
    messages=messages,
)
print_anthropic_usage(response, label="Step 1 (tool selection)")

# Find tool_use blocks (Anthropic returns parsed input, not JSON strings)
tool_uses = [b for b in response.content if b.type == "tool_use"]

if tool_uses:
    tu = tool_uses[0]
    print(f"Tool call: {tu.name}({tu.input})")  # Already a dict!

    result = get_weather(**tu.input)
    print(f"Tool result: {result}")

    # Step 2: Send tool_result back
    messages.append({"role": "assistant", "content": response.content})
    messages.append({
        "role": "user",
        "content": [
            {"type": "tool_result", "tool_use_id": tu.id, "content": result}
        ],
    })

    response2 = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=256,
        tools=tools,
        messages=messages,
    )
    print(f"\nAssistant: {response2.content[0].text}")
    print_anthropic_usage(response2, label="Step 2 (final answer)")
