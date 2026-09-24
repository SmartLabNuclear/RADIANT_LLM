#!/usr/bin/env python3
"""
visual-parser.py — Convenience top-level script for the Visual-RAG PDF Parser.

Run this file directly from the Visual-Parser/ directory:

    python visual-parser.py --input-dir ./my_pdfs --vision-provider gpt

All CLI logic lives in the package entrypoint so it can also be invoked as:

    python -m visual_parser --input-dir ./my_pdfs ...
    visual-parser --help
    visual-parser --input-dir ./my_pdfs ...   (after: pip install -e .)

Run with --help to see all available options.
"""

import sys
from visual_parser.cli_main import main

if __name__ == "__main__":
    sys.exit(main())
