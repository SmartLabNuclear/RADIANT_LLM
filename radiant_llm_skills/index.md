# RADIANT Skills Catalog

RADIANT-LLM organizes specialty guidance under `specialties/` so the base system prompt can remain broad while deeper topic packs are loaded only when relevant.

## Bundled Specialties
- `safety-pra-severe-accident`: safety principles, PRA framing, transient and severe-accident interpretation
- `security-cyber-physical-protection`: defensive nuclear security and cyber-physical protection guidance
- `safeguards-mca-and-fuel-cycle-monitoring`: safeguards, MC&A, process monitoring, diversion analysis
- `geniv-reactors-and-fuel-cycles`: reactor-family context and 3S implications across advanced concepts
- `digital-twin-monitoring-and-control`: monitoring, state estimation, anomaly detection, supervisory analytics
- `regulatory-standards-and-licensing`: technical interpretation support for codes, standards, and licensing questions

## Folder Contract
- `specialties/<slug>/SKILL.md`: required self-contained specialty guidance, reference anchors, equation/formula notes, examples, and limitations
- Optional adjacent files may live anywhere inside `specialties/<slug>/`, including user-chosen subfolders such as `references/`, `equations/`, `inputs/`, `examples/`, or `assets/`.
- The loader treats adjacent files as supplemental artifacts for the selected skill directory; `SKILL.md` remains the only bundled example file required.
- Allowed prompt-loadable adjacent file types are `.md`, `.txt`, `.yaml`, `.yml`, `.json`, `.csv`, `.inp`, and `.i`.

## User Skill Layouts
- `SKILL.md`: one simple external skill rooted at the selected directory
- `*.md`: one or more simple external skills in the selected directory
- `specialties/<slug>/SKILL.md`: structured external skills with optional adjacent files
