"""Shared token-usage helpers for OpenAI and Anthropic API responses."""

import os

def check_env_keys():
    """Print which API keys are configured."""
    keys = {
        "OPENAI_API_KEY": bool(os.environ.get("OPENAI_API_KEY")),
        "ANTHROPIC_API_KEY": bool(os.environ.get("ANTHROPIC_API_KEY")),
    }
    print("Environment:")
    for k, v in keys.items():
        print(f"  {k}: {'✓ set' if v else '✗ NOT SET'}")
    print()
    return keys


def print_openai_usage(response, label=""):
    """Print token usage from an OpenAI ChatCompletion or Response object."""
    prefix = f"[{label}] " if label else ""
    usage = getattr(response, "usage", None)
    if not usage:
        print(f"{prefix}Token usage: not available")
        return
    print(f"\n{prefix}Token Usage:")
    print(f"  Input tokens:  {usage.prompt_tokens}")
    print(f"  Output tokens: {usage.completion_tokens}")
    print(f"  Total tokens:  {usage.total_tokens}")
    # Cached tokens (available in newer models / Responses API)
    details = getattr(usage, "prompt_tokens_details", None)
    if details:
        cached = getattr(details, "cached_tokens", 0) or 0
        print(f"  Cached input:  {cached}")


def print_anthropic_usage(response, label=""):
    """Print token usage from an Anthropic Messages response."""
    prefix = f"[{label}] " if label else ""
    usage = getattr(response, "usage", None)
    if not usage:
        print(f"{prefix}Token usage: not available")
        return
    print(f"\n{prefix}Token Usage:")
    print(f"  Input tokens:  {usage.input_tokens}")
    print(f"  Output tokens: {usage.output_tokens}")
    cache_create = getattr(usage, "cache_creation_input_tokens", 0) or 0
    cache_read = getattr(usage, "cache_read_input_tokens", 0) or 0
    if cache_create or cache_read:
        print(f"  Cache created:  {cache_create}")
        print(f"  Cache read:     {cache_read}")
