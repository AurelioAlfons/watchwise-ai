import asyncio
import time

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.schemas import RecommendRequest, RecommendResponse, Recommendation
from app.services import tmdb_service, ai_service

app = FastAPI(title="WatchWise AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.on_event("shutdown")
async def shutdown():
    await tmdb_service.get_client().aclose()


async def _get_candidates(req: RecommendRequest, media_type: str) -> list[dict]:
    genre_id = None

    if req.genre:
        genres = await tmdb_service.get_genres(media_type)
        genre_id = genres.get(req.genre.lower())

    if req.similar_title:
        results = await tmdb_service.search_title(req.similar_title, "multi")
    else:
        results = await tmdb_service.discover(media_type, genre_id)

    candidates = []

    for r in results[:15]:
        title = r.get("title") or r.get("name")
        if not title:
            continue

        candidates.append({
            "id": r["id"],
            "title": title,
            "media_type": r.get("media_type", media_type),
            "overview": r.get("overview", ""),
            "genre_names": req.genre or "",
            "poster_path": r.get("poster_path"),
        })

    return candidates


@app.post("/recommend", response_model=RecommendResponse)
async def recommend(req: RecommendRequest):
    start_time = time.perf_counter()

    media_types = ["movie", "tv"] if req.media_type == "any" else [req.media_type]

    t0 = time.perf_counter()
    candidate_lists = await asyncio.gather(*[
        _get_candidates(req, mt)
        for mt in media_types
    ])
    print(f"[TIMING] Candidate search: {time.perf_counter() - t0:.2f}s")

    candidates = [c for sub in candidate_lists for c in sub]

    if not candidates:
        raise HTTPException(404, "No matching titles found")

    t1 = time.perf_counter()
    picks = await ai_service.rank_and_explain(req, candidates)
    print(f"[TIMING] AI ranking: {time.perf_counter() - t1:.2f}s")

    if not picks:
        raise HTTPException(502, "AI ranking failed")

    candidate_map = {c["id"]: c for c in candidates}

    valid_picks = [
        p for p in picks[:5]
        if p["id"] in candidate_map
    ]

    t2 = time.perf_counter()
    infos = await asyncio.gather(*[
        tmdb_service.get_full_title_info(
            candidate_map[p["id"]]["media_type"],
            p["id"],
        )
        for p in valid_picks
    ])
    print(f"[TIMING] TMDB enrichment: {time.perf_counter() - t2:.2f}s")

    recommendations = []

    for pick, info in zip(valid_picks, infos):
        c = candidate_map[pick["id"]]

        recommendations.append(
            Recommendation(
                title=c["title"],
                media_type=c["media_type"],
                reason=pick["reason"],
                genre=", ".join(info["genres"]) or (req.genre or ""),
                runtime=info["runtime"],
                age_rating=info["age_rating"],
                rating=info["rating"],
                where_to_watch=info["where_to_watch"],
                poster_url=(
                    f"https://image.tmdb.org/t/p/w342{c['poster_path']}"
                    if c.get("poster_path")
                    else None
                ),
            )
        )

    print(f"[TIMING] Total request: {time.perf_counter() - start_time:.2f}s")

    return RecommendResponse(recommendations=recommendations)