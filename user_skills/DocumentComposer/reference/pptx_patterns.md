# PowerPoint patterns (python-pptx)

Use for **programmatic** `.pptx` decks on any topic. Full reference implementation:

`{PACK_ROOT}/scripts/create_ai_llm_teaching_deck.py`

(`PACK_ROOT` = folder containing `DocumentComposer/SKILL.md`.)

## Layout defaults

- Widescreen: `prs.slide_width = Inches(13.333)`, `prs.slide_height = Inches(7.5)`
- Blank slide layout: `prs.slide_layouts[6]`
- Position/size: `Inches(x)`, font sizes: `Pt(n)`
- Colors: `RGBColor(r, g, b)` from `pptx.dml.color`

## Core imports

```python
from pathlib import Path
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Inches, Pt
```

## Text box helper (minimal)

```python
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

## Bullets

`python-pptx` bullet formatting is limited; prefix with `•` for reliable output:

```python
p.text = f"• {item}"
```

## Deck shell

```python
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank = prs.slide_layouts[6]
slide = prs.slides.add_slide(blank)
prs.save(output_path)  # user-supplied absolute path
```

## Template-based posters

For fixed `.pptx` templates and placeholder indices, read `{PACK_ROOT}/scripts/make_posters.py` instead. Never guess placeholder `idx` values without inspecting the template.
