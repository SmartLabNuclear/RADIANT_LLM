import json
import os

from visual_parser import pipeline
from visual_parser.config import ParserConfig


def test_ollama_warm_up_deferred_until_after_nougat_releases_gpu(monkeypatch, tmp_path):
    """Regression test: loading a local Ollama vision model must happen AFTER
    Nougat (Step 1) has run and released its GPU memory, not before. Real
    hardware testing found the warm-up call originally ran before Nougat even
    started, forcing Nougat to compete for whatever VRAM was left instead of
    having the GPU to itself first and releasing it afterward."""
    call_order = []

    fake_pdf = str(tmp_path / "doc.pdf")
    monkeypatch.setattr(pipeline, "find_new_pdfs", lambda input_dir, rebuild: [fake_pdf])

    def fake_nougat_initializer(model_name):
        call_order.append("nougat_initializer")
        return ("fake_processor", "fake_model", "cpu")

    def fake_nougat_extract(**kwargs):
        call_order.append("nougat_extract")
        return ("summary", ["doc.pdf"], [], 5)

    monkeypatch.setattr("visual_parser.nougat_engine.NougatInitializer", fake_nougat_initializer)
    monkeypatch.setattr("visual_parser.text_extractor.nougat_extract_pdfs", fake_nougat_extract)

    monkeypatch.setattr(
        "visual_parser.ollama_local.warm_up_model",
        lambda model_name: call_order.append("ollama_warm_up"),
    )
    monkeypatch.setattr("visual_parser.ollama_local.get_loaded_model_gpu_status", lambda model_name: None)
    monkeypatch.setattr("visual_parser.ollama_local.describe_gpu_status", lambda status: "unknown")

    monkeypatch.setattr(
        pipeline, "extract_pdf_metadata",
        lambda **kwargs: call_order.append("metadata_extraction") or {},
    )
    monkeypatch.setattr(
        pipeline, "describe_figures_for_new_pdfs",
        lambda **kwargs: call_order.append("figure_description"),
    )
    monkeypatch.setattr(pipeline, "mark_as_processed", lambda *a, **k: None)

    config = ParserConfig(
        input_dir=str(tmp_path),
        text_mode="nougat",
        vision_provider="ollama",
        ollama_vision_model="qwen3.6:35b-128k",  # explicit -- skips auto-selection
    )

    pipeline.run_pipeline(config)

    assert "nougat_initializer" in call_order and "ollama_warm_up" in call_order
    assert call_order.index("nougat_initializer") < call_order.index("ollama_warm_up"), (
        "Ollama's model load must happen AFTER Nougat starts, not before"
    )
    assert call_order.index("nougat_extract") < call_order.index("ollama_warm_up"), (
        "Ollama's model load must happen AFTER Nougat finishes, not before"
    )
    assert call_order.index("ollama_warm_up") < call_order.index("metadata_extraction")
    assert call_order.index("ollama_warm_up") < call_order.index("figure_description")


def test_ollama_warm_up_not_deferred_for_lightweight_text_mode(monkeypatch, tmp_path):
    """Lightweight text extraction never touches the GPU, so there's no
    Nougat-vs-Ollama contention to defer for -- warm-up should happen
    immediately, before metadata extraction, same as before this fix."""
    call_order = []

    fake_pdf = str(tmp_path / "doc.pdf")
    monkeypatch.setattr(pipeline, "find_new_pdfs", lambda input_dir, rebuild: [fake_pdf])
    monkeypatch.setattr(
        "visual_parser.text_extractor.lightweight_extract_pdfs",
        lambda **kwargs: ("summary", ["doc.pdf"], [], 5),
    )
    monkeypatch.setattr(
        "visual_parser.ollama_local.warm_up_model",
        lambda model_name: call_order.append("ollama_warm_up"),
    )
    monkeypatch.setattr("visual_parser.ollama_local.get_loaded_model_gpu_status", lambda model_name: None)
    monkeypatch.setattr("visual_parser.ollama_local.describe_gpu_status", lambda status: "unknown")
    monkeypatch.setattr(
        pipeline, "extract_pdf_metadata",
        lambda **kwargs: call_order.append("metadata_extraction") or {},
    )
    monkeypatch.setattr(pipeline, "describe_figures_for_new_pdfs", lambda **kwargs: None)
    monkeypatch.setattr(pipeline, "mark_as_processed", lambda *a, **k: None)

    config = ParserConfig(
        input_dir=str(tmp_path),
        text_mode="lightweight",
        vision_provider="ollama",
        ollama_vision_model="qwen3.6:35b-128k",
    )

    pipeline.run_pipeline(config)

    assert call_order == ["ollama_warm_up", "metadata_extraction"]


