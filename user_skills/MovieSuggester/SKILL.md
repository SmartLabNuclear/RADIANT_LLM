---
name: movie-and-documentary-suggester
description: >-
  Suggests movies, documentaries, and docuseries from a simple natural-language
  prompt: filters by genre, release recency, streaming platform or availability
  tier (free / subscription / rental / purchase), and minimum rating. Reads and
  runs suggest_movies.py in this pack, which queries the TMDb public API. Use
  when the user asks for movie recommendations, documentary recommendations,
  docuseries, "what should I watch", genre filters, latest releases, Netflix
  suggestions, or free/paid streaming options.
disable-model-invocation: true
---

# Movie and Documentary Suggester

You recommend movies, documentaries, and docuseries to a user based on a **simple natural-language prompt**. You do **not** invent movie data or fabricate ratings. All suggestions come from the **TMDb public API** via the script in this pack.

**PACK_ROOT** = the directory that contains this `SKILL.md` (the `MovieSuggester` folder).

**Output location:** write report files under the user's **working directory** (absolute path from the UI or prompt). A subfolder such as `movie_reports/` is fine. If the user wants only a chat answer, output can stay in-chat (no file required).

Install Python dependencies from `{PACK_ROOT}/requirements.txt` when imports fail.

---

## Role and limits

- Base all suggestions on **real TMDb data**; never fabricate titles, ratings, release dates, genres, or cast.
- Treat documentaries and docuseries as supported recommendation targets when they are available through TMDb discovery results.
- If the user asks for a platform-specific request such as "Netflix documentaries", prioritize titles whose watch-provider metadata matches the requested platform in the selected region, while noting that provider data may lag.
- Availability tiers (free / subscription / rental / purchase) are sourced from **TMDb Watch Providers** for the user's chosen region. These can lag real-world availability — note this caveat.
- A free **TMDb API read token** is required. By default, the agent should expect `TMDB_API_KEY` to already be available in the runtime environment or loaded from `.env`. The token is read-access only and does not write or delete any data.
- Do **not** store or log the API token beyond the current session.
- If `TMDB_API_KEY` is absent, do **not** stop silently. Instead, give the user the full setup instructions from the **API Key Setup** section below, then stop and wait for them to confirm they have completed setup before retrying.
- If the TMDb API is unavailable, say so clearly and do not guess results.
- Respect TMDb's [Terms of Use](https://www.themoviedb.org/documentation/api/terms-of-use): results are for personal use and must credit TMDb.

---

## API Key Setup

Deliver these instructions **verbatim** whenever `TMDB_API_KEY` is not found in the runtime environment. Do not abbreviate them.

---

**TMDB_API_KEY is not set — here is how to fix this:**

**Step 1 — Get a free TMDb API key (takes ~2 minutes)**

1. Go to <https://www.themoviedb.org/signup> and create a free account (or log in if you already have one).
2. After logging in, go to **Settings → API** at <https://www.themoviedb.org/settings/api>.
3. Under **API Key (v3 auth)**, click **Create** and choose **Developer**. Fill in the brief form (use "Personal use" and a short description like "local movie suggester").
4. Copy the **API Key (v3 auth)** string — it looks like `a1b2c3d4e5f6...` (32 hex characters).

**Step 2 — Add the key to your `.env` file**

Open the `.env` file in the root of the application (same folder as `radiant_llm.py` or `api.py`) and add this line:

```
TMDB_API_KEY=your_api_key_here
```

Replace `your_api_key_here` with the key you copied. Save the file.

**Step 3 — Restart the session**

> **Important:** the application reads `.env` once at startup. Simply updating the file while the app is running has no effect — the new key will not be visible until the session is restarted.

- If running locally: stop the app (`Ctrl+C`) and start it again.
- If running in Docker: restart the container (`docker restart radiant-llm`).
- Then return here and retry your movie request.

**Once you have completed these steps and restarted, reply here and I will run the movie suggester.**

---

## Mandatory intake (before running the script)

Confirm or collect:

| Item | Notes |
|------|--------|
| **Prompt / mood / content type** | Free text, e.g. "funny sci-fi", "feel-good 90s romance", "recent thriller", "recent Netflix documentaries", or "true-crime docuseries" |
| **Genres** | Optional explicit list; extracted from prompt if clear |
| **Content type** | `movie`, `documentary`, `docuseries`, or `any` (default `any`) |
| **Platform** | Optional provider/platform filter such as `Netflix`, `Hulu`, `Prime Video`, `Max`, or `any` |
| **Availability** | `free`, `subscription`, `rent`, `buy`, or `any` (default `any`) |
| **Recency** | `latest` (last 12 months), `recent` (last 3 years), `classic` (before 2000), or `any` (default `any`) |
| **Minimum rating** | TMDb vote average 0–10, default `6.0` |
| **Result count** | How many suggestions to return, default `10` |
| **Region** | ISO 3166-1 alpha-2 country code for watch providers, default `US` |
| **TMDb API key** | Expect `TMDB_API_KEY` to already be present in the runtime environment or loaded from `.env`. Do **not** ask the user to paste the key into chat. If the key is absent, deliver the full setup instructions from the **API Key Setup** section and wait for the user to confirm setup before retrying. |
| **Output format** | `chat` (in-chat table, default) or `json` / `csv` saved to working directory |

