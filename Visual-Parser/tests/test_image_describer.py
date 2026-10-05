import json

import pytest
from PIL import Image

from visual_parser import image_describer


def _make_png(path, color=(255, 0, 0)):
    img = Image.new("RGB", (8, 8), color=color)
    img.save(str(path), format="PNG")
    return str(path)


def _read_jsonl(path):
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


# ---------------------------------------------------------------------------
# _parse_single_image_response
# ---------------------------------------------------------------------------

def test_parse_well_formed_object():
    raw = json.dumps({"description": "**Subject:** A Chart"})
    parsed = image_describer._parse_single_image_response(raw, "img.png")
    assert parsed == {"description": "**Subject:** A Chart"}


def test_parse_prose_wrapped_object():
    raw = 'Sure, here is the result:\n```json\n{"description": "**Subject:** X"}\n```\nHope that helps!'
    parsed = image_describer._parse_single_image_response(raw, "img.png")
    assert parsed == {"description": "**Subject:** X"}


def test_parse_malformed_returns_none():
    parsed = image_describer._parse_single_image_response("not json at all {{{", "img.png")
    assert parsed is None


def test_parse_unwraps_single_element_list():
    """A model that ignores 'NOT a list' and returns [{...}] anyway should
    still be recovered, mirroring figure_describer.py's own defensive
    normalization for the opposite shape mismatch."""
    raw = json.dumps([{"description": "**Subject:** Y"}])
    parsed = image_describer._parse_single_image_response(raw, "img.png")
    assert parsed == {"description": "**Subject:** Y"}


def test_parse_recovers_real_answer_when_model_echoes_the_prompt_template():
    """Regression test: a greedy regex would span from the first '{' to the
    LAST '}' across both blocks, producing one invalid blob when a model
    echoes the prompt's own OUTPUT FORMAT example alongside its real answer.
    The real answer appears first here, so it must be the one recovered."""
    raw = (
        'Here is my answer:\n'
        '{"description": "**Subject:** Real Answer"}\n'
        'Reminder of the format: { "description": "**Subject:** [Title]..." }'
    )
    parsed = image_describer._parse_single_image_response(raw, "img.png")
    assert parsed == {"description": "**Subject:** Real Answer"}


def test_parse_handles_literal_brace_inside_description_text():
    """A naive lazy regex would stop at the first '}' even if it's just a
    character inside a string value (e.g. set notation in the description),
    truncating the object early and failing to parse. A proper JSON-aware
    scan must not have this problem. Wrapped in prose so json.loads(body)
    fails directly and the fallback scan path is actually exercised."""
    raw = 'Answer:\n{"description": "Shows the set {A, B, C} on the x-axis"}\nDone.'
    parsed = image_describer._parse_single_image_response(raw, "img.png")
    assert parsed == {"description": "Shows the set {A, B, C} on the x-axis"}


# ---------------------------------------------------------------------------
# _flatten_to_rgb
# ---------------------------------------------------------------------------

def test_flatten_composites_transparency_onto_white():
    """Regression test: Image.convert('RGB') alone drops alpha without
    compositing, commonly exposing (0,0,0) stored under fully-transparent
    pixels -- a transparent-background PNG would silently turn black."""
    img = Image.new("RGBA", (4, 4), (0, 0, 0, 0))  # fully transparent, black underneath
    img.putpixel((0, 0), (10, 20, 30, 255))  # one opaque pixel

    flattened = image_describer._flatten_to_rgb(img)

    assert flattened.mode == "RGB"
    assert flattened.getpixel((1, 1)) == (255, 255, 255)  # transparent area -> white, not black
    assert flattened.getpixel((0, 0)) == (10, 20, 30)  # opaque pixel preserved


def test_flatten_leaves_opaque_rgb_image_unchanged():
    img = Image.new("RGB", (4, 4), (10, 20, 30))
    flattened = image_describer._flatten_to_rgb(img)
    assert flattened.mode == "RGB"
    assert flattened.getpixel((0, 0)) == (10, 20, 30)


