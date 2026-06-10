# RADIANT Skill Creation Policy

This document defines how RADIANT-LLM loads bundled and user-defined skills, and how humans and the assistant create, update, or retire skill content.

## Tiers

### Tier 0 — Global policy (always-on, minimal footprint)

- `index.md` — bundled skill catalog
- `SKILL.md` — core domain contract and global rules

### Tier 1 — Bundled modules (toggles in Settings)

| Module | Folder | Purpose |
|--------|--------|---------|
| Safety / PRA / Severe Accident | `safety-pra-severe-accident/` | Safety principles, PRA framing, transient and severe-accident interpretation |
| Security / Cyber-Physical | `security-cyber-physical-protection/` | Defensive nuclear security and cyber-physical protection guidance |
| Safeguards / MC&A | `safeguards-mca-and-fuel-cycle-monitoring/` | Safeguards, MC&A, process monitoring, diversion analysis |
| Gen-IV / Advanced Reactors | `geniv-reactors-and-fuel-cycles/` | Reactor-family context and 3S implications across advanced reactor concepts |
| Digital Twin / Monitoring | `digital-twin-monitoring-and-control/` | Monitoring, state estimation, anomaly detection, supervisory analytics |
| Regulatory / Licensing | `regulatory-standards-and-licensing/` | Technical interpretation for codes, standards, and licensing questions |

All bundled modules are **on by default** under the Full context preset. Deselect modules to reduce token use.

### Tier 2 — User-defined skills (personal or team packs)

Point **User skills path** in Settings at a folder containing one subdirectory per skill pack:

```text
my_skill_packs/
  facility-loop-notes/
    SKILL.md
  team-bc-checklist/
    SKILL.md
```

Each pack requires a `SKILL.md` file. Minimal YAML frontmatter:

```yaml
---
name: Facility Loop Notes
description: Lessons from our facility loop commissioning runs.
---
```

RADIANT-LLM recognizes only:
- `name` — required
- `description` — required

User packs are routed through `name`, `description`, path tokens, and body content. They are **additive**: bundled `radiant_llm_skills/` always loads from the installation; your directory never replaces it.

---

## When to create a user skill

**Create** a user skill when:

- You repeat the same guidance across sessions
- You have facility- or project-specific conventions not in the bundled skills
- You validated an analysis pattern worth reusing
- You want a checklist that loads only for matching queries

**Do not** create a user skill for:

- One-off answers with no reuse value
- Unvalidated or preliminary results (distill into a reviewed note first)
- Content that duplicates bundled specialty guidance
- Secrets, API keys, credentials, internal URLs, or export-controlled data

---

## User skill pack layout

Required tree under **User skills path**:

```text
<user_skills_path>/
  <pack-slug>/
    SKILL.md            (* required)
    reference/          (optional extra .md notes or data files)
    scripts/            (optional helpers; not auto-executed)
```

**Pack slug rules:** 3–40 characters, lowercase letters, digits, and hyphens only (`[a-z0-9-]`), must start and end with a letter or digit. The six bundled module slugs are reserved and may not be used as pack slugs.

---

## SKILL.md content contract

Required frontmatter:

```yaml
---
name: Human-readable pack title
description: One sentence describing when RADIANT-LLM should load this pack.
---
```

Required body sections (in order):

1. **Scope** — cases, assumptions, reactor types, or standards this pack covers
2. **When to use** — query phrases or signal keywords that should load this pack
3. **Guidance** — concise rules, checklists, equations, and workflow notes
4. **Limits** — what this pack does not override (bundled policy, safety policy, tool rules)
5. **Evidence** (optional) — paths to validated references or data files

Keep packs focused. The loader budget-truncates injected skill text; `description` must be strong enough to trigger routing even if the body is partially cut.

---

## Creation workflow (human + assistant)

### Phase A — Detect

The assistant may enter this workflow when the user says:

- "Save this as a skill"
- "Remember this for next time"
- "Create a user skill from this session"
- "Add this to my skill packs"

The assistant must **not** write any files in this phase.

### Phase B — Propose

The assistant presents a **Skill Proposal** block:

```markdown
### Skill Proposal (awaiting your approval)

- **Action:** create | update | retire
- **Pack slug:** `my-pack-name`
- **Target path:** `<user_skills_path>/my-pack-name/SKILL.md`
- **Trigger summary:** when queries mention …
- **Draft SKILL.md:** (full preview below)
- **Security note:** passes / may require review because …
- **Alternatives:** update existing pack X / add to reference/ only

Do you approve writing this skill pack? Reply **yes** to proceed, **no** to cancel, or suggest edits.
```

The assistant must include the **full draft `SKILL.md`** in the proposal.

### Phase C — Approve (mandatory)

| User reply | Assistant action |
|------------|-----------------|
| **yes** / **approve** / **go ahead** | Proceed to Phase D |
| **no** / **cancel** | Stop; do not write |
| Edits requested | Revise proposal; return to Phase B |
| Ambiguous ("maybe", "looks fine") | Ask again; do **not** write |

### Phase D — Write

Use `SkillPromotionTool` only after explicit approval:

1. **Preview:** `SkillPromotionTool(operation="create_user_skill_pack", dry_run=True, pack_slug="...", skill_md_content="...", user_approved=False)`
2. **Write:** same call with `user_approved=True`, `dry_run=False`

