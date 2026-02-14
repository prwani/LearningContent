"""Level 6 — Claude Agent SDK: Autonomous Agent with Tools (3+ turns).

The Agent SDK manages the agentic loop automatically — no manual
while-loop needed. The agent discovers tools, reasons, and acts.
Env: ANTHROPIC_API_KEY
"""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv; load_dotenv()
from _common.token_utils import check_env_keys

check_env_keys()

import anyio
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, TextBlock, ToolUseBlock

MOCK_DATA = {
    "get_weather": lambda args: json.dumps({"location": args.get("location", ""), "temp_c": 22, "condition": "sunny"}),
    "get_stock_price": lambda args: json.dumps({"symbol": args.get("symbol", ""), "price": 178.50, "change": "+1.2%"}),
    "get_news": lambda args: json.dumps({"category": args.get("category", "tech"), "headlines": ["AI market grows 40%", "New chip breakthrough"]}),
}

def tool_handler(name: str, args: dict) -> str:
    handler = MOCK_DATA.get(name)
    if handler:
        return handler(args)
    return json.dumps({"error": f"Unknown tool: {name}"})

async def main():
    print("=== Claude Agent SDK — Autonomous Agent (3+ turns) ===\n")

    tools = [
        {"name": "get_weather", "description": "Get weather for a city.",
         "input_schema": {"type": "object", "properties": {"location": {"type": "string"}}, "required": ["location"]}},
        {"name": "get_stock_price", "description": "Get stock price by symbol.",
         "input_schema": {"type": "object", "properties": {"symbol": {"type": "string"}}, "required": ["symbol"]}},
        {"name": "get_news", "description": "Get news headlines by category.",
         "input_schema": {"type": "object", "properties": {"category": {"type": "string"}}, "required": ["category"]}},
    ]

    options = ClaudeAgentOptions(
        system_prompt="You are a morning briefing agent. Check weather, stocks, and news, then compile a summary.",
        max_turns=6,
        model="claude-sonnet-4-20250514",
    )

    turn = 0
    async for message in query(
        prompt="Give me a complete morning briefing: weather in San Francisco, AAPL and NVDA stock prices, and latest tech news.",
        options=options,
        tools=tools,
        tool_handler=tool_handler,
    ):
        turn += 1
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(f"[Turn {turn}] Assistant: {block.text[:200]}...")
                elif isinstance(block, ToolUseBlock):
                    result = tool_handler(block.name, block.input)
                    print(f"[Turn {turn}] Tool: {block.name}({block.input}) → {result[:80]}")

    print(f"\nTotal turns: {turn}")

if __name__ == "__main__":
    anyio.run(main)
