"""Level 7 — Claude Agent SDK: Skills with Agent (3+ turns).

Uses the Agent SDK to load skills and execute multi-step workflows.
The SDK manages tool invocation, context, and session state.
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
    # Skill: Weekly Report Writer
    ## Instructions
    1. Query the database for weekly data
    2. Get relevant metrics
    3. Generate charts for key indicators
    4. Compile a structured report with sections: Summary, Data, Charts, Recommendations""")

def tool_handler(name: str, args: dict) -> str:
    if name == "query_database":
        return json.dumps({"rows": [
            {"week": "W1", "revenue": 95000, "users": 1200},
            {"week": "W2", "revenue": 102000, "users": 1350},
            {"week": "W3", "revenue": 98000, "users": 1280},
        ]})
    elif name == "get_metrics":
        return json.dumps({"growth": "8%", "retention": "94%", "avg_order": "$78"})
    elif name == "generate_chart":
        return json.dumps({"chart": f"{args.get('chart_type', 'bar')}_chart.png", "status": "generated"})
    return json.dumps({"error": f"Unknown tool: {name}"})

async def main():
    print("=== Claude Agent SDK — Skills + Agent (3+ turns) ===\n")

    tools = [
        {"name": "query_database", "description": "Run SQL query on the data warehouse.",
         "input_schema": {"type": "object", "properties": {"sql": {"type": "string"}}, "required": ["sql"]}},
        {"name": "get_metrics", "description": "Get business metrics.",
         "input_schema": {"type": "object", "properties": {"category": {"type": "string"}}, "required": ["category"]}},
        {"name": "generate_chart", "description": "Generate a chart.",
         "input_schema": {"type": "object", "properties": {"chart_type": {"type": "string"}, "data": {"type": "string"}}, "required": ["chart_type", "data"]}},
    ]

    options = ClaudeAgentOptions(
        system_prompt=f"You are a report-writing agent with the following skill:\n\n{SKILL_MD}",
        max_turns=6,
        model="claude-sonnet-4-20250514",
    )

    queries = [
        "Pull this week's sales data.",
        "Get the customer retention metrics.",
        "Generate a revenue trend chart and write the final weekly report.",
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
                        print(f"  Tool: {block.name}({json.dumps(block.input)[:80]})")
        print()

if __name__ == "__main__":
    anyio.run(main)
