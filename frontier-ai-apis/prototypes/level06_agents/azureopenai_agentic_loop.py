"""Level 6 — OpenAI: Full Agentic Loop with Structured Output.

Demonstrates a complete agent:
  1. Agentic loop: while stop_reason != "stop", handle tool_calls
  2. Structured output via response_format (json_schema)
  3. Uses get_weather + get_stock_price as tools
Env: AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY, AZURE_OPENAI_DEPLOYMENT
"""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv; load_dotenv()
from openai import AzureOpenAI
from _common.token_utils import print_openai_usage

client = AzureOpenAI(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    api_version="2024-12-01-preview",
)

# --- Tools ---
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a location.",
            "parameters": {
                "type": "object",
                "properties": {"location": {"type": "string"}},
                "required": ["location"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_stock_price",
            "description": "Get stock price by ticker symbol.",
            "parameters": {
                "type": "object",
                "properties": {"symbol": {"type": "string"}},
                "required": ["symbol"],
            },
        },
    },
]

def run_tool(name: str, args: dict) -> str:
    if name == "get_weather":
        return json.dumps({"location": args["location"], "temp_c": 22, "condition": "sunny"})
    elif name == "get_stock_price":
        return json.dumps({"symbol": args["symbol"], "price": 178.50, "currency": "USD"})
    return json.dumps({"error": "unknown tool"})

# --- Structured output schema ---
response_format = {
    "type": "json_schema",
    "json_schema": {
        "name": "briefing",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "weather_summary": {"type": "string"},
                "stock_summary":   {"type": "string"},
                "recommendation":  {"type": "string"},
            },
            "required": ["weather_summary", "stock_summary", "recommendation"],
            "additionalProperties": False,
        },
    },
}

print("=== Azure OpenAI — Agentic Loop + Structured Output ===\n")

messages = [
    {"role": "system", "content": "You are a morning briefing agent. Check weather and stocks, then return a structured briefing."},
    {"role": "user",   "content": "Give me a briefing for San Francisco. Also check AAPL stock."},
]

step = 0
while True:
    step += 1
    response = client.chat.completions.create(
        model=os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini"),
        messages=messages,
        tools=tools,
        response_format=response_format if step > 1 else None,  # structured on final
    )
    print_openai_usage(response, label=f"Step {step}")
    msg = response.choices[0].message

    if not msg.tool_calls:
        print(f"\nStructured output:\n{msg.content}")
        break

    messages.append(msg)
    for tc in msg.tool_calls:
        args = json.loads(tc.function.arguments)
        print(f"  Tool: {tc.function.name}({args})")
        result = run_tool(tc.function.name, args)
        messages.append({"role": "tool", "tool_call_id": tc.id, "content": result})

    if step > 5:
        print("Max steps reached.")
        break
