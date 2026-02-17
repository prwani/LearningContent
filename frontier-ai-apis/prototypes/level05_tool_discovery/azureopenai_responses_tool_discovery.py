"""Level 5 — Azure OpenAI Responses API: Tool Discovery with stateful caching (3+ turns).

Uses previous_response_id to persist tool schemas server-side,
enabling prompt caching (~50% discount on unchanged tokens).
Multi-turn meta-tool discovery pattern.
Env: AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_DEPLOYMENT
Auth: Uses DefaultAzureCredential (Entra ID) — no API key needed.
"""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv; load_dotenv()
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from _common.token_utils import print_openai_usage, check_env_keys


# Note: Azure OpenAI Responses API requires api_version="2024-12-01-preview" or later.
check_env_keys()
credential = DefaultAzureCredential()
token_provider = get_bearer_token_provider(credential, "https://cognitiveservices.azure.com/.default")

client = AzureOpenAI(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    azure_ad_token_provider=token_provider,
    api_version="2024-12-01-preview",
)

# Large tool catalog
TOOL_CATALOG = {
    "get_weather": {"desc": "Get weather for a city", "params": {"location": "string"}},
    "send_email": {"desc": "Send an email", "params": {"to": "string", "subject": "string", "body": "string"}},
    "get_stock_price": {"desc": "Get stock price", "params": {"symbol": "string"}},
    "book_restaurant": {"desc": "Book a restaurant table", "params": {"name": "string", "date": "string"}},
    "translate_text": {"desc": "Translate text", "params": {"text": "string", "target_language": "string"}},
    "search_books": {"desc": "Search books", "params": {"query": "string"}},
    "get_exchange_rate": {"desc": "Get currency exchange rate", "params": {"from": "string", "to": "string"}},
    "check_calendar": {"desc": "Check calendar events", "params": {"date": "string"}},
    "get_news": {"desc": "Get news headlines", "params": {"category": "string"}},
    "order_food": {"desc": "Order food delivery", "params": {"restaurant": "string", "items": "string"}},
}

meta_tools = [
    {"type": "function", "function": {"name": "list_tools", "description": "List available tools.", "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {"name": "describe_tool", "description": "Get schema for a tool.", "parameters": {"type": "object", "properties": {"tool_name": {"type": "string"}}, "required": ["tool_name"]}}},
    {"type": "function", "function": {"name": "run_tool", "description": "Execute a tool.", "parameters": {"type": "object", "properties": {"tool_name": {"type": "string"}, "arguments": {"type": "object"}}, "required": ["tool_name", "arguments"]}}},
]

def handle_meta_tool(name, args):
    if name == "list_tools":
        return json.dumps({k: v["desc"] for k, v in TOOL_CATALOG.items()})
    elif name == "describe_tool":
        return json.dumps(TOOL_CATALOG.get(args["tool_name"], {}))
    elif name == "run_tool":
        return json.dumps({"tool": args["tool_name"], "result": f"Mock result for {args['tool_name']}"})
    return json.dumps({"error": "unknown"})

print("=== Azure OpenAI Responses API — Tool Discovery with Caching (3+ turns) ===\n")

queries = [
    "What tools do you have? Then check the weather in Tokyo.",
    "Now also get the stock price for AAPL.",
    "Translate 'Hello World' to French.",
]

previous_id = None
for i, user_query in enumerate(queries, 1):
    print(f"--- Turn {i} ---")
    print(f"User: {user_query}")

    kwargs = {
        "model": "gpt-4o-mini",
        "instructions": "Use list_tools, describe_tool, run_tool to discover and execute tools.",
        "input": user_query,
        "tools": meta_tools,
        "store": True,
    }
    if previous_id:
        kwargs["previous_response_id"] = previous_id

    response = client.responses.create(**kwargs)
    previous_id = response.id

    # Handle function calls in loop
    while True:
        function_calls = [item for item in response.output if item.type == "function_call"]
        if not function_calls:
            print(f"  Assistant: {response.output_text}")
            break

        tool_outputs = []
        for fc in function_calls:
            args = json.loads(fc.arguments) if fc.arguments else {}
            print(f"  Meta-tool: {fc.name}({args})")
            result = handle_meta_tool(fc.name, args)
            print(f"  Result: {result[:80]}...")
            tool_outputs.append({"type": "function_call_output", "call_id": fc.call_id, "output": result})

        response = client.responses.create(
            model=os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini"),
            previous_response_id=response.id,
            input=tool_outputs,
            tools=meta_tools,
            store=True,
        )

    print_openai_usage(response, label=f"Turn {i}")
    print()
