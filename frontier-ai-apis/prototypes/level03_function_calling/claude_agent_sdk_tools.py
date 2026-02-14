"""Level 3 — Claude Agent SDK: Tool Calling with Agent Loop.

Uses the claude-agent-sdk to let the agent autonomously discover and call
tools across multiple turns. The SDK handles the agentic loop automatically.
Env: ANTHROPIC_API_KEY
"""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv; load_dotenv()
from _common.token_utils import check_env_keys

check_env_keys()

import anyio
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, TextBlock, ToolUseBlock, ToolResultBlock

# Define tools as MCP-compatible functions
WEATHER_DATA = {
    "tokyo": {"condition": "sunny", "temp_c": 24},
    "london": {"condition": "cloudy", "temp_c": 14},
    "cairo": {"condition": "hot", "temp_c": 35},
}

def get_weather(location: str) -> str:
    """Get current weather for a location."""
    data = WEATHER_DATA.get(location.lower(), {"condition": "unknown", "temp_c": 20})
    return json.dumps({"location": location, **data})

# Register tool handler
tool_handlers = {"get_weather": get_weather}

async def main():
    print("=== Claude Agent SDK — Tool Calling (3+ turns) ===\n")

    options = ClaudeAgentOptions(
        system_prompt="You are a weather assistant. Check each city separately using the get_weather tool.",
        max_turns=5,
        model="claude-sonnet-4-20250514",
    )

    turn = 0
    async for message in query(
        prompt="Compare weather in Tokyo, London, and Cairo. Which is the hottest?",
        options=options,
        tools=[{
            "name": "get_weather",
            "description": "Get current weather for a location.",
            "input_schema": {
                "type": "object",
                "properties": {"location": {"type": "string"}},
                "required": ["location"],
            },
        }],
        tool_handler=lambda name, args: tool_handlers[name](**args),
    ):
        turn += 1
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(f"[Turn {turn}] Assistant: {block.text}")
                elif isinstance(block, ToolUseBlock):
                    print(f"[Turn {turn}] Tool call: {block.name}({block.input})")
                elif isinstance(block, ToolResultBlock):
                    print(f"[Turn {turn}] Tool result: {block.content}")

    print(f"\nTotal turns: {turn}")

if __name__ == "__main__":
    anyio.run(main)
