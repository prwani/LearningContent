"""Level 8 — Anthropic: Full Agentic Stack (Skills + Tools + MCP).

Combines:
  1. Loaded SKILL in system prompt
  2. Custom tools + MCP tools from toolscout server1 (if running on localhost:8000)
  3. Agentic loop until end_turn
  4. Structured output via forced tool_choice
Env: ANTHROPIC_API_KEY
"""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv; load_dotenv()
import anthropic
from _common.token_utils import print_anthropic_usage

client = anthropic.Anthropic()

SKILL = """## Skill: Daily Briefing Agent
1. Check weather for the user's city
2. Get latest news headlines
3. Compile into a structured briefing using return_briefing tool"""

# --- Tools (simulating MCP tools from toolscout server1) ---
tools = [
    {
        "name": "get_weather",
        "description": "Get current weather for a location (from MCP server1).",
        "input_schema": {
            "type": "object",
            "properties": {"location": {"type": "string"}},
            "required": ["location"],
        },
    },
    {
        "name": "get_news_headlines",
        "description": "Get latest news headlines by category (from MCP server1).",
        "input_schema": {
            "type": "object",
            "properties": {"category": {"type": "string"}},
            "required": ["category"],
        },
    },
    {
        "name": "return_briefing",
        "description": "Return the final structured daily briefing.",
        "input_schema": {
            "type": "object",
            "properties": {
                "city":      {"type": "string"},
                "weather":   {"type": "string"},
                "headlines": {"type": "array", "items": {"type": "string"}},
                "summary":   {"type": "string"},
            },
            "required": ["city", "weather", "headlines", "summary"],
        },
    },
]

def run_tool(name: str, args: dict) -> str:
    """Simulate MCP tool execution (same responses as toolscout server1)."""
    if name == "get_weather":
        return json.dumps({"location": args["location"], "condition": "clear", "temperature_c": 22, "wind_kph": 9})
    elif name == "get_news_headlines":
        return json.dumps({
            "category": args.get("category", "general"),
            "headlines": [
                {"title": "Markets hit record high", "source": "Finance Times"},
                {"title": "New tech breakthrough announced", "source": "Tech Daily"},
                {"title": "Weather alert issued for region", "source": "Local News"},
            ],
        })
    return json.dumps({"error": "unknown tool"})

print("=== Anthropic — Full Stack Agent (Skill + MCP Tools + Structured Output) ===\n")

messages = [
    {"role": "user", "content": "Give me a daily briefing for Mumbai. When done, call return_briefing."},
]

step = 0
while True:
    step += 1
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system=f"You are a daily briefing agent.\n\n{SKILL}",
        tools=tools,
        messages=messages,
    )
    print_anthropic_usage(response, label=f"Step {step}")

    tool_uses = [b for b in response.content if b.type == "tool_use"]

    if not tool_uses or response.stop_reason == "end_turn":
        text = [b for b in response.content if b.type == "text"]
        if text:
            print(f"\nAssistant: {text[0].text}")
        break

    # Check for structured output
    for tu in tool_uses:
        if tu.name == "return_briefing":
            print(f"\nStructured Briefing:\n{json.dumps(tu.input, indent=2)}")

    messages.append({"role": "assistant", "content": response.content})
    tool_results = []
    for tu in tool_uses:
        if tu.name == "return_briefing":
            tool_results.append({"type": "tool_result", "tool_use_id": tu.id, "content": "Briefing accepted."})
        else:
            print(f"  Tool: {tu.name}({tu.input})")
            result = run_tool(tu.name, tu.input)
            tool_results.append({"type": "tool_result", "tool_use_id": tu.id, "content": result})

    messages.append({"role": "user", "content": tool_results})

    if any(tu.name == "return_briefing" for tu in tool_uses):
        break

    if step > 5:
        print("Max steps reached.")
        break