# ---------------------------------------------------------------------------
# _derive_title
# ---------------------------------------------------------------------------

def test_derive_title_extracts_subject_heading():
    description = "**Subject:** Vertical Parabolic Gate Schematic\n**Verbatim Text Content:** ..."
    assert image_describer._derive_title(description) == "Vertical Parabolic Gate Schematic"


def test_derive_title_falls_back_to_first_sentence():
    description = "A plot of decay heat over time. More detail follows here."
    assert image_describer._derive_title(description) == "A plot of decay heat over time."


def test_derive_title_hard_truncates_as_last_resort():
    description = "x" * 300  # no sentence boundary, no Subject heading
    title = image_describer._derive_title(description)
    assert title == "x" * 100


# ---------------------------------------------------------------------------
# describe_images
# ---------------------------------------------------------------------------

def test_describe_images_skips_non_string_description(tmp_path, monkeypatch):
    """Regression test: a weak/non-compliant model can return 'description'
    as a nested object instead of the documented flat string (e.g. one field
    per heading instead of folding them into one string). Before the
    isinstance(description, str) fix, this crashed _derive_title()'s regex
    search with 'TypeError: expected string or bytes-like object, got dict'
    instead of being skipped like a missing field."""
    img = _make_png(tmp_path / "a.png")

    monkeypatch.setattr(
        image_describer, "call_vision_llm",
        lambda **kwargs: json.dumps({"description": {"Subject": "nested, not flat"}}),
    )

    written = image_describer.describe_images(
        new_image_paths=[img],
        output_dir=str(tmp_path),
        vision_provider="gpt",
        vision_api_key="sk-test",
        vision_model="gpt-5.4",
    )

    assert written == []
    assert _read_jsonl(tmp_path / "image_descriptions.jsonl") == []


def test_describe_images_writes_rows_for_each_image(tmp_path, monkeypatch):
    img1 = _make_png(tmp_path / "a.png")
    img2 = _make_png(tmp_path / "b.png")

    monkeypatch.setattr(
        image_describer, "call_vision_llm",
        lambda **kwargs: json.dumps({"description": "**Subject:** Something"}),
    )

    written = image_describer.describe_images(
        new_image_paths=[img1, img2],
        output_dir=str(tmp_path),
        vision_provider="gpt",
        vision_api_key="sk-test",
        vision_model="gpt-5.4",
    )

    assert set(written) == {"a.png", "b.png"}
    rows = _read_jsonl(tmp_path / "image_descriptions.jsonl")
    assert {r["source"] for r in rows} == {"a.png", "b.png"}
    for row in rows:
        assert row["title"] == "Something"
        assert len(row["image_id"]) == 16


def test_failed_image_is_not_marked_written(tmp_path, monkeypatch):
    """A failed vision call must not be reported as written -- the caller
    uses the return value to decide what to mark processed, and a failed
    image must stay eligible for retry on the next run."""
    good = _make_png(tmp_path / "good.png")
    corrupt = tmp_path / "corrupt.png"
    corrupt.write_bytes(b"this is not a real image")

    monkeypatch.setattr(
        image_describer, "call_vision_llm",
        lambda **kwargs: json.dumps({"description": "**Subject:** Fine"}),
    )

    written = image_describer.describe_images(
        new_image_paths=[good, str(corrupt)],
        output_dir=str(tmp_path),
        vision_provider="gpt",
        vision_api_key="sk-test",
        vision_model="gpt-5.4",
    )

    assert written == ["good.png"]
    rows = _read_jsonl(tmp_path / "image_descriptions.jsonl")
    assert {r["source"] for r in rows} == {"good.png"}


def test_vision_call_exception_is_not_marked_written(tmp_path, monkeypatch):
    img1 = _make_png(tmp_path / "a.png")
    img2 = _make_png(tmp_path / "b.png")

    call_count = {"n": 0}

    def fake(**kwargs):
        call_count["n"] += 1
        if call_count["n"] == 1:
            raise RuntimeError("simulated failure")
        return json.dumps({"description": "**Subject:** OK"})

    monkeypatch.setattr(image_describer, "call_vision_llm", fake)

    written = image_describer.describe_images(
        new_image_paths=[img1, img2],
        output_dir=str(tmp_path),
        vision_provider="gpt",
        vision_api_key="sk-test",
        vision_model="gpt-5.4",
        max_workers=1,  # deterministic call order
    )

    assert len(written) == 1
    rows = _read_jsonl(tmp_path / "image_descriptions.jsonl")
    assert len(rows) == 1


