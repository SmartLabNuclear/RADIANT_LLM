"""
test_integration.py — Real, end-to-end tests against live vision-LLM
providers (actual network calls, real cost/time for cloud providers).

Opt-in only: excluded by pyproject.toml's `addopts = "-m 'not integration'"`,
so a plain `pytest tests/` never runs these or spends real API cost/time on
any machine. `addopts` applies regardless of how tests are selected on the
command line -- naming this file directly still deselects everything in it.
Run explicitly with `pytest -m integration` (overrides addopts's default `-m`
expression rather than combining with it).

Each provider variant skips cleanly (not fails) when its prerequisite isn't
available on the running machine -- no OPENAI_API_KEY, no GEMINI_API_KEY, no
reachable Ollama instance with a vision-capable model pulled.

Assertions are about output SHAPE, never exact LLM-generated text -- real
model output is non-deterministic across runs.
"""

import json
import os
from pathlib import Path

import pytest

from visual_parser.config import ParserConfig
from visual_parser.pipeline import run_pipeline

pytestmark = pytest.mark.integration

FIXTURE_PDF = Path(__file__).parent / "fixtures" / "Todreas_and_Kazimir_p62.pdf"


def _read_jsonl(path: Path):
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _run_real_pipeline_and_assert_shape(
    tmp_path,
    vision_provider: str,
    gpt_vision_model: str = "gpt-5.4",
    gemini_vision_model: str = "gemini-3.8-flash",
    ollama_vision_model: str = "",
) -> None:
    input_dir = tmp_path
    (input_dir / FIXTURE_PDF.name).write_bytes(FIXTURE_PDF.read_bytes())

    config = ParserConfig(
        input_dir=str(input_dir),
        skip_text=True,  # focus on the vision path (metadata + figures); this
                         # fixture is a scanned page with no text layer anyway
        vision_provider=vision_provider,
        gpt_vision_model=gpt_vision_model,
        gemini_vision_model=gemini_vision_model,
        ollama_vision_model=ollama_vision_model,
    )

    summary = run_pipeline(config)

    assert summary["status"] == "success", summary
    assert not summary["failed_basenames"], summary["failed_basenames"]

    visuals = _read_jsonl(input_dir / "02_visuals_kb.jsonl")
    assert len(visuals) == 1, "expected exactly one figure on this fixture's single page"
    row = visuals[0]
    assert {"source", "page", "document_id", "figure_index", "figure_id", "description"} <= row.keys()
    assert isinstance(row["description"], str) and row["description"].strip()

    metadata = _read_jsonl(input_dir / "03_metadata_kb.jsonl")
    assert len(metadata) == 1
    assert metadata[0].get("source") == FIXTURE_PDF.name


@pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="OPENAI_API_KEY not set")
def test_real_pipeline_gpt(tmp_path):
    _run_real_pipeline_and_assert_shape(tmp_path, vision_provider="gpt")


@pytest.mark.skipif(not os.getenv("GEMINI_API_KEY"), reason="GEMINI_API_KEY not set")
def test_real_pipeline_gemini(tmp_path):
    _run_real_pipeline_and_assert_shape(tmp_path, vision_provider="gemini")


def _first_pulled_vision_model():
    try:
        from visual_parser.ollama_local import list_vision_capable_models
        models = list_vision_capable_models()
        return models[0].id if models else None
    except Exception:
        return None


def test_real_pipeline_ollama(tmp_path):
    # Checked lazily, inside the test body, not at collection time -- a
    # module-level call here would run on every `pytest tests/` collection
    # (even with this whole file marker-deselected by addopts), making a
    # real network probe to Ollama on every machine regardless of whether
    # this test will actually run. Deferring it means that probe only
    # happens when this specific test is actually selected (`pytest -m
    # integration`), matching this module's own "never runs/costs anything
    # by default" claim.
    model = _first_pulled_vision_model()
    if model is None:
        pytest.skip("No reachable Ollama instance with a vision-capable model pulled")

    # Explicit model, not select_best_vision_model()'s auto-pick -- this test
    # is about validating the real call path works, not about whether
    # auto-selection also happens to fit this machine's current free VRAM
    # (that VRAM-budget logic is already covered by mocked unit tests in
    # test_ollama_local.py).
    _run_real_pipeline_and_assert_shape(tmp_path, vision_provider="ollama", ollama_vision_model=model)
