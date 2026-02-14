"""Level 9 — OpenAI: Plugin-like Pattern with Responses API (3+ turns).

Demonstrates how to build a plugin system for OpenAI:
  1. Load plugin manifest → discover tools
  2. Register tools with Responses API
  3. Route tool calls through a plugin dispatcher
Env: OPENAI_API_KEY
"""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv; load_dotenv()
from openai import OpenAI
from _common.token_utils import print_openai_usage, check_env_keys

check_env_keys()
client = OpenAI()

# --- Plugin manifest (similar to Anthropic's plugin.json) ---
PLUGIN = {
    "name": "sales-toolkit",
    "skills": [{"name": "pipeline-report", "instructions": "Gather pipeline data, get metrics, compile report."}],
    "tools": {
        "get_pipeline": {"desc": "Get sales pipeline data", "params": {"stage": "string"}},
        "get_metrics": {"desc": "Get sales metrics", "params": {"metric_type": "string"}},
        "search_contacts": {"desc": "Search CRM contacts", "params": {"query": "string"}},
    },
}

# Build OpenAI tools array from plugin manifest
tools = []
for name, spec in PLUGIN["tools"].items():
    tools.append({
        "type": "function",
        "function": {
            "name": name,
            "description": spec["desc"],
            "parameters": {
                "type": "object",
                "properties": {k: {"type": "string"} for k in spec["params"]},
                "required": list(spec["params"].keys()),
            },
        },
    })

def dispatch_tool(name, args):
    """Plugin dispatcher — routes to correct backend."""
    if name == "get_pipeline":
        return json.dumps({"deals": [
            {"name": "Acme Corp", "value": "$250K", "stage": args.get("stage", "all")},
            {"name": "TechStart", "value": "$180K", "stage": "closing"},
        ], "total_value": "$430K"})
    elif name == "get_metrics":
        return json.dumps({"type": args.get("metric_type", "revenue"), "value": "$2.1M", "growth": "+15%"})
    elif name == "search_contacts":
        return json.dumps({"contacts": [
            {"name": "John Smith", "company": "Acme", "role": "CTO"},
            {"name": "Jane Doe", "company": "TechStart", "role": "VP Engineering"},
        ]})
    return json.dumps({"error": "unknown"})

skill_prompt = "\n".join(f"- {s['name']}: {s['instructions']}" for s in PLUGIN["skills"])
system = f"You are powered by the '{PLUGIN['name']}' plugin.\nSkills:\n{skill_prompt}"

print(f"=== OpenAI — Plugin Pattern: {PLUGIN['name']} (3+ turns) ===\n")

queries = [
    "Show me the current sales pipeline in the negotiation stage.",
    "Get the revenue metrics for this quarter.",
    "Search for contacts at our top accounts and summarize the pipeline status.",
]

previous_id = None
for qi, user_msg in enumerate(queries, 1):
    print(f"--- Turn {qi} ---")
    print(f"User: {user_msg}")

    kwargs = {
        "model": "gpt-4o-mini",
        "instructions": system,
        "input": user_msg,
        "tools": tools,
        "store": True,
    }
    if previous_id:
        kwargs["previous_response_id"] = previous_id

    response = client.responses.create(**kwargs)
    previous_id = response.id

    while True:
        function_calls = [item for item in response.output if item.type == "function_call"]
        if not function_calls:
            print(f"  Assistant: {response.output_text[:200]}...")
            break
        tool_outputs = []
        for fc in function_calls:
            args = json.loads(fc.arguments) if fc.arguments else {}
            print(f"  Plugin dispatch: {fc.name}({args})")
            result = dispatch_tool(fc.name, args)
            print(f"  Result: {result[:80]}...")
            tool_outputs.append({"type": "function_call_output", "call_id": fc.call_id, "output": result})
        response = client.responses.create(
            model="gpt-4o-mini", previous_response_id=response.id,
            input=tool_outputs, tools=tools, store=True,
        )
        previous_id = response.id

    print_openai_usage(response, label=f"Turn {qi}")
    print()
