# Frontier AI APIs — Working Python Prototypes

Hands-on Python demos for every level of the Frontier AI APIs curriculum.
Each script is self-contained and prints **token usage** (input, output, cached) for every API call.

## Quick Start

```bash
# 1. Install dependencies
pip install -r _common/requirements.txt

# 2. Set API keys
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."

# 3. Run any demo
python level01_basics/openai_chat_completion.py
```

## Levels

| Level | Directory | Scripts | What You Learn |
|-------|-----------|---------|----------------|
| 1 | `level01_basics/` | `openai_chat_completion.py`, `openai_responses_api.py`, `anthropic_messages.py` | Single-turn: Chat Completions vs Responses API vs Messages API |
| 2 | `level02_multi_turn/` | `openai_chat_multi_turn.py`, `openai_responses_stateful.py`, `anthropic_messages_multi_turn.py` | Multi-turn: stateless history, stateful `previous_response_id`, prompt caching |
| 3 | `level03_function_calling/` | `openai_function_calling.py`, `openai_responses_function.py`, `anthropic_tool_use.py`, **`claude_agent_sdk_tools.py`** | Function calling (3+ turns): tool definitions, arg parsing, **Agent SDK tool loop** |
| 4 | `level04_builtin_tools/` | `openai_chat_builtin_tools.py`, `openai_web_search.py`, `openai_code_interpreter.py`, `anthropic_code_execution.py`, **`claude_agent_sdk_tools.py`** | Built-in tools (3+ turns): web search, code interpreter, **Agent SDK built-in tools** |
| 5 | `level05_tool_discovery/` | `openai_meta_tool_registry.py`, `openai_responses_tool_discovery.py`, `anthropic_tool_search.py`, **`claude_agent_sdk_discovery.py`** | Scaling 50+ tools (3+ turns): meta-tool registry, defer_loading, **Agent SDK MCP discovery** |
| 6 | `level06_agents/` | `openai_agentic_loop.py`, `anthropic_agentic_loop.py`, **`claude_agent_sdk_agent.py`** | Agentic loops + structured output (3+ turns), **Agent SDK autonomous agent** |
| 7 | `level07_skills/` | `skill_template_demo.py`, `openai_chat_skills.py`, `openai_shell_tool.py`, `anthropic_messages_skills.py`, **`claude_agent_sdk_skills.py`** | SKILL.md standard (3+ turns), skills + tools, **Agent SDK skills** |
| 8 | `level08_full_stack/` | `openai_full_agent.py`, `anthropic_full_agent.py`, **`claude_agent_sdk_full.py`** | Full stack: skills + tools + MCP (3+ turns), **Agent SDK full stack** |
| 9 | `level09_plugins/` | `plugin_loader.py`, `openai_plugin_pattern.py`, `azureopenai_plugin_pattern.py`, `anthropic_plugin_demo.py`, **`claude_agent_sdk_plugin.py`** | Plugin architecture (3+ turns): manifest parsing, MCP routing, **Agent SDK plugins** |
| 10 | `level10_reference/` | `unified_api_demo.py`, `decision_tree.py`, **`agent_sdk_comparison.py`** | Side-by-side comparison (OpenAI + Azure + Anthropic), decision tree, **Messages API vs Agent SDK** |

## API Coverage per Level

Every level includes examples for all five approaches:

| Approach | Package | Levels |
|----------|---------|--------|
| **OpenAI Chat Completions** | `openai` | 1-10 |
| **OpenAI Responses API** | `openai` | 1-10 |
| **Azure OpenAI Chat Completions** | `openai` (AzureOpenAI) | 1-10 |
| **Azure OpenAI Responses API** | `openai` (AzureOpenAI) | 1-10 |
| **Anthropic Messages API** | `anthropic` | 1-10 |
| **Claude Agent SDK** | `claude-agent-sdk` | 3-10 |

## MCP Servers (from [toolscout](https://github.com/prwani/toolscout))

Three sample MCP servers are included for demos that need external tools:

| Server | Port | Domain | Tools |
|--------|------|--------|-------|
| `server1.py` | 8000 | General | Users, weather, email, restaurant, calendar, etc. (25 tools) |
| `server2.py` | 9000 | Library | Books, members, lending, overdue tracking (12 tools) |
| `server3.py` | 10000 | Stocks | Buy/sell, portfolio, watchlist, market status (15 tools) |

```bash
# Start all MCP servers (needed for levels 5, 8, 9)
cd mcp_servers && bash start_servers.sh
```

## Environment Variables

| Variable | Required For | Description |
|----------|-------------|-------------|
| `OPENAI_API_KEY` | All OpenAI demos | OpenAI API key |
| `AZURE_OPENAI_ENDPOINT` | All Azure OpenAI demos | Azure OpenAI endpoint URL |
| `AZURE_OPENAI_API_KEY` | All Azure OpenAI demos | Azure OpenAI API key |
| `AZURE_OPENAI_DEPLOYMENT` | All Azure OpenAI demos | Model deployment name (defaults to `gpt-4o-mini`) |
| `ANTHROPIC_API_KEY` | All Anthropic + Agent SDK demos | Anthropic API key |

## Token Usage

Every script prints token usage after each API call:

```
Environment:
  OPENAI_API_KEY: ✓ set
  ANTHROPIC_API_KEY: ✓ set

Token Usage:
  Input tokens:  42
  Output tokens: 128
  Total tokens:  170
  Cached input:  0
```

## Multi-Turn Conversations

Level 3 onwards, every example involves **3+ turns** to demonstrate:
- Multi-step tool calling (e.g., weather for 3 cities)
- Iterative refinement (e.g., build on previous code results)
- Conversational context (e.g., follow-up questions using prior answers)
