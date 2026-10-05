"""
vision_llm.py — Thin, cb-free wrapper around OpenAI and Google Gemini vision APIs.

Model routing
-------------
When the user picks provider "gpt" or "gemini" without specifying a model,
the pipeline defaults to the most capable current model for each provider:

    gpt    -> gpt-5.4
             (also accepts: gpt-6-luna, gpt-6-sol, gpt-5.5,
              gpt-5.2, gpt-5.1, gpt-5, gpt-4o, gpt-4.1)
    gemini → gemini-3.8-flash
             (also accepts: gemini-3.1-pro-preview, gemini-2.5-flash)

GPT-5.x models
--------------
GPT-5 reasoning models support a ``reasoning_effort`` parameter instead of
temperature. This wrapper detects those models and adds the parameter
automatically. Any model name ending in ``-chat-latest`` is accepted but
follows the non-reasoning path instead, matching the main RADIANT-LLM app.
"""

from __future__ import annotations

import base64
import io
import logging
import os
import re
import threading
from typing import List, Literal, Optional

from PIL import Image

logger = logging.getLogger(__name__)

# genai.configure() mutates process-global SDK state (unlike the GPT/Ollama
# paths, which build a fresh, isolated client object per call) -- since
# figure_describer.py added real thread concurrency, multiple workers could
# call it at once. In practice every concurrent call in this codebase uses
# the same api_key, so the race is benign today, but this lock removes it
# outright rather than relying on that happening to stay true. Only the
# configure+model-construction step is guarded; the slow generate_content()
# call itself runs outside the lock so concurrent Gemini calls still overlap.
_gemini_configure_lock = threading.Lock()

DetailLevel = Literal["low", "high", "auto"]
ReasoningEffort = Literal["minimal", "none", "low", "medium", "high", "xhigh"]

# GPT-family models with explicit reasoning_effort support -- kept for the
# per-model *allowed values* lookup below, not for detecting whether a model
# is reasoning-capable at all (see _GPT_REASONING_FAMILY_PREFIX for that).
_GPT_REASONING_MODELS = {"gpt-5", "gpt-5.1", "gpt-5.2", "gpt-5.4", "gpt-5.5"}

# Whole-family fallback: any gpt-5-and-up model not ending in "-chat-latest"
# is treated as reasoning-capable (no temperature param sent), the same
# "family, not individual ids" principle model_catalog.py's o-series prefix
# already uses. Without this, a real, live-listed model like gpt-5.6 (not in
# _GPT_REASONING_MODELS above, since that set predates its release) silently
# fell through to the "older models" branch and got sent temperature=0 --
# confirmed via a live 400: "temperature does not support 0 with this model.
# Only the default (1) value is supported."
_GPT_REASONING_FAMILY_PREFIX = re.compile(r"^gpt-([5-9]|\d{2,})(\.\d+)?(-|$)")

# Default reasoning_effort values offered to a reasoning-capable model this
# wrapper doesn't have an explicit entry for below, rather than silently
# dropping the parameter for every new release -- the union of every known
# generation's allowed set; "medium" (the CLI's own default) is valid in all
# of them, including gpt-5's narrower one.
_GPT_REASONING_EFFORT_DEFAULT = {"none", "low", "medium", "high", "xhigh"}

_GPT_REASONING_EFFORT_OPTIONS = {
    "gpt-5": {"minimal", "low", "medium", "high"},
    "gpt-5.1": {"none", "low", "medium", "high"},
    "gpt-5.2": {"none", "low", "medium", "high", "xhigh"},
    "gpt-5.4": {"none", "low", "medium", "high", "xhigh"},
    "gpt-5.5": {"none", "low", "medium", "high", "xhigh"},
}

# Latest default model per provider
LATEST_GPT_MODEL    = "gpt-5.4"
LATEST_GEMINI_MODEL = "gemini-3.8-flash"


