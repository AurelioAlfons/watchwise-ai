import httpx
from app.config import settings

GENRE_MAP_MOVIE = {}  # populated lazily
GENRE_MAP_TV = {}

async def _client():
    return httpx.AsyncClient(
        base_url=settings.TMDB_BASE_URL,
        params={"api_key": settings.TMDB_API_KEY},
        timeout=10.0,
    )

async def search_title(query: str, media_type: str = "multi"):
    async with await _client() as client:
        r = await client.get(f"/search/{media_type}", params={"query": query})
        r.raise_for_status()
        return r.json().get("results", [])

async def discover(media_type: str, genre_id: int | None = None, page: int = 1):
    async with await _client() as client:
        params = {"sort_by": "popularity.desc", "page": page}
        if genre_id:
            params["with_genres"] = genre_id
        r = await client.get(f"/discover/{media_type}", params=params)
        r.raise_for_status()
        return r.json().get("results", [])

async def get_genres(media_type: str):
    async with await _client() as client:
        r = await client.get(f"/genre/{media_type}/list")
        r.raise_for_status()
        return {g["name"].lower(): g["id"] for g in r.json().get("genres", [])}

async def get_details(media_type: str, tmdb_id: int):
    async with await _client() as client:
        r = await client.get(f"/{media_type}/{tmdb_id}")
        r.raise_for_status()
        return r.json()

async def get_watch_providers(media_type: str, tmdb_id: int):
    async with await _client() as client:
        r = await client.get(f"/{media_type}/{tmdb_id}/watch/providers")
        r.raise_for_status()
        data = r.json().get("results", {}).get(settings.REGION, {})
        flatrate = data.get("flatrate", [])
        return [p["provider_name"] for p in flatrate]

async def get_age_rating(media_type: str, tmdb_id: int):
    async with await _client() as client:
        if media_type == "movie":
            r = await client.get(f"/movie/{tmdb_id}/release_dates")
            r.raise_for_status()
            for entry in r.json().get("results", []):
                if entry["iso_3166_1"] == settings.REGION:
                    for rel in entry.get("release_dates", []):
                        if rel.get("certification"):
                            return rel["certification"]
        else:
            r = await client.get(f"/tv/{tmdb_id}/content_ratings")
            r.raise_for_status()
            for entry in r.json().get("results", []):
                if entry["iso_3166_1"] == settings.REGION:
                    return entry.get("rating")
    return None