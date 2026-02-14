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
| 1 | `level01_basics/` | `openai_chat_completion.py`, `openai_responses_api.py`, `anthropic_messages.py` | Single-turn API calls — Chat Completions vs Responses vs Messages |
| 2 | `level02_multi_turn/` | `openai_chat_multi_turn.py`, `openai_responses_stateful.py`, `anthropic_messages_multi_turn.py` | Multi-turn: stateless history, stateful `previous_response_id`, prompt caching |
| 3 | `level03_function_calling/` | `openai_function_calling.py`, `openai_responses_function.py`, `anthropic_tool_use.py` | Function calling: tool definitions, argument parsing, result handling |
| 4 | `level04_builtin_tools/` | `openai_web_search.py`, `openai_code_interpreter.py`, `anthropic_code_execution.py` | Built-in tools: web search, code interpreter, code execution |
| 5 | `level05_tool_discovery/` | `openai_meta_tool_registry.py`, `anthropic_tool_search.py` | Scaling 50+ tools: meta-tool registry, tool search + defer_loading |
| 6 | `level06_agents/` | `openai_agentic_loop.py`, `anthropic_agentic_loop.py` | Complete agentic loop + structured output |
| 7 | `level07_skills/` | `skill_template_demo.py`, `openai_shell_tool.py` | SKILL.md standard, shell tool containers |
| 8 | `level08_full_stack/` | `openai_full_agent.py`, `anthropic_full_agent.py` | Full stack: skills + tools + MCP + structured output |
| 9 | `level09_plugins/` | `plugin_loader.py`, `anthropic_plugin_demo.py` | Plugin architecture: manifest parsing, MCP routing |
| 10 | `level10_reference/` | `unified_api_demo.py`, `decision_tree.py` | Side-by-side comparison, API decision tree |

## MCP Servers (from [toolscout](https://github.com/prwani/toolscout))

Three sample MCP servers are included for demos that need external tools:

| Server | Port | Domain | Tools |
|--------|------|--------|-------|
| `server1.py` | 8000 | General | Users, weather, email, restaurant, calendar, translate, etc. (25 tools) |
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
| `ANTHROPIC_API_KEY` | All Anthropic demos | Anthropic API key |

## Token Usage

Every script prints token usage after each API call:

```
Token Usage:
  Input tokens:  42
  Output tokens: 128
  Total tokens:  170
  Cached input:  0
```

For Anthropic (with prompt caching):
```
Token Usage:
  Input tokens:  38
  Output tokens: 95
  Cache created:  12
  Cache read:     26
```

## Project Structure

```
prototypes/
├── _common/               # Shared utilities
│   ├── token_utils.py     # print_openai_usage(), print_anthropic_usage()
│   └── requirements.txt   # pip dependencies
├── level01_basics/        # Level 1: Single-turn basics
├── level02_multi_turn/    # Level 2: Multi-turn conversations
├── level03_function_calling/ # Level 3: Function/tool calling
├── level04_builtin_tools/ # Level 4: Built-in tools
├── level05_tool_discovery/ # Level 5: Scaling 50+ tools
├── level06_agents/        # Level 6: Agentic loops
├── level07_skills/        # Level 7: Skills & shell
├── level08_full_stack/    # Level 8: Full agentic stack
├── level09_plugins/       # Level 9: Plugin architecture
├── level10_reference/     # Level 10: Comparison & decision tree
└── mcp_servers/           # MCP servers from toolscout
```
