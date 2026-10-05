"""
ollama_local.py — Local Ollama vision-model support: reachability, model
listing, vision-capability detection, and VRAM-aware auto-selection.

Mirrors the base-url resolution / model-listing conventions already
established in RADIANT-LLM/AutoSAM's utils/ollama_local.py (raw `requests`,
same env-var/probe precedence) but adds functions with no existing precedent
elsewhere in the wider codebase: vision-capability detection and live-VRAM-
based model selection (see select_best_vision_model()).
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from typing import List, Optional

import requests

logger = logging.getLogger(__name__)

_BASE_URL_PROBE_TIMEOUT = 1.5
_API_TIMEOUT = 3.0

_resolved_base_url_cache: Optional[str] = None

# Name-fragment heuristic for vision-capable Ollama models, used as a fallback
# when /api/show's `capabilities` field is absent (older Ollama versions) or
# doesn't list "vision" for a model that name-wise clearly is one. Same
# "pragmatic filter, not perfect" philosophy as model_catalog.py's
# _looks_chat_capable -- expect this list to go stale the same way.
_VISION_NAME_FRAGMENTS = (
    "llava", "vision", "-vl", "vl-", "pixtral", "moondream", "minicpm-v", "bakllava",
)


def _looks_vision_capable(model_name: str) -> bool:
    lowered = model_name.lower()
    return any(fragment in lowered for fragment in _VISION_NAME_FRAGMENTS)


def resolve_ollama_base_url(force_refresh: bool = False) -> Optional[str]:
    """
    Returns the OpenAI-compatible base URL for a reachable Ollama instance
    (e.g. "http://localhost:11434/v1"), or None if nothing responds.

    Precedence: OLLAMA_BASE_URL env var (used verbatim, no probing) -> cached
    result from an earlier call (unless force_refresh) -> probe
    localhost:11434 -> probe host.docker.internal:11434 (the containerized
    case, matching RADIANT-LLM's docker-compose host-gateway setup).
    """
    global _resolved_base_url_cache

    env_url = os.getenv("OLLAMA_BASE_URL", "").strip()
    if env_url:
        return env_url.rstrip("/")

    if not force_refresh and _resolved_base_url_cache:
        return _resolved_base_url_cache

    for host in ("http://localhost:11434", "http://host.docker.internal:11434"):
        try:
            resp = requests.get(f"{host}/api/tags", timeout=_BASE_URL_PROBE_TIMEOUT)
            resp.raise_for_status()
        except requests.RequestException:
            continue
        _resolved_base_url_cache = f"{host}/v1"
        return _resolved_base_url_cache

    return None


def _native_host(base_url: str) -> str:
    """Strip the /v1 suffix to get the native-API host for /api/tags, /api/show."""
    return base_url[:-3] if base_url.endswith("/v1") else base_url


@dataclass
class OllamaModel:
    id: str
    label: str
    size_bytes: int
    quantization: str
    modified_at: str


def list_ollama_models(timeout: float = _API_TIMEOUT) -> List[OllamaModel]:
    """
    Live list of locally-pulled Ollama models via the native /api/tags
    endpoint (richer metadata than the OpenAI-compat /v1/models, which only
    returns bare ids). Never raises -- returns [] on any failure, including
    Ollama being unreachable.
    """
    base_url = resolve_ollama_base_url()
    if not base_url:
        return []

    host = _native_host(base_url)
    try:
        resp = requests.get(f"{host}/api/tags", timeout=timeout)
        resp.raise_for_status()
        data = resp.json()
    except (requests.RequestException, ValueError):
        return []

    models: List[OllamaModel] = []
    for entry in data.get("models", []):
        model_id = entry.get("name") or entry.get("model") or ""
        if not model_id:
            continue
        details = entry.get("details", {}) or {}
        param_size = details.get("parameter_size", "")
        quant = details.get("quantization_level", "")
        label = f"{model_id} ({param_size}, {quant})" if (param_size or quant) else model_id
        models.append(OllamaModel(
            id=model_id,
            label=label,
            size_bytes=int(entry.get("size", 0) or 0),
            quantization=quant,
            modified_at=str(entry.get("modified_at", "")),
        ))

    models.sort(key=lambda m: m.modified_at, reverse=True)
    return models


def get_model_capabilities(model_name: str, timeout: float = _API_TIMEOUT) -> List[str]:
    """
    Query Ollama's /api/show for *model_name*'s reported `capabilities` list
    (e.g. ["completion", "vision", "tools"]) -- newer Ollama versions only.
    Returns [] on any failure or if the field is absent, so callers should
    fall back to _looks_vision_capable() for vision detection.
    """
    base_url = resolve_ollama_base_url()
    if not base_url:
        return []

    host = _native_host(base_url)
    try:
        resp = requests.post(f"{host}/api/show", json={"name": model_name}, timeout=timeout)
        resp.raise_for_status()
        data = resp.json()
    except (requests.RequestException, ValueError):
        return []

    capabilities = data.get("capabilities")
    return capabilities if isinstance(capabilities, list) else []


def list_vision_capable_models() -> List[OllamaModel]:
    """
    list_ollama_models(), filtered to models that are vision-capable --
    determined primarily via /api/show's `capabilities` field, falling back
    to a name heuristic when that field is absent or doesn't list "vision"
    for a model that name-wise clearly is one.
    """
    vision_models = []
    for m in list_ollama_models():
        capabilities = get_model_capabilities(m.id)
        if "vision" in capabilities or _looks_vision_capable(m.id):
            vision_models.append(m)
    return vision_models


def warm_up_model(model_name: str, timeout: float = 120.0) -> None:
    """
    Fire a minimal real request to force Ollama to load *model_name* before
    the real (possibly concurrent) vision calls begin. Without this, the
    first of several concurrent figure-description workers would absorb the
    full cold-load delay (documented by Ollama as "tens of seconds for
    larger models") while the others wait on it unnecessarily. Fire-and-
    forget: failures are swallowed here, since the real vision calls will
    surface any genuine problem (e.g. model not found) with a clearer error.
    """
    base_url = resolve_ollama_base_url()
    if not base_url:
        return
    try:
        requests.post(
            f"{base_url}/chat/completions",
            json={
                "model": model_name,
                "messages": [{"role": "user", "content": "hi"}],
                "max_tokens": 1,
            },
            timeout=timeout,
        )
    except requests.RequestException:
        pass


def get_loaded_model_gpu_status(model_name: str, timeout: float = 3.0) -> Optional[dict]:
    """
    Query Ollama's native /api/ps (currently-loaded models) for *model_name*'s
    GPU/CPU memory split. Returns {"size_bytes": int, "size_vram_bytes": int}
    or None if the model isn't currently loaded (e.g. it was evicted, or the
    warm-up call failed). size_vram_bytes == size_bytes means fully
    GPU-resident; 0 means fully CPU; anything in between is a partial offload
    -- confirmed live on this machine with a 35B model only partially fitting
    free VRAM (2.6 GB of 23.4 GB on GPU, the rest on CPU).
    """
    base_url = resolve_ollama_base_url()
    if not base_url:
        return None

    host = _native_host(base_url)
    try:
        resp = requests.get(f"{host}/api/ps", timeout=timeout)
        resp.raise_for_status()
        data = resp.json()
    except (requests.RequestException, ValueError):
        return None

    # Ollama treats an untagged reference as implicitly ":latest" and reports
    # it back fully-qualified in /api/ps -- e.g. a user-passed "llava" must
    # still match an entry named "llava:latest", or this always reports
    # "not loaded" for the exact example the README itself gives
    # (`ollama pull llava`).
    wanted = model_name if ":" in model_name else f"{model_name}:latest"
    for entry in data.get("models", []):
        entry_name = entry.get("name") or entry.get("model") or ""
        if entry_name in (model_name, wanted):
            return {
                "size_bytes": int(entry.get("size", 0) or 0),
                "size_vram_bytes": int(entry.get("size_vram", 0) or 0),
            }
    return None


def describe_gpu_status(status: Optional[dict]) -> str:
    """Human-readable one-line summary of get_loaded_model_gpu_status()'s result."""
    if status is None:
        return "unknown (Ollama did not report this model as currently loaded)"

    size_bytes = status["size_bytes"]
    vram_bytes = status["size_vram_bytes"]
    size_gb = size_bytes / 1e9
    vram_gb = vram_bytes / 1e9

    if size_bytes == 0:
        return "unknown (model reported with 0 size)"
    if vram_bytes <= 0:
        return f"CPU only ({size_gb:.1f} GB) -- no GPU offload"
    if vram_bytes >= size_bytes:
        return f"fully on GPU ({vram_gb:.1f} GB)"
    return f"partially on GPU ({vram_gb:.1f} GB of {size_gb:.1f} GB total, {vram_bytes / size_bytes:.0%} offloaded)"


def get_free_vram_bytes() -> Optional[int]:
    """
    Currently-free GPU memory visible to THIS process, in bytes, or None if
    no CUDA GPU is visible (no GPU at all, or running in a container without
    --gpus all while a GPU exists only on the host). Deliberately uses
    torch.cuda.mem_get_info() rather than shelling out to nvidia-smi (the
    only existing precedent, in AutoSAM's standalone setup-advisor script) --
    torch is already a hard dependency here, and mem_get_info() reports live
    free memory, correctly reflecting whatever else (e.g. Nougat) already
    holds VRAM in this same process, which a static nvidia-smi total-VRAM
    snapshot would not.
    """
    try:
        import torch
    except ImportError:
        return None

    if not torch.cuda.is_available():
        return None

    free_bytes, _total_bytes = torch.cuda.mem_get_info()
    return free_bytes


def select_best_vision_model(safety_margin: float = 0.85) -> str:
    """
    Pick the largest locally-pulled, vision-capable Ollama model whose
    on-disk size fits within currently-free VRAM * safety_margin.

    size_bytes is the model's on-disk blob size, not its exact runtime VRAM
    footprint (KV-cache/context buffers and CUDA-context overhead aren't
    included) -- safety_margin is a deliberate approximation, not a solved
    problem.

    Raises RuntimeError with an actionable message if:
      - Ollama isn't reachable or has no models pulled at all.
      - none of the pulled models are vision-capable.
      - every vision-capable model is too large for the free VRAM budget
        (this one case stays strict on purpose -- a real GPU exists but
        nothing fits, so silently falling back to heavy CPU offload would
        hide a config/hardware mismatch worth surfacing explicitly).

    When no CUDA GPU is visible to this process at all (no GPU on the
    machine, or running in a container without --gpus all while Ollama runs
    on the host with a real GPU -- mem_get_info() only sees what's visible to
    the calling process), this does NOT raise: CPU-only Ollama is a
    legitimate setup, so it falls back to the smallest pulled vision-capable
    model (CPU inference time scales hard with size) and logs a warning
    rather than forcing every CPU-only user to already know and type an
    exact --vision-model.
    """
    vision_models = list_vision_capable_models()
    if not vision_models:
        all_models = list_ollama_models()
        if not all_models:
            raise RuntimeError(
                "No Ollama models found (or Ollama is unreachable). "
                "Pull a vision-capable model first, e.g.: ollama pull llava"
            )
        raise RuntimeError(
            "No vision-capable Ollama models are pulled. "
            "Pull one first, e.g.: ollama pull llava"
        )

    free_bytes = get_free_vram_bytes()
    if free_bytes is None:
        smallest = min(vision_models, key=lambda m: m.size_bytes)
        message = (
            f"No CUDA GPU visible to this process -- falling back to CPU-only "
            f"inference with the smallest pulled vision-capable model: {smallest.id} "
            f"({smallest.size_bytes / 1e9:.1f} GB). This will be slow. Pass an "
            f"explicit --vision-model to choose a different one."
        )
        logger.warning(message)
        # Also print directly: the default --log-level is ERROR, which
        # filters out WARNING-level log records entirely (both console and
        # 05_pipeline.log) -- this message is important enough that it must
        # reach the user regardless of their configured log level, matching
        # the other unmissable "[OLLAMA] ..." status lines in pipeline.py.
        print(f"[OLLAMA] {message}")
        return smallest.id

    budget = int(free_bytes * safety_margin)
    fitting = [m for m in vision_models if m.size_bytes <= budget]
    if not fitting:
        smallest = min(vision_models, key=lambda m: m.size_bytes)
        raise RuntimeError(
            f"No vision-capable Ollama model fits in the current VRAM budget "
            f"({budget / 1e9:.1f} GB, {safety_margin:.0%} of free VRAM). The "
            f"smallest pulled vision-capable model, {smallest.id}, is "
            f"{smallest.size_bytes / 1e9:.1f} GB. Pull a smaller vision-capable "
            f"model, or pass an explicit --vision-model."
        )

    best = max(fitting, key=lambda m: m.size_bytes)
    logger.info(
        "Auto-selected Ollama vision model %s (%.1f GB) -- %.1f GB free VRAM, safety margin %.0f%%",
        best.id, best.size_bytes / 1e9, free_bytes / 1e9, safety_margin * 100,
    )
    return best.id
