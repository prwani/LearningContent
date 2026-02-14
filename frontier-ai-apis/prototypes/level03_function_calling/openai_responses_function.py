"""Level 3 — OpenAI Responses API: Function Calling.

Same get_weather tool but using the Responses API.
Env: OPENAI_API_KEY
"""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv; load_dotenv()
from openai import OpenAI
from _common.token_utils import print_openai_usage

client = OpenAI()

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

def get_weather(location: str) -> str:
    return json.dumps({"location": location, "condition": "cloudy", "temp_c": 18})

print("=== OpenAI Responses API — Function Calling ===\n")

# Step 1: Model decides to call the tool
response = client.responses.create(
    model="gpt-4o-mini",
    instructions="You are a helpful assistant.",
    input="What's the weather in London?",
    tools=tools,
)
print_openai_usage(response, label="Step 1 (tool selection)")

# Find function_call output items
function_calls = [item for item in response.output if item.type == "function_call"]

if function_calls:
    fc = function_calls[0]
    args = json.loads(fc.arguments)
    print(f"Tool call: {fc.name}({args})")

    result = get_weather(**args)
    print(f"Tool result: {result}")

    # Step 2: Send result back via previous_response_id
    response2 = client.responses.create(
        model="gpt-4o-mini",
        previous_response_id=response.id,
        input=[{
            "type": "function_call_output",
            "call_id": fc.call_id,
            "output": result,
        }],
    )
    print(f"\nAssistant: {response2.output_text}")
    print_openai_usage(response2, label="Step 2 (final answer)")
