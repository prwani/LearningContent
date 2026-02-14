"""Level 10 — Decision Tree: Interactive CLI to recommend which API to use.

Walks through a series of questions and recommends the best
API/provider combination based on the use case.
"""
import sys

DECISION_TREE = {
    "start": {
        "question": "Do you need tool/function calling?",
        "yes": "tools_type",
        "no": "stateful_needed",
    },
    "stateful_needed": {
        "question": "Do you need multi-turn stateful conversations (server-managed history)?",
        "yes": "recommend_responses_api",
        "no": "recommend_basic",
    },
    "tools_type": {
        "question": "Do you need built-in tools (web search, code execution, computer use)?",
        "yes": "builtin_type",
        "no": "custom_tools_count",
    },
    "builtin_type": {
        "question": "Do you need computer/desktop automation?",
        "yes": "recommend_anthropic_computer",
        "no": "recommend_responses_builtin",
    },
    "custom_tools_count": {
        "question": "Do you have more than 20 custom tools?",
        "yes": "tool_discovery",
        "no": "recommend_either_tools",
    },
    "tool_discovery": {
        "question": "Do you want automatic tool search/discovery (reduce context)?",
        "yes": "recommend_anthropic_tool_search",
        "no": "recommend_openai_meta_registry",
    },
    # --- Leaf nodes (recommendations) ---
    "recommend_basic": {
        "recommendation": True,
        "api": "Either provider works",
        "details": [
            "OpenAI: Chat Completions API (gpt-4o-mini) — simplest, widely used",
            "Anthropic: Messages API (claude-sonnet-4) — required max_tokens, parsed content blocks",
            "Tip: Use OpenAI for lowest cost; Anthropic for strongest instruction-following",
        ],
    },
    "recommend_responses_api": {
        "recommendation": True,
        "api": "OpenAI Responses API",
        "details": [
            "Use previous_response_id for server-side state (no history resending)",
            "Automatic prompt caching for repeated prefixes (~50% savings)",
            "Set store: true to persist conversation",
        ],
    },
    "recommend_responses_builtin": {
        "recommendation": True,
        "api": "OpenAI Responses API (built-in tools)",
        "details": [
            "web_search_preview — real-time web search",
            "code_interpreter — Python sandbox",
            "file_search — vector store document search",
            "No agentic loop needed — tools execute server-side",
        ],
    },
    "recommend_anthropic_computer": {
        "recommendation": True,
        "api": "Anthropic Messages API (computer_use)",
        "details": [
            "computer_20250124 — desktop screenshot + click automation",
            "bash_20250124 — shell execution relay",
            "text_editor_20250124 — file operations",
            "Requires client-side relay for tool execution",
        ],
    },
    "recommend_either_tools": {
        "recommendation": True,
        "api": "Either provider (function calling)",
        "details": [
            "OpenAI: tools[] with type:'function', args returned as JSON strings (need parsing)",
            "Anthropic: tools[] with input_schema, args returned as parsed objects",
            "OpenAI Responses API: previous_response_id chains tool results",
        ],
    },
    "recommend_anthropic_tool_search": {
        "recommendation": True,
        "api": "Anthropic Messages API (tool_search + defer_loading)",
        "details": [
            "tool_search_20250522 — model discovers tools on demand",
            "defer_loading: true — strips tool schemas from initial context",
            "85% context reduction (55K → 8.7K tokens for 50+ tools)",
            "Alternative: programmatic tool calling via code_execution sandbox",
        ],
    },
    "recommend_openai_meta_registry": {
        "recommendation": True,
        "api": "OpenAI (Meta-Tool Registry pattern)",
        "details": [
            "3 meta-tools: list_tools(), describe_tool(), run_tool()",
            "Only sends 3 schemas instead of 50+",
            "Model discovers and invokes tools on demand",
            "Combine with Responses API prompt caching for best performance",
        ],
    },
}


def run_decision_tree():
    print("=" * 60)
    print("  API Decision Tree — Choose the Right API for Your Use Case")
    print("=" * 60)
    print()

    node = "start"
    while True:
        data = DECISION_TREE[node]

        if data.get("recommendation"):
            print(f"\n{'='*60}")
            print(f"  ✅ Recommendation: {data['api']}")
            print(f"{'='*60}")
            for detail in data["details"]:
                print(f"  • {detail}")
            print()
            break

        print(f"  Q: {data['question']}")
        answer = input("  Your answer (yes/no): ").strip().lower()
        if answer in ("y", "yes"):
            node = data["yes"]
        elif answer in ("n", "no"):
            node = data["no"]
        else:
            print("  Please answer 'yes' or 'no'.")
            continue
        print()


if __name__ == "__main__":
    run_decision_tree()
