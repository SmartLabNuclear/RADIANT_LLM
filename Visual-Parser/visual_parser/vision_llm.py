"""
vision_llm.py — Thin, cb-free wrapper around OpenAI and Google Gemini vision APIs.

Model routing
-------------
When the user picks provider "gpt" or "gemini" without specifying a model,
the pipeline defaults to the most capable current model for each provider:

    gpt    -> gpt-5.4
             (also accepts: gpt-5.5, gpt-5.3-chat-latest, gpt-5.2, gpt-5.1,
              gpt-5, gpt-4o, gpt-4.1)
    gemini → gemini-3-pro-preview
             (also accepts: gemini-2.5-flash, gemini-1.5-pro)

GPT-5.x models
--------------
GPT-5 reasoning models support a ``reasoning_effort`` parameter instead of
temperature. This wrapper detects those models and adds the parameter
automatically. ``gpt-5.3-chat-latest`` is accepted, but follows the non-
reasoning path used by the main RADIANT-LLM app.
"""

from __future__ import annotations

import base64
import io
import logging
import os
from typing import List, Literal, Optional

from PIL import Image

logger = logging.getLogger(__name__)

DetailLevel = Literal["low", "high", "auto"]
ReasoningEffort = Literal["minimal", "none", "low", "medium", "high", "xhigh"]

# GPT-family models with explicit reasoning_effort support.
_GPT_REASONING_MODELS = {"gpt-5", "gpt-5.1", "gpt-5.2", "gpt-5.4", "gpt-5.5"}

# GPT-family models accepted by the app but not documented here with
# reasoning_effort support.
_GPT_NO_REASONING_MODELS = {"gpt-5.3-chat-latest"}

_GPT_REASONING_EFFORT_OPTIONS = {
    "gpt-5": {"minimal", "low", "medium", "high"},
    "gpt-5.1": {"none", "low", "medium", "high"},
    "gpt-5.2": {"none", "low", "medium", "high", "xhigh"},
    "gpt-5.4": {"none", "low", "medium", "high", "xhigh"},
    "gpt-5.5": {"none", "low", "medium", "high", "xhigh"},
}

# Latest default model per provider
LATEST_GPT_MODEL    = "gpt-5.4"
LATEST_GEMINI_MODEL = "gemini-3-pro-preview"


def _supports_reasoning_effort(model: str) -> bool:
    """Return True when *model* supports reasoning_effort in this wrapper."""
    return model.lower() in _GPT_REASONING_MODELS


def _is_gpt5_chat_latest(model: str) -> bool:
    """Return True for accepted GPT-5-era models without reasoning_effort support."""
    return model.lower() in _GPT_NO_REASONING_MODELS


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
    allowed = _GPT_REASONING_EFFORT_OPTIONS.get(normalized_model, set())
    if normalized_effort in allowed:
        return normalized_effort

    if allowed:
        logger.warning(
            "Ignoring unsupported reasoning_effort=%s for model=%s. Allowed: %s",
            reasoning_effort,
            model,
            ", ".join(sorted(allowed)),
        )
    return None


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
    is passed to the API instead of temperature. ``gpt-5.3-chat-latest`` is
    accepted without ``reasoning_effort``.

    Args:
        images:           List of raw PNG byte strings.
        prompt:           Text instruction for the model.
        api_key:          OpenAI API key.
        model:            Vision-capable model name.
        detail:           Image resolution hint ('low', 'high', or 'auto').
        reasoning_effort: Reasoning depth for supported GPT-5.x models.
                          Ignored for gpt-5.3-chat-latest and older models
                          such as gpt-4o and gpt-4.1.

    Returns:
        Model response as a plain string.
    """
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise RuntimeError("openai package not installed. Run: pip install openai") from exc

    if not api_key:
        raise RuntimeError("OpenAI API key is not set.")

    client = OpenAI(api_key=api_key)

    # Build the multimodal message content
    content = [{"type": "text", "text": prompt}]
    for img_bytes in images:
        b64 = base64.b64encode(img_bytes).decode("ascii")
        content.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/png;base64,{b64}",
                "detail": detail,
            },
        })

    # Build API call kwargs
    call_kwargs: dict = {
        "model":    model,
        "messages": [{"role": "user", "content": content}],
    }

    if _supports_reasoning_effort(model):
        # GPT-5 reasoning models: use reasoning_effort; temperature is not supported.
        normalized_effort = _normalize_reasoning_effort(model, reasoning_effort)
        if normalized_effort:
            call_kwargs["reasoning_effort"] = normalized_effort
        logger.info("[GPT-5 reasoning] Using model=%s reasoning_effort=%s", model, normalized_effort)
    elif _is_gpt5_chat_latest(model):
        # Keep parity with the main RADIANT-LLM app for gpt-5.3-chat-latest.
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
) -> str:
    """
    Unified vision-LLM dispatcher.

    Automatically routes to the correct provider backend.  When *model* is
    empty or None, falls back to the latest default for that provider.

    Args:
        images:           List of raw PNG byte strings.
        prompt:           Text instruction for the model.
        provider:         ``'gpt'`` or ``'gemini'``.
        api_key:          API key for the chosen provider.
        model:            Model name string.
        detail:           Image detail level (GPT only; ignored for Gemini).
        reasoning_effort: Reasoning depth for GPT-5.x (ignored for older GPT
                          models and all Gemini models).

    Returns:
        Model response as a plain string.
    """
    resolved_model = model or (
        LATEST_GPT_MODEL if provider == "gpt" else LATEST_GEMINI_MODEL
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

    raise RuntimeError(
        f"Unknown vision provider: {provider!r}. Must be 'gpt' or 'gemini'."
    )
