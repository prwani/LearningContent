"""Level 8 — OpenAI: Full Agentic Stack (Skills + Tools + MCP + Structured Output).

Combines:
  1. A loaded SKILL.md (report-writer) in system prompt
  2. Custom function tools (get_project_status, get_team_members)
  3. MCP connector to toolscout server (if running)
  4. Structured output via json_schema
Env: OPENAI_API_KEY
"""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv; load_dotenv()
from openai import OpenAI
from _common.token_utils import print_openai_usage

client = OpenAI()

# --- Skill loaded into system prompt ---
SKILL = """## Skill: Project Status Reporter
1. Gather project status and team info using available tools
2. Compile into a structured report
3. Return using the structured output format"""

# --- Custom tools ---
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_project_status",
            "description": "Get current status of a project by name.",
            "parameters": {
                "type": "object",
                "properties": {"project_name": {"type": "string"}},
                "required": ["project_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_team_members",
            "description": "Get team members for a project.",
            "parameters": {
                "type": "object",
                "properties": {"project_name": {"type": "string"}},
                "required": ["project_name"],
            },
        },
    },
]

def run_tool(name: str, args: dict) -> str:
    if name == "get_project_status":
        return json.dumps({
            "project": args["project_name"], "status": "on_track",
            "completion": "72%", "sprint": "Sprint 14",
            "blockers": ["Waiting on API specs from partner team"],
        })
    elif name == "get_team_members":
        return json.dumps({
            "project": args["project_name"],
            "members": [
                {"name": "Alice", "role": "Lead"},
                {"name": "Bob", "role": "Backend"},
                {"name": "Carol", "role": "Frontend"},
            ],
        })
    return json.dumps({"error": "unknown"})

# --- Structured output schema ---
response_format = {
    "type": "json_schema",
    "json_schema": {
        "name": "project_report",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "project_name": {"type": "string"},
                "status":       {"type": "string"},
                "completion":   {"type": "string"},
                "team_size":    {"type": "integer"},
                "blockers":     {"type": "array", "items": {"type": "string"}},
                "summary":      {"type": "string"},
            },
            "required": ["project_name", "status", "completion", "team_size", "blockers", "summary"],
            "additionalProperties": False,
        },
    },
}

print("=== OpenAI — Full Stack Agent (Skill + Tools + Structured Output) ===\n")

messages = [
    {"role": "system", "content": f"You are a project reporting agent.\n\n{SKILL}"},
    {"role": "user", "content": "Generate a status report for Project Phoenix."},
]

step = 0
while True:
    step += 1
    use_format = response_format if step > 1 else None
    response = client.chat.completions.create(
        model="gpt-4o-mini", messages=messages, tools=tools,
        response_format=use_format,
    )
    print_openai_usage(response, label=f"Step {step}")
    msg = response.choices[0].message

    if not msg.tool_calls:
        print(f"\nStructured Report:\n{msg.content}")
        break

    messages.append(msg)
    for tc in msg.tool_calls:
        args = json.loads(tc.function.arguments)
        print(f"  Tool: {tc.function.name}({args})")
        result = run_tool(tc.function.name, args)
        messages.append({"role": "tool", "tool_call_id": tc.id, "content": result})

    if step > 5:
        print("Max steps reached.")
        break
