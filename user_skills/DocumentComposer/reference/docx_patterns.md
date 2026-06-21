# Word document patterns (python-docx)

Use for structured `.docx` files: teacher notes, guides, technical reports. Full reference:

`{PACK_ROOT}/scripts/create_ai_llm_teaching_notes_docx.py`

## Core imports

```python
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor
```

## Document setup

- Set margins on `doc.sections[0]` (`Inches` for top/bottom/left/right).
- Style body: `styles["Normal"].font.name = "Aptos"`, `Pt(10.5)`.
- Headings: `doc.add_heading(text, level=n)` with colored runs if needed.

## Table cell shading (OOXML)

```python
def set_cell_shading(cell, fill: str) -> None:
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = tc_pr.find(qn("w:shd"))
    if shd is None:
        shd = OxmlElement("w:shd")
        tc_pr.append(shd)
    shd.set(qn("w:fill"), fill)  # hex without '#', e.g. "E9F0FF"
```

## Callout table pattern

Single-cell table with shaded background and border; put title (bold) and body in separate paragraphs inside the cell.

## Content-driven builds

Keep slide/page content in Python data structures (lists of dicts) or external JSON/YAML; loop to emit sections rather than one giant paste block.

## Output

Save to the user’s **absolute output path**, not the script directory, unless generating a local example.