def test_ollama_never_contacted_when_nothing_to_do(monkeypatch, tmp_path):
    """Regression test: a no-op run (no new PDFs) must stay a true no-op for
    --vision-provider ollama too, same as it already is for gpt/gemini --
    must not contact Ollama or load a model just to then do nothing with it."""
    monkeypatch.setattr(pipeline, "find_new_pdfs", lambda input_dir, rebuild: [])

    def fail_if_called(*a, **k):
        raise AssertionError("should not be called on a no-op run")

    monkeypatch.setattr("visual_parser.ollama_local.select_best_vision_model", fail_if_called)
    monkeypatch.setattr("visual_parser.ollama_local.warm_up_model", fail_if_called)

    config = ParserConfig(
        input_dir=str(tmp_path),
        text_mode="nougat",
        vision_provider="ollama",
        # no ollama_vision_model -- would normally trigger select_best_vision_model()
    )

    summary = pipeline.run_pipeline(config)
    assert summary["new_pdfs_found"] == 0


def test_ollama_never_contacted_when_nothing_to_do_skip_text(monkeypatch, tmp_path):
    def fail_if_called(*a, **k):
        raise AssertionError("should not be called on a no-op run")

    monkeypatch.setattr("visual_parser.ollama_local.select_best_vision_model", fail_if_called)
    monkeypatch.setattr("visual_parser.ollama_local.warm_up_model", fail_if_called)

    config = ParserConfig(
        input_dir=str(tmp_path),  # empty directory -- no PDFs at all
        skip_text=True,
        vision_provider="ollama",
    )

    pipeline.run_pipeline(config)


def test_ollama_warm_up_not_deferred_for_skip_text(monkeypatch, tmp_path):
    """--skip-text never runs Nougat at all, so there's nothing to defer for."""
    call_order = []
    fake_pdf = tmp_path / "doc.pdf"
    fake_pdf.write_bytes(b"%PDF-1.4 fake")

    monkeypatch.setattr(
        "visual_parser.ollama_local.warm_up_model",
        lambda model_name: call_order.append("ollama_warm_up"),
    )
    monkeypatch.setattr("visual_parser.ollama_local.get_loaded_model_gpu_status", lambda model_name: None)
    monkeypatch.setattr("visual_parser.ollama_local.describe_gpu_status", lambda status: "unknown")
    monkeypatch.setattr(
        pipeline, "extract_pdf_metadata",
        lambda **kwargs: call_order.append("metadata_extraction") or {},
    )
    monkeypatch.setattr(pipeline, "describe_figures_for_new_pdfs", lambda **kwargs: None)
    monkeypatch.setattr(pipeline, "mark_as_processed", lambda *a, **k: None)

    config = ParserConfig(
        input_dir=str(tmp_path),
        skip_text=True,
        vision_provider="ollama",
        ollama_vision_model="qwen3.6:35b-128k",
    )

    pipeline.run_pipeline(config)

    assert call_order == ["ollama_warm_up", "metadata_extraction"]


