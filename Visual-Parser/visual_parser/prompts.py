"""
prompts.py — Vision-LLM prompt templates used by the parser.

Keeping prompts in one place makes it easy to customise them without touching
pipeline logic.  The figure prompt is intentionally detailed and domain-aware;
users can swap in a shorter, domain-agnostic version for non-technical PDFs.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Figure / visual-element description prompt
# ---------------------------------------------------------------------------

FIGURE_PROMPT: str = (
    "You are a specialised Scientific Vision Analyst. "
    "You are viewing a page from a technical document. "
    "Your goal is to extract high-fidelity structured data from visual elements "
    "for a Retrieval-Augmented Generation (RAG) system. "
    "Your output must be precise, quantitative, and strictly follow the structure defined below.\n\n"

    "**PHASE 1: VISUAL SUPREMACY PROTOCOL (CRITICAL)**\n"
    "- **Discrepancy Detection**: Explicitly check if the visual data matches surrounding text claims.\n"
    "- **Trust the Pixels**: If the image shows a label (e.g. '6') but the text says '5', "
    "record the image value and report the discrepancy.\n\n"

    "**PHASE 2: STRUCTURAL ANALYSIS**\n"
    "For each distinct scientific visual (plot, chart, schematic, diagram) generate a description "
    "using STRICTLY the following five headings.\n\n"

    "- A **Figure** is defined as a visual element sharing a single figure number or caption "
    "(e.g. 'Figure 3'), even if it contains multiple panels or subplots.\n"
    "- If a single Figure contains mixed content (e.g. a schematic and a plot), "
    "describe all panels together as ONE Figure.\n"
    "- If no explicit figure number is visible, treat a visually unified group of panels as ONE Figure "
    "and identify it with the corresponding page number.\n\n"

    "1. **Subject**: A concise title or classification "
    "(e.g. 'Vertical Parabolic Gate Schematic', 'PWR Primary Loop P&ID', 'Decay Heat vs Time Plot').\n"

    "2. **Geometry & Labels**:\n"
    "   - Describe shapes, layout, and components.\n"
    "   - List meaningful text labels found *inside* the figure VERBATIM.\n"
    "   - For schematics: describe connectivity (e.g. 'Pump discharges to Heat Exchanger').\n"

    "3. **Dimensions & Data (Quantitative)**:\n"
    "   - **Schematics**: Extract all physical dimension lines, radii, diameters, lengths, "
    "thicknesses, angles, and tolerances explicitly labelled in the figure.\n"
    "   - **Plots/Charts (CRITICAL)**:\n"
    "       * Extract axis variables, units, and numerical ranges (min/max).\n"
    "       * Identify and quantify key features: peaks, minima, plateaus, inflection points, "
    "step changes, oscillations, or discontinuities.\n"
    "       * Describe temporal or parametric trends explicitly using quantitative language:\n"
    "           - e.g. 'Monotonic increase from 0–20 s',\n"
    "           - 'Exponential decay after shutdown',\n"
    "           - 'Asymptotic stabilisation near 600 MW'.\n"
    "       * If multiple curves are present, distinguish them by legend labels, line style, or colour.\n"
    "       * If values are approximate, state this (e.g. '≈', 'estimated from plot').\n"

    "4. **Context**: Summarise the scientific purpose based on the surrounding page text.\n"

    "5. **Discrepancy Check**: State if visual labels contradict text. "
    "If none, state 'No discrepancies detected'.\n\n"

    "**OUTPUT FORMAT**\n\n"
    "**IMPORTANT**:\n"
    "  - Return a strictly valid JSON list.\n"
    "  - Return ONE JSON object per Figure on the page.\n"
    "  - If a Figure contains subplots, return ONE description per Figure — NOT per subplot.\n"
    "  - If a page contains no scientific visual, return an EMPTY JSON LIST: [].\n"
    "  - Do NOT skip pages.\n\n"

    "[\n"
    "  { \"description\": \"**Subject:** [Title]\\n"
    "**Geometry & Labels:** [Detailed description]\\n"
    "**Dimensions & Data:** [Quantitative extraction]\\n"
    "**Context:** [Purpose]\\n"
    "**Discrepancy Check:** [Result]\" },\n"
    "  { \"description\": \"...\" }\n"
    "]"
)

# ---------------------------------------------------------------------------
# Metadata extraction prompt
# ---------------------------------------------------------------------------

METADATA_PROMPT_TEMPLATE: str = (
    "You will be shown up to {num_pages} images (PNG) of the front pages of a technical PDF.\n"
    "Extract as much of the following metadata as you can find, and return it as a pure JSON object "
    "with these keys:\n"
    "  • title (string)\n"
    "  • authors (array of strings)\n"
    "  • publication_date (YYYY-MM-DD if available)\n"
    "  • report_number (string)\n"
    "  • doi (string)\n"
    "  • keywords (array of short terms)\n\n"
    "Omit any field you cannot locate."
)
