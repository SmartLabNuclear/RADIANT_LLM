# Publishing `visual-parser` to PyPI

No documented publish process existed before this — the previous 8 releases (1.0.0 through 2.0.4) were pushed ad hoc, and 5 of them ended up yanked (3 for a licensing change, 4 more for a stale README). This runbook exists so that doesn't keep happening.

## 0. Before you touch any of this

Check the current live state first: **https://pypi.org/project/visual-parser/** — confirm the version you're about to build doesn't already exist there (PyPI never lets you reuse a version number, even after a yank).

## 1. Bump the version — in *both* places

These two **must** agree, or you get exactly the three-way version confusion this project already had once (`pyproject.toml` said 2.0.4, `__init__.py` said 2.0.2, the built `dist/` said 2.0.3 — all different, all at once):

- `pyproject.toml` → `version = "X.Y.Z"`
- `visual_parser/__init__.py` → `__version__ = "X.Y.Z"`

Use semantic versioning: patch (`X.Y.Z+1`) for bug-fix-only releases, minor (`X.Y+1.0`) when you've added new backward-compatible functionality (new flags, new features), major for breaking changes.

## 2. Sanity-check the packaging itself, not just the code

This is the step that got skipped 4 times in a row before. Actually look at:

- `README.md` — does it mention everything new since the last release? Check the "Common configuration flags" list and the `.env` / API keys section specifically — new CLI flags and new env vars are the easiest things to forget.
- `requirements.txt` vs. `pyproject.toml`'s `dependencies` — do they actually agree? (They didn't, once — `pyproject.toml` had hard `==` pins while `requirements.txt` had the correct `>=` ranges with useful comments like the GPU-wheel caveat.)
- `LICENSE` — does a real file exist at the repo root matching what `pyproject.toml` declares? (It didn't, once.)

## 3. Clean and build

```bash
cd C:\Dev\CodeBase_Local\visual-parser
rm dist/visual_parser-*          # remove any older-version artifacts sitting in dist/
python -m pip install --upgrade build   # only if not already installed
python -m build
```

Confirms the built filenames actually match your bumped version — if they don't, something above didn't get saved.

## 4. Verify the actual built artifact before uploading anything

Don't trust the source tree — inspect what actually got packaged:

```bash
python -c "
import zipfile
with zipfile.ZipFile('dist/visual_parser-X.Y.Z-py3-none-any.whl') as z:
    print(z.read('visual_parser-X.Y.Z.dist-info/METADATA').decode())
"
```

Check: `Version:` matches, `License-Expression:`/`License-File:` are present (not just declared in `pyproject.toml` with nothing backing it), and `Requires-Dist:` lines look like ranges (`>=`), not surprise exact pins.

Then do a real install test in a throwaway venv — this is what actually catches "works from my editable install but not from the real package" bugs:

```bash
python -m venv /tmp/vp_test_venv
/tmp/vp_test_venv/Scripts/pip install dist/visual_parser-X.Y.Z-py3-none-any.whl
/tmp/vp_test_venv/Scripts/visual-parser --version
/tmp/vp_test_venv/Scripts/visual-parser --help
```
Watch the `--help`/`--version` output for any unexpected warnings (a fresh venv resolves the *newest* version satisfying your `>=` ranges, which can surface deprecation warnings — e.g. `torch`/PyMuPDF — that don't show up in your own older, already-installed dev venv).

Delete the throwaway venv when done.

## 5. Upload

```bash
pip install twine   # if not already installed
python -m twine upload dist/visual_parser-X.Y.Z.tar.gz dist/visual_parser-X.Y.Z-py3-none-any.whl
```

Credentials: username `__token__`, password = your PyPI API token (or however `~/.pypirc`/env vars are already configured on this machine).

**Optional but worth it for a release with real new functionality**: dry-run against TestPyPI first (`--repository testpypi`, needs a separate TestPyPI account/token) before the real upload.

## 6. After uploading

- Check **https://pypi.org/project/visual-parser/** — confirm the new version shows as the current release, not yanked.
- Sync the same version bump + any fixes into the SmartLab-org mirror at `C:\Dev\CodeBase_Local\Github-Repos\RADIANT-llm-git\RADIANT_LLM\Visual-Parser\` (its `pyproject.toml`/`Homepage`/`Repository` point at `github.com/SmartLabNuclear/RADIANT_LLM`, and it should stay a mirror of whatever actually got published). Diff-check before copying, same as always. Not committed/pushed automatically — that part is a deliberate, separate `git add`/`commit`/`push` step.

## If something's wrong after publishing

You can **yank** a version (removes it from being installable by default, without deleting it — the version number still can't be reused): from the PyPI web UI, on the release's page. That's the safety net if step 2 or 4 above gets skipped again.