def test_image_only_folder_is_not_skipped(monkeypatch, tmp_path):
    """Regression test: an image-only folder (zero new/unprocessed PDFs) must
    not hit the early return meant for 'nothing to do' -- found during design
    review, this would have silently skipped all image processing for the
    very case (mixed/image-only folders) this feature is meant to support."""
    monkeypatch.setattr(pipeline, "find_new_pdfs", lambda input_dir, rebuild: [])
    monkeypatch.setattr(pipeline, "find_new_images", lambda input_dir, registry_path, rebuild: ["fake.png"])

    def fail_if_nougat_called(model_name):
        raise AssertionError("Nougat must not load for an image-only pass")

    monkeypatch.setattr("visual_parser.nougat_engine.NougatInitializer", fail_if_nougat_called)
    monkeypatch.setattr(pipeline, "describe_images", lambda **kwargs: ["fake.png"])
    monkeypatch.setattr(pipeline, "mark_as_processed", lambda *a, **k: None)

    config = ParserConfig(
        input_dir=str(tmp_path),
        text_mode="nougat",
        vision_provider="gpt",
        openai_api_key="sk-test",
    )

    summary = pipeline.run_pipeline(config)

    assert summary["new_pdfs_found"] == 0
    assert summary["new_images_found"] == 1
    assert summary["images_written"] == 1
    assert summary["status"] == "success"


def test_image_only_folder_is_not_skipped_in_skip_text_mode(monkeypatch, tmp_path):
    """Same regression as above, but for the entirely separate skip_text
    code path, which has its own independent early-return."""
    monkeypatch.setattr(pipeline, "find_new_images", lambda input_dir, registry_path, rebuild: ["fake.png"])
    monkeypatch.setattr(pipeline, "describe_images", lambda **kwargs: ["fake.png"])
    monkeypatch.setattr(pipeline, "mark_as_processed", lambda *a, **k: None)

    config = ParserConfig(
        input_dir=str(tmp_path),  # empty of PDFs
        skip_text=True,
        vision_provider="gpt",
        openai_api_key="sk-test",
    )

    summary = pipeline.run_pipeline(config)

    assert summary["new_pdfs_found"] == 0
    assert summary["images_written"] == 1


def test_skip_images_flag_skips_image_processing(monkeypatch, tmp_path):
    monkeypatch.setattr(pipeline, "find_new_pdfs", lambda input_dir, rebuild: [])
    monkeypatch.setattr(pipeline, "find_new_images", lambda input_dir, registry_path, rebuild: ["fake.png"])

    def fail_if_called(**kwargs):
        raise AssertionError("describe_images must not be called when skip_images=True")

    monkeypatch.setattr(pipeline, "describe_images", fail_if_called)

    config = ParserConfig(
        input_dir=str(tmp_path),
        vision_provider="gpt",
        openai_api_key="sk-test",
        skip_images=True,
    )

    summary = pipeline.run_pipeline(config)

    assert summary["images_written"] == 0
    assert summary["status"] == "success"


def test_ollama_not_warmed_up_for_image_only_pass_with_skip_images(monkeypatch, tmp_path):
    """Regression test: an image-only folder with --skip-images and a local
    Ollama provider must stay a true no-op -- found during a post-ship review
    pass, _ensure_ollama_vision_model() had no skip_images awareness of its
    own and the early-return check didn't account for skip_images either, so
    this combination used to needlessly load a multi-GB local model for work
    that was about to be skipped entirely."""
    monkeypatch.setattr(pipeline, "find_new_pdfs", lambda input_dir, rebuild: [])
    monkeypatch.setattr(pipeline, "find_new_images", lambda input_dir, registry_path, rebuild: ["fake.png"])

    def fail_if_called(*a, **k):
        raise AssertionError("Ollama must not be contacted when the only work is skipped images")

    monkeypatch.setattr("visual_parser.ollama_local.select_best_vision_model", fail_if_called)
    monkeypatch.setattr("visual_parser.ollama_local.warm_up_model", fail_if_called)
    monkeypatch.setattr(pipeline, "describe_images", fail_if_called)

    config = ParserConfig(
        input_dir=str(tmp_path),
        text_mode="nougat",
        vision_provider="ollama",
        ollama_vision_model="qwen3.6:35b-128k",
        skip_images=True,
    )

    summary = pipeline.run_pipeline(config)

    assert summary["images_written"] == 0
    assert summary["status"] == "success"


