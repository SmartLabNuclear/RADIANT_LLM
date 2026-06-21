"""
nougat_engine.py — Nougat model initialisation, PDF rasterisation, and
                   the stopping-criteria classes from the original Nougat paper.

Extracted and cleaned from utils/nougat_helpers.py.
No chatbot, no LangChain, no Dash dependencies.
"""

from __future__ import annotations

import io
import logging
from collections import defaultdict
from pathlib import Path
from typing import List, Optional

import fitz  # PyMuPDF
import torch
from PIL import Image
from transformers import (
    AutoProcessor,
    StoppingCriteria,
    StoppingCriteriaList,
    VisionEncoderDecoderModel,
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Model initialisation
# ---------------------------------------------------------------------------

def _normalize_nougat_processor(processor) -> None:
    """
    Apply compatibility fixes for processor configs across transformers versions.

    Some newer processor/image-processor builds reject ``None`` for boolean
    fields that older Nougat configs may omit. Normalize those fields to safe
    defaults after loading the processor.
    """
    image_processor = getattr(processor, "image_processor", None)
    if image_processor is None:
        return

    fixed_fields = []
    for attr_name in dir(image_processor):
        if not attr_name.startswith("do_"):
            continue
        try:
            attr_value = getattr(image_processor, attr_name)
        except Exception:
            continue
        if attr_value is None:
            try:
                setattr(image_processor, attr_name, False)
                fixed_fields.append(attr_name)
            except Exception:
                continue

    if fixed_fields:
        logger.warning(
            "[NOUGAT] Normalized image-processor boolean flags with None values: %s",
            ", ".join(sorted(fixed_fields)),
        )

def NougatInitializer(model_name: str = "facebook/nougat-small"):
    """
    Load the Nougat processor and model onto the best available device.

    If ``HF_TOKEN`` is present in the environment (e.g. loaded from .env),
    the function authenticates with the HuggingFace Hub before downloading
    weights, which suppresses the unauthenticated-request warning and gives
    higher rate limits.

    Returns:
        (processor, model, device) tuple ready for inference.
    """
    import os
    hf_token = os.environ.get("HF_TOKEN") or os.environ.get("HUGGING_FACE_HUB_TOKEN")
    if hf_token:
        try:
            import huggingface_hub
            huggingface_hub.login(token=hf_token, add_to_git_credential=False)
            logger.info("[NOUGAT] Authenticated with HuggingFace Hub.")
        except Exception as exc:
            logger.warning("[NOUGAT] HF login attempt failed (non-fatal): %s", exc)
    else:
        logger.info(
            "[NOUGAT] No HF_TOKEN found — downloads may be rate-limited. "
            "Add HF_TOKEN to your .env to silence this."
        )

    print(f"[NOUGAT] Loading model: {model_name} …")
    processor = AutoProcessor.from_pretrained(model_name, token=hf_token)
    _normalize_nougat_processor(processor)
    model     = VisionEncoderDecoderModel.from_pretrained(model_name, token=hf_token)
    device    = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)
    print(f"[NOUGAT] Model loaded on {device}.")
    return processor, model, device


# ---------------------------------------------------------------------------
# PDF rasterisation
# ---------------------------------------------------------------------------

def RasterizePaper(
    pdf: Path | str,
    outpath: Optional[Path] = None,
    dpi: int = 96,
    return_pil: bool = False,
    pages: Optional[range] = None,
) -> Optional[List[io.BytesIO]]:
    """
    Rasterize each page of *pdf* to PNG.

    Args:
        pdf:        Path to the PDF file.
        outpath:    Directory to write ``01.png``, ``02.png`` … files.
                    When *None*, ``return_pil`` is forced to True.
        dpi:        Rendering resolution (96 dpi for Nougat, 200 for figures).
        return_pil: Return a list of :class:`io.BytesIO` objects instead of
                    writing files.
        pages:      Subset of page indices to process.  Defaults to all pages.

    Returns:
        List of :class:`io.BytesIO` objects when ``return_pil=True``,
        otherwise *None* (files written to *outpath*).
    """
    if outpath is None:
        return_pil = True

    pillow_images: List[io.BytesIO] = []
    try:
        doc = fitz.open(pdf) if isinstance(pdf, (str, Path)) else pdf
        if pages is None:
            pages = range(len(doc))
        for i in pages:
            page_bytes: bytes = doc[i].get_pixmap(dpi=dpi).pil_tobytes(format="PNG")
            if return_pil:
                pillow_images.append(io.BytesIO(page_bytes))
            else:
                with (outpath / ("%02d.png" % (i + 1))).open("wb") as f:
                    f.write(page_bytes)
    except Exception as exc:
        logger.error("Error rasterizing PDF %s: %s", pdf, exc)

    return pillow_images if return_pil else None


# ---------------------------------------------------------------------------
# Nougat stopping criteria (from the original Nougat repository)
# ---------------------------------------------------------------------------

class RunningVarTorch:
    """Maintains a sliding-window variance for a sequence of tensors."""

    def __init__(self, L: int = 15, norm: bool = False):
        self.values = None
        self.L      = L
        self.norm   = norm

    def push(self, x: torch.Tensor) -> None:
        assert x.dim() == 1
        if self.values is None:
            self.values = x[:, None]
        elif self.values.shape[1] < self.L:
            self.values = torch.cat((self.values, x[:, None]), 1)
        else:
            self.values = torch.cat((self.values[:, 1:], x[:, None]), 1)

    def variance(self):
        if self.values is None:
            return None
        if self.norm:
            return torch.var(self.values, 1) / self.values.shape[1]
        return torch.var(self.values, 1)


class StoppingCriteriaScores(StoppingCriteria):
    """
    Stops generation when the variance of the score distribution stabilises —
    as recommended by the Nougat authors to avoid repetition loops.
    """

    def __init__(self, threshold: float = 0.015, window_size: int = 200):
        super().__init__()
        self.threshold   = threshold
        self.vars        = RunningVarTorch(norm=True)
        self.varvars     = RunningVarTorch(L=window_size)
        self.stop_inds   = defaultdict(int)
        self.stopped     = defaultdict(bool)
        self.size        = 0
        self.window_size = window_size

    @torch.no_grad()
    def __call__(
        self,
        input_ids: torch.LongTensor,
        scores:    torch.FloatTensor,
    ) -> bool:
        last_scores = scores[-1]
        self.vars.push(last_scores.max(1)[0].float().cpu())
        self.varvars.push(self.vars.variance())
        self.size += 1
        if self.size < self.window_size:
            return False

        varvar = self.varvars.variance()
        for b in range(len(last_scores)):
            if varvar[b] < self.threshold:
                if self.stop_inds[b] > 0 and not self.stopped[b]:
                    self.stopped[b] = self.stop_inds[b] >= self.size
                else:
                    self.stop_inds[b] = int(
                        min(max(self.size, 1) * 1.15 + 150 + self.window_size, 4095)
                    )
            else:
                self.stop_inds[b] = 0
                self.stopped[b]   = False
        return all(self.stopped.values()) and len(self.stopped) > 0
