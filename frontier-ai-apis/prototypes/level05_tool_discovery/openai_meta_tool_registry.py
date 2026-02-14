"""Level 5 — OpenAI: Meta-Tool Registry pattern for 50+ tools.

When you have many tools, sending all schemas every turn bloats context.
Instead, expose 3 meta-tools: list_tools, describe_tool, run_tool.
The model discovers and invokes tools on demand.
Env: OPENAI_API_KEY
"""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv; load_dotenv()
from openai import OpenAI
from _common.token_utils import print_openai_usage

client = OpenAI()

# --- Simulated large tool catalog (only names + short descriptions) ---
TOOL_CATALOG = {
    "get_weather":       {"desc": "Get weather for a city",               "params": {"location": "string"}},
    "send_email":        {"desc": "Send an email",                        "params": {"to": "string", "subject": "string", "body": "string"}},
    "get_user_info":     {"desc": "Get user info by ID",                  "params": {"user_id": "string"}},
    "book_restaurant":   {"desc": "Book a restaurant table",              "params": {"restaurant_name": "string", "date": "string", "time": "string", "party_size": "int"}},
    "get_stock_price":   {"desc": "Get current stock price",              "params": {"symbol": "string"}},
    "translate_text":    {"desc": "Translate text to another language",   "params": {"text": "string", "target_language": "string"}},
    "check_calendar":    {"desc": "Check calendar for a date",            "params": {"date": "string"}},
    "search_books":      {"desc": "Search books by title or author",      "params": {"query": "string"}},
    "get_news_headlines": {"desc": "Get latest news by category",         "params": {"category": "string"}},
    "get_exchange_rate": {"desc": "Get currency exchange rate",           "params": {"from_currency": "string", "to_currency": "string"}},
}

def execute_tool(name: str, args: dict) -> str:
    """Simulate executing any tool from the catalog."""
    return json.dumps({"tool": name, "args": args, "result": f"Mock result for {name}"})

# --- Only 3 meta-tools are sent to the model (tiny context!) ---
meta_tools = [
    {
        "type": "function",
        "function": {
            "name": "list_tools",
            "description": "List all available tools with short descriptions.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "describe_tool",
            "description": "Get full schema/parameters for a specific tool.",
            "parameters": {
                "type": "object",
                "properties": {"tool_name": {"type": "string"}},
                "required": ["tool_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "run_tool",
            "description": "Execute a tool by name with the given arguments.",
            "parameters": {
                "type": "object",
                "properties": {
                    "tool_name": {"type": "string"},
                    "arguments": {"type": "object"},
                },
                "required": ["tool_name", "arguments"],
            },
        },
    },
]

def handle_meta_tool(name: str, args: dict) -> str:
    if name == "list_tools":
        listing = {k: v["desc"] for k, v in TOOL_CATALOG.items()}
        return json.dumps(listing)
    elif name == "describe_tool":
        tool = TOOL_CATALOG.get(args["tool_name"], {})
        return json.dumps(tool)
    elif name == "run_tool":
        return execute_tool(args["tool_name"], args.get("arguments", {}))
    return json.dumps({"error": "unknown meta-tool"})

print("=== OpenAI — Meta-Tool Registry (10 tools, 3 meta-tools sent) ===\n")

messages = [
    {"role": "system", "content": "You have access to many tools via list_tools, describe_tool, and run_tool. Use them to help the user."},
    {"role": "user", "content": "What's the current price of AAPL stock?"},
]

# Agentic loop
for step in range(1, 6):
    response = client.chat.completions.create(
        model="gpt-4o-mini", messages=messages, tools=meta_tools,
    )
    print_openai_usage(response, label=f"Step {step}")
    msg = response.choices[0].message

    if not msg.tool_calls:
        print(f"\nAssistant: {msg.content}")
        break

    messages.append(msg)
    for tc in msg.tool_calls:
        args = json.loads(tc.function.arguments)
        print(f"  Meta-tool: {tc.function.name}({args})")
        result = handle_meta_tool(tc.function.name, args)
        print(f"  Result: {result}")
        messages.append({"role": "tool", "tool_call_id": tc.id, "content": result})
