# visual-parser — Docker usage examples

Image: `zev94/radiant-llm:visual-parser-latest` (pinned: `visual-parser-1.0.2`)

All examples assume:
- A `.env` file with `OPENAI_API_KEY` and/or `GEMINI_API_KEY` in the directory where you run `docker`.
- PDFs are mounted at `/data` inside the container (`-v "/host/path/to/pdfs:/data"`).
- Outputs are written to the same folder unless `--output-dir` points elsewhere.

**Windows PowerShell:** use `` ` `` instead of `\` for line continuation, and mount paths like `"C:\path\to\pdfs:/data"`.

**Help (all flags):**
```bash
docker run --rm zev94/radiant-llm:visual-parser-latest --help
```

---

## Vision model presets

### Default (GPT-5.2, medium reasoning)

No extra flags needed — defaults are `--vision-provider gpt`, `--vision-model gpt-5.2`, `--reasoning-effort medium`.

```bash
docker run --rm --env-file .env \
  -v "/path/to/pdfs:/data" \
  zev94/radiant-llm:visual-parser-latest \
  --input-dir /data --output-dir /data
```

### Maximum reasoning (complex figures)

```bash
docker run --rm --env-file .env \
  -v "/path/to/pdfs:/data" \
  zev94/radiant-llm:visual-parser-latest \
  --input-dir /data --output-dir /data \
  --reasoning-effort xhigh
```

### Gemini 3 (latest Gemini preview)

```bash
docker run --rm --env-file .env \
  -v "/path/to/pdfs:/data" \
  zev94/radiant-llm:visual-parser-latest \
  --input-dir /data --output-dir /data \
  --vision-provider gemini
```

### Gemini 2.5 Flash (faster / lower cost)

```bash
docker run --rm --env-file .env \
  -v "/path/to/pdfs:/data" \
  zev94/radiant-llm:visual-parser-latest \
  --input-dir /data --output-dir /data \
  --vision-provider gemini --vision-model gemini-2.5-flash
```

### GPT-4o (previous-generation OpenAI)

```bash
docker run --rm --env-file .env \
  -v "/path/to/pdfs:/data" \
  zev94/radiant-llm:visual-parser-latest \
  --input-dir /data --output-dir /data \
  --vision-model gpt-4o
```

---

## Paths and text extraction

### Minimal (input directory only)

Output defaults to the same directory as input.

```bash
docker run --rm --env-file .env \
  -v "/path/to/pdfs:/data" \
  zev94/radiant-llm:visual-parser-latest \
  --input-dir /data
```

### Separate output directory + lightweight text mode

Mount a second volume for outputs. `lightweight` skips Nougat (faster, no GPU; uses PDF text layer).

```bash
docker run --rm --env-file .env \
  -v "/path/to/pdfs:/data" \
  -v "/path/to/out:/out" \
  zev94/radiant-llm:visual-parser-latest \
  --input-dir /data --output-dir /out --text-mode lightweight
```

### Nougat with custom chunking

```bash
docker run --rm --env-file .env \
  -v "/path/to/pdfs:/data" \
  zev94/radiant-llm:visual-parser-latest \
  --input-dir /data --output-dir /data \
  --text-mode nougat --chunk-size 500 --chunk-overlap 100
```

---

## Performance and parallel runs

### More worker threads (default is 4)

```bash
docker run --rm --env-file .env \
  -v "/path/to/pdfs:/data" \
  zev94/radiant-llm:visual-parser-latest \
  --input-dir /data --output-dir /data \
  --max-workers 6
```

### Gemini, fewer metadata pages, higher parallelism

```bash
docker run --rm --env-file .env \
  -v "/path/to/pdfs:/data" \
  zev94/radiant-llm:visual-parser-latest \
  --input-dir /data --output-dir /data \
  --vision-provider gemini --metadata-pages 1 --max-workers 8
```

---

## Rebuild and logging

### Full rebuild (ignore processed-PDF tracker)

Use after changing models, prompts, or chunk settings.

```bash
docker run --rm --env-file .env \
  -v "/path/to/pdfs:/data" \
  zev94/radiant-llm:visual-parser-latest \
  --input-dir /data --output-dir /data \
  --rebuild --reasoning-effort high --log-level INFO
```

### High image detail (dense schematics, GPT only)

```bash
docker run --rm --env-file .env \
  -v "/path/to/pdfs:/data" \
  zev94/radiant-llm:visual-parser-latest \
  --input-dir /data --output-dir /data \
  --vision-detail high
```

---

## Windows PowerShell (single example)

```powershell
docker run --rm --env-file .env `
  -v "C:\path\to\pdfs:/data" `
  zev94/radiant-llm:visual-parser-latest `
  --input-dir /data --output-dir /data `
  --vision-provider gemini --vision-model gemini-2.5-flash --text-mode lightweight
```

---

## Flag quick reference

| Group | Flags |
|-------|--------|
| **Paths** | `--input-dir` / `-i` (required), `--output-dir` / `-o` |
| **Text** | `--text-mode nougat\|lightweight`, `--nougat-model`, `--chunk-size`, `--chunk-overlap` |
| **Vision** | `--vision-provider gpt\|gemini`, `--vision-model`, `--vision-detail low\|high\|auto`, `--reasoning-effort none\|low\|medium\|high\|xhigh`, `--metadata-pages` |
| **Performance** | `--max-workers` |
| **Misc** | `--rebuild`, `--log-level DEBUG\|INFO\|WARNING\|ERROR` |

For the same scenarios run locally with Python, see `usage_examples.txt` in the full Visual-Parser source tree.
