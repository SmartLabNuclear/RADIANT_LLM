"""
model_catalog.py — Live OpenAI/Gemini vision-model catalogs for visual-parser.

Same philosophy as the equivalent module in AutoSAM/RADIANT-LLM: instead of a
hardcoded model list in --help text that silently goes stale, ask each
provider what's actually usable right now via its own model-listing endpoint.
Ported and trimmed for this standalone package -- no Ollama/Grace-vLLM local
model support here, since visual-parser only ever calls a cloud vision LLM
(--vision-provider {gpt,gemini}), never a local/self-hosted one.
"""

from __future__ import annotations

import re
import time
from dataclasses import dataclass, field
from typing import Dict, Optional, Tuple

import openai
import google.generativeai as genai

_CATALOG_TTL_SECONDS = 3600  # process-lifetime-ish cache; --list-models always force-refreshes

# Name-fragment heuristics for excluding non-chat/non-vision models from a
# provider's raw catalog (embeddings, TTS, image/audio generation, moderation,
# realtime/live voice API, legacy pre-chat completion models). Neither
# provider's listing endpoint reliably flags "chat-capable" as a single
# structured field -- this is a pragmatic filter, not a perfect one.
_NON_CHAT_NAME_FRAGMENTS: Tuple[str, ...] = (
    "embedding", "whisper", "tts", "audio", "image", "vision-preview",
    "transcribe", "moderation", "dall-e", "davinci", "babbage", "ada",
    "curie", "search", "similarity", "edit", "realtime", "computer-use",
    "instruct", "sora", "lyria", "robotics",
    # A real "gpt-live-1" slipped through an earlier version of this filter
    # in AutoSAM/RADIANT-LLM and reached a user: listed by /v1/models,
    # picked from a dropdown, rejected with a genuine 404 ("This is not a
    # chat model... Did you mean to use v1/completions?"). Same conceptual
    # family "realtime" above already excludes -- just a different exact
    # branding term.
    "live",
)

# Dated/pinned-snapshot suffix, e.g. "gpt-4.1-2025-04-14" or "gpt-4-0613" --
# these are exact-pinned duplicates of an already-listed rolling alias.
_DATED_SNAPSHOT_SUFFIX = re.compile(r"-(\d{4}-\d{2}-\d{2}|\d{3,4})$")

_MODEL_VERSION_RE = re.compile(r"^gpt-(\d+(?:\.\d+)?)")


def _model_version_sort_key(model_id: str) -> Tuple[float, str]:
    match = _MODEL_VERSION_RE.match(model_id)
    version = float(match.group(1)) if match else -1.0
    return (version, model_id)


_OPENAI_O_SERIES_PREFIX = re.compile(r"^o\d")

# Explicitly excluded despite being genuinely chat-capable -- same list
# AutoSAM/RADIANT-LLM maintain for the same underlying reason, since this
# package's vision_llm.py calls the same client.chat.completions.create(...)
# endpoint they do:
#   - gpt-6-astra requires the OpenAI Responses API instead, which this
#     package doesn't call.
#   - chat-latest is returned by /v1/models (owned_by="system") but absent
#     from OpenAI's own documented model list -- unclear provenance.
#   - The rest are confirmed via live testing (real 404s) to be listed but
#     dead: two unresolvable "-latest" rolling-alias tags and several
#     deprecated dated preview snapshots / the legacy 32k-context variant.
_EXPLICITLY_EXCLUDED_MODEL_IDS: Tuple[str, ...] = (
    "gpt-6-astra",
    "chat-latest",
    "chatgpt-4o-latest",
    "gpt-4o-latest",
    "gpt-4-0125-preview",
    "gpt-4-1106-preview",
    "gpt-4-turbo-preview",
    "gpt-4-32k",
)


def _looks_chat_capable(model_id: str) -> bool:
    lowered = model_id.lower()
    if any(fragment in lowered for fragment in _NON_CHAT_NAME_FRAGMENTS):
        return False
    if _DATED_SNAPSHOT_SUFFIX.search(model_id):
        return False
    return True


