"""
image_tracker.py — Utilities for detecting new standalone images and
                    persisting the set of already-processed filenames across
                    pipeline runs.

Mirrors pdf_tracker.py's registry pattern. load_processed_pdfs/
save_processed_pdfs/mark_as_processed are reused directly from pdf_tracker.py
(despite the module name, they have no PDF-specific logic at all).
"""

from __future__ import annotations

import logging
import os
from typing import List

from visual_parser.pdf_tracker import load_processed_pdfs

logger = logging.getLogger(__name__)

IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp")
PROCESSED_IMAGES_REGISTRY = "parsed_images.txt"


# ---------------------------------------------------------------------------
# Image discovery
# ---------------------------------------------------------------------------

def find_new_images(
    input_dir: str,
    registry_path: str,
    rebuild: bool = False,
) -> List[str]:
    """
    Walk *input_dir* recursively and return full paths of standalone images
    that have NOT yet been processed.

    Unlike find_new_pdfs(), *registry_path* is an explicit parameter rather
    than being joined internally against *input_dir* -- this lets the caller
    anchor the registry at effective_output_dir() unambiguously, sidestepping
    a pre-existing bug on the PDF side where find_new_pdfs() always resolves
    its registry against input_dir while pipeline.py separately writes it
    against output_dir (the two diverge, and PDFs get reprocessed forever,
    whenever --output-dir differs from --input-dir).

    Args:
        input_dir:     Root directory to search for image files.
        registry_path: Full path to the tracking file.
        rebuild:       When True, return *all* images regardless of the
                       registry (forces a full re-describe).

    Returns:
        Sorted list of absolute image paths.
    """
    processed = set() if rebuild else set(load_processed_pdfs(registry_path))

    new_images = [
        os.path.join(root, filename)
        for root, _, files in os.walk(input_dir)
        for filename in files
        if filename.lower().endswith(IMAGE_EXTENSIONS)
        and os.path.basename(filename) not in processed
    ]

    new_images.sort()
    if new_images:
        logger.info("Found %d new image(s) to process.", len(new_images))
    else:
        logger.info("No new images detected in %s.", input_dir)

    return new_images
