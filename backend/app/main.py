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
    if req.similar_title:
        seed, results = await tmdb_service.find_similar_titles(req.similar_title)

        if not results:
            genre_id = None
            if req.genre:
                genres = await tmdb_service.get_genres(media_type)
                genre_id = genres.get(req.genre.lower())

            results = await tmdb_service.discover(media_type, genre_id)
    else:
        genre_id = None

        if req.genre:
            genres = await tmdb_service.get_genres(media_type)
            genre_id = genres.get(req.genre.lower())

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

    t0 = time.perf_counter()

    if req.similar_title:
        candidates = await _get_candidates(req, "movie")
    else:
        media_types = ["movie", "tv"] if req.media_type == "any" else [req.media_type]

        candidate_lists = await asyncio.gather(*[
            _get_candidates(req, mt)
            for mt in media_types
        ])

        candidates = [c for sub in candidate_lists for c in sub]

    print(f"TIME:     Candidate search: {time.perf_counter() - t0:.2f}s", flush=True)

    if not candidates:
        raise HTTPException(404, "No matching titles found")

    t1 = time.perf_counter()

    try:
        picks = await ai_service.rank_and_explain(req, candidates)
    except ai_service.AIServiceError as e:
        print(f"AI:       {e.status_code} {e.message}", flush=True)
        raise HTTPException(status_code=e.status_code, detail=e.message)

    print(f"TIME:     AI ranking: {time.perf_counter() - t1:.2f}s", flush=True)

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

    print(f"TIME:     TMDB enrichment: {time.perf_counter() - t2:.2f}s", flush=True)

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

    print(f"TIME:     Total request: {time.perf_counter() - start_time:.2f}s", flush=True)

    return RecommendResponse(recommendations=recommendations)