def _supports_reasoning_effort(model: str) -> bool:
    """Return True when *model* supports reasoning_effort in this wrapper."""
    lowered = model.lower()
    if lowered.endswith("-chat-latest"):
        return False
    return lowered in _GPT_REASONING_MODELS or bool(_GPT_REASONING_FAMILY_PREFIX.match(lowered))


def _is_gpt5_chat_latest(model: str) -> bool:
    """Return True for accepted GPT-5-era models without reasoning_effort support."""
    return model.lower().endswith("-chat-latest")


def _normalize_reasoning_effort(
    model: str,
    reasoning_effort: Optional[ReasoningEffort],
) -> Optional[str]:
    """
    Keep supported reasoning-effort values only for models that accept them.
    """
    if not reasoning_effort:
        return None

    normalized_model = model.lower()
    normalized_effort = reasoning_effort.lower()
    allowed = _GPT_REASONING_EFFORT_OPTIONS.get(normalized_model)
    if allowed is None:
        # Unrecognized but reasoning-capable per _supports_reasoning_effort()
        # (e.g. a newer release like gpt-5.6) -- fall back to the broadest
        # known-valid set instead of silently dropping the parameter.
        allowed = _GPT_REASONING_EFFORT_DEFAULT
    if normalized_effort in allowed:
        return normalized_effort

    logger.warning(
        "Ignoring unsupported reasoning_effort=%s for model=%s. Allowed: %s",
        reasoning_effort,
        model,
        ", ".join(sorted(allowed)),
    )
    return None


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

def _build_image_content(images: List[bytes], prompt: str, detail: DetailLevel = "low") -> list:
    """
    Build the multimodal ``content`` list (text block + one image_url block
    per image) shared by the GPT and Ollama call paths -- both talk to an
    OpenAI-compatible chat.completions endpoint, just with different base_url.
    """
    content: list = [{"type": "text", "text": prompt}]
    for img_bytes in images:
        b64 = base64.b64encode(img_bytes).decode("ascii")
        content.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/png;base64,{b64}",
                "detail": detail,
            },
        })
    return content


# ---------------------------------------------------------------------------
# OpenAI / GPT
# ---------------------------------------------------------------------------

def call_vision_llm_gpt(
    images: List[bytes],
    prompt: str,
    api_key: str,
    model: str = LATEST_GPT_MODEL,
    detail: DetailLevel = "low",
    reasoning_effort: Optional[ReasoningEffort] = "medium",
) -> str:
    """
    Send *images* (PNG bytes) and *prompt* to an OpenAI vision model.

    For supported GPT-5 reasoning models, the ``reasoning_effort`` parameter
    is passed to the API instead of temperature. Any model name ending in
    ``-chat-latest`` is accepted without ``reasoning_effort``.

    Args:
        images:           List of raw PNG byte strings.
        prompt:           Text instruction for the model.
        api_key:          OpenAI API key.
        model:            Vision-capable model name.
        detail:           Image resolution hint ('low', 'high', or 'auto').
        reasoning_effort: Reasoning depth for supported GPT-5.x models.
                          Ignored for models ending in -chat-latest and
                          older models such as gpt-4o and gpt-4.1.

    Returns:
        Model response as a plain string.
    """
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise RuntimeError("openai package not installed. Run: pip install openai") from exc

    if not api_key:
        raise RuntimeError("OpenAI API key is not set.")

    # api_key already carries whichever key config.py resolved (OPENAI_API_KEY
    # or Portkey's) -- resolve_openai_connection() here is only to pick up the
    # matching base_url/model_prefix, since it's a pure/cheap env-var read.
    from visual_parser.openai_gateway import resolve_openai_connection, prefixed_model
    _conn = resolve_openai_connection()
    client = OpenAI(api_key=api_key, base_url=_conn["base_url"])

    content = _build_image_content(images, prompt, detail)

    # Build API call kwargs. model_prefix (if any) is applied only here, not
    # to `model` itself -- every capability check above/below must keep
    # matching on the bare model name.
    call_kwargs: dict = {
        "model":    prefixed_model(_conn, model),
        "messages": [{"role": "user", "content": content}],
    }

    if _supports_reasoning_effort(model):
        # GPT-5 reasoning models: use reasoning_effort; temperature is not supported.
        normalized_effort = _normalize_reasoning_effort(model, reasoning_effort)
        if normalized_effort:
            call_kwargs["reasoning_effort"] = normalized_effort
        logger.info("[GPT-5 reasoning] Using model=%s reasoning_effort=%s", model, normalized_effort)
    elif _is_gpt5_chat_latest(model):
        # Keep parity with the main RADIANT-LLM app for "-chat-latest" models.
        call_kwargs["temperature"] = 1.0
        logger.info("[GPT-5 chat-latest] Using model=%s temperature=1.0", model)
    else:
        # Older models: standard temperature
        call_kwargs["temperature"] = 0

    try:
        response = client.chat.completions.create(**call_kwargs)
        return response.choices[0].message.content.strip()
    except Exception as exc:
        raise RuntimeError(f"OpenAI vision call failed (model={model}): {exc}") from exc