def test_ollama_warmed_up_for_image_only_pass_without_skip_images(monkeypatch, tmp_path):
    """Sanity counterpart to the above: when images are NOT skipped, Ollama
    must still be warmed up for an image-only pass (this must keep working)."""
    monkeypatch.setattr(pipeline, "find_new_pdfs", lambda input_dir, rebuild: [])
    monkeypatch.setattr(pipeline, "find_new_images", lambda input_dir, registry_path, rebuild: ["fake.png"])

    warmed_up = []
    monkeypatch.setattr(
        "visual_parser.ollama_local.warm_up_model",
        lambda model_name: warmed_up.append(model_name),
    )
    monkeypatch.setattr("visual_parser.ollama_local.get_loaded_model_gpu_status", lambda model_name: None)
    monkeypatch.setattr("visual_parser.ollama_local.describe_gpu_status", lambda status: "unknown")
    monkeypatch.setattr(pipeline, "describe_images", lambda **kwargs: ["fake.png"])
    monkeypatch.setattr(pipeline, "mark_as_processed", lambda *a, **k: None)

    config = ParserConfig(
        input_dir=str(tmp_path),
        text_mode="nougat",
        vision_provider="ollama",
        ollama_vision_model="qwen3.6:35b-128k",
    )

    summary = pipeline.run_pipeline(config)

    assert warmed_up == ["qwen3.6:35b-128k"]
    assert summary["images_written"] == 1


def test_rebuild_gathers_everything_and_clears_before_discovery(monkeypatch, tmp_path):
    """--rebuild must gather every PDF/image basename currently in input_dir
    and clear them via kb_redo.redo_entries() BEFORE the main discovery
    calls run -- not force individual write functions to bypass their own
    resume checks (the old approach, which produced duplicate rows)."""
    call_order = []

    def fake_find_new_pdfs(input_dir, rebuild):
        call_order.append(("find_new_pdfs", rebuild))
        return ["a.pdf"] if rebuild else []

    def fake_find_new_images(input_dir, registry_path, rebuild):
        call_order.append(("find_new_images", rebuild))
        return ["b.png"] if rebuild else []

    monkeypatch.setattr(pipeline, "find_new_pdfs", fake_find_new_pdfs)
    monkeypatch.setattr(pipeline, "find_new_images", fake_find_new_images)

    captured = {}

    def fake_redo_entries(output_dir, names):
        call_order.append(("redo_entries", set(names)))
        captured["names"] = set(names)
        return {
            "cleared": sorted(names), "not_found": [], "jsonl_files": [], "registries": [],
            "names_requested": sorted(names),
            "totals": {"rows_removed": 0, "registry_entries_removed": 0},
        }

    monkeypatch.setattr("visual_parser.kb_redo.redo_entries", fake_redo_entries)

    config = ParserConfig(
        input_dir=str(tmp_path),
        vision_provider="gpt",
        openai_api_key="sk-test",
        rebuild=True,
    )

    summary = pipeline.run_pipeline(config)

    assert captured["names"] == {"a.pdf", "b.png"}
    assert summary["redone_basenames"] == ["a.pdf", "b.png"]
    # Gather calls (rebuild=True) happen, then clearing, then the real
    # discovery calls (rebuild=False) happen strictly after.
    assert call_order[0] == ("find_new_pdfs", True)
    assert call_order[1] == ("find_new_images", True)
    assert call_order[2] == ("redo_entries", {"a.pdf", "b.png"})
    assert ("find_new_images", False) in call_order[3:]


def test_redo_names_clears_only_the_named_entries(monkeypatch, tmp_path):
    """--redo NAME (independent of --rebuild) must reach kb_redo.redo_entries()
    with exactly the requested names, nothing gathered from the directory."""
    monkeypatch.setattr(pipeline, "find_new_pdfs", lambda input_dir, rebuild: [])
    monkeypatch.setattr(pipeline, "find_new_images", lambda input_dir, registry_path, rebuild: [])

    captured = {}

    def fake_redo_entries(output_dir, names):
        captured["names"] = set(names)
        return {
            "cleared": sorted(names), "not_found": [], "jsonl_files": [], "registries": [],
            "names_requested": sorted(names),
            "totals": {"rows_removed": 0, "registry_entries_removed": 0},
        }

    monkeypatch.setattr("visual_parser.kb_redo.redo_entries", fake_redo_entries)

    config = ParserConfig(
        input_dir=str(tmp_path),
        vision_provider="gpt",
        openai_api_key="sk-test",
        redo_names=["doc1.pdf", "diagram2.png"],
    )

    summary = pipeline.run_pipeline(config)

    assert captured["names"] == {"doc1.pdf", "diagram2.png"}
    assert summary["redone_basenames"] == ["diagram2.png", "doc1.pdf"]