def test_resume_skips_already_done_images(tmp_path, monkeypatch):
    img1 = _make_png(tmp_path / "a.png")
    img2 = _make_png(tmp_path / "b.png")

    descriptions_path = tmp_path / "image_descriptions.jsonl"
    descriptions_path.write_text(
        json.dumps({"source": "a.png", "image_id": "x", "title": "Old", "description": "already done"}) + "\n",
        encoding="utf-8",
    )

    called = []
    monkeypatch.setattr(
        image_describer, "call_vision_llm",
        lambda **kwargs: called.append(True) or json.dumps({"description": "**Subject:** New"}),
    )

    written = image_describer.describe_images(
        new_image_paths=[img1, img2],
        output_dir=str(tmp_path),
        vision_provider="gpt",
        vision_api_key="sk-test",
        vision_model="gpt-5.4",
    )

    assert len(called) == 1  # only b.png was actually called
    assert written == ["b.png"]
    rows = _read_jsonl(descriptions_path)
    assert {r["source"] for r in rows} == {"a.png", "b.png"}
    assert next(r for r in rows if r["source"] == "a.png")["description"] == "already done"




def test_write_failure_is_not_marked_written(tmp_path, monkeypatch):
    """Regression test: append_to_jsonl can fail silently (disk full,
    permissions, transient network-share issue) -- describe_images() must
    check its return value rather than assume the row landed, or the image
    gets permanently marked processed with no row ever written and no retry
    path short of --redo/--rebuild."""
    img = _make_png(tmp_path / "a.png")

    monkeypatch.setattr(
        image_describer, "call_vision_llm",
        lambda **kwargs: json.dumps({"description": "**Subject:** X"}),
    )
    monkeypatch.setattr(image_describer, "append_to_jsonl", lambda path, rows: False)

    written = image_describer.describe_images(
        new_image_paths=[img],
        output_dir=str(tmp_path),
        vision_provider="gpt",
        vision_api_key="sk-test",
        vision_model="gpt-5.4",
    )

    assert written == []


def test_describe_images_uses_its_own_ollama_timeout(tmp_path, monkeypatch):
    """Regression test: this path's timeout must be decoupled from
    figure_describer.py's context-window-scaled formula -- calibrated
    separately (900s) against a real measured baseline, since
    IMAGE_DESCRIPTION_PROMPT's verbatim-text-transcription requirement can
    demand much more output than FIGURE_PROMPT ever needs."""
    img = _make_png(tmp_path / "a.png")
    captured = {}

    def fake(**kwargs):
        captured.update(kwargs)
        return json.dumps({"description": "**Subject:** X"})

    monkeypatch.setattr(image_describer, "call_vision_llm", fake)

    image_describer.describe_images(
        new_image_paths=[img],
        output_dir=str(tmp_path),
        vision_provider="ollama",
        vision_api_key="",
        vision_model="qwen2.5-vl:32b",
    )

    assert captured["ollama_timeout_seconds"] == image_describer._OLLAMA_IMAGE_TIMEOUT_SECONDS
    assert image_describer._OLLAMA_IMAGE_TIMEOUT_SECONDS == 900.0


def test_no_new_images_returns_empty_list_without_calling_vision(tmp_path, monkeypatch):
    def fail_if_called(**kwargs):
        raise AssertionError("should not be called")

    monkeypatch.setattr(image_describer, "call_vision_llm", fail_if_called)

    written = image_describer.describe_images(
        new_image_paths=[],
        output_dir=str(tmp_path),
        vision_provider="gpt",
        vision_api_key="sk-test",
        vision_model="gpt-5.4",
    )
    assert written == []
