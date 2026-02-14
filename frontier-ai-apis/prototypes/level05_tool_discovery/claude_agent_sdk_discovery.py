"""Level 5 — Claude Agent SDK: Tool Discovery with MCP servers.

Uses the Agent SDK to connect to MCP servers from toolscout,
automatically discovering and invoking tools across 3+ turns.
The SDK handles tool schema loading and routing.

Prerequisites: Start MCP servers first:
  cd mcp_servers && bash start_servers.sh

Env: ANTHROPIC_API_KEY
"""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv; load_dotenv()
from _common.token_utils import check_env_keys

check_env_keys()

import anyio
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, TextBlock, ToolUseBlock

async def main():
    print("=== Claude Agent SDK — Tool Discovery via MCP (3+ turns) ===\n")
    print("Note: This demo requires MCP servers running on localhost:8000, 9000, 10000\n")

    # The Agent SDK can connect to MCP servers and auto-discover tools
    options = ClaudeAgentOptions(
        system_prompt=(
            "You are a helpful assistant with access to multiple tool servers. "
            "You can manage users, check weather, search books, and trade stocks. "
            "Discover what tools are available and use them to help the user."
        ),
        max_turns=6,
        model="claude-sonnet-4-20250514",
        mcp_servers=[
            {"url": "http://localhost:8000", "name": "general-server"},
            {"url": "http://localhost:9000", "name": "library-server"},
            {"url": "http://localhost:10000", "name": "stock-server"},
        ],
    )

    queries = [
        "What's the weather in San Francisco and what stocks should I check?",
        "Get the price of MSFT and NVDA stocks.",
        "Search for books about 'artificial intelligence' in the library.",
    ]

    for i, prompt in enumerate(queries, 1):
        print(f"--- Turn {i} ---")
        print(f"User: {prompt}")

        async for message in query(prompt=prompt, options=options):
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(f"  Assistant: {block.text[:200]}...")
                    elif isinstance(block, ToolUseBlock):
                        print(f"  Tool discovered & called: {block.name}({json.dumps(block.input)[:80]})")
        print()

if __name__ == "__main__":
    anyio.run(main)
