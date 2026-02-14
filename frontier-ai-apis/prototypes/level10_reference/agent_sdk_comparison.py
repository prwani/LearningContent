"""Level 10 — Agent SDK Comparison: Messages API loop vs Claude Agent SDK.

Side-by-side comparison showing the same task implemented two ways:
  1. Manual agentic loop with Messages API (verbose, explicit control)
  2. Claude Agent SDK (concise, SDK manages the loop)

Demonstrates when to use each approach.
Env: ANTHROPIC_API_KEY
"""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv; load_dotenv()
import anthropic
from _common.token_utils import print_anthropic_usage, check_env_keys

check_env_keys()

TOOLS_SCHEMA = [
    {"name": "get_weather", "description": "Get weather for a city.",
     "input_schema": {"type": "object", "properties": {"location": {"type": "string"}}, "required": ["location"]}},
    {"name": "get_stock_price", "description": "Get stock price.",
     "input_schema": {"type": "object", "properties": {"symbol": {"type": "string"}}, "required": ["symbol"]}},
]

def tool_handler(name: str, args: dict) -> str:
    if name == "get_weather":
        return json.dumps({"location": args["location"], "temp_c": 22, "condition": "sunny"})
    elif name == "get_stock_price":
        return json.dumps({"symbol": args["symbol"], "price": 178.50, "change": "+1.2%"})
    return json.dumps({"error": "unknown"})

PROMPT = "Check the weather in Tokyo and get the AAPL stock price, then summarize."

# ============================================================
# Approach 1: Manual Messages API loop
# ============================================================
def run_messages_api():
    print("=" * 60)
    print("  Approach 1: Manual Messages API Agentic Loop")
    print("=" * 60)

    client = anthropic.Anthropic()
    messages = [{"role": "user", "content": PROMPT}]

    step = 0
    while step < 5:
        step += 1
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            system="You are a helpful assistant.",
            tools=TOOLS_SCHEMA,
            messages=messages,
        )
        print_anthropic_usage(response, label=f"Step {step}")

        tool_uses = [b for b in response.content if b.type == "tool_use"]
        if not tool_uses:
            text = [b for b in response.content if b.type == "text"]
            if text:
                print(f"\nResult: {text[0].text[:200]}...")
            break

        messages.append({"role": "assistant", "content": response.content})
        tool_results = []
        for tu in tool_uses:
            print(f"  Tool: {tu.name}({tu.input})")
            result = tool_handler(tu.name, tu.input)
            tool_results.append({"type": "tool_result", "tool_use_id": tu.id, "content": result})
        messages.append({"role": "user", "content": tool_results})

    print(f"\n  Lines of orchestration code: ~30")
    print(f"  Control level: Full (manual loop, message management)")
    print()

# ============================================================
# Approach 2: Claude Agent SDK
# ============================================================
def run_agent_sdk():
    print("=" * 60)
    print("  Approach 2: Claude Agent SDK")
    print("=" * 60)

    import anyio
    from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, TextBlock, ToolUseBlock

    async def agent_task():
        options = ClaudeAgentOptions(
            system_prompt="You are a helpful assistant.",
            max_turns=5,
            model="claude-sonnet-4-20250514",
        )

        async for message in query(
            prompt=PROMPT,
            options=options,
            tools=TOOLS_SCHEMA,
            tool_handler=lambda name, args: tool_handler(name, args),
        ):
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(f"\nResult: {block.text[:200]}...")
                    elif isinstance(block, ToolUseBlock):
                        print(f"  Tool: {block.name}({block.input})")

    anyio.run(agent_task)

    print(f"\n  Lines of orchestration code: ~15")
    print(f"  Control level: SDK-managed (automatic loop, streaming)")
    print()

# ============================================================
# Comparison
# ============================================================
print("=== Level 10 — Agent SDK Comparison ===\n")

run_messages_api()
run_agent_sdk()

print("=" * 60)
print("  When to Use Each Approach")
print("=" * 60)
print("""
  Messages API (manual loop):
    ✓ Full control over every step
    ✓ Custom retry/error handling
    ✓ Fine-grained token budget management
    ✓ Works with any HTTP client

  Claude Agent SDK:
    ✓ Less boilerplate code
    ✓ Built-in streaming + async
    ✓ Automatic tool routing
    ✓ Session/context management
    ✓ MCP server integration
    ✓ Hooks and guardrails
""")
