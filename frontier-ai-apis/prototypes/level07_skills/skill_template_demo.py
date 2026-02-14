"""Level 7 — Skills: SKILL.md Template Creation and Loading.

Demonstrates the open SKILL.md standard (agentskills.io):
  1. Creates a SKILL.md file programmatically
  2. Loads it into a system prompt for the model
  3. The model follows the skill's step-by-step instructions
Env: OPENAI_API_KEY
"""
import os, sys, textwrap
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv; load_dotenv()
from openai import OpenAI
from _common.token_utils import print_openai_usage

client = OpenAI()

# --- Create a SKILL.md in memory ---
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
    Use markdown with ## headers for each section.
    Keep the tone professional but concise.
""")

print("=== Skills — SKILL.md Template Demo ===\n")
print("--- SKILL.md content ---")
print(SKILL_MD)
print("--- End SKILL.md ---\n")

# Load skill into system prompt (progressive disclosure pattern)
system_prompt = f"""You are an assistant with the following skill loaded:

{SKILL_MD}

Follow the skill instructions precisely when the user asks for a report."""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": textwrap.dedent("""\
            Here are my notes for this week:
            - Finished API integration with payment provider
            - Code review for auth module PR
            - Working on database migration script (70% done)
            - Blocked on design specs for new dashboard
            - Had 3 customer support escalations
            - Started performance testing framework
        """)},
    ],
)

print(f"Generated Report:\n{response.choices[0].message.content}")
print_openai_usage(response)
