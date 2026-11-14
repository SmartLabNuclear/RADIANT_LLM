# Changelog

All notable changes to `visual-parser`, newest first. Dates are PyPI upload dates.

## 2.2.5 - 2026-11-13

Changed (upgrade note)
- No copyleft dependencies. PyMuPDF (AGPL-3.0) is replaced by pypdfium2 (Apache-2.0 or BSD-3-Clause) for page rendering and the lightweight text layer, and python-Levenshtein (GPL-2.0-or-later) by RapidFuzz (MIT) for Nougat's post-processing. `pypdf` is now a declared dependency: the PyPDFLoader fallback needs it, but nothing installed it. The Docker image is built from `python:3.11-slim`; the older base image it started from carried PyMuPDF, MuPDF (`libmupdf-dev`) and Levenshtein in its layers.
- Output differs slightly from 2.2.4. Page images (and so Nougat text and figure descriptions), lightweight text, chunk contents and some `chunk_id`s can change. Rows already in a knowledge base are untouched; a document parsed again gets the new output. To reproduce results made with 2.2.4 or earlier, use `pip install visual-parser==2.2.4`. Each `03_metadata_kb.jsonl` `parser` block now records `pdf_engine` (for example `pypdfium2 5.15.2 (PDFium 8149)`); rows without it were made with PyMuPDF.
- PDF reading and rendering are serialised behind one lock, because PDFium is not thread-safe. Nougat inference and the vision-model calls still run in parallel across `--max-workers`.

Fixed
- A failure in Nougat's post-processing no longer sends the whole PDF to lightweight extraction. 2.2.4 caught only `AttributeError` there; any other error (for example the Levenshtein library being absent) made the PDF fail and fall back. Post-processing now keeps the raw decoded text and logs a warning.

Comparison with 2.2.4
Ten documents (507 pages, 2,571 chunks): the SAM Theory Manual and User Guide, the AutoSAM paper and the ASAP-SAM summary, the ABTR and MSRE source reports, two tech reports, a Monte Carlo course and one scanned textbook page. PyMuPDF 2.1 against pypdfium2 5.15.2 on Windows, transformers 5.22.2.
- Lightweight text, per page (Indel similarity of whitespace-normalised text): mean 0.994, median 0.998, 5th percentile 0.984, minimum 0.717; 84 pages below 0.99 and 2 below 0.90. Page counts match for every document.
- Chunks: 2,648 now against 2,571 before (+3.0%). 99.1% of the old chunk IDs still exist. The text of 16% of the chunks is identical; the rest differ in line breaks or spacing.
- Page images at 96 dpi (26 pages): the same pixel size on all of them; mean absolute pixel difference 2.5 on a 0-255 scale (range 0.2 to 7.2).
- Nougat on 8 of those pages, same model and same post-processing: four identical; three within 2.5% (similarity 0.9962, 0.9983, 0.9758); one near-blank page differs (0.31, 81 against 15 characters). The differences are OCR variants such as a gamma read as "y", or "Example 3-4" against "Example 3.4:".
- Speed: pypdfium2 was not faster here. Reading the text layer of all 507 pages took 1.1 s with PyMuPDF and 2.7 s with pypdfium2 (a few milliseconds per page either way), and the lock means concurrent workers do not speed up PDF reading. Nougat inference and the vision calls, which dominate a run, are unaffected.

Known differences in lightweight text
- PDFium puts spaces between tokens that a PDF draws as separate text runs. The engine rejoins the cases that matter for SAM input and citations (`[ EOS ]` to `[EOS]`, `[ 12 ]` to `[12]`, `2.151 E -02` to `2.151E-02`; 129 of the 507 pages had them) and turns the control character PDFium emits for a hyphen at a line end back into `-`. Other spacing differences remain, for example letter-spaced slide titles come out as `Beg i n n er` and some mathematical spacing differs from MuPDF's.
- Some PDFs hold small-font duplicate text that PDFium reads and MuPDF leaves out: on 2 of the 507 pages (both in the SAM Theory Manual) passages appear twice, plus a running header.
- Math-font bracket pieces on equation pages are control characters, now removed; the blank lines they leave make the splitter produce a few more, smaller chunks.

Added
- `visual_parser/pdf_engine.py`: the one module that touches a PDF library.
- Tests: the engine on rotated, cropped, encrypted (empty user password), JPEG-carrying and non-ASCII-named PDFs, and under four threads; the Nougat post-processing against outputs recorded with 2.2.4 and Levenshtein installed, and with Levenshtein absent; a guard that fails if a copyleft package returns to the code, the declared dependencies or the Dockerfile.

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
