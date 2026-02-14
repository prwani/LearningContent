"""Level 7 — Anthropic Messages API: Skills + Tools (3+ turns).

Loads a SKILL.md into the system prompt with cache_control.
Multi-turn tool use following skill instructions.
Env: ANTHROPIC_API_KEY
"""
import os, sys, json, textwrap
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv; load_dotenv()
import anthropic
from _common.token_utils import print_anthropic_usage, check_env_keys

check_env_keys()
client = anthropic.Anthropic()

SKILL_MD = textwrap.dedent("""\
    # Skill: Data Analyst
    ## Instructions
    1. Gather data using available tools
    2. Analyze the data for patterns
    3. Generate a structured summary
    4. Cite your data sources""")

tools = [
    {"name": "query_database", "description": "Run SQL on the sales database.",
     "input_schema": {"type": "object", "properties": {"sql": {"type": "string"}}, "required": ["sql"]}},
    {"name": "get_metrics", "description": "Get business metrics by category.",
     "input_schema": {"type": "object", "properties": {"category": {"type": "string"}}, "required": ["category"]}},
    {"name": "generate_chart", "description": "Generate a chart from data.",
     "input_schema": {"type": "object", "properties": {"chart_type": {"type": "string"}, "data_description": {"type": "string"}}, "required": ["chart_type", "data_description"]}},
]

def run_tool(name, args):
    if name == "query_database":
        return json.dumps({"rows": [{"month": "Jan", "revenue": 120000}, {"month": "Feb", "revenue": 135000}, {"month": "Mar", "revenue": 128000}]})
    elif name == "get_metrics":
        return json.dumps({"category": args["category"], "growth": "12%", "churn": "3.2%", "nps": 72})
    elif name == "generate_chart":
        return json.dumps({"chart_url": f"chart_{args['chart_type']}.png", "status": "generated"})
    return json.dumps({"error": "unknown"})

system_prompt = [{"type": "text", "text": f"You are a data analyst.\n\n{SKILL_MD}", "cache_control": {"type": "ephemeral"}}]

print("=== Anthropic Messages API — Skills + Tools (3+ turns) ===\n")

messages = []
user_queries = [
    "Pull the Q1 sales data from the database.",
    "Get the customer satisfaction metrics.",
    "Create a bar chart of the monthly revenue and summarize your findings.",
]

for qi, user_msg in enumerate(user_queries, 1):
    print(f"--- Turn {qi} ---")
    print(f"User: {user_msg}")
    messages.append({"role": "user", "content": user_msg})

    step = 0
    while step < 4:
        step += 1
        response = client.messages.create(
            model="claude-sonnet-4-20250514", max_tokens=1024,
            system=system_prompt, tools=tools, messages=messages,
        )
        print_anthropic_usage(response, label=f"  Step {step}")
        tool_uses = [b for b in response.content if b.type == "tool_use"]
        if not tool_uses:
            text = [b for b in response.content if b.type == "text"]
            if text:
                print(f"  Assistant: {text[0].text[:200]}...")
            messages.append({"role": "assistant", "content": response.content})
            break
        messages.append({"role": "assistant", "content": response.content})
        tool_results = []
        for tu in tool_uses:
            print(f"    Tool: {tu.name}({tu.input})")
            result = run_tool(tu.name, tu.input)
            tool_results.append({"type": "tool_result", "tool_use_id": tu.id, "content": result})
        messages.append({"role": "user", "content": tool_results})
    print()