# ---------------------------------------------------------------------------
# Google Gemini
# ---------------------------------------------------------------------------

def call_vision_llm_gemini(
    images: List[bytes],
    prompt: str,
    api_key: str,
    model: str = LATEST_GEMINI_MODEL,
) -> str:
    """
    Send *images* (PNG bytes) and *prompt* to a Google Gemini vision model.

    Args:
        images:  List of raw PNG byte strings.
        prompt:  Text instruction for the model.
        api_key: Gemini API key.
        model:   Gemini model name.

    Returns:
        Model response as a plain string.
    """
    try:
        import google.generativeai as genai
    except ImportError as exc:
        raise RuntimeError(
            "google-generativeai package not installed. "
            "Run: pip install google-generativeai"
        ) from exc

    if not api_key:
        raise RuntimeError("Gemini API key is not set.")

    with _gemini_configure_lock:
        genai.configure(api_key=api_key)
        vision_model = genai.GenerativeModel(model)

    pil_images = [Image.open(io.BytesIO(b)).convert("RGB") for b in images]
    logger.info("[GEMINI] Using model=%s", model)

    try:
        response = vision_model.generate_content([prompt] + pil_images)
        return response.text
    except Exception as exc:
        raise RuntimeError(f"Gemini vision call failed (model={model}): {exc}") from exc


# ---------------------------------------------------------------------------
# Local Ollama
# ---------------------------------------------------------------------------

def call_vision_llm_ollama(
    images: List[bytes],
    prompt: str,
    model: str,
    detail: DetailLevel = "low",
    timeout_seconds: Optional[float] = None,
) -> str:
    """
    Send *images* (PNG bytes) and *prompt* to a local vision-capable model
    served by Ollama, via its OpenAI-compatible endpoint. No API key needed --
    Ollama ignores the dummy key the OpenAI client still requires to be
    non-empty (same convention as RADIANT-LLM's build_ollama_chat_openai()).
    No reasoning_effort/``-chat-latest`` handling here -- that's GPT-5.x
    model-family logic, not relevant to a locally-served model.

    Args:
        images:          List of raw PNG byte strings.
        prompt:          Text instruction for the model.
        model:           Ollama model tag (e.g. "qwen2.5-vl:32b").
        detail:          Image detail hint forwarded in the image_url block,
                         same as the GPT path -- whether a given
                         Ollama-served model honors it is up to that
                         model/Ollama's own handling, not this wrapper.
        timeout_seconds: Explicit override. When None (default), falls back
                         to the context-window-scaled formula below, which
                         was calibrated for figure_describer.py's bounded,
                         structured FIGURE_PROMPT output -- callers whose
                         prompt can demand much longer generation (e.g.
                         image_describer.py's verbatim full-text
                         transcription requirement) should pass their own
                         value rather than rely on that formula.

    Returns:
        Model response as a plain string.
    """
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise RuntimeError("openai package not installed. Run: pip install openai") from exc

    from visual_parser.ollama_local import resolve_ollama_base_url
    base_url = resolve_ollama_base_url()
    if not base_url:
        raise RuntimeError(
            "Ollama is not reachable (checked OLLAMA_BASE_URL, localhost:11434, "
            "and host.docker.internal:11434). Is it running?"
        )

    if timeout_seconds is None:
        # Local CPU-bound inference has no SLA the way cloud APIs do, so the
        # SDK's cloud-oriented 600s default doesn't fit here. Scale with image
        # count -- more context pages means proportionally more vision-
        # encoding + generation work: 10 min for a single image, +2.5 min per
        # additional image (15 min at the 3-image case from
        # --vision-context-pages 1).
        timeout_seconds = 600.0 + (len(images) - 1) * 150.0
    client = OpenAI(api_key="ollama", base_url=base_url, timeout=timeout_seconds)
    content = _build_image_content(images, prompt, detail)

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": content}],
        )
        return response.choices[0].message.content.strip()
    except Exception as exc:
        raise RuntimeError(f"Ollama vision call failed (model={model}): {exc}") from exc


