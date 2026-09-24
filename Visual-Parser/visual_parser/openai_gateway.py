"""
Centralized OpenAI-compatible connection resolution.

Lets visual-parser's OpenAI-family calls (vision LLM, the model-catalog
fetch) transparently route through a Portkey gateway instead of OpenAI
directly, by setting PORTKEY_API_KEY + PORTKEY_OPENAI_PROVIDER_SLUG in .env
instead of OPENAI_API_KEY. OPENAI_API_KEY always takes precedence when set --
Portkey is only used as a fallback when it's absent, so an existing working
OpenAI setup never changes behavior just because a Portkey key also happens
to be present.

Ported from AutoSAM/RADIANT-LLM's utils/openai_gateway.py -- same
api_key/base_url swap works for raw openai.OpenAI/openai.Client (including
.models.list()), no separate SDK needed. One wrinkle: Portkey's
.models.list() returns model ids already prefixed with "@<slug>/" -- see
model_catalog.py's list_openai_models(), which strips that prefix back off
so the rest of this package keeps working with bare model names throughout.
The prefix is re-applied only at the point an actual client/request is
constructed, via prefixed_model() below -- it should never be stored on
ParserConfig.gpt_vision_model or written to any output JSONL.
"""

import os
from typing import Optional, TypedDict

PORTKEY_BASE_URL = "https://api.portkey.ai/v1"


class OpenAIConnection(TypedDict):
    api_key: str
    base_url: Optional[str]
    model_prefix: str


def resolve_openai_connection() -> OpenAIConnection:
    """
    Returns connection kwargs for constructing any OpenAI-compatible client.

    Callers should already guard on `if not conn["api_key"]:` the same way
    they previously guarded on `if not openai_api_key:` -- an empty api_key
    here means neither OPENAI_API_KEY nor a valid Portkey configuration is set.
    """
    # Explicit escape hatch: on a machine where OPENAI_API_KEY is also set at
    # the OS/system level (outside any .env file), commenting it out of .env
    # alone can't disable it, since that system-level value is still
    # inherited by the process. Setting this forces Portkey regardless,
    # without touching system state.
    force_portkey = os.getenv("VISUAL_PARSER_FORCE_PORTKEY", "").strip().lower() in ("1", "true", "yes")

    openai_key = os.getenv("OPENAI_API_KEY", "").strip()
    if openai_key and not force_portkey:
        return {"api_key": openai_key, "base_url": None, "model_prefix": ""}

    portkey_key = os.getenv("PORTKEY_API_KEY", "").strip()
    if portkey_key:
        provider_slug = os.getenv("PORTKEY_OPENAI_PROVIDER_SLUG", "").strip()
        if not provider_slug:
            raise RuntimeError(
                "PORTKEY_API_KEY is set but PORTKEY_OPENAI_PROVIDER_SLUG is missing -- "
                "set it to your Portkey AI Provider slug (e.g. 'myworkspace-openai-abc123'), "
                "found on your Portkey integration's detail page."
            )
        return {
            "api_key": portkey_key,
            "base_url": PORTKEY_BASE_URL,
            "model_prefix": f"@{provider_slug}/",
        }

    return {"api_key": "", "base_url": None, "model_prefix": ""}


def prefixed_model(conn: OpenAIConnection, model: str) -> str:
    """Apply conn's Portkey prefix (if any) to a bare OpenAI model name."""
    return f"{conn['model_prefix']}{model}"


def strip_model_prefix(conn: OpenAIConnection, model_id: str) -> str:
    """Inverse of prefixed_model() -- used when a provider (Portkey) hands
    back model ids that already carry the prefix, so callers can normalize
    back to bare names before doing any name-based filtering/matching."""
    prefix = conn["model_prefix"]
    if prefix and model_id.startswith(prefix):
        return model_id[len(prefix):]
    return model_id
