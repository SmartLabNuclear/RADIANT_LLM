"""
text_extractor.py — Two text-extraction engines for PDF pages.

Nougat (default)
    Uses the Facebook Nougat transformer to OCR each page rendered as an image.
    Best for: scanned PDFs, PDFs with equations, complex layouts.
    Requires: nougat_engine.NougatInitializer() result to be passed in.

Lightweight (fast)
    Uses PyMuPDF's native text layer (fitz.Page.get_text) with a PyPDFLoader
    fallback.  Also extracts embedded equations via regex + pytesseract.
    Best for: born-digital PDFs where text is already machine-readable.
    Requires: only PyMuPDF + langchain_community; no GPU.

Both engines:
    • Walk only the PDFs listed in *only_process_these*
    • Skip PDFs already recorded in 04_processed_pdfs.txt
    • Chunk extracted text with RecursiveCharacterTextSplitter
    • Write chunks to 01_chunks_kb.jsonl
    • Return the list of successfully processed PDF basenames
"""

from __future__ import annotations

import io
import logging
import os
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Optional, Tuple

import fitz  # PyMuPDF
from PIL import Image

from visual_parser.jsonl_writer import append_to_jsonl, make_document_id
from visual_parser.pdf_tracker import load_processed_pdfs

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Shared text-splitter factory
# ---------------------------------------------------------------------------

def _make_splitter(chunk_size: int = 500, chunk_overlap: int = 100):
    try:
        from langchain_text_splitters import RecursiveCharacterTextSplitter
    except ImportError:
        from langchain.text_splitter import RecursiveCharacterTextSplitter  # legacy fallback
    return RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", " ", ""],
    )


# ===========================================================================
# ENGINE 1 — Nougat (transformer-based OCR)
# ===========================================================================

def nougat_extract_pdfs(
    only_process_these: List[str],
    output_dir: str,
    processor,
    model,
    device: str,
    chunk_size: int = 500,
    chunk_overlap: int = 100,
    max_workers: int = 4,
) -> Tuple[str, List[str], List[str], int]:
    """
    Extract text from each PDF in *only_process_these* using the Nougat model,
    chunk it, and append chunks to ``01_chunks_kb.jsonl`` in *output_dir*.

    Args:
        only_process_these: Full paths of PDFs to attempt.
        output_dir:         Directory where JSONL files are written.
        processor:          Nougat AutoProcessor instance.
        model:              Nougat VisionEncoderDecoderModel instance.
        device:             ``'cuda'`` or ``'cpu'``.
        chunk_size:         Characters per chunk.
        chunk_overlap:      Overlap between adjacent chunks.
        max_workers:        Thread-pool size for parallel PDF processing.

    Returns:
        (summary_message, successful_basenames, failed_basenames, chunks_written_this_run)
    """
    from transformers import StoppingCriteriaList

    from visual_parser.nougat_engine import RasterizePaper, StoppingCriteriaScores

    registry_path  = os.path.join(output_dir, "04_processed_pdfs.txt")
    processed_set  = set(load_processed_pdfs(registry_path))
    pdfs_to_run    = [p for p in only_process_these if os.path.basename(p) not in processed_set]

    if not pdfs_to_run:
        return "No new PDFs to process (Nougat).", [], [], 0

    text_splitter = _make_splitter(chunk_size, chunk_overlap)

    # -----------------------------------------------------------------------
    def _process_one(pdf_path: str) -> Tuple[List[Dict], bool]:
        chunks: List[Dict] = []
        pdf_name = os.path.basename(pdf_path)
        document_id = make_document_id(pdf_name)

        try:
            images = RasterizePaper(pdf=pdf_path, return_pil=True)
            if not images:
                logger.warning("No images rasterized for %s", pdf_name)
                return [], False

            for page_num, image_bytes_obj in enumerate(images):
                image        = Image.open(io.BytesIO(image_bytes_obj.getvalue()))
                try:
                    pixel_values = processor(
                        images=image,
                        return_tensors="pt",
                        do_crop_margin=False,
                    ).pixel_values.to(device)
                except TypeError:
                    pixel_values = processor(
                        images=image,
                        return_tensors="pt",
                    ).pixel_values.to(device)

                outputs = model.generate(
                    pixel_values,
                    min_length=1,
                    max_length=3584,
                    bad_words_ids=[[processor.tokenizer.unk_token_id]],
                    return_dict_in_generate=True,
                    output_scores=True,
                    stopping_criteria=StoppingCriteriaList([StoppingCriteriaScores()]),
                )

                generated_text = processor.batch_decode(outputs[0], skip_special_tokens=True)[0]
                # post_process_generation was removed in newer tokenizers builds;
                # fall back to the raw decoded string when the method is absent.
                try:
                    generated_text = processor.post_process_generation(
                        generated_text, fix_markdown=False
                    )
                except AttributeError:
                    pass

                for i, chunk_text in enumerate(text_splitter.split_text(generated_text)):
                    chunks.append({
                        "source":      pdf_name,
                        "page":        page_num + 1,
                        "content":     chunk_text,
                        "chunk_index": i,
                        "document_id": document_id,
                        "chunk_id":    f"{document_id}:p{page_num+1}:c{i}",
                        "extractor":   "nougat",
                    })

        except Exception as exc:
            logger.error("Nougat failed on %s: %s", pdf_name, exc)
            return [], False

        if not chunks:
            logger.error("Nougat produced no chunks for %s.", pdf_name)
            return [], False

        return chunks, True
    # -----------------------------------------------------------------------

    chunks_path          = os.path.join(output_dir, "01_chunks_kb.jsonl")
    total_chunks         = 0
    processed_basenames: List[str] = []
    failed_basenames:    List[str] = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(_process_one, p): p for p in pdfs_to_run}
        for future in as_completed(futures):
            pdf_path = futures[future]
            try:
                result, succeeded = future.result()
                if succeeded and result:
                    # Flush this PDF's chunks immediately — safe against crashes
                    append_to_jsonl(chunks_path, result)
                    total_chunks += len(result)
                    processed_basenames.append(os.path.basename(pdf_path))
                else:
                    failed_basenames.append(os.path.basename(pdf_path))
            except Exception as exc:
                logger.error("Error collecting result for %s: %s", pdf_path, exc)
                failed_basenames.append(os.path.basename(pdf_path))

    summary = (
        f"Nougat extraction complete. "
        f"{len(processed_basenames)} PDF(s) processed -> {total_chunks} chunks. "
        f"{len(failed_basenames)} PDF(s) failed."
    )
    return summary, processed_basenames, failed_basenames, total_chunks


