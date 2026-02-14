"""Level 5 — Anthropic: Tool Search with Deferred Loading.

Demonstrates tool_search + defer_loading to handle 50+ tools efficiently.
Tools marked defer_loading:true are stripped from context until the model
calls the search tool and discovers them.
Env: ANTHROPIC_API_KEY
"""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv; load_dotenv()
import anthropic
from _common.token_utils import print_anthropic_usage

client = anthropic.Anthropic()

# --- Define many tools, all with defer_loading ---
deferred_tools = [
    {"name": "get_weather",     "description": "Get current weather for a city.",
     "input_schema": {"type": "object", "properties": {"location": {"type": "string"}}, "required": ["location"]},
     "defer_loading": True},
    {"name": "get_stock_price", "description": "Get current stock price by symbol.",
     "input_schema": {"type": "object", "properties": {"symbol": {"type": "string"}}, "required": ["symbol"]},
     "defer_loading": True},
    {"name": "send_email",      "description": "Send an email to a recipient.",
     "input_schema": {"type": "object", "properties": {"to": {"type": "string"}, "subject": {"type": "string"}, "body": {"type": "string"}}, "required": ["to", "subject", "body"]},
     "defer_loading": True},
    {"name": "book_restaurant", "description": "Book a table at a restaurant.",
     "input_schema": {"type": "object", "properties": {"name": {"type": "string"}, "date": {"type": "string"}, "party_size": {"type": "integer"}}, "required": ["name", "date", "party_size"]},
     "defer_loading": True},
    {"name": "translate_text",  "description": "Translate text to another language.",
     "input_schema": {"type": "object", "properties": {"text": {"type": "string"}, "target_language": {"type": "string"}}, "required": ["text", "target_language"]},
     "defer_loading": True},
]

# Tool search tool — Anthropic discovers deferred tools via this
tool_search = {"type": "tool_search_20250522"}

all_tools = [tool_search] + deferred_tools

def execute_tool(name: str, args: dict) -> str:
    return json.dumps({"tool": name, "result": f"Mock result for {name}", "args": args})

print("=== Anthropic — Tool Search with Deferred Loading ===\n")
print(f"Total tools defined: {len(deferred_tools)} (all deferred)")
print(f"Tools in initial context: only tool_search\n")

messages = [
    {"role": "user", "content": "What is the weather in Tokyo right now?"},
]

# Agentic loop
for step in range(1, 6):
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        tools=all_tools,
        messages=messages,
    )
    print_anthropic_usage(response, label=f"Step {step}")

    # Check for tool_use blocks
    tool_uses = [b for b in response.content if b.type == "tool_use"]
    text_blocks = [b for b in response.content if b.type == "text"]

    if not tool_uses:
        for tb in text_blocks:
            print(f"\nAssistant: {tb.text}")
        break

    messages.append({"role": "assistant", "content": response.content})
    tool_results = []
    for tu in tool_uses:
        print(f"  Tool call: {tu.name}({tu.input})")
        if tu.name == "tool_search":
            # The API handles tool search internally; we pass an empty result
            tool_results.append({"type": "tool_result", "tool_use_id": tu.id, "content": "Search complete."})
        else:
            result = execute_tool(tu.name, tu.input)
            print(f"  Result: {result}")
            tool_results.append({"type": "tool_result", "tool_use_id": tu.id, "content": result})

    messages.append({"role": "user", "content": tool_results})
