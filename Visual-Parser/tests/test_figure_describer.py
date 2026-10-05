import json
import threading
import time

import pymupdf as fitz
import pytest

from visual_parser import figure_describer


def _make_pdf(path, num_pages: int):
    doc = fitz.open()
    for i in range(num_pages):
        page = doc.new_page()
        page.insert_text((72, 72), f"Page {i + 1}")
    doc.save(str(path))
    doc.close()
    return str(path)


def _fake_describe(images, prompt, provider, api_key, model, detail, reasoning_effort):
    """Mimics call_vision_llm's signature; records what it was called with via
    a shared list the test can inspect, and returns one figure per call."""
    return json.dumps([{"description": f"saw {len(images)} image(s)"}])


@pytest.fixture(autouse=True)
def _patch_call_vision_llm(monkeypatch):
    monkeypatch.setattr(figure_describer, "call_vision_llm", _fake_describe)


def _read_jsonl(path):
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def test_context_pages_zero_sends_one_image_per_call(tmp_path, monkeypatch):
    pdf_path = _make_pdf(tmp_path / "doc.pdf", num_pages=3)
    captured_image_counts = []

    def fake(images, prompt, provider, api_key, model, detail, reasoning_effort):
        captured_image_counts.append(len(images))
        return json.dumps([{"description": "x"}])

    monkeypatch.setattr(figure_describer, "call_vision_llm", fake)

    figure_describer.describe_figures_for_new_pdfs(
        new_pdf_paths=[pdf_path],
        output_dir=str(tmp_path),
        vision_provider="gpt",
        vision_api_key="sk-test",
        vision_model="gpt-5.4",
        max_workers=2,
        context_pages=0,
    )

    assert captured_image_counts == [1, 1, 1]
    rows = _read_jsonl(tmp_path / "02_visuals_kb.jsonl")
    assert {r["page"] for r in rows} == {1, 2, 3}


def test_context_pages_window_bounded_at_pdf_edges(tmp_path, monkeypatch):
    pdf_path = _make_pdf(tmp_path / "doc.pdf", num_pages=3)
    captured = {}  # page_number -> image_count

    def fake(images, prompt, provider, api_key, model, detail, reasoning_effort):
        # the fake prompt-builder already baked the target index into the
        # preamble text, but it's simpler here to just record counts per call
        # order (pages are submitted/queued in order even though they may
        # complete out of order under concurrency)
        captured.setdefault("counts", []).append(len(images))
        return json.dumps([{"description": "x"}])

    monkeypatch.setattr(figure_describer, "call_vision_llm", fake)

    figure_describer.describe_figures_for_new_pdfs(
        new_pdf_paths=[pdf_path],
        output_dir=str(tmp_path),
        vision_provider="gpt",
        vision_api_key="sk-test",
        vision_model="gpt-5.4",
        max_workers=1,  # deterministic ordering for this assertion
        context_pages=1,
    )

    # page 1: [1,2] (no page before it) -> 2 images
    # page 2: [1,2,3] -> 3 images
    # page 3: [2,3] (no page after it) -> 2 images
    assert sorted(captured["counts"]) == [2, 2, 3]


def test_context_window_never_crosses_pdf_boundary(tmp_path, monkeypatch):
    pdf_a = _make_pdf(tmp_path / "a.pdf", num_pages=1)
    pdf_b = _make_pdf(tmp_path / "b.pdf", num_pages=1)
    captured_counts = []

    def fake(images, prompt, provider, api_key, model, detail, reasoning_effort):
        captured_counts.append(len(images))
        return json.dumps([{"description": "x"}])

    monkeypatch.setattr(figure_describer, "call_vision_llm", fake)

    figure_describer.describe_figures_for_new_pdfs(
        new_pdf_paths=[pdf_a, pdf_b],
        output_dir=str(tmp_path),
        vision_provider="gpt",
        vision_api_key="sk-test",
        vision_model="gpt-5.4",
        max_workers=2,
        context_pages=1,
    )

    # Each PDF has only 1 page -- context window can't borrow from the other
    # PDF's page 1, so every call should see exactly 1 image.
    assert captured_counts == [1, 1]


def test_concurrent_completion_order_does_not_lose_or_duplicate_rows(tmp_path, monkeypatch):
    pdf_path = _make_pdf(tmp_path / "doc.pdf", num_pages=6)

    def fake(images, prompt, provider, api_key, model, detail, reasoning_effort):
        # Deliberately vary delay so completion order scrambles relative to
        # submission order.
        time.sleep(0.01 if threading.get_ident() % 2 == 0 else 0.02)
        return json.dumps([{"description": "x"}])

    monkeypatch.setattr(figure_describer, "call_vision_llm", fake)

    figure_describer.describe_figures_for_new_pdfs(
        new_pdf_paths=[pdf_path],
        output_dir=str(tmp_path),
        vision_provider="gpt",
        vision_api_key="sk-test",
        vision_model="gpt-5.4",
        max_workers=4,
        context_pages=0,
    )

    rows = _read_jsonl(tmp_path / "02_visuals_kb.jsonl")
    assert sorted(r["page"] for r in rows) == [1, 2, 3, 4, 5, 6]
    assert len(rows) == 6  # no duplicates


def test_resume_skips_already_done_pages_under_concurrency(tmp_path, monkeypatch):
    pdf_path = _make_pdf(tmp_path / "doc.pdf", num_pages=3)
    figures_path = tmp_path / "02_visuals_kb.jsonl"
    figures_path.write_text(
        json.dumps({"source": "doc.pdf", "page": 2, "document_id": "x", "figure_index": 0,
                    "figure_id": "x:p2:f0", "description": "already done"}) + "\n",
        encoding="utf-8",
    )

    called_pages = []

    def fake(images, prompt, provider, api_key, model, detail, reasoning_effort):
        called_pages.append(True)
        return json.dumps([{"description": "new"}])

    monkeypatch.setattr(figure_describer, "call_vision_llm", fake)

    figure_describer.describe_figures_for_new_pdfs(
        new_pdf_paths=[pdf_path],
        output_dir=str(tmp_path),
        vision_provider="gpt",
        vision_api_key="sk-test",
        vision_model="gpt-5.4",
        max_workers=2,
        context_pages=0,
    )

    assert len(called_pages) == 2  # only pages 1 and 3 -- page 2 was already done
    rows = _read_jsonl(figures_path)
    assert sorted(r["page"] for r in rows) == [1, 2, 3]
    descriptions_by_page = {r["page"]: r["description"] for r in rows}
    assert descriptions_by_page[2] == "already done"  # untouched, not re-described