@dataclass
class _Cache:
    models: Dict[str, str] = field(default_factory=dict)  # id -> display label
    fetched_at: float = 0.0
    error: Optional[str] = None


_openai_cache = _Cache()
_gemini_cache = _Cache()


def list_openai_models(
    api_key: Optional[str],
    base_url: Optional[str] = None,
    model_prefix: str = "",
    force_refresh: bool = False,
) -> Dict[str, str]:
    """Live OpenAI vision-capable model catalog: {id: label}. Fails soft (empty dict) on error.

    base_url/model_prefix let this transparently go through Portkey instead of
    OpenAI directly (see openai_gateway.py). Portkey's .models.list() returns
    ids already carrying the "@<slug>/" prefix -- stripped below so callers
    always get bare model ids, same as the direct-OpenAI path.
    """
    if not force_refresh and _openai_cache.models and (
        time.time() - _openai_cache.fetched_at < _CATALOG_TTL_SECONDS
    ):
        return _openai_cache.models
    if not api_key:
        return {}
    try:
        client = openai.Client(api_key=api_key, base_url=base_url)
        resp = client.models.list()
        has_real_timestamps = any(m.created for m in resp.data)
        if has_real_timestamps:
            candidates = sorted(resp.data, key=lambda m: m.created or 0, reverse=True)
        else:
            candidates = sorted(
                resp.data,
                key=lambda m: _model_version_sort_key(
                    m.id[len(model_prefix):] if model_prefix and m.id.startswith(model_prefix) else m.id
                ),
                reverse=True,
            )
        models = {}
        for m in candidates:
            bare_id = m.id[len(model_prefix):] if model_prefix and m.id.startswith(model_prefix) else m.id
            # gpt-3.x is two full generations behind the current lineup.
            if (
                _looks_chat_capable(bare_id)
                and not bare_id.startswith("gpt-3")
                and "codex" not in bare_id
                and not _OPENAI_O_SERIES_PREFIX.match(bare_id)
                and bare_id not in _EXPLICITLY_EXCLUDED_MODEL_IDS
                and not bare_id.endswith("-pro")
                and not bare_id.endswith("-chat-latest")
            ):
                models[bare_id] = f"{bare_id}-augmented"
        _openai_cache.models = models
        _openai_cache.fetched_at = time.time()
        _openai_cache.error = None
        return models
    except Exception as exc:
        _openai_cache.error = str(exc)
        return _openai_cache.models  # serve stale cache over nothing, if we have one


def list_gemini_models(api_key: Optional[str], force_refresh: bool = False) -> Dict[str, str]:
    """Live Gemini vision-capable model catalog: {id: label}. Fails soft (empty dict) on error.

    Unlike AutoSAM/RADIANT-LLM's chat-agent catalog, this does NOT restrict to
    gemini-3.x and up -- visual-parser's own documented --vision-model range
    already includes gemini-2.5-flash and gemini-3.1-pro-preview as valid choices.
    """
    if not force_refresh and _gemini_cache.models and (
        time.time() - _gemini_cache.fetched_at < _CATALOG_TTL_SECONDS
    ):
        return _gemini_cache.models
    if not api_key:
        return {}
    try:
        genai.configure(api_key=api_key)
        candidates = list(genai.list_models())[::-1]  # best-effort newest-first
        models: Dict[str, str] = {}
        for m in candidates:
            if "generateContent" not in m.supported_generation_methods:
                continue
            short_id = m.name.split("/", 1)[-1]  # "models/gemini-3.8-flash" -> "gemini-3.8-flash"
            if not _looks_chat_capable(short_id):
                continue
            if "omni" in short_id:
                continue
            models[short_id] = f"{short_id}-augmented"
        _gemini_cache.models = models
        _gemini_cache.fetched_at = time.time()
        _gemini_cache.error = None
        return models
    except Exception as exc:
        _gemini_cache.error = str(exc)
        return _gemini_cache.models
