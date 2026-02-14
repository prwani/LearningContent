"""Level 9 — Plugin Loader: Parse plugin.json and discover skills/tools/MCP.

Demonstrates the Anthropic plugin architecture:
  1. Parse a plugin.json manifest
  2. Discover skills, commands, MCP server configs
  3. Construct a Messages API call from plugin metadata
"""
import os, sys, json

print("=== Plugin Loader — Parse plugin.json ===\n")

# --- Sample plugin.json (Anthropic Knowledge Work Plugin format) ---
plugin_manifest = {
    "name": "sales-toolkit",
    "version": "1.0.0",
    "description": "Sales team productivity plugin with CRM tools and report generation.",
    "skills": [
        {
            "name": "quarterly-report",
            "description": "Generate a quarterly sales report from CRM data.",
            "instructions_file": "skills/quarterly-report/SKILL.md",
        },
        {
            "name": "lead-scorer",
            "description": "Score and prioritize sales leads.",
            "instructions_file": "skills/lead-scorer/SKILL.md",
        },
    ],
    "commands": [
        {"name": "/pipeline", "description": "Show sales pipeline summary"},
        {"name": "/forecast", "description": "Generate revenue forecast"},
    ],
    "mcp_servers": [
        {
            "name": "crm-server",
            "command": "python",
            "args": ["mcp/crm_server.py"],
            "port": 8001,
            "tools": ["get_leads", "update_deal", "search_contacts", "get_pipeline"],
        },
        {
            "name": "analytics-server",
            "command": "python",
            "args": ["mcp/analytics_server.py"],
            "port": 8002,
            "tools": ["run_query", "get_metrics", "generate_chart"],
        },
    ],
    "agents": [
        {"name": "deal-closer", "description": "Autonomous agent for deal follow-ups"},
    ],
    "hooks": {
        "on_install": "hooks/setup.sh",
        "on_command": "hooks/validate.py",
    },
}

print("Plugin manifest:")
print(json.dumps(plugin_manifest, indent=2))

# --- Extract components ---
print("\n--- Discovered Components ---")
print(f"\nSkills ({len(plugin_manifest['skills'])}):")
for s in plugin_manifest["skills"]:
    print(f"  • {s['name']}: {s['description']}")

print(f"\nCommands ({len(plugin_manifest['commands'])}):")
for c in plugin_manifest["commands"]:
    print(f"  • {c['name']}: {c['description']}")

print(f"\nMCP Servers ({len(plugin_manifest['mcp_servers'])}):")
for m in plugin_manifest["mcp_servers"]:
    print(f"  • {m['name']} (port {m['port']}): {len(m['tools'])} tools — {', '.join(m['tools'])}")

print(f"\nAgents ({len(plugin_manifest['agents'])}):")
for a in plugin_manifest["agents"]:
    print(f"  • {a['name']}: {a['description']}")

# --- Build tool list from MCP servers (what would be sent to Messages API) ---
api_tools = []
for mcp_srv in plugin_manifest["mcp_servers"]:
    for tool_name in mcp_srv["tools"]:
        api_tools.append({
            "name": f"{mcp_srv['name']}__{tool_name}",
            "description": f"Tool '{tool_name}' from MCP server '{mcp_srv['name']}'",
            "input_schema": {"type": "object", "properties": {}},
        })

print(f"\n--- API Tools constructed: {len(api_tools)} ---")
for t in api_tools:
    print(f"  • {t['name']}")
