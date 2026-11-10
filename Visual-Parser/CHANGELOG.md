# Changelog

All notable changes to `visual-parser`, newest first. Dates are PyPI upload dates.

## 2.2.4 - 2026-10-20

Added
- Per-document provenance, additive (no existing field or ID changed). Every `02_visuals_kb.jsonl` and `image_descriptions_kb.jsonl` row carries `vision_provider` and `vision_model`; every `03_metadata_kb.jsonl` row carries a `parser` block with the `visual_parser` version, `parsed_at`, `text_engine` (`nougat`, `lightweight` or `skipped`), `text_fallback`, the resolved `vision_model`, and the run's chunking/context settings. Older rows simply lack these fields.
- Mixed-model guard: if a PDF already has figures described under a different `vision_model` than the current run's, its remaining pages are skipped entirely (not partially re-described), a clear error names both models, and its basename is reported back. Reprocess it with `--redo NAME`. Pre-upgrade rows with no recorded model are treated as unknown, not as a mismatch. The summary returned by `run_pipeline()` gains `figure_model_mismatches`.

Fixed
- When `--output-dir` differed from `--input-dir`, `find_new_pdfs()` looked for the processed-PDF registry in the input folder while the pipeline wrote it to the output folder, so every run after the first treated every PDF as new and repeated the per-PDF metadata vision call (and reloaded Nougat/Ollama). It now uses the registry in the output folder; no KB rows were ever duplicated.

## 2.2.3 - 2026-10-08

Changed (upgrade note)
- The standalone-image KB file was renamed from `image_descriptions.jsonl` to `image_descriptions_kb.jsonl`, matching the `NN_name_kb.jsonl` convention of the other KB files. Existing data is not migrated: the resume check only looks at the new name, so images already described in an old file would be described again. If you built a KB with 2.2.1 or 2.2.2, rename the file before re-running: `image_descriptions.jsonl` -> `image_descriptions_kb.jsonl`. Standalone image support first shipped in 2.2.1, so earlier versions are not affected.

## 2.2.2 - 2026-10-06

Added
- `--nougat-crop-margin` (env `VISUAL_PARSER_NOUGAT_CROP_MARGIN`), off by default: passes `do_crop_margin` to Nougat's image processor. It is off by default because autocropping whitespace margins can crop into real content on unusual page layouts.

## 2.2.1 - 2026-10-05

Added
- Standalone image support: image files found alongside the PDFs in `--input-dir` are detected by extension and described one holistic description per image, written to `image_descriptions.jsonl` (renamed in 2.2.3). Disable with `--skip-images`. `--redo` and `--rebuild` now cover images too.

## 2.2.0 - 2026-10-01

Added
- Local Ollama vision provider, with GPU-aware model auto-selection.

Changed
- Figure description now runs concurrently; before, the vision model was called one page at a time.

## 2.1.0 - 2026-09-24

Added
- Portkey gateway support and a live model catalog (`--list-models`); GPU/CUDA Docker support.

Changed
- Packaging modernized.
