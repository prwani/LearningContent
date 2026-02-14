"""Level 3 — OpenAI Responses API: Function Calling (3+ turns).

Uses the Responses API with previous_response_id chaining for multi-turn tool use.
Env: OPENAI_API_KEY
"""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv; load_dotenv()
from openai import OpenAI
from _common.token_utils import print_openai_usage, check_env_keys

check_env_keys()
client = OpenAI()

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a location.",
            "parameters": {
                "type": "object",
                "properties": {"location": {"type": "string", "description": "City name"}},
                "required": ["location"],
            },
        },
    }
]

WEATHER_DATA = {
    "tokyo": {"condition": "sunny", "temp_c": 24},
    "london": {"condition": "cloudy", "temp_c": 14},
    "sydney": {"condition": "warm", "temp_c": 28},
}

def get_weather(location: str) -> str:
    data = WEATHER_DATA.get(location.lower(), {"condition": "unknown", "temp_c": 20})
    return json.dumps({"location": location, **data})

print("=== OpenAI Responses API — Function Calling (3+ turns) ===\n")

previous_id = None
turn = 0

# Initial request
response = client.responses.create(
    model="gpt-4o-mini",
    instructions="You are a helpful weather assistant. Check each city separately.",
    input="What's the weather in Tokyo, London, and Sydney? Summarize which is best for outdoor activities.",
    tools=tools,
    store=True,
)
turn += 1
print_openai_usage(response, label=f"Turn {turn}")

while turn < 6:
    function_calls = [item for item in response.output if item.type == "function_call"]

    if not function_calls:
        print(f"\nAssistant: {response.output_text}")
        break

    # Process all function calls and send results
    tool_outputs = []
    for fc in function_calls:
        args = json.loads(fc.arguments)
        print(f"  Tool call: {fc.name}({args})")
        result = get_weather(**args)
        print(f"  Result: {result}")
        tool_outputs.append({
            "type": "function_call_output",
            "call_id": fc.call_id,
            "output": result,
        })

    response = client.responses.create(
        model="gpt-4o-mini",
        previous_response_id=response.id,
        input=tool_outputs,
        tools=tools,
        store=True,
    )
    turn += 1
    print_openai_usage(response, label=f"Turn {turn}")

print(f"\nTotal turns: {turn}")
