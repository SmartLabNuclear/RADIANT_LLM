# TMDb API Patterns

Reference for `suggest_movies.py`. Read this when extending the script or debugging API behavior.

---

## Authentication

All requests use a **v3 API key** passed as the `api_key` query parameter:

```python
params = {"api_key": api_key, **other_params}
requests.get(url, params=params)
```

- Obtain a free API key at <https://www.themoviedb.org/settings/api> (account required).
- The key is read-only: it cannot create, modify, or delete TMDb records.
- Never commit keys to source control. Pass via `--api-key` flag or `TMDB_API_KEY` env var.

---

## Key endpoints used

### Discover movies

`GET https://api.themoviedb.org/3/discover/movie`

Returns a paginated list of movies matching filter criteria.

| Parameter | Type | Notes |
|-----------|------|-------|
| `with_genres` | string | Comma-separated TMDb genre ids |
| `primary_release_date.gte` | date (YYYY-MM-DD) | Lower bound on release date |
| `primary_release_date.lte` | date (YYYY-MM-DD) | Upper bound on release date |
| `vote_average.gte` | float | Minimum average rating (0–10) |
| `vote_count.gte` | int | Minimum vote count (avoids obscure low-vote films) |
| `sort_by` | string | `popularity.desc` is the useful default |
| `region` | string | ISO 3166-1 alpha-2; biases results toward that market |
| `page` | int | 1-based; max 500 pages per query |

Response shape (relevant fields):

```json
{
  "page": 1,
  "results": [
    {
      "id": 12345,
      "title": "Example Movie",
      "release_date": "2024-03-15",
      "vote_average": 7.4,
      "vote_count": 1200,
      "genre_ids": [28, 878],
      "overview": "Short plot summary..."
    }
  ],
  "total_pages": 42,
  "total_results": 830
}
```

### Watch providers

`GET https://api.themoviedb.org/3/movie/{movie_id}/watch/providers`

Returns streaming/rental/purchase availability per country region.

Response shape (relevant fields):

```json
{
  "results": {
    "US": {
      "flatrate": [{"provider_name": "Netflix", "provider_id": 8}],
      "free":     [{"provider_name": "Tubi TV",  "provider_id": 73}],
      "ads":      [{"provider_name": "Pluto TV", "provider_id": 300}],
      "rent":     [{"provider_name": "Apple TV", "provider_id": 2}],
      "buy":      [{"provider_name": "Amazon Video", "provider_id": 10}]
    }
  }
}
```

**Monetization type → availability tier mapping:**

| Tier | TMDb key(s) |
|------|-------------|
| `free` | `free`, `ads` |
| `subscription` | `flatrate` |
| `rent` | `rent` |
| `buy` | `buy` |
| `any` | all of the above |

**Caveat:** Watch provider data can lag real-world availability by days to weeks. Always note this to the user.

### Genre list

`GET https://api.themoviedb.org/3/genre/movie/list?language=en`

Returns the current official TMDb genre id ↔ name mapping. Use this to validate or refresh `GENRE_MAP` in the script if genre ids drift over time.

---

## Rate limits

- Free tier: ~40 requests per 10 seconds.
- The script makes 1 discover call + 1 watch-providers call per candidate movie.
- For `count=10`, expect ~15–30 API calls total (across pagination and provider checks).
- On HTTP 429, wait and retry with exponential backoff (not yet implemented; add if needed).

---

## Pagination

- Each discover page returns up to 20 results.
- The script fetches up to 5 pages (100 candidates) and stops once `count` matches are found.
- Increase `page` limit in `build_suggestions()` if filters are strict and results are sparse.

---

## Extending the script

### Add search by keyword/text

`GET https://api.themoviedb.org/3/search/movie?query=<text>`

Useful for title-based lookups; combine with the discover approach for fuzzy intent matching.

### Add cast/director filters

`GET https://api.themoviedb.org/3/search/person?query=<name>` → get person `id`  
Then pass `with_cast=<id>` or `with_crew=<id>` to `/discover/movie`.

### Add TV show support

Replace `/discover/movie` with `/discover/tv` and `/movie/{id}/watch/providers` with `/tv/{id}/watch/providers`. Genre ids differ for TV; fetch separately from `/genre/tv/list`.

---

## Attribution requirement

Per TMDb Terms of Use, any product using the API must display:

> This product uses the TMDb API but is not endorsed or certified by TMDb.

Include the TMDb logo where practical.