# ---------------------------------------------------------------------------
# Unified dispatcher
# ---------------------------------------------------------------------------

def call_vision_llm(
    images: List[bytes],
    prompt: str,
    provider: str,
    api_key: str,
    model: str,
    detail: DetailLevel = "low",
    reasoning_effort: Optional[ReasoningEffort] = "medium",
    ollama_timeout_seconds: Optional[float] = None,
) -> str:
    """
    Unified vision-LLM dispatcher.

    Automatically routes to the correct provider backend.  When *model* is
    empty or None, falls back to the latest default for that provider.

    Args:
        images:                 List of raw PNG byte strings.
        prompt:                 Text instruction for the model.
        provider:               ``'gpt'``, ``'gemini'``, or ``'ollama'``.
        api_key:                API key for the chosen provider (unused for ollama).
        model:                  Model name string.
        detail:                 Image detail level. Forwarded to GPT and
                                Ollama; ignored for Gemini (no equivalent in
                                its API).
        reasoning_effort:       Reasoning depth for GPT-5.x (ignored for
                                older GPT models and all Gemini/Ollama models).
        ollama_timeout_seconds: Forwarded to call_vision_llm_ollama's own
                                timeout_seconds override (ignored for gpt/
                                gemini -- cloud APIs are reliably fast, this
                                isn't their problem). See that function's
                                docstring for why this needs to be settable
                                per caller rather than always using its
                                built-in context-window-scaled formula.

    Returns:
        Model response as a plain string.
    """
    if model:
        resolved_model = model
    elif provider == "gpt":
        resolved_model = LATEST_GPT_MODEL
    elif provider == "gemini":
        resolved_model = LATEST_GEMINI_MODEL
    elif provider == "ollama":
        # No static default makes sense for "ollama" -- local availability is
        # machine-specific. Callers should resolve a model via
        # ollama_local.select_best_vision_model() before reaching here.
        raise RuntimeError(
            "No vision model specified for provider='ollama'. Call "
            "ollama_local.select_best_vision_model() first, or pass an explicit model."
        )
    else:
        raise RuntimeError(
            f"Unknown vision provider: {provider!r}. Must be 'gpt', 'gemini', or 'ollama'."
        )

    if provider == "gpt":
        return call_vision_llm_gpt(
            images, prompt, api_key,
            model=resolved_model,
            detail=detail,
            reasoning_effort=reasoning_effort,
        )
    if provider == "gemini":
        return call_vision_llm_gemini(images, prompt, api_key, model=resolved_model)
    if provider == "ollama":
        return call_vision_llm_ollama(
            images, prompt, model=resolved_model, detail=detail,
            timeout_seconds=ollama_timeout_seconds,
        )

    raise RuntimeError(
        f"Unknown vision provider: {provider!r}. Must be 'gpt', 'gemini', or 'ollama'."
    )