# ===========================================================================
# ENGINE 2 — Lightweight (PyMuPDF native text layer)
# ===========================================================================

def _extract_equations(text: str, images: list) -> List[str]:
    """
    Extract LaTeX/math-like patterns from *text* and (optionally) OCR *images*.
    """
    patterns = [
        (r'\$\$(.*?)\$\$',                         True),
        (r'\$(.*?)\$',                             True),
        (r'\w+\^\w+|\w+\^\{.*?\}',                False),
        (r'\\frac\{.*?\}\{.*?\}',                  False),
        (r'\\int_.*?\^.*? ',                       False),
        (r'\\log\(.*?\)|\\ln\(.*?\)',              False),
        (r'\\begin\{.*?matrix\}(.*?)\\end\{.*?matrix\}', True),
        (r'\\sum_.*?\^.*?',                        False),
        (r'\\prod_.*?\^.*?',                       False),
        (r'\\frac{d.*?}{d.*?}|\\partial.*?',       False),
        (r'\\[a-zA-Z]+',                           False),
        (r'\\lim_.*?',                             False),
        (r'\\vec{.*?}|\\mathbf{.*?}',              False),
        (r'\\in|\\cup|\\cap|\\forall|\\exists',   False),
        (r'\\langle.*?\\rangle',                   False),
    ]
    equations: List[str] = []
    for pattern, is_latex in patterns:
        for match in re.findall(pattern, text, re.DOTALL):
            equations.append(f"$$ {match} $$" if is_latex else match)

    for img in images:
        try:
            import pytesseract
            ocr_text = pytesseract.image_to_string(img)
            for pattern, is_latex in patterns:
                for match in re.findall(pattern, ocr_text, re.DOTALL):
                    equations.append(f"$$ {match} $$" if is_latex else match)
        except Exception:
            pass  # pytesseract is optional

    return equations


