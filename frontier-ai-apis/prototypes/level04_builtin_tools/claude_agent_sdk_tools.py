"""Level 4 — Claude Agent SDK: Built-in Tools (3+ turns).

Uses the Agent SDK with built-in tools (Read, Bash, WebSearch)
to perform a multi-step research task autonomously.
Env: ANTHROPIC_API_KEY
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv; load_dotenv()
from _common.token_utils import check_env_keys

check_env_keys()

import anyio
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, TextBlock, ToolUseBlock

async def main():
    print("=== Claude Agent SDK — Built-in Tools (3+ turns) ===\n")

    options = ClaudeAgentOptions(
        system_prompt="You are a research assistant. Use available tools to complete multi-step tasks.",
        max_turns=5,
        model="claude-sonnet-4-20250514",
        allowed_tools=["Bash", "Read"],
        permission_mode="acceptEdits",
    )

    queries = [
        "Write a Python script that generates 20 random numbers between 1 and 100, saves them to /tmp/numbers.txt",
        "Read /tmp/numbers.txt and calculate the mean, median, and standard deviation",
        "Create a summary report of the statistical analysis",
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
                        print(f"  Tool: {block.name}")
        print()

if __name__ == "__main__":
    anyio.run(main)