def test_rebuild_produces_no_duplicate_rows_end_to_end(monkeypatch, tmp_path):
    """The actual bug this whole mechanism exists to fix: --rebuild must not
    leave an old row and a new row both present. Real KB files/registry on
    disk; only the heavy PDF engine and vision call are mocked."""
    (tmp_path / "doc.pdf").write_bytes(b"%PDF-1.4 fake")
    (tmp_path / "01_chunks_kb.jsonl").write_text(
        json.dumps({"source": "doc.pdf", "page": 1, "content": "old chunk", "chunk_index": 0,
                    "document_id": "x", "chunk_id": "x:p1:c0", "extractor": "lightweight"}) + "\n",
        encoding="utf-8",
    )
    (tmp_path / "04_processed_pdfs.txt").write_text("doc.pdf\n", encoding="utf-8")

    def fake_lightweight_extract(**kwargs):
        from visual_parser.jsonl_writer import append_to_jsonl
        append_to_jsonl(
            os.path.join(kwargs["output_dir"], "01_chunks_kb.jsonl"),
            [{"source": "doc.pdf", "page": 1, "content": "new chunk", "chunk_index": 0,
              "document_id": "x", "chunk_id": "x:p1:c0", "extractor": "lightweight"}],
        )
        return ("summary", ["doc.pdf"], [], 1)

    monkeypatch.setattr("visual_parser.text_extractor.lightweight_extract_pdfs", fake_lightweight_extract)
    monkeypatch.setattr(pipeline, "describe_figures_for_new_pdfs", lambda **kwargs: None)
    monkeypatch.setattr(pipeline, "extract_pdf_metadata", lambda **kwargs: {})

    config = ParserConfig(
        input_dir=str(tmp_path),
        text_mode="lightweight",
        vision_provider="gpt",
        openai_api_key="sk-test",
        rebuild=True,
    )

    pipeline.run_pipeline(config)

    chunk_lines = [
        line for line in (tmp_path / "01_chunks_kb.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    assert len(chunk_lines) == 1  # not 2 -- old row was cleared, not duplicated
    assert json.loads(chunk_lines[0])["content"] == "new chunk"

    registry = (tmp_path / "04_processed_pdfs.txt").read_text(encoding="utf-8").split()
    assert registry == ["doc.pdf"]  # re-marked processed after reprocessing, not duplicated either


def test_failed_image_not_marked_processed_via_pipeline(monkeypatch, tmp_path):
    """describe_images() returns only the basenames it actually wrote a row
    for -- the pipeline must mark only those as processed, not the full
    discovered list, or a failed image would silently vanish from future
    find_new_images() output with no row ever written."""
    monkeypatch.setattr(pipeline, "find_new_pdfs", lambda input_dir, rebuild: [])
    monkeypatch.setattr(
        pipeline, "find_new_images",
        lambda input_dir, registry_path, rebuild: ["good.png", "corrupt.png"],
    )
    monkeypatch.setattr(pipeline, "describe_images", lambda **kwargs: ["good.png"])

    mark_calls = []
    monkeypatch.setattr(
        pipeline, "mark_as_processed",
        lambda registry_path, names: mark_calls.append(list(names)),
    )

    config = ParserConfig(
        input_dir=str(tmp_path),
        vision_provider="gpt",
        openai_api_key="sk-test",
    )

    summary = pipeline.run_pipeline(config)

    assert summary["images_written"] == 1
    assert any(names == ["good.png"] for names in mark_calls), mark_calls
    assert not any("corrupt.png" in names for names in mark_calls)
