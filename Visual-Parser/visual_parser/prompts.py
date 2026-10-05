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
    "   - For tables: transcribe EVERY cell's contents VERBATIM and IN FULL, preserving "
    "row/column association (e.g. 'Row \"Ext. loop A\": Outcome = Pass'). Do not summarise "
    "or paraphrase table contents.\n"

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


def build_figure_prompt_with_context(base_prompt: str, target_image_index: int, total_images: int) -> str:
    """
    Prepend a multi-image framing preamble to *base_prompt* when adjacent
    pages are included as context (--vision-context-pages > 0). Images are
    always sent in page order; target_image_index (0-based) identifies which
    one is the page to actually describe -- the rest are context only, used
    solely to correctly interpret a figure or caption that continues onto/from
    the target page. Only figures primarily on the target page should be
    described; figures that belong entirely to a context page are already
    covered by that page's own call and must not be duplicated here.

    When total_images == 1 (context_pages == 0), this returns base_prompt
    unchanged -- today's single-page behavior is untouched, and this composes
    correctly whether base_prompt is the default FIGURE_PROMPT or a caller's
    custom override.
    """
    if total_images <= 1:
        return base_prompt

    preamble = (
        f"You are shown {total_images} consecutive pages from a technical document, "
        f"in page order (image 1 = earliest page shown). "
        f"**Image {target_image_index + 1} of {total_images} is the TARGET page** -- "
        "describe figures from this page only. "
        "The other image(s) are provided solely as context, to help you correctly "
        "interpret a figure, diagram, or caption that continues onto or from the "
        "target page. Do NOT generate descriptions for figures that belong entirely "
        "to a context page -- that page has its own separate call covering it.\n\n"
    )
    return preamble + base_prompt


# ---------------------------------------------------------------------------
# Standalone-image description prompt
# ---------------------------------------------------------------------------

IMAGE_DESCRIPTION_PROMPT: str = (
    "You are a specialised Scientific Vision Analyst. You are viewing a single "
    "standalone image with NO external document text supplied alongside it. "
    "This image could be almost anything: a diagram, chart, schematic, CAD "
    "drawing, P&ID, plot, photograph, a slide (e.g. a PowerPoint slide saved as "
    "an image) containing both text and a figure, or a region cropped from a "
    "larger page. Do not assume its origin, and do not assume it is text-free -- "
    "many such images contain real body text (titles, bullet points, captions, "
    "title-block notes, tables, revision stamps) in addition to or instead of a "
    "diagram. Your goal is to extract high-fidelity structured data for a "
    "Retrieval-Augmented Generation (RAG) system. Your output must be precise, "
    "quantitative, and strictly follow the structure defined below.\n\n"

    "**TRUST THE PIXELS**: Transcribe all visible labels, numbers, units, and "
    "annotations VERBATIM, exactly as shown in the image.\n\n"

    "Generate ONE description for this image using STRICTLY the following six "
    "headings.\n\n"

    "1. **Subject**: A concise title or classification "
    "(e.g. 'Vertical Parabolic Gate Schematic', 'PWR Primary Loop P&ID', "
    "'Decay Heat vs Time Plot', 'Slide: Reactor Safety Overview').\n\n"

    "2. **Verbatim Text Content**: If the image contains any text beyond short "
    "diagram labels -- slide titles, bullet points, paragraphs, captions, table "
    "or title-block text, notes, revision stamps -- transcribe it VERBATIM and "
    "IN FULL, preserving reading order. This text must be captured, not "
    "summarised. If the image has no such text (a pure diagram, chart, or "
    "photograph), state 'No additional text content.'\n\n"

    "3. **Geometry & Labels**:\n"
    "   - Describe shapes, layout, and components of any diagram/drawing/chart "
    "present.\n"
    "   - List short text labels and tags found INSIDE the diagram itself "
    "VERBATIM (distinct from the body text already captured in heading 2).\n"
    "   - For schematics/CAD/P&ID: describe connectivity (e.g. 'Pump discharges "
    "to Heat Exchanger').\n"
    "   - If the image is pure text with no diagram (e.g. a text-only slide), "
    "state 'No diagram present.'\n\n"

    "4. **Dimensions & Data (Quantitative)**:\n"
    "   - Schematics/CAD/P&ID: extract all physical dimension lines, radii, "
    "diameters, lengths, thicknesses, angles, tolerances, and part/revision "
    "numbers explicitly labelled.\n"
    "   - Plots/Charts: extract axis variables, units, numerical ranges; "
    "identify peaks, minima, trends, discontinuities with quantitative "
    "language.\n"
    "   - If values are approximate, state this (e.g. '~', 'estimated from "
    "plot').\n\n"

    "5. **Context**: Summarise the apparent scientific, engineering, or "
    "presentational purpose of this image, based on everything visible in it "
    "(both the text from heading 2 and any diagram from headings 3-4) -- no "
    "external document text is supplied to draw on.\n\n"

    "6. **Discrepancy Check**: If the image contains BOTH text (heading 2) and "
    "a diagram/chart (headings 3-4), check whether a claim made in the text "
    "matches what the diagram actually shows (e.g. text says '5 units' but the "
    "diagram is labelled '6') -- apply TRUST THE PIXELS and report the "
    "discrepancy. Otherwise, note any purely internal inconsistency (mismatched "
    "units, unlabeled axes, ambiguous legend entries). If none, state "
    "'No discrepancies detected.'\n\n"

    "**OUTPUT FORMAT**\n"
    "Return a strictly valid JSON object (NOT a list):\n"
    "{ \"description\": \"**Subject:** [Title]\\n**Verbatim Text Content:** [...]\\n"
    "**Geometry & Labels:** [...]\\n**Dimensions & Data:** [...]\\n**Context:** [...]\\n"
    "**Discrepancy Check:** [...]\" }"
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
