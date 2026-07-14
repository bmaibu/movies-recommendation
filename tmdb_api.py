"""
TMDB API helper module for fetching movie posters, details, and metadata.
API Key: 2484efa411f3e542fa29cdb743469f04
"""

import requests

TMDB_API_KEY = "2484efa411f3e542fa29cdb743469f04"
TMDB_BASE_URL = "https://api.tmdb.org/3"
TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w500"
TMDB_PLACEHOLDER = "https://via.placeholder.com/500x750/1a1a2e/e94560?text=No+Poster"


def search_movie(title: str) -> dict | None:
    """Search TMDB for a movie by title. Returns first match or None."""
    try:
        url = f"{TMDB_BASE_URL}/search/movie"
        params = {
            "api_key": TMDB_API_KEY,
            "query": title,
            "language": "en-US",
            "page": 1,
            "include_adult": False,
        }
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        results = response.json().get("results", [])
        return results[0] if results else None
    except Exception:
        return None


def get_movie_details(title: str) -> dict:
    """
    Fetch enriched movie details from TMDB by title.

    Returns a dict with:
      - poster_url: Full poster image URL
      - overview: Movie description
      - vote_average: TMDB rating (0–10)
      - release_year: 4-digit year string
      - genres: Comma-separated genre names
      - tmdb_id: TMDB movie ID
    """
    result = search_movie(title)

    if not result:
        return {
            "poster_url": TMDB_PLACEHOLDER,
            "overview": "No overview available.",
            "vote_average": 0.0,
            "release_year": "N/A",
            "genres": "Unknown",
            "tmdb_id": None,
        }

    poster_path = result.get("poster_path")
    poster_url = f"{TMDB_IMAGE_BASE}{poster_path}" if poster_path else TMDB_PLACEHOLDER

    release_date = result.get("release_date", "")
    release_year = release_date[:4] if release_date else "N/A"

    # Fetch full details for genre names
    genre_names = "Unknown"
    tmdb_id = result.get("id")
    if tmdb_id:
        try:
            detail_url = f"{TMDB_BASE_URL}/movie/{tmdb_id}"
            detail_resp = requests.get(
                detail_url,
                params={"api_key": TMDB_API_KEY, "language": "en-US"},
                timeout=5,
            )
            detail_resp.raise_for_status()
            details = detail_resp.json()
            genres = details.get("genres", [])
            genre_names = ", ".join(g["name"] for g in genres) if genres else "Unknown"
        except Exception:
            genre_names = "Unknown"

    return {
        "poster_url": poster_url,
        "overview": result.get("overview", "No overview available."),
        "vote_average": round(result.get("vote_average", 0.0), 1),
        "release_year": release_year,
        "genres": genre_names,
        "tmdb_id": tmdb_id,
    }


def get_poster_url(poster_path: str | None) -> str:
    """Build a full TMDB poster URL from a poster_path string."""
    if not poster_path:
        return TMDB_PLACEHOLDER
    return f"{TMDB_IMAGE_BASE}{poster_path}"
