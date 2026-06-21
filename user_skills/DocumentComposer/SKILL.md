---
name: document-composer
description: >-
  Composes PowerPoint (.pptx), Word (.docx), HTML slide decks, and figure assets
  for any topic and length using python-pptx, python-docx, and matplotlib patterns
  in this pack. Requires plan-first workflow and user output directory. Use when
  the user asks to create or edit presentations, teaching decks, posters,
  technical reports, handouts, or browser-based slide HTML.
disable-model-invocation: true
---

# Document Composer

You compose **offline documents** for **any topic** and **any length**: `.pptx`, `.docx`, optional HTML slide decks, and PNG figures for slides. You **do not invent Office or python-pptx/python-docx APIs**. Reuse the patterns in this pack.

**PACK_ROOT** = the directory that contains this `SKILL.md` file (the `DocumentComposer` folder).

Install Python dependencies from `{PACK_ROOT}/requirements.txt` when running generated scripts.

---

## Role and limits

- Save deliverables only under a **user-supplied absolute output directory** (ask the user to confirm the path exists or should be created).
- Do not hard-code sandbox paths like `/mnt/data` unless the runtime is explicitly that environment.
- Ask for missing intake items before writing long code or prose.
- Example scripts under `{PACK_ROOT}/scripts/` are **pattern libraries**, not fixed content to copy verbatim for unrelated topics.

---

## Mandatory intake (before code)

Confirm or collect:

| Item | Notes |
|------|--------|
| **Output type** | `.pptx`, `.docx`, HTML deck, or combination |
| **Topic and audience** | Subject matter and who will read it |
| **Target length** | Slide count, page count, or approximate duration |
| **Output directory** | Absolute path for all generated files |
| **Template** | Optional `.pptx`/`.docx` template path; if none, build programmatically |
| **Branding** | Optional colors, fonts, institution; else use neutral defaults |

If any item is unclear, ask targeted questions.

---

## Plan before build

1. Propose a **slide/page outline** (titles and main points only).
2. Get user confirmation or one round of edits.
3. Then generate code or files.

**Scaling length:**

- **Short:** inline content in the generator script or a small dict.
- **Medium:** JSON/YAML spec file the script reads.
- **Long:** chunked generation (e.g. slides 1–10, then 11–20) using the same helpers, or a loop over a spec list.

---

## Output-type decision tree — mandatory file reads

Before writing new code for the chosen output type, you **must read** the listed reference path with the host’s file tools (e.g. AutoFLUKA `text_file_reader_tool`, Cursor Read). Do not guess APIs from memory alone.

| When | You must read first |
|------|---------------------|
| Programmatic widescreen `.pptx` (any topic/length) | `{PACK_ROOT}/scripts/create_ai_llm_teaching_deck.py` |
| Structured `.docx` (notes, guides, reports) | `{PACK_ROOT}/scripts/create_ai_llm_teaching_notes_docx.py` |
| Template-based poster or fixed-layout `.pptx` | `{PACK_ROOT}/scripts/make_posters.py` |
| Self-contained HTML slide deck | `{PACK_ROOT}/scripts/ai_and_llms_for_students.html` |
| Node + pptxgenjs reference only | `{PACK_ROOT}/scripts/AI-Presentation.py` (**do not run as Python**) |

Quick pattern summaries (may also load via Extended discovery): `{PACK_ROOT}/reference/pptx_patterns.md`, `docx_patterns.md`, `html_deck_patterns.md`.

**Template placeholders:** indices in `make_posters.py` apply only to its specific template. Inspect placeholders before editing; do not reuse idx numbers for other templates.

**Slide size default:** wide **13.333 × 7.5 in**, blank layout **6**, unless the user or template specifies otherwise.

---

## Workflow after reading references

1. Read the mandatory reference path for the chosen output type.
2. Draft or adapt a generator script; write content for the **user’s topic**, not the example topic in the reference scripts.
3. Write all outputs to the **user output directory**.
4. Run the script (or equivalent) and confirm files exist.
5. Report output paths to the user.

---

## Compact API excerpts (fallback if full read is skipped)

### python-pptx — text box

```python
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Inches, Pt

def add_text(slide, text, x, y, w, h, size=24, color=RGBColor(32, 45, 71),
             bold=False, align=PP_ALIGN.LEFT, font="Aptos", valign=MSO_ANCHOR.TOP):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.clear()
    tf.word_wrap = True
    tf.vertical_anchor = valign
    p = tf.paragraphs[0]
    p.text = text
    p.alignment = align
    for run in p.runs:
        run.font.name = font
        run.font.size = Pt(size)
        run.font.bold = bold
        run.font.color.rgb = color
    return box
```

### python-pptx — deck shell

```python
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank = prs.slide_layouts[6]
slide = prs.slides.add_slide(blank)
prs.save(output_path)
```

### python-pptx — bullets

```python
p.text = f"• {item}"
```

### python-docx — cell shading

```python
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def set_cell_shading(cell, fill: str) -> None:
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = tc_pr.find(qn("w:shd"))
    if shd is None:
        shd = OxmlElement("w:shd")
        tc_pr.append(shd)
    shd.set(qn("w:fill"), fill)
```

### Template poster — picture placeholder

```python
placeholders = {sh.placeholder_format.idx: sh for sh in slide.placeholders if sh.is_placeholder}
placeholders[25].insert_picture(str(image_path))  # idx is template-specific
```

### matplotlib figure for slides

```python
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.savefig(path, dpi=220, bbox_inches="tight", facecolor="white")
plt.close()
```

---

## Dependencies

| Stack | Packages |
|-------|----------|
| PowerPoint | `python-pptx`, optional `Pillow` for image crop |
| Word | `python-docx` |
| Slide figures | `matplotlib` |
| HTML deck | none (Python); CDN fonts optional |

---

## Future helper

A small `{PACK_ROOT}/scripts/inspect_pptx_placeholders.py` may be added to list placeholder idx/name/type per template slide.
