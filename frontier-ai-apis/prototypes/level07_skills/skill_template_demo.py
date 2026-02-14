"""Level 7 — OpenAI Responses API: SKILL.md Template + Shell (3+ turns).

Demonstrates:
  1. SKILL.md creation and loading into system prompt
  2. Multi-turn conversation following skill instructions
  3. Responses API with previous_response_id for stateful skills
Env: OPENAI_API_KEY
"""
import os, sys, textwrap
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv; load_dotenv()
from openai import OpenAI
from _common.token_utils import print_openai_usage, check_env_keys

check_env_keys()
client = OpenAI()

SKILL_MD = textwrap.dedent("""\
    # Skill: Weekly Report Writer
    ## Description
    Generate a structured weekly status report from bullet-point notes.
    ## Instructions
    1. Read the user's bullet-point notes
    2. Group items by category: Accomplishments, In Progress, Blockers
    3. Write 1-2 sentence summaries for each item
    4. Add a "Next Week" section with priorities
    5. Format as a professional status report with headers
    ## Output Format
    Use markdown with ## headers for each section.""")

print("=== OpenAI Responses API — SKILL.md Template (3+ turns) ===\n")
print("--- SKILL.md loaded ---\n")

queries = [
    textwrap.dedent("""\
        Here are my notes:
        - Finished API integration with payment provider
        - Code review for auth module PR
        - Working on database migration script (70% done)
        - Blocked on design specs for new dashboard"""),
    "Add these items too: Started performance testing framework, had 3 customer support escalations.",
    "Now reformat the entire report with priority rankings for next week.",
]

previous_id = None
for i, query in enumerate(queries, 1):
    print(f"--- Turn {i} ---")
    print(f"User: {query[:80]}...")

    kwargs = {
        "model": "gpt-4o-mini",
        "instructions": f"You are an assistant with this skill:\n\n{SKILL_MD}\n\nFollow the skill instructions precisely.",
        "input": query,
        "store": True,
    }
    if previous_id:
        kwargs["previous_response_id"] = previous_id

    response = client.responses.create(**kwargs)
    previous_id = response.id

    print(f"Assistant: {response.output_text[:200]}...")
    print_openai_usage(response, label=f"Turn {i}")
    print()
