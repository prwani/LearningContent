"""Level 6 — Anthropic: Full Agentic Loop with Forced Tool Call (Structured Output).

Demonstrates:
  1. Agentic loop: while stop_reason == "tool_use", execute tools, loop
  2. Structured output via forced tool_choice (tool as schema)
  3. Uses get_weather + get_stock_price
Env: ANTHROPIC_API_KEY
"""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv; load_dotenv()
import anthropic
from _common.token_utils import print_anthropic_usage

client = anthropic.Anthropic()

# --- Real tools ---
action_tools = [
    {
        "name": "get_weather",
        "description": "Get current weather for a location.",
        "input_schema": {
            "type": "object",
            "properties": {"location": {"type": "string"}},
            "required": ["location"],
        },
    },
    {
        "name": "get_stock_price",
        "description": "Get stock price by ticker symbol.",
        "input_schema": {
            "type": "object",
            "properties": {"symbol": {"type": "string"}},
            "required": ["symbol"],
        },
    },
]

# --- Schema tool for structured output ---
briefing_tool = {
    "name": "return_briefing",
    "description": "Return the final structured briefing.",
    "input_schema": {
        "type": "object",
        "properties": {
            "weather_summary": {"type": "string"},
            "stock_summary":   {"type": "string"},
            "recommendation":  {"type": "string"},
        },
        "required": ["weather_summary", "stock_summary", "recommendation"],
    },
}

all_tools = action_tools + [briefing_tool]

def run_tool(name: str, args: dict) -> str:
    if name == "get_weather":
        return json.dumps({"location": args["location"], "temp_c": 19, "condition": "foggy"})
    elif name == "get_stock_price":
        return json.dumps({"symbol": args["symbol"], "price": 178.50, "currency": "USD"})
    return json.dumps({"error": "unknown tool"})

print("=== Anthropic — Agentic Loop + Structured Output ===\n")

messages = [
    {"role": "user", "content": "Give me a morning briefing for San Francisco. Also check AAPL stock. When done, use return_briefing to structure your answer."},
]

step = 0
while True:
    step += 1
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system="You are a morning briefing agent. Gather data, then call return_briefing with structured results.",
        tools=all_tools,
        messages=messages,
    )
    print_anthropic_usage(response, label=f"Step {step}")

    tool_uses = [b for b in response.content if b.type == "tool_use"]

    if not tool_uses or response.stop_reason == "end_turn":
        text = [b for b in response.content if b.type == "text"]
        if text:
            print(f"\nAssistant: {text[0].text}")
        break

    # Check if the structured output tool was called
    for tu in tool_uses:
        if tu.name == "return_briefing":
            print(f"\nStructured output:\n{json.dumps(tu.input, indent=2)}")

    messages.append({"role": "assistant", "content": response.content})
    tool_results = []
    for tu in tool_uses:
        if tu.name == "return_briefing":
            tool_results.append({"type": "tool_result", "tool_use_id": tu.id, "content": "Briefing accepted."})
        else:
            args = tu.input
            print(f"  Tool: {tu.name}({args})")
            result = run_tool(tu.name, args)
            tool_results.append({"type": "tool_result", "tool_use_id": tu.id, "content": result})

    messages.append({"role": "user", "content": tool_results})

    # If briefing was returned, we're done
    if any(tu.name == "return_briefing" for tu in tool_uses):
        break

    if step > 5:
        print("Max steps reached.")
        break
