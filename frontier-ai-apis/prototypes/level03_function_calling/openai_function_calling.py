"""Level 3 — OpenAI Chat Completions: Function Calling.

Defines a get_weather tool, handles tool_calls in the response,
executes the function locally, and sends results back.
Env: OPENAI_API_KEY
"""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv; load_dotenv()
from openai import OpenAI
from _common.token_utils import print_openai_usage

client = OpenAI()

# --- Tool definition (OpenAI wraps in type: "function") ---
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a location.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "City name"},
                },
                "required": ["location"],
            },
        },
    }
]

# --- Local function implementation ---
def get_weather(location: str) -> str:
    return json.dumps({"location": location, "condition": "sunny", "temp_c": 24})

print("=== OpenAI Chat Completions — Function Calling ===\n")

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user",   "content": "What's the weather in Tokyo?"},
]

# Step 1: Initial call — model decides to call a tool
response = client.chat.completions.create(
    model="gpt-4o-mini", messages=messages, tools=tools,
)
print_openai_usage(response, label="Step 1 (tool selection)")
msg = response.choices[0].message

if msg.tool_calls:
    tc = msg.tool_calls[0]
    args = json.loads(tc.function.arguments)  # OpenAI returns JSON string
    print(f"Tool call: {tc.function.name}({args})")

    result = get_weather(**args)
    print(f"Tool result: {result}")

    # Step 2: Send tool result back
    messages.append(msg)
    messages.append({"role": "tool", "tool_call_id": tc.id, "content": result})

    response2 = client.chat.completions.create(
        model="gpt-4o-mini", messages=messages, tools=tools,
    )
    print(f"\nAssistant: {response2.choices[0].message.content}")
    print_openai_usage(response2, label="Step 2 (final answer)")
