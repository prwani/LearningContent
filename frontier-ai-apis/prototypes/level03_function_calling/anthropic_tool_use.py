"""Level 3 — Anthropic Messages API: Tool Use (3+ turns).

Multi-turn tool use: model calls get_weather for multiple cities,
each producing a tool_use/tool_result round-trip.
Env: ANTHROPIC_API_KEY
"""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv; load_dotenv()
import anthropic
from _common.token_utils import print_anthropic_usage, check_env_keys

check_env_keys()
client = anthropic.Anthropic()

tools = [
    {
        "name": "get_weather",
        "description": "Get current weather for a location.",
        "input_schema": {
            "type": "object",
            "properties": {"location": {"type": "string", "description": "City name"}},
            "required": ["location"],
        },
    }
]

WEATHER_DATA = {
    "paris": {"condition": "rainy", "temp_c": 15},
    "berlin": {"condition": "snowy", "temp_c": 2},
    "rome": {"condition": "sunny", "temp_c": 22},
}

def get_weather(location: str) -> str:
    data = WEATHER_DATA.get(location.lower(), {"condition": "unknown", "temp_c": 20})
    return json.dumps({"location": location, **data})

print("=== Anthropic Messages API — Tool Use (3+ turns) ===\n")

messages = [
    {"role": "user", "content": "Compare weather in Paris, Berlin, and Rome. Which is best for sightseeing?"},
]

turn = 0
while turn < 6:
    turn += 1
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        tools=tools,
        messages=messages,
    )
    print_anthropic_usage(response, label=f"Turn {turn}")

    tool_uses = [b for b in response.content if b.type == "tool_use"]

    if not tool_uses:
        text = [b for b in response.content if b.type == "text"]
        if text:
            print(f"\nAssistant: {text[0].text}")
        break

    messages.append({"role": "assistant", "content": response.content})
    tool_results = []
    for tu in tool_uses:
        print(f"  Tool call: {tu.name}({tu.input})")
        result = get_weather(**tu.input)
        print(f"  Result: {result}")
        tool_results.append({"type": "tool_result", "tool_use_id": tu.id, "content": result})
    messages.append({"role": "user", "content": tool_results})

print(f"\nTotal turns: {turn}")
