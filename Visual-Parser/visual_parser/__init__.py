"""
visual_parser — Standalone Visual-RAG PDF & Image Parser
=========================================================
Detects new PDFs (and standalone images alongside them) in a user-supplied
directory, extracts text (via Nougat or lightweight PyMuPDF/PyPDFLoader),
describes every figure/chart/schematic and every standalone image using a
Vision LLM (OpenAI GPT, Google Gemini, or a local model via Ollama), and
writes JSONL knowledge bases ready for any downstream RAG system:

    01_chunks_kb.jsonl          – text chunks with stable IDs
    02_visuals_kb.jsonl         – per-figure visual descriptions
    03_metadata_kb.jsonl        – document-level metadata (title, authors, DOI …)
    image_descriptions_kb.jsonl – one holistic description per standalone image

No chatbot, no vector store, no retrieval – just a robust parser.
"""

from visual_parser.config import ParserConfig
from visual_parser.pipeline import run_pipeline

__all__ = ["ParserConfig", "run_pipeline"]
__version__ = "2.2.3"
