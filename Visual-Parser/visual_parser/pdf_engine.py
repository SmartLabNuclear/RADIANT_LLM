"""
pdf_engine.py — the one place Visual-Parser touches a PDF library.

Backed by pypdfium2 (PDFium; BSD-3-Clause / Apache-2.0). Every other module
asks this one for page images, page text, embedded images and page counts.

PDFium is not thread-safe, and Visual-Parser extracts PDFs on a thread pool
(``--max-workers``, default 4). Calling it from several threads at once
crashes the process or silently returns truncated text. Every PDFium call
therefore runs under one process-wide lock (``PDFIUM_LOCK``). Only the PDFium
work is serialised: PNG encoding, Nougat inference and the vision-model calls
stay outside the lock and still run in parallel.

Typical use::

    with open_pdf(path) as pdf:
        for i in range(pdf.page_count):
            png = pdf.render_png(i, dpi=200)
            text = pdf.page_text(i)
"""

from __future__ import annotations

import io
import logging
import re
import threading

import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
from PIL import Image

logger = logging.getLogger(__name__)

# Re-entrant so one engine method can call another while holding it.
PDFIUM_LOCK = threading.RLock()

# 1 PDF point = 1/72 inch, so scale = dpi / 72 (PDFium renders at scale 1 == 72 dpi).
_POINTS_PER_INCH = 72.0


# --- text tidying ---------------------------------------------------------
#
# PDFium's text layer differs from MuPDF's (the engine through 2.2.4) in ways
# that matter for retrieval over technical documents:
#   * an end-of-line hyphen comes out as the control character U+0002
#     ("model\x02ing"), where MuPDF gave "model-";
#   * tokens drawn as separate text runs get spaces between them: the SAM input
#     syntax "[EOS]" arrives as "[ EOS ]" and "2.151E-02" as "2.151 E -02".
# tidy_text() undoes exactly those three things and nothing else.

_CONTROL_CHARS = re.compile(r"[\x00-\x08\x0b-\x1f\x7f]")   # all C0 controls except \t and \n
_SPACED_BRACKETS = re.compile(r"\[ ([^\[\]\n]{1,80}?) \]")
_SPACED_EXPONENT = re.compile(r"(?<=\d) E ([+-])(?=\d)")


def tidy_text(text: str) -> str:
    """Normalise one page of PDFium text (see the notes above)."""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = text.replace("\x02", "-")                       # hyphen at a line end, as MuPDF wrote it
    text = _CONTROL_CHARS.sub("", text)
    text = _SPACED_BRACKETS.sub(r"[\1]", text)
    text = _SPACED_EXPONENT.sub(r"E\1", text)
    return text


def engine_name() -> str:
    """Human-readable engine and version, for the per-document ``parser`` provenance block."""
    version = str(getattr(pdfium, "PYPDFIUM_INFO", "unknown"))
    build = getattr(getattr(pdfium, "PDFIUM_INFO", None), "build", None)
    return f"pypdfium2 {version}" + (f" (PDFium {build})" if build else "")


class PdfFile:
    """An open PDF. Use through :func:`open_pdf` so the file is always closed."""

    def __init__(self, path: str):
        with PDFIUM_LOCK:
            self._pdf = pdfium.PdfDocument(str(path))
            self._count = len(self._pdf)
        self.path = str(path)

    @property
    def page_count(self) -> int:
        return self._count

    # -- context management -------------------------------------------------

    def close(self) -> None:
        with PDFIUM_LOCK:
            pdf, self._pdf = self._pdf, None
            if pdf is not None:
                pdf.close()

    def __enter__(self) -> PdfFile:
        return self

    def __exit__(self, *exc) -> None:
        self.close()

    # -- page images --------------------------------------------------------

    def render_pil(self, index: int, dpi: int = 96) -> Image.Image:
        """Render page *index* (0-based) to an RGB image at *dpi*."""
        with PDFIUM_LOCK:
            page = self._pdf[index]
            try:
                bitmap = page.render(scale=dpi / _POINTS_PER_INCH)
                try:
                    # copy(): the PIL image must not point into PDFium-owned memory
                    # once the lock is released and the bitmap is closed.
                    return bitmap.to_pil().copy()
                finally:
                    bitmap.close()   # explicit, under the lock: never left to the garbage collector
            finally:
                page.close()

    def render_png(self, index: int, dpi: int = 96) -> bytes:
        """Render page *index* to PNG bytes. The PNG encoding runs outside the lock."""
        image = self.render_pil(index, dpi)
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        return buffer.getvalue()

    # -- page text ----------------------------------------------------------

    def page_text(self, index: int) -> str:
        """Text layer of page *index*: ``\\n`` line endings, no control characters, and the
        token spacing fixes of :func:`tidy_text`."""
        with PDFIUM_LOCK:
            page = self._pdf[index]
            try:
                textpage = page.get_textpage()
                try:
                    text = textpage.get_text_bounded()
                finally:
                    textpage.close()
            finally:
                page.close()
        return tidy_text(text)

    # -- embedded images ----------------------------------------------------

    def page_images(self, index: int) -> list[Image.Image]:
        """Embedded raster images on page *index* (used only by the optional equation OCR)."""
        images: list[Image.Image] = []
        with PDFIUM_LOCK:
            page = self._pdf[index]
            try:
                for obj in page.get_objects(filter=[pdfium_c.FPDF_PAGEOBJ_IMAGE]):
                    try:
                        # A "foreign" bitmap: PDFium owns it and frees it with the page,
                        # so (unlike render bitmaps) it must not be closed here.
                        images.append(obj.get_bitmap().to_pil().copy())
                    except Exception as exc:  # one undecodable image must not lose the page
                        logger.debug("Skipping an embedded image on page %d of %s: %s", index + 1, self.path, exc)
            finally:
                page.close()
        return images


def open_pdf(path: str) -> PdfFile:
    """Open *path*. Raises (e.g. ``pypdfium2.PdfiumError``) when the file cannot be opened."""
    return PdfFile(path)
