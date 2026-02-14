"""Level 8 — Claude Agent SDK: Full Stack (Skills + MCP + Tools, 3+ turns).

Complete agent using the SDK: loads skills, connects to MCP servers,
handles multi-turn autonomous workflows.

Prerequisites: Start MCP servers:
  cd mcp_servers && bash start_servers.sh

Env: ANTHROPIC_API_KEY
"""
import os, sys, json, textwrap
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv; load_dotenv()
from _common.token_utils import check_env_keys

check_env_keys()

import anyio
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, TextBlock, ToolUseBlock

SKILL_MD = textwrap.dedent("""\
    # Skill: Investment Research Agent
    ## Instructions
    1. Check current stock prices for requested tickers
    2. Get market status and conditions
    3. Search for relevant books/resources on investing
    4. Compile a structured investment brief with: Market Overview, Stock Analysis, Resources""")

# Mock tool handlers (simulating MCP server responses)
def tool_handler(name: str, args: dict) -> str:
    handlers = {
        "get_stock_price": lambda a: json.dumps({"symbol": a.get("symbol", ""), "price": 178.50, "change": "+1.2%"}),
        "get_stock_info": lambda a: json.dumps({"symbol": a.get("symbol", ""), "pe_ratio": 28.5, "market_cap": "$2.8T"}),
        "get_market_status": lambda a: json.dumps({"market": "NYSE", "status": "open", "indices": {"SPX": "+0.5%", "DJIA": "+0.3%"}}),
        "search_books": lambda a: json.dumps({"results": [{"title": "The Intelligent Investor", "author": "Graham"}, {"title": "A Random Walk Down Wall Street", "author": "Malkiel"}]}),
        "get_weather": lambda a: json.dumps({"location": a.get("location", ""), "temp_c": 22, "condition": "clear"}),
        "get_news_headlines": lambda a: json.dumps({"headlines": ["Fed holds rates steady", "Tech earnings beat expectations"]}),
    }
    handler = handlers.get(name)
    return handler(args) if handler else json.dumps({"error": f"Unknown tool: {name}"})

async def main():
    print("=== Claude Agent SDK — Full Stack Agent (Skills + MCP + Tools) ===\n")

    tools = [
        {"name": "get_stock_price", "description": "Get stock price (from Stock MCP server).",
         "input_schema": {"type": "object", "properties": {"symbol": {"type": "string"}}, "required": ["symbol"]}},
        {"name": "get_stock_info", "description": "Get detailed stock info (from Stock MCP server).",
         "input_schema": {"type": "object", "properties": {"symbol": {"type": "string"}}, "required": ["symbol"]}},
        {"name": "get_market_status", "description": "Get market status (from Stock MCP server).",
         "input_schema": {"type": "object", "properties": {}}},
        {"name": "search_books", "description": "Search books (from Library MCP server).",
         "input_schema": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}},
        {"name": "get_news_headlines", "description": "Get news (from General MCP server).",
         "input_schema": {"type": "object", "properties": {"category": {"type": "string"}}, "required": ["category"]}},
    ]

    options = ClaudeAgentOptions(
        system_prompt=f"You are an investment research agent.\n\n{SKILL_MD}",
        max_turns=8,
        model="claude-sonnet-4-20250514",
    )

    queries = [
        "Check the current prices and details for AAPL and MSFT.",
        "What's the market status and latest financial news?",
        "Find me books about value investing and compile your investment brief.",
    ]

    for i, prompt in enumerate(queries, 1):
        print(f"--- Turn {i} ---")
        print(f"User: {prompt}")

        async for message in query(
            prompt=prompt, options=options,
            tools=tools, tool_handler=tool_handler,
        ):
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(f"  Assistant: {block.text[:200]}...")
                    elif isinstance(block, ToolUseBlock):
                        result = tool_handler(block.name, block.input)
                        print(f"  Tool: {block.name} → {result[:80]}")
        print()

if __name__ == "__main__":
    anyio.run(main)