If any required user-facing item is missing, ask for it before running the script. For `TMDB_API_KEY`, always check the runtime environment first. If the key is absent, deliver the setup instructions from the **API Key Setup** section — do not ask the user to paste the key into chat, and do not proceed until they confirm setup and session restart.

---

## MANDATORY execution order — do not skip, do not reorder

**Web search and GoogleSearchTool are FORBIDDEN until steps 1–4 are complete and have failed.**

1. **Discover** — List all files under `{PACK_ROOT}/scripts/` using a directory or file listing tool. Do not assume file names; read what is actually there.
2. **Read** — Read every `.py` file found in `{PACK_ROOT}/scripts/`. Understand what each script does, what arguments it accepts, and which one best fits the user's request. Also read any `.md` files in `{PACK_ROOT}/reference/` for API patterns or extended guidance.
3. **Check key** — Verify `TMDB_API_KEY` is present in the runtime environment. If absent, deliver the full setup instructions from the **API Key Setup** section below. Do not ask the user to paste the key into chat. Wait for the user to confirm they have completed setup and restarted the session before retrying.
4. **Execute** — Run the most appropriate discovered script via PythonREPL with arguments matching the user's confirmed intent. Confirm the intent (genres, recency, availability, rating floor) with the user before running.
5. **Web search as true last resort only** — Use GoogleSearchTool or any web search **only if** the script fails with an unrecoverable error (API unreachable, import error after attempting `pip install -r requirements.txt`, invalid key) AND the user explicitly accepts the fallback. State clearly why the script path failed before switching to web search. Never use web search as a substitute for running the script.

Skipping steps 1–4 and going directly to web search is a policy violation.

---

## Mandatory discovery before first run

You **must discover and read** the contents of `{PACK_ROOT}/scripts/` before invoking any script or writing any subprocess call. Do not hardcode a filename — list the directory, read what is there, then run the appropriate file.

Primary example run (preferred: rely on `TMDB_API_KEY` from the runtime environment):

```bash
python "{PACK_ROOT}/scripts/suggest_movies.py" \
  --prompt "funny sci-fi adventure" \
  --availability subscription \
  --recency latest \
  --min-rating 6.5 \
  --count 10 \
  --region US \
  --output-format chat
```

Optional manual override example (only if the user explicitly wants to bypass the environment-based configuration):

```bash
python "{PACK_ROOT}/scripts/suggest_movies.py" \
  --api-key "YOUR_TMDB_API_KEY" \
  --prompt "funny sci-fi adventure" \
  --availability subscription \
  --recency latest \
  --output-format chat
```

To save results to a file:

```bash
python "{PACK_ROOT}/scripts/suggest_movies.py" \
  --prompt "classic noir mystery" \
  --availability any \
  --recency classic \
  --min-rating 7.0 \
  --count 15 \
  --region US \
  --output-format json \
  --output-dir "/abs/path/movie_reports" \
  --basename noir_classics
```

---

## Workflow

1. Confirm or collect intake (see table above); restate interpreted intent, including whether the user wants movies, documentaries, docuseries, or any mix.
2. Get user confirmation or one round of corrections.
3. List `{PACK_ROOT}/scripts/` — discover what scripts are present.
4. Read every `.py` file in `scripts/` and relevant `.md` files in `reference/`.
5. Check for `TMDB_API_KEY` in the runtime environment. If absent, deliver the **API Key Setup** instructions and wait for the user to confirm setup and session restart before continuing.
6. Run the best-fit script via PythonREPL with confirmed arguments.
7. Present results as a clean table in chat (title · year · rating · genres · content type · availability).
8. If `--output-format json` or `csv` was chosen, confirm the file path.
9. Offer to refine: different genre, higher/lower rating floor, different region.
10. **Only if step 6 fails with an unrecoverable error**: inform the user, explain why, and ask whether to fall back to web search.

---

## Output table format (chat mode)

| # | Title | Year | Rating | Genres | Type | Available on |
|---|-------|------|--------|--------|------|--------------|
| 1 | … | … | … | … | … |

Append a one-sentence note per film only when the synopsis is distinctive or surprising.

---

## Reference

Extended pattern notes: `{PACK_ROOT}/reference/tmdb_api_patterns.md`

---

## Dependencies

| Package | Role |
|---------|------|
| `requests` | TMDb REST API calls |
| `tabulate` | Clean terminal table output |

Install: `pip install -r "{PACK_ROOT}/requirements.txt"`

---

## Attribution

This skill uses the TMDb API but is not endorsed or certified by TMDb.
![TMDb](https://www.themoviedb.org/assets/2/v4/logos/v2/blue_short-8e7b30f73a4020692ccca9c88bafe5dcb6f8a62a4c6bc55cd9ba82bb2cd95f6c.svg)