def lightweight_extract_pdfs(
    only_process_these: List[str],
    output_dir: str,
    chunk_size: int = 500,
    chunk_overlap: int = 100,
    max_workers: int = 4,
) -> Tuple[str, List[str], List[str], int]:
    """
    Extract text from each PDF in *only_process_these* using PyMuPDF's native
    text layer (fast, no GPU required), chunk it, and append to
    ``01_chunks_kb.jsonl`` in *output_dir*.

    Falls back to LangChain's PyPDFLoader when PyMuPDF fails on a file.

    Args:
        only_process_these: Full paths of PDFs to attempt.
        output_dir:         Directory where JSONL files are written.
        chunk_size:         Characters per chunk.
        chunk_overlap:      Overlap between adjacent chunks.
        max_workers:        Thread-pool size for parallel PDF processing.

    Returns:
        (summary_message, successful_basenames, failed_basenames, chunks_written_this_run)
    """
    from io import BytesIO

    registry_path  = os.path.join(output_dir, "04_processed_pdfs.txt")
    processed_set  = set(load_processed_pdfs(registry_path))
    pdfs_to_run    = [p for p in only_process_these if os.path.basename(p) not in processed_set]

    if not pdfs_to_run:
        return "No new PDFs to process (lightweight).", [], [], 0

    text_splitter = _make_splitter(chunk_size, chunk_overlap)

    # -----------------------------------------------------------------------
    def _extract_images_from_page(page) -> list:
        imgs = []
        for img_info in page.get_images(full=True):
            xref = img_info[0]
            try:
                base_image  = page.parent.extract_image(xref)
                image_bytes = base_image.get("image", b"")
                if image_bytes:
                    imgs.append(Image.open(BytesIO(image_bytes)))
            except Exception:
                pass
        return imgs

    def _process_one(pdf_path: str) -> Tuple[List[Dict], bool]:
        chunks: List[Dict] = []
        pdf_name    = os.path.basename(pdf_path)
        document_id = make_document_id(pdf_name)
        start       = time.time()

        try:
            doc = fitz.open(pdf_path)
            for page_num in range(len(doc)):
                page     = doc.load_page(page_num)
                text     = page.get_text("text")
                images   = _extract_images_from_page(page)
                equations = _extract_equations(text, images)

                eq_text   = "\n\n".join(equations)
                full_text = (
                    f"{text.strip()}\n\nExtracted Equations:\n{eq_text}"
                    if equations else text.strip()
                )

                for i, chunk_text in enumerate(text_splitter.split_text(full_text)):
                    chunks.append({
                        "source":      pdf_name,
                        "page":        page_num + 1,
                        "content":     chunk_text,
                        "chunk_index": i,
                        "document_id": document_id,
                        "chunk_id":    f"{document_id}:p{page_num+1}:c{i}",
                        "extractor":   "lightweight",
                    })
            doc.close()

        except Exception as exc:
            logger.warning("PyMuPDF failed on %s (%s) — trying PyPDFLoader.", pdf_name, exc)
            try:
                from langchain_community.document_loaders import PyPDFLoader
                loader = PyPDFLoader(file_path=pdf_path)
                for page_num, doc_obj in enumerate(loader.load(), start=1):
                    for i, chunk_text in enumerate(
                        text_splitter.split_text(doc_obj.page_content or "")
                    ):
                        chunks.append({
                            "source":      pdf_name,
                            "page":        page_num,
                            "content":     chunk_text,
                            "chunk_index": i,
                            "document_id": document_id,
                            "chunk_id":    f"{document_id}:p{page_num}:c{i}",
                            "extractor":   "pypdf",
                        })
            except Exception as exc2:
                logger.error("Both extractors failed on %s: %s", pdf_name, exc2)
                return [], False

        elapsed = time.time() - start
        if not chunks:
            logger.error(
                "Lightweight extraction produced no chunks for %s. "
                "This usually means the PDF is image-only/scanned and has no usable text layer.",
                pdf_name,
            )
            return [], False
        logger.info("Lightweight: %s processed in %.1f s (%d chunks)", pdf_name, elapsed, len(chunks))
        return chunks, True
    # -----------------------------------------------------------------------

    chunks_path          = os.path.join(output_dir, "01_chunks_kb.jsonl")
    total_chunks         = 0
    processed_basenames: List[str] = []
    failed_basenames:    List[str] = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(_process_one, p): p for p in pdfs_to_run}
        for future in as_completed(futures):
            pdf_path = futures[future]
            try:
                result, succeeded = future.result()
                if succeeded and result:
                    # Flush this PDF's chunks immediately — safe against crashes
                    append_to_jsonl(chunks_path, result)
                    total_chunks += len(result)
                    processed_basenames.append(os.path.basename(pdf_path))
                else:
                    failed_basenames.append(os.path.basename(pdf_path))
            except Exception as exc:
                logger.error("Error collecting result for %s: %s", pdf_path, exc)
                failed_basenames.append(os.path.basename(pdf_path))

    summary = (
        f"Lightweight extraction complete. "
        f"{len(processed_basenames)} PDF(s) processed -> {total_chunks} chunks. "
        f"{len(failed_basenames)} PDF(s) failed."
    )
    return summary, processed_basenames, failed_basenames, total_chunks
