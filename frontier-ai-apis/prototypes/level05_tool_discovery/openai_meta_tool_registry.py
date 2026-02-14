"""Level 5 — OpenAI Chat Completions: Meta-Tool Registry for 50+ tools (3+ turns).

Only 3 meta-tools sent to the model. The model discovers and invokes
tools on demand across multiple turns.
Env: OPENAI_API_KEY
"""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv; load_dotenv()
from openai import OpenAI
from _common.token_utils import print_openai_usage, check_env_keys

check_env_keys()
client = OpenAI()

TOOL_CATALOG = {
    "get_weather": {"desc": "Get weather for a city", "params": {"location": "string"}},
    "send_email": {"desc": "Send an email", "params": {"to": "string", "subject": "string", "body": "string"}},
    "get_user_info": {"desc": "Get user info by ID", "params": {"user_id": "string"}},
    "book_restaurant": {"desc": "Book a restaurant table", "params": {"name": "string", "date": "string", "time": "string", "party_size": "int"}},
    "get_stock_price": {"desc": "Get current stock price", "params": {"symbol": "string"}},
    "translate_text": {"desc": "Translate text to another language", "params": {"text": "string", "target_language": "string"}},
    "check_calendar": {"desc": "Check calendar for a date", "params": {"date": "string"}},
    "search_books": {"desc": "Search books by title or author", "params": {"query": "string"}},
    "get_news_headlines": {"desc": "Get latest news by category", "params": {"category": "string"}},
    "get_exchange_rate": {"desc": "Get currency exchange rate", "params": {"from_currency": "string", "to_currency": "string"}},
}

def execute_tool(name, args):
    return json.dumps({"tool": name, "args": args, "result": f"Mock result for {name}"})

meta_tools = [
    {"type": "function", "function": {"name": "list_tools", "description": "List all available tools.", "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {"name": "describe_tool", "description": "Get full schema for a tool.", "parameters": {"type": "object", "properties": {"tool_name": {"type": "string"}}, "required": ["tool_name"]}}},
    {"type": "function", "function": {"name": "run_tool", "description": "Execute a tool by name.", "parameters": {"type": "object", "properties": {"tool_name": {"type": "string"}, "arguments": {"type": "object"}}, "required": ["tool_name", "arguments"]}}},
]

def handle_meta_tool(name, args):
    if name == "list_tools":
        return json.dumps({k: v["desc"] for k, v in TOOL_CATALOG.items()})
    elif name == "describe_tool":
        return json.dumps(TOOL_CATALOG.get(args["tool_name"], {}))
    elif name == "run_tool":
        return execute_tool(args["tool_name"], args.get("arguments", {}))
    return json.dumps({"error": "unknown"})

print("=== OpenAI Chat Completions — Meta-Tool Registry (3+ turns) ===\n")

messages = [
    {"role": "system", "content": "Use list_tools, describe_tool, run_tool to discover and execute tools."},
]

user_queries = [
    "What tools are available? Then check the weather in Tokyo.",
    "Get the AAPL stock price too.",
    "Translate 'Good morning' to Spanish.",
]

for qi, user_msg in enumerate(user_queries, 1):
    print(f"--- Query {qi} ---")
    print(f"User: {user_msg}")
    messages.append({"role": "user", "content": user_msg})

    step = 0
    while step < 5:
        step += 1
        response = client.chat.completions.create(
            model="gpt-4o-mini", messages=messages, tools=meta_tools,
        )
        print_openai_usage(response, label=f"  Step {step}")
        msg = response.choices[0].message

        if not msg.tool_calls:
            print(f"  Assistant: {msg.content}")
            messages.append(msg)
            break

        messages.append(msg)
        for tc in msg.tool_calls:
            args = json.loads(tc.function.arguments)
            print(f"    Meta-tool: {tc.function.name}({args})")
            result = handle_meta_tool(tc.function.name, args)
            print(f"    Result: {result[:80]}...")
            messages.append({"role": "tool", "tool_call_id": tc.id, "content": result})
    print()
