# RADIANT Skills Catalog

RADIANT-LLM organizes bundled specialty guidance as immediate child skill packs so the base system prompt can remain broad while deeper topic packs load only when relevant.

## Bundled skill packs (tier 1)

- `safety-pra-severe-accident`: safety principles, PRA framing, transient and severe-accident interpretation
- `security-cyber-physical-protection`: defensive nuclear security and cyber-physical protection guidance
- `safeguards-mca-and-fuel-cycle-monitoring`: safeguards, MC&A, process monitoring, diversion analysis
- `geniv-reactors-and-fuel-cycles`: reactor-family context and 3S implications across advanced concepts
- `digital-twin-monitoring-and-control`: monitoring, state estimation, anomaly detection, supervisory analytics
- `regulatory-standards-and-licensing`: technical interpretation support for codes, standards, and licensing questions

## Folder contract

- `<slug>/SKILL.md`: required self-contained specialty guidance, reference anchors, equation/formula notes, examples, and limitations
- Root `index.md` and `SKILL.md` are tier-0 policy only (not discoverable as packs)
- Optional adjacent files may live inside each pack folder (`references/`, `equations/`, etc.)
- Allowed prompt-loadable adjacent file types: `.md`, `.txt`, `.yaml`, `.yml`, `.json`, `.csv`, `.inp`, and `.i`

## User skill packs (tier 2)

- External user skills use the same layout: `<user_skills_root>/<PackName>/SKILL.md`
- User packs are query-ranked even in **Chat only** preset; bundled tier-1 auto-route is gated by **Full context** module settings

## Loading presets

- **Full context**: all bundled modules enabled for auto-route
- **Chat only**: tier-0 bundled policy only; bundled specialties load only when manually pinned or user packs match the query
- **Extended discovery**: optional adjacent helper files inside a selected pack folder
