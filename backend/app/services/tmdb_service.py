import asyncio
import httpx

from app.config import settings

_genre_cache: dict[str, dict[str, int]] = {}
_client_instance: httpx.AsyncClient | None = None


def get_client() -> httpx.AsyncClient:
    global _client_instance

    if _client_instance is None:
        _client_instance = httpx.AsyncClient(
            base_url=settings.TMDB_BASE_URL,
            params={"api_key": settings.TMDB_API_KEY},
            timeout=10.0,
            limits=httpx.Limits(
                max_keepalive_connections=20,
                max_connections=20,
            ),
        )

    return _client_instance


async def search_title(query: str, media_type: str = "multi"):
    client = get_client()
    r = await client.get(f"/search/{media_type}", params={"query": query})
    r.raise_for_status()
    return r.json().get("results", [])


async def find_similar_titles(title: str) -> tuple[dict | None, list[dict]]:
    client = get_client()

    search_results = await search_title(title, "multi")
    seed = next(
        (r for r in search_results if r.get("media_type") in ("movie", "tv")),
        None,
    )

    if not seed:
        return None, []

    media_type = seed["media_type"]
    tmdb_id = seed["id"]

    rec_resp, sim_resp = await asyncio.gather(
        client.get(f"/{media_type}/{tmdb_id}/recommendations"),
        client.get(f"/{media_type}/{tmdb_id}/similar"),
    )

    rec_resp.raise_for_status()
    sim_resp.raise_for_status()

    combined = (
        rec_resp.json().get("results", [])
        + sim_resp.json().get("results", [])
    )

    seed_title_lower = title.strip().lower()
    seen_ids = {tmdb_id}
    results = []

    for r in combined:
        if r.get("id") in seen_ids:
            continue

        r_title = (r.get("title") or r.get("name") or "").lower()

        if seed_title_lower and seed_title_lower in r_title:
            continue

        seen_ids.add(r["id"])
        r["media_type"] = r.get("media_type", media_type)
        results.append(r)

    return seed, results


async def discover(media_type: str, genre_id: int | None = None, page: int = 1):
    client = get_client()
    params = {"sort_by": "popularity.desc", "page": page}

    if genre_id:
        params["with_genres"] = genre_id

    r = await client.get(f"/discover/{media_type}", params=params)
    r.raise_for_status()
    return r.json().get("results", [])


async def get_genres(media_type: str):
    if media_type in _genre_cache:
        return _genre_cache[media_type]

    client = get_client()
    r = await client.get(f"/genre/{media_type}/list")
    r.raise_for_status()

    result = {
        g["name"].lower(): g["id"]
        for g in r.json().get("genres", [])
    }

    _genre_cache[media_type] = result
    return result


async def get_full_title_info(media_type: str, tmdb_id: int):
    append = (
        "watch/providers,release_dates"
        if media_type == "movie"
        else "watch/providers,content_ratings"
    )

    client = get_client()
    r = await client.get(
        f"/{media_type}/{tmdb_id}",
        params={"append_to_response": append},
    )
    r.raise_for_status()
    data = r.json()

    runtime = None
    if media_type == "movie" and data.get("runtime"):
        runtime = f"{data['runtime']} min"
    elif data.get("episode_run_time"):
        episode_times = data["episode_run_time"]
        if episode_times:
            runtime = f"{episode_times[0]} min/ep"

    watch_data = (
        data.get("watch/providers", {})
        .get("results", {})
        .get(settings.REGION, {})
    )

    providers = [
        p["provider_name"]
        for p in watch_data.get("flatrate", [])
    ]

    age_rating = None

    if media_type == "movie":
        for entry in data.get("release_dates", {}).get("results", []):
            if entry.get("iso_3166_1") == settings.REGION:
                for release in entry.get("release_dates", []):
                    if release.get("certification"):
                        age_rating = release["certification"]
                        break
                break
    else:
        for entry in data.get("content_ratings", {}).get("results", []):
            if entry.get("iso_3166_1") == settings.REGION:
                age_rating = entry.get("rating")
                break

    return {
        "genres": [g["name"] for g in data.get("genres", [])],
        "runtime": runtime,
        "rating": data.get("vote_average"),
        "age_rating": age_rating,
        "where_to_watch": providers,
    }