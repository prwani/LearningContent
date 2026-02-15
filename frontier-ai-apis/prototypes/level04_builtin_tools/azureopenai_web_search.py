"""Level 4 — Azure OpenAI Responses API: Web Search (built-in tool, 3+ turns).

Uses web_search_preview built-in tool with follow-up questions
for a multi-turn research conversation.
Env: AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY, AZURE_OPENAI_DEPLOYMENT
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv; load_dotenv()
from openai import AzureOpenAI
from _common.token_utils import print_openai_usage, check_env_keys


# Note: Azure OpenAI Responses API requires api_version="2024-12-01-preview" or later.
# Note: Built-in tools (web_search, code_interpreter, container) availability varies by Azure OpenAI region and model.
check_env_keys()
client = AzureOpenAI(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    api_version="2024-12-01-preview",
)

print("=== Azure OpenAI Responses API — Web Search (3+ turns) ===\n")

queries = [
    "What are the latest breakthroughs in quantum computing this year?",
    "Which companies are leading in quantum computing research?",
    "What are the practical applications expected in the next 5 years?",
]

previous_id = None
for i, query in enumerate(queries, 1):
    kwargs = {
        "model": "gpt-4o-mini",
        "tools": [{"type": "web_search_preview"}],
        "input": query,
        "store": True,
    }
    if previous_id:
        kwargs["previous_response_id"] = previous_id

    response = client.responses.create(**kwargs)
    previous_id = response.id

    print(f"--- Turn {i} ---")
    print(f"User: {query}")
    print(f"Assistant: {response.output_text[:200]}...")
    print_openai_usage(response, label=f"Turn {i}")
    print()
