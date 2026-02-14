"""Level 9 — Claude Agent SDK: Plugin-driven Agent (3+ turns).

Uses the Agent SDK to implement a plugin system:
  1. Load plugin manifest (skills, tools, MCP configs)
  2. Agent SDK handles MCP server connections
  3. Agent autonomously uses plugin tools across turns
Env: ANTHROPIC_API_KEY
"""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv; load_dotenv()
from _common.token_utils import check_env_keys

check_env_keys()

import anyio
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, TextBlock, ToolUseBlock

# --- Plugin manifest ---
PLUGIN = {
    "name": "sales-toolkit",
    "version": "1.0.0",
    "skills": [
        {"name": "pipeline-report", "instructions": "1. Get pipeline data 2. Get metrics 3. Compile report"},
    ],
    "mcp_servers": [
        {"name": "crm-server", "tools": ["get_pipeline", "search_contacts", "update_deal"]},
        {"name": "analytics-server", "tools": ["get_metrics", "run_query"]},
    ],
}

# Build skill prompt from plugin
skill_text = "\n".join(f"### {s['name']}\n{s['instructions']}" for s in PLUGIN["skills"])
system_prompt = f"You are powered by the '{PLUGIN['name']}' plugin v{PLUGIN['version']}.\n\nSkills:\n{skill_text}"

def tool_handler(name: str, args: dict) -> str:
    """Route to appropriate MCP server."""
    crm_tools = {"get_pipeline", "search_contacts", "update_deal"}
    analytics_tools = {"get_metrics", "run_query"}

    server = "crm-server" if name in crm_tools else "analytics-server" if name in analytics_tools else "unknown"
    print(f"    → Routed to MCP: {server}")

    handlers = {
        "get_pipeline": lambda a: json.dumps({
            "deals": [{"name": "Acme Corp", "value": "$250K", "stage": a.get("stage", "all")},
                      {"name": "TechStart", "value": "$180K", "stage": "closing"}],
            "total": "$430K",
        }),
        "search_contacts": lambda a: json.dumps({
            "contacts": [{"name": "John Smith", "company": "Acme", "role": "CTO"}],
        }),
        "get_metrics": lambda a: json.dumps({
            "type": a.get("metric_type", "revenue"), "value": "$2.1M", "growth": "+15%",
        }),
        "run_query": lambda a: json.dumps({
            "results": [{"month": "Jan", "deals_closed": 5}, {"month": "Feb", "deals_closed": 8}],
        }),
    }
    handler = handlers.get(name)
    return handler(args) if handler else json.dumps({"error": f"Unknown tool: {name}"})

async def main():
    print(f"=== Claude Agent SDK — Plugin: {PLUGIN['name']} (3+ turns) ===\n")
    print(f"MCP Servers: {', '.join(s['name'] for s in PLUGIN['mcp_servers'])}")
    print(f"Total tools: {sum(len(s['tools']) for s in PLUGIN['mcp_servers'])}\n")

    # Build tools from plugin manifest
    tools = []
    for mcp in PLUGIN["mcp_servers"]:
        for tool_name in mcp["tools"]:
            tools.append({
                "name": tool_name,
                "description": f"Tool '{tool_name}' from {mcp['name']}.",
                "input_schema": {"type": "object", "properties": {
                    "stage": {"type": "string"}, "query": {"type": "string"},
                    "metric_type": {"type": "string"},
                }},
            })

    options = ClaudeAgentOptions(
        system_prompt=system_prompt,
        max_turns=6,
        model="claude-sonnet-4-20250514",
    )

    queries = [
        "Show me the current sales pipeline.",
        "Get the revenue metrics and deal closure trends.",
        "Search for contacts at Acme Corp and compile a full pipeline report.",
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
                        print(f"  Tool: {block.name}({json.dumps(block.input)[:60]})")
        print()

if __name__ == "__main__":
    anyio.run(main)