If **User skills path** is empty or invalid, stop and ask the user to set it in Settings or via the `RADIANT_SKILLS_DIR` environment variable.

### Phase E — Verify

1. File exists at `<user_skills_path>/<pack-slug>/SKILL.md`
2. Settings → **User skills path** points at the correct parent folder
3. Send a test query matching the `description` keywords
4. Confirm the Alerts panel shows `User skill loaded: <name>`, or check `/skill-catalog`

### Phase F — Maintain

- **Update:** same propose → approve → write flow; set `allow_overwrite=True` only after approval
- **Retire:** approve → rename folder to `_retired-<slug>` or delete after backup
- **Promote to bundled:** separate flow via bundled promotion (see below); requires writable bundled tree

---

## Agent hard rules

1. Never write without explicit user approval in the current turn.
2. Never write user packs under the bundled `radiant_llm_skills/` directory.
3. Never overwrite an existing pack without naming the target and receiving approval.
4. Always call `SkillPromotionTool` with `dry_run=True` first, unless the user already approved a shown preview.
5. Stop if User skills path is unset or missing; ask the user to configure it.
6. Treat bundled promotion as a separate, higher-impact action requiring its own explicit approval.

---

## Bundled promotion vs user skill

| Action | Target | Typical environment |
|--------|--------|---------------------|
| User skill pack | `<user_skills_path>/` | Docker: `/host/user_skills` |
| Working example | `radiant_llm_skills/working_examples/` | Local dev with writable bundled tree |
| Reusable rule | `radiant_llm_skills/<module>/rules/` | Local dev with writable bundled tree |

Bundled promotion uses `SkillPromotionTool` with:

- `operation="promote_working_example"` — curated reference bundle + `README.md`
- `operation="promote_reusable_rule"` — reusable `.md` rule in an existing module family

Same approval pattern: `dry_run=True` first, then `user_approved=True` and `dry_run=False`.

**Docker note:** the bundled `radiant_llm_skills/` tree is often mounted read-only (`:ro`). Bundled promotion returns `blocked_readonly` in that case. Use user skill packs in the `/host/user_skills` data volume instead.

---

## Docker and local paths

| Environment | Bundled skills | User skills directory | Env variable |
|-------------|----------------|----------------------|--------------|
| Local dev | repo `radiant_llm_skills/` | user-chosen path in Settings | `RADIANT_SKILLS_DIR` (optional override) |
| Docker | mount → `/radiant-llm/radiant_llm_skills:ro` | `/host/user_skills` (working-data volume) | `RADIANT_SKILLS_DIR=/host/user_skills` |

Use container paths inside Docker, host paths on native Windows or Linux.

---

## Bundled skill metadata

Bundled `SKILL.md` files use the same minimal YAML frontmatter schema.

- `name` and `description` are required on all bundled `SKILL.md` files.
- Frontmatter is routing metadata only. It does not control execution, tool use, or safety policy.
- After editing any bundled file, regenerate the content manifest:
  `python maintenance_scripts/generate_skill_manifest.py`

**Important — Docker mount workflow:** When mounting a local `radiant_llm_skills/` directory
into Docker (`-v "/path/to/radiant_llm_skills:/radiant-llm/radiant_llm_skills:ro"`), the mounted
directory shadows the image's baked-in copy entirely. If you have edited any bundled skill file,
you **must** regenerate `MANIFEST.json` locally before starting the container:

```bash
python maintenance_scripts/generate_skill_manifest.py
```

If you skip this step, every edited file will be flagged as `tampered` on every startup and
warnings will appear in the Alerts panel. Unedited files pulled directly from the repository
already ship with a matching `MANIFEST.json` and require no regeneration.

---

## Security

User-defined skill files go through a security check before injection. Content that does not pass is blocked and surfaced as an alert. Bundled skills with a verified content signature are trusted at load time. Edit bundled content deliberately and regenerate the manifest afterward.

When proposing or explaining a skill pack, describe any content concern in terms of what the skill says (e.g., "this instruction asks the assistant to expose credentials"), not in terms of how the check works internally. The checking mechanism is not disclosed to users.

---

## Extending bundled skills

1. **Working examples** — add a folder under `radiant_llm_skills/working_examples/` with `README.md` and curated reference companions.
2. **Reusable rules** — add `.md` files under the appropriate module family (`radiant_llm_skills/<module>/rules/`).
3. **New bundled module** — new top-level modules must be registered in `RADIANT_AVAILABLE_SKILL_MODULES` in the skill loader before they can auto-route. Discovery surfaces a warning. For drop-in packs with no loader change, place them in the user skills directory instead.

Do not promote unvalidated or preliminary material into the bundled skills tree.

---

## User template

Copy `user_skills/_template/` into your skills directory and edit its `SKILL.md`.

---

## Agent checklist

```
[ ] User asked to save/promote session knowledge
[ ] Confirmed User skills path is set and exists
[ ] Drafted full SKILL.md with name + description
[ ] Presented Skill Proposal with full draft; waiting for explicit yes
[ ] User said yes (not ambiguous)
[ ] Called SkillPromotionTool with dry_run=True first, then user_approved=True
[ ] Wrote only under <user_skills_path>/<pack-slug>/
[ ] Suggested a verification query matching the description
[ ] Did NOT modify bundled radiant_llm_skills/ unless bundled promotion was explicitly approved
[ ] Reminded user to rescan in Settings if the directory was newly configured
```
