"""Level 4 — OpenAI Responses API: Web Search (built-in tool).

The model autonomously searches the web and synthesizes an answer.
No agentic loop needed — web_search executes server-side.
Env: OPENAI_API_KEY
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv; load_dotenv()
from openai import OpenAI
from _common.token_utils import print_openai_usage

client = OpenAI()

print("=== OpenAI Responses API — Web Search (Built-in Tool) ===\n")

response = client.responses.create(
    model="gpt-4o-mini",
    tools=[{"type": "web_search_preview"}],
    input="What were the top AI announcements this week?",
)

print(f"Response: {response.output_text}")
print_openai_usage(response)
