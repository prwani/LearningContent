"""Level 7 — Azure OpenAI Chat Completions: Skills loaded into system prompt (3+ turns).

Loads a SKILL.md into the system prompt. The model follows the skill
instructions across a multi-turn conversation with tool use.
Env: AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY, AZURE_OPENAI_DEPLOYMENT
"""
import os, sys, json, textwrap
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv; load_dotenv()
from openai import AzureOpenAI
from _common.token_utils import print_openai_usage, check_env_keys

check_env_keys()
client = AzureOpenAI(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    api_version="2024-12-01-preview",
)

SKILL_MD = textwrap.dedent("""\
    # Skill: Data Analyst
    ## Instructions
    1. Gather data using available tools
    2. Analyze the data for patterns and insights
    3. Generate a structured summary with recommendations
    4. Always cite which tools/data sources you used""")

tools = [
    {"type": "function", "function": {
        "name": "query_database", "description": "Run a SQL query on the sales database.",
        "parameters": {"type": "object", "properties": {"sql": {"type": "string"}}, "required": ["sql"]}}},
    {"type": "function", "function": {
        "name": "get_metrics", "description": "Get business metrics by category.",
        "parameters": {"type": "object", "properties": {"category": {"type": "string"}}, "required": ["category"]}}},
    {"type": "function", "function": {
        "name": "generate_chart", "description": "Generate a chart from data.",
        "parameters": {"type": "object", "properties": {"chart_type": {"type": "string"}, "data_description": {"type": "string"}}, "required": ["chart_type", "data_description"]}}},
]

def run_tool(name, args):
    if name == "query_database":
        return json.dumps({"rows": [{"month": "Jan", "revenue": 120000}, {"month": "Feb", "revenue": 135000}, {"month": "Mar", "revenue": 128000}]})
    elif name == "get_metrics":
        return json.dumps({"category": args["category"], "growth": "12%", "churn": "3.2%", "nps": 72})
    elif name == "generate_chart":
        return json.dumps({"chart_url": f"chart_{args['chart_type']}.png", "status": "generated"})
    return json.dumps({"error": "unknown"})

print("=== Azure OpenAI Chat Completions — Skills + Tools (3+ turns) ===\n")

messages = [
    {"role": "system", "content": f"You are a data analyst assistant.\n\n{SKILL_MD}"},
]

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
        response = client.chat.completions.create(model=os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini"), messages=messages, tools=tools)
        print_openai_usage(response, label=f"  Step {step}")
        msg = response.choices[0].message
        if not msg.tool_calls:
            print(f"  Assistant: {msg.content[:200]}...")
            messages.append(msg)
            break
        messages.append(msg)
        for tc in msg.tool_calls:
            args = json.loads(tc.function.arguments)
            print(f"    Tool: {tc.function.name}({args})")
            result = run_tool(tc.function.name, args)
            messages.append({"role": "tool", "tool_call_id": tc.id, "content": result})
    print()
