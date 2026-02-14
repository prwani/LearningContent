"""Level 9 — Anthropic: Plugin-driven Messages API call with MCP routing.

Demonstrates how a plugin system constructs a Messages API call:
  1. Load plugin manifest → discover tools from MCP servers
  2. Build system prompt from skills
  3. Send Messages API call with tools
  4. Route tool_use responses to the correct MCP server
Env: ANTHROPIC_API_KEY
"""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv; load_dotenv()
import anthropic
from _common.token_utils import print_anthropic_usage

client = anthropic.Anthropic()

# --- Simulated plugin: sales toolkit with 2 MCP servers ---
PLUGIN_SKILLS = """## Skill: Sales Pipeline Reporter
1. Query the CRM for current pipeline data
2. Get key metrics from analytics
3. Compile a summary with deal count, total value, and top deals"""

# Tools as they'd be constructed from MCP server tool lists
tools = [
    {
        "name": "get_pipeline",
        "description": "Get current sales pipeline (from CRM MCP server).",
        "input_schema": {
            "type": "object",
            "properties": {"stage": {"type": "string", "description": "Filter by stage: prospecting, negotiation, closing"}},
        },
    },
    {
        "name": "get_metrics",
        "description": "Get sales metrics (from Analytics MCP server).",
        "input_schema": {
            "type": "object",
            "properties": {"metric_type": {"type": "string", "description": "Type: revenue, conversion, deals"}},
        },
    },
    {
        "name": "return_report",
        "description": "Return the structured pipeline report.",
        "input_schema": {
            "type": "object",
            "properties": {
                "total_deals": {"type": "integer"},
                "total_value": {"type": "string"},
                "top_deals":   {"type": "array", "items": {"type": "string"}},
                "summary":     {"type": "string"},
            },
            "required": ["total_deals", "total_value", "top_deals", "summary"],
        },
    },
]

# --- MCP routing table (maps tool name → server) ---
MCP_ROUTES = {
    "get_pipeline": "crm-server",
    "get_metrics":  "analytics-server",
}

def route_to_mcp(tool_name: str, args: dict) -> str:
    """Simulate routing tool calls to MCP servers."""
    server = MCP_ROUTES.get(tool_name, "local")
    print(f"    → Routed to MCP server: {server}")

    if tool_name == "get_pipeline":
        return json.dumps({
            "stage": args.get("stage", "all"),
            "deals": [
                {"name": "Acme Corp", "value": "$250K", "stage": "negotiation"},
                {"name": "TechStart", "value": "$180K", "stage": "closing"},
                {"name": "GlobalInc", "value": "$420K", "stage": "prospecting"},
            ],
            "total": 3, "total_value": "$850K",
        })
    elif tool_name == "get_metrics":
        return json.dumps({
            "metric_type": args.get("metric_type", "revenue"),
            "q4_revenue": "$2.1M", "conversion_rate": "23%",
            "avg_deal_size": "$175K", "deals_closed": 12,
        })
    return json.dumps({"error": "unknown"})

print("=== Anthropic — Plugin-Driven Agent with MCP Routing ===\n")

messages = [
    {"role": "user", "content": "Show me the current sales pipeline status. Use return_report for the final output."},
]

step = 0
while True:
    step += 1
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system=f"You are a sales assistant powered by the sales-toolkit plugin.\n\n{PLUGIN_SKILLS}",
        tools=tools,
        messages=messages,
    )
    print_anthropic_usage(response, label=f"Step {step}")

    tool_uses = [b for b in response.content if b.type == "tool_use"]

    if not tool_uses or response.stop_reason == "end_turn":
        text = [b for b in response.content if b.type == "text"]
        if text:
            print(f"\nAssistant: {text[0].text}")
        break

    for tu in tool_uses:
        if tu.name == "return_report":
            print(f"\nStructured Report:\n{json.dumps(tu.input, indent=2)}")

    messages.append({"role": "assistant", "content": response.content})
    tool_results = []
    for tu in tool_uses:
        if tu.name == "return_report":
            tool_results.append({"type": "tool_result", "tool_use_id": tu.id, "content": "Report accepted."})
        else:
            print(f"  Tool: {tu.name}({tu.input})")
            result = route_to_mcp(tu.name, tu.input)
            tool_results.append({"type": "tool_result", "tool_use_id": tu.id, "content": result})

    messages.append({"role": "user", "content": tool_results})

    if any(tu.name == "return_report" for tu in tool_uses):
        break
    if step > 5:
        print("Max steps reached.")
        break
