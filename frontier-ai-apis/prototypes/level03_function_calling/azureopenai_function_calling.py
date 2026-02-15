"""Level 3 — Azure OpenAI Chat Completions: Function Calling (3+ turns).

Demonstrates multi-turn tool use: the user asks about weather in 3 cities,
each requiring a separate tool call and result round-trip.
Env: AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY, AZURE_OPENAI_DEPLOYMENT
"""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv; load_dotenv()
from openai import AzureOpenAI
from _common.token_utils import print_openai_usage, check_env_keys

check_env_keys()
client = AzureOpenAI(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    api_version="2024-12-01-preview",
)

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

WEATHER_DATA = {
    "tokyo": {"condition": "sunny", "temp_c": 24, "humidity": 55},
    "london": {"condition": "cloudy", "temp_c": 14, "humidity": 78},
    "new york": {"condition": "rainy", "temp_c": 18, "humidity": 85},
}

def get_weather(location: str) -> str:
    data = WEATHER_DATA.get(location.lower(), {"condition": "unknown", "temp_c": 20, "humidity": 60})
    return json.dumps({"location": location, **data})

print("=== Azure OpenAI Chat Completions — Function Calling (3+ turns) ===\n")

messages = [
    {"role": "system", "content": "You are a helpful weather assistant. When asked about multiple cities, check each one separately."},
    {"role": "user", "content": "Compare the weather in Tokyo, London, and New York. Which city is warmest?"},
]

turn = 0
while turn < 6:
    turn += 1
    response = client.chat.completions.create(
        model=os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini"), messages=messages, tools=tools,
    )
    print_openai_usage(response, label=f"Turn {turn}")
    msg = response.choices[0].message

    if not msg.tool_calls:
        print(f"\nAssistant: {msg.content}")
        break

    messages.append(msg)
    for tc in msg.tool_calls:
        args = json.loads(tc.function.arguments)
        print(f"  Tool call: {tc.function.name}({args})")
        result = get_weather(**args)
        print(f"  Result: {result}")
        messages.append({"role": "tool", "tool_call_id": tc.id, "content": result})

print(f"\nTotal turns: {turn}")
