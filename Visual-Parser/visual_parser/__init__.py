"""
visual_parser — Standalone Visual-RAG PDF Parser
=================================================
Detects new PDFs in a user-supplied directory, extracts text (via Nougat or
lightweight PyMuPDF/PyPDFLoader), describes every figure/chart/schematic using
a Vision LLM (OpenAI GPT-4o or Google Gemini), and writes three JSONL knowledge
bases ready for any downstream RAG system:

    01_chunks_kb.jsonl   – text chunks with stable IDs
    02_visuals_kb.jsonl  – per-figure visual descriptions
    03_metadata_kb.jsonl – document-level metadata (title, authors, DOI …)

No chatbot, no vector store, no retrieval – just a robust parser.
"""

from visual_parser.config import ParserConfig
from visual_parser.pipeline import run_pipeline

__all__ = ["ParserConfig", "run_pipeline"]
__version__ = "1.0.2"
