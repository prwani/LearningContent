"""Level 5 — Anthropic Messages API: Tool Search with Deferred Loading (3+ turns).

Uses tool_search + defer_loading to handle many tools efficiently.
Deferred tools are stripped from context until discovered via search.
Multi-turn conversation with 3+ queries.
Env: ANTHROPIC_API_KEY
"""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv; load_dotenv()
import anthropic
from _common.token_utils import print_anthropic_usage, check_env_keys

check_env_keys()
client = anthropic.Anthropic()

deferred_tools = [
    {"name": "get_weather", "description": "Get current weather for a city.",
     "input_schema": {"type": "object", "properties": {"location": {"type": "string"}}, "required": ["location"]},
     "defer_loading": True},
    {"name": "get_stock_price", "description": "Get current stock price by symbol.",
     "input_schema": {"type": "object", "properties": {"symbol": {"type": "string"}}, "required": ["symbol"]},
     "defer_loading": True},
    {"name": "send_email", "description": "Send an email to a recipient.",
     "input_schema": {"type": "object", "properties": {"to": {"type": "string"}, "subject": {"type": "string"}, "body": {"type": "string"}}, "required": ["to", "subject", "body"]},
     "defer_loading": True},
    {"name": "translate_text", "description": "Translate text to another language.",
     "input_schema": {"type": "object", "properties": {"text": {"type": "string"}, "target_language": {"type": "string"}}, "required": ["text", "target_language"]},
     "defer_loading": True},
    {"name": "search_books", "description": "Search books by title or author.",
     "input_schema": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]},
     "defer_loading": True},
]

tool_search = {"type": "tool_search_20250522"}
all_tools = [tool_search] + deferred_tools

def execute_tool(name, args):
    return json.dumps({"tool": name, "result": f"Mock result for {name}", "args": args})

print("=== Anthropic — Tool Search with Deferred Loading (3+ turns) ===\n")
print(f"Total tools: {len(deferred_tools)} (all deferred) + tool_search\n")

user_queries = [
    "What's the weather in Tokyo?",
    "Get the stock price of MSFT.",
    "Translate 'Hello World' to Japanese.",
]

messages = []
for qi, user_msg in enumerate(user_queries, 1):
    print(f"--- Query {qi} ---")
    print(f"User: {user_msg}")
    messages.append({"role": "user", "content": user_msg})

    step = 0
    while step < 5:
        step += 1
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            tools=all_tools,
            messages=messages,
        )
        print_anthropic_usage(response, label=f"  Step {step}")

        tool_uses = [b for b in response.content if b.type == "tool_use"]
        text_blocks = [b for b in response.content if b.type == "text"]

        if not tool_uses:
            for tb in text_blocks:
                print(f"  Assistant: {tb.text}")
            messages.append({"role": "assistant", "content": response.content})
            break

        messages.append({"role": "assistant", "content": response.content})
        tool_results = []
        for tu in tool_uses:
            print(f"    Tool: {tu.name}({tu.input})")
            if tu.name == "tool_search":
                tool_results.append({"type": "tool_result", "tool_use_id": tu.id, "content": "Search complete."})
            else:
                result = execute_tool(tu.name, tu.input)
                print(f"    Result: {result[:80]}...")
                tool_results.append({"type": "tool_result", "tool_use_id": tu.id, "content": result})
        messages.append({"role": "user", "content": tool_results})
    print()
