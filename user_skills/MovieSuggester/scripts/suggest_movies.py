"""
Suggest movies from a natural-language prompt using the TMDb public API.

Usage:
    python suggest_movies.py --api-key "YOUR_KEY" --prompt "funny sci-fi" \\
        --availability subscription --recency latest --min-rating 6.5 \\
        --count 10 --region US --output-format chat

Save to file:
    python suggest_movies.py --api-key "YOUR_KEY" --prompt "classic noir" \\
        --recency classic --output-format json \\
        --output-dir /abs/path/movie_reports --basename noir_results

Install dependencies:
    pip install -r ../requirements.txt

TMDb API key:
    Obtain a free API key at https://www.themoviedb.org/settings/api
    Pass it via --api-key or the TMDB_API_KEY environment variable.
    The key is used only for read requests and is never stored or logged.

Attribution:
    This script uses the TMDb API but is not endorsed or certified by TMDb.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from datetime import date, timedelta
from pathlib import Path
from typing import Any

try:
    import requests
except ImportError:
    sys.exit("Missing dependency: pip install requests")

try:
    from tabulate import tabulate
    _TABULATE_AVAILABLE = True
except ImportError:
    _TABULATE_AVAILABLE = False

# ---------------------------------------------------------------------------
# TMDb constants
# ---------------------------------------------------------------------------

TMDB_BASE = "https://api.themoviedb.org/3"

# TMDb genre id → name mapping (static; matches TMDb genre list as of 2024)
GENRE_MAP: dict[int, str] = {
    28: "Action", 12: "Adventure", 16: "Animation", 35: "Comedy",
    80: "Crime", 99: "Documentary", 18: "Drama", 10751: "Family",
    14: "Fantasy", 36: "History", 27: "Horror", 10402: "Music",
    9648: "Mystery", 10749: "Romance", 878: "Science Fiction",
    10770: "TV Movie", 53: "Thriller", 10752: "War", 37: "Western",
}

# Keyword synonyms → TMDb genre ids (lower-case prompt matching)
KEYWORD_TO_GENRE_IDS: dict[str, list[int]] = {
    "action":          [28],
    "adventure":       [12],
    "animation":       [16],
    "animated":        [16],
    "comedy":          [35],
    "funny":           [35],
    "humor":           [35],
    "humour":          [35],
    "crime":           [80],
    "documentary":     [99],
    "doc":             [99],
    "drama":           [18],
    "family":          [10751],
    "kids":            [10751, 16],
    "children":        [10751, 16],
    "fantasy":         [14],
    "history":         [36],
    "historical":      [36],
    "horror":          [27],
    "scary":           [27],
    "music":           [10402],
    "musical":         [10402],
    "mystery":         [9648],
    "noir":            [9648, 80, 53],
    "romance":         [10749],
    "romantic":        [10749],
    "love":            [10749],
    "sci-fi":          [878],
    "scifi":           [878],
    "science fiction": [878],
    "space":           [878, 12],
    "thriller":        [53],
    "suspense":        [53],
    "war":             [10752],
    "western":         [37],
}

# Watch monetization types per availability tier
AVAILABILITY_MONETIZATION: dict[str, list[str]] = {
    "free":         ["free", "ads"],
    "subscription": ["flatrate"],
    "rent":         ["rent"],
    "buy":          ["buy"],
    "any":          ["free", "ads", "flatrate", "rent", "buy"],
}


# ---------------------------------------------------------------------------
# API helpers
# ---------------------------------------------------------------------------

def _get(url: str, api_key: str, params: dict | None = None) -> dict:
    merged = {"api_key": api_key, **(params or {})}
    resp = requests.get(url, params=merged, timeout=10)
    resp.raise_for_status()
    return resp.json()


def fetch_genre_ids_from_tmdb(api_key: str) -> dict[str, int]:
    """Return {genre_name_lower: id} from the live TMDb genre list."""
    data = _get(f"{TMDB_BASE}/genre/movie/list", api_key, {"language": "en"})
    return {g["name"].lower(): g["id"] for g in data.get("genres", [])}


def resolve_genre_ids(prompt: str) -> list[int]:
    """Map prompt keywords to a deduplicated list of TMDb genre ids."""
    prompt_lower = prompt.lower()
    ids: list[int] = []
    for keyword, genre_ids in KEYWORD_TO_GENRE_IDS.items():
        if keyword in prompt_lower:
            for gid in genre_ids:
                if gid not in ids:
                    ids.append(gid)
    return ids


def date_range_for_recency(recency: str) -> tuple[str | None, str | None]:
    """Return (gte_date, lte_date) strings for the recency filter."""
    today = date.today()
    if recency == "latest":
        gte = (today - timedelta(days=365)).isoformat()
        return gte, today.isoformat()
    if recency == "recent":
        gte = (today - timedelta(days=365 * 3)).isoformat()
        return gte, today.isoformat()
    if recency == "classic":
        return None, "2000-01-01"
    return None, None  # "any"


def discover_movies(
    api_key: str,
    genre_ids: list[int],
    recency: str,
    min_rating: float,
    region: str,
    page: int = 1,
) -> list[dict]:
    gte, lte = date_range_for_recency(recency)
    params: dict[str, Any] = {
        "language": "en-US",
        "sort_by": "popularity.desc",
        "vote_average.gte": min_rating,
        "vote_count.gte": 50,
        "region": region,
        "page": page,
    }
    if genre_ids:
        params["with_genres"] = ",".join(str(g) for g in genre_ids)
    if gte:
        params["primary_release_date.gte"] = gte
    if lte:
        params["primary_release_date.lte"] = lte

    data = _get(f"{TMDB_BASE}/discover/movie", api_key, params)
    return data.get("results", [])


def fetch_watch_providers(
    api_key: str, movie_id: int, region: str
) -> list[str]:
    """Return provider names available in the given region."""
    try:
        data = _get(f"{TMDB_BASE}/movie/{movie_id}/watch/providers", api_key)
        region_data = data.get("results", {}).get(region, {})
        names: list[str] = []
        for entry in region_data.values():
            if isinstance(entry, list):
                for provider in entry:
                    name = provider.get("provider_name", "")
                    if name and name not in names:
                        names.append(name)
        return names
    except Exception:
        return []


def fetch_watch_providers_filtered(
    api_key: str, movie_id: int, region: str, availability: str
) -> list[str]:
    """Return provider names matching the requested monetization tier."""
    if availability == "any":
        return fetch_watch_providers(api_key, movie_id, region)

    wanted_types = AVAILABILITY_MONETIZATION.get(availability, [])
    try:
        data = _get(f"{TMDB_BASE}/movie/{movie_id}/watch/providers", api_key)
        region_data = data.get("results", {}).get(region, {})
        names: list[str] = []
        for mon_type, entries in region_data.items():
            if mon_type in wanted_types and isinstance(entries, list):
                for provider in entries:
                    name = provider.get("provider_name", "")
                    if name and name not in names:
                        names.append(name)
        return names
    except Exception:
        return []


# ---------------------------------------------------------------------------
# Core pipeline
# ---------------------------------------------------------------------------

def build_suggestions(
    api_key: str,
    prompt: str,
    availability: str,
    recency: str,
    min_rating: float,
    count: int,
    region: str,
) -> list[dict]:
    genre_ids = resolve_genre_ids(prompt)

    candidates: list[dict] = []
    page = 1
    while len(candidates) < count * 3 and page <= 5:
        results = discover_movies(api_key, genre_ids, recency, min_rating, region, page)
        if not results:
            break
        candidates.extend(results)
        page += 1

    suggestions: list[dict] = []
    for movie in candidates:
        movie_id = movie["id"]
        providers = fetch_watch_providers_filtered(api_key, movie_id, region, availability)

        if availability != "any" and not providers:
            continue

        genre_names = [
            GENRE_MAP.get(gid, str(gid)) for gid in movie.get("genre_ids", [])
        ]
        release_year = (movie.get("release_date") or "")[:4] or "N/A"

        suggestions.append({
            "id":           movie_id,
            "title":        movie.get("title", "Unknown"),
            "year":         release_year,
            "rating":       round(movie.get("vote_average", 0.0), 1),
            "genres":       ", ".join(genre_names) if genre_names else "N/A",
            "overview":     (movie.get("overview") or "")[:200],
            "available_on": ", ".join(providers) if providers else "N/A",
            "tmdb_url":     f"https://www.themoviedb.org/movie/{movie_id}",
        })

        if len(suggestions) >= count:
            break

    return suggestions


# ---------------------------------------------------------------------------
# Output formatters
# ---------------------------------------------------------------------------

def format_chat(suggestions: list[dict]) -> str:
    if not suggestions:
        return "No movies found matching your criteria. Try relaxing the filters."

    rows = [
        [
            i + 1,
            s["title"],
            s["year"],
            s["rating"],
            s["genres"],
            s["available_on"],
        ]
        for i, s in enumerate(suggestions)
    ]
    headers = ["#", "Title", "Year", "Rating", "Genres", "Available on"]

    if _TABULATE_AVAILABLE:
        table = tabulate(rows, headers=headers, tablefmt="github")
    else:
        col_widths = [max(len(str(r[c])) for r in ([headers] + rows)) for c in range(len(headers))]
        def fmt_row(row: list) -> str:
            return "| " + " | ".join(str(v).ljust(col_widths[i]) for i, v in enumerate(row)) + " |"
        sep = "| " + " | ".join("-" * w for w in col_widths) + " |"
        lines = [fmt_row(headers), sep] + [fmt_row(r) for r in rows]
        table = "\n".join(lines)

    notes = []
    for i, s in enumerate(suggestions):
        if s["overview"]:
            notes.append(f"{i + 1}. **{s['title']}** — {s['overview'].rstrip('.')}.")

    footer = (
        "\n\n_Availability data from TMDb Watch Providers and may lag real-world "
        "offerings. This product uses the TMDb API but is not endorsed by TMDb._"
    )
    return table + "\n\n" + "\n".join(notes) + footer


def save_json(suggestions: list[dict], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as fh:
        json.dump(suggestions, fh, indent=2, ensure_ascii=False)
    print(f"JSON saved: {output_path.resolve()}")


def save_csv(suggestions: list[dict], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["title", "year", "rating", "genres", "available_on", "tmdb_url", "overview"]
    with output_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(suggestions)
    print(f"CSV saved: {output_path.resolve()}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Suggest movies from a prompt using the TMDb public API."
    )
    parser.add_argument(
        "--api-key",
        default=os.environ.get("TMDB_API_KEY", ""),
        help="TMDb API key (or set TMDB_API_KEY env var)",
    )
    parser.add_argument(
        "--prompt",
        required=True,
        help='Natural-language prompt, e.g. "funny sci-fi adventure"',
    )
    parser.add_argument(
        "--availability",
        choices=["free", "subscription", "rent", "buy", "any"],
        default="any",
        help="Filter by watch availability tier (default: any)",
    )
    parser.add_argument(
        "--recency",
        choices=["latest", "recent", "classic", "any"],
        default="any",
        help=(
            "latest = last 12 months; recent = last 3 years; "
            "classic = before 2000; any = no filter (default: any)"
        ),
    )
    parser.add_argument(
        "--min-rating",
        type=float,
        default=6.0,
        help="Minimum TMDb vote average 0–10 (default: 6.0)",
    )
    parser.add_argument(
        "--count",
        type=int,
        default=10,
        help="Number of suggestions to return (default: 10)",
    )
    parser.add_argument(
        "--region",
        default="US",
        help="ISO 3166-1 alpha-2 region for watch providers (default: US)",
    )
    parser.add_argument(
        "--output-format",
        choices=["chat", "json", "csv"],
        default="chat",
        help="Output format: chat (terminal table), json, or csv (default: chat)",
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Absolute directory for json/csv output (required when not using chat format)",
    )
    parser.add_argument(
        "--basename",
        default="movie_suggestions",
        help="Output filename stem without extension (default: movie_suggestions)",
    )
    args = parser.parse_args()

    # --- Validate API key ---
    api_key = args.api_key.strip()
    if not api_key:
        print(
            "Error: TMDb API key is required.\n"
            "  Pass --api-key 'YOUR_KEY' or set TMDB_API_KEY in the environment.\n"
            "  Get a free key at https://www.themoviedb.org/settings/api",
            file=sys.stderr,
        )
        return 1

    # --- Validate output path for file formats ---
    output_dir: Path | None = None
    if args.output_format in ("json", "csv"):
        if not args.output_dir:
            print(
                "Error: --output-dir is required when --output-format is json or csv.",
                file=sys.stderr,
            )
            return 1
        output_dir = Path(args.output_dir).expanduser().resolve()
        if output_dir.exists() and not output_dir.is_dir():
            print(f"Error: output path is not a directory: {output_dir}", file=sys.stderr)
            return 1

    # --- Validate numeric arguments ---
    if not (0.0 <= args.min_rating <= 10.0):
        print("Error: --min-rating must be between 0.0 and 10.0.", file=sys.stderr)
        return 1
    if args.count < 1:
        print("Error: --count must be at least 1.", file=sys.stderr)
        return 1

    print(f"Querying TMDb for: {args.prompt!r}")
    print(f"  availability={args.availability}  recency={args.recency}  "
          f"min_rating={args.min_rating}  count={args.count}  region={args.region}")

    try:
        suggestions = build_suggestions(
            api_key=api_key,
            prompt=args.prompt,
            availability=args.availability,
            recency=args.recency,
            min_rating=args.min_rating,
            count=args.count,
            region=args.region,
        )
    except requests.exceptions.HTTPError as exc:
        status = exc.response.status_code if exc.response is not None else "?"
        if status == 401:
            print("Error: TMDb API returned 401 Unauthorized. Check your bearer token.", file=sys.stderr)
        elif status == 429:
            print("Error: TMDb rate limit reached. Wait a moment and retry.", file=sys.stderr)
        else:
            print(f"Error: TMDb API request failed ({status}): {exc}", file=sys.stderr)
        return 1
    except requests.exceptions.ConnectionError:
        print("Error: Could not reach the TMDb API. Check your internet connection.", file=sys.stderr)
        return 1
    except requests.exceptions.Timeout:
        print("Error: TMDb API request timed out. Retry or check your connection.", file=sys.stderr)
        return 1

    if args.output_format == "chat":
        print("\n" + format_chat(suggestions))
    elif args.output_format == "json":
        save_json(suggestions, output_dir / f"{args.basename}.json")
    elif args.output_format == "csv":
        save_csv(suggestions, output_dir / f"{args.basename}.csv")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
