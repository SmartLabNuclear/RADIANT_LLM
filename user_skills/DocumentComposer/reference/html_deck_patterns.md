# HTML slide deck patterns

Use for a **single-file** browser presentation (shareable, no Office install). Full example:

`{PACK_ROOT}/scripts/ai_and_llms_for_students.html`

## Canvas

- Fixed frame: **1280×720** px (16∶9), class e.g. `.slide-deck`
- Scale to viewport with JS `transform: scale(...)` on resize
- Each slide: `<div class="slide">`; one slide has `.active` for visibility

## Brand tokens (CSS variables)

Define in `:root`:

```css
:root {
  --maroon: #500000;
  --cream: #FAF6EE;
  --gold: #C69214;
  --charcoal: #2E2D2C;
}
```

Reuse variables for headings, accents, and card backgrounds.

## Slide title row

Typical structure: `.slide-title` with heading text plus optional `.slide-index` badge (e.g. `3 / 12`).

## Layout components

- Two columns: `.grid-2` with CSS grid
- Callouts: `.callout-card`
- Lists: `.custom-bullets` (HTML `<ul>` is fine here; unlike journal prose)

## Images

Prefer **local** `./assets/` paths. Avoid non-portable generated URLs; provide `onerror` fallback only when needed.

## Export to `.pptx`

No faithful one-click conversion. Options: rebuild content with python-pptx, or screenshot each slide (visual only, poor editability).

## Offline use

CDN fonts/icons break without network; optional system font stack for classroom/offline delivery.
