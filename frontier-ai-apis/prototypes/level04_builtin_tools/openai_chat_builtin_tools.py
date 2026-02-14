"""Level 4 — OpenAI Chat Completions: Built-in Tools via function calling (3+ turns).

Chat Completions doesn't have built-in tools natively, but you can simulate
the pattern by defining tools that wrap external services (web search, code exec).
This shows a 3-turn conversation with multiple tool calls.
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
            "name": "web_search",
            "description": "Search the web for current information.",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string", "description": "Search query"}},
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "run_python",
            "description": "Execute Python code and return the output.",
            "parameters": {
                "type": "object",
                "properties": {"code": {"type": "string", "description": "Python code to execute"}},
                "required": ["code"],
            },
        },
    },
]

def web_search(query: str) -> str:
    return json.dumps({"results": [
        {"title": f"Result 1 for: {query}", "snippet": "AI spending reached $200B globally in 2025."},
        {"title": f"Result 2 for: {query}", "snippet": "Top companies: Microsoft, Google, Amazon."},
    ]})

def run_python(code: str) -> str:
    return json.dumps({"output": "Calculation result: 42.5 billion USD growth year-over-year"})

tool_handlers = {"web_search": web_search, "run_python": run_python}

print("=== OpenAI Chat Completions — Built-in Tool Patterns (3+ turns) ===\n")

messages = [
    {"role": "system", "content": "You are a research assistant. Use web_search to find data and run_python to analyze it."},
    {"role": "user", "content": "Research the current AI market size, then calculate the year-over-year growth rate, and summarize your findings."},
]

turn = 0
while turn < 6:
    turn += 1
    response = client.chat.completions.create(
        model="gpt-4o-mini", messages=messages, tools=tools,
    )
    print_openai_usage(response, label=f"Turn {turn}")
    msg = response.choices[0].message

    if not msg.tool_calls:
        print(f"\nAssistant: {msg.content}")
        break

    messages.append(msg)
    for tc in msg.tool_calls:
        args = json.loads(tc.function.arguments)
        print(f"  Tool: {tc.function.name}({args})")
        result = tool_handlers[tc.function.name](**args)
        print(f"  Result: {result[:100]}...")
        messages.append({"role": "tool", "tool_call_id": tc.id, "content": result})

print(f"\nTotal turns: {turn}")
