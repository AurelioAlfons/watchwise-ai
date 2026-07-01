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

@app.post("/recommend", response_model=RecommendResponse)
async def recommend(req: RecommendRequest):
    media_types = ["movie", "tv"] if req.media_type == "any" else [req.media_type]
    candidates = []

    for mt in media_types:
        genre_id = None
        if req.genre:
            genres = await tmdb_service.get_genres(mt)
            genre_id = genres.get(req.genre.lower())

        if req.similar_title:
            results = await tmdb_service.search_title(req.similar_title, "multi")
        else:
            results = await tmdb_service.discover(mt, genre_id)

        for r in results[:15]:
            title = r.get("title") or r.get("name")
            if not title:
                continue

            candidates.append({
                "id": r["id"],
                "title": title,
                "media_type": r.get("media_type", mt),
                "overview": r.get("overview", ""),
                "genre_names": req.genre or "",
                "poster_path": r.get("poster_path"),
            })

    if not candidates:
        raise HTTPException(404, "No matching titles found")

    picks = await ai_service.rank_and_explain(req, candidates)

    if not picks:
        raise HTTPException(502, "AI ranking failed")

    candidate_map = {c["id"]: c for c in candidates}
    recommendations = []

    for pick in picks[:5]:
        c = candidate_map.get(pick["id"])
        if not c:
            continue

        details = await tmdb_service.get_details(c["media_type"], c["id"])
        providers = await tmdb_service.get_watch_providers(c["media_type"], c["id"])
        age_rating = await tmdb_service.get_age_rating(c["media_type"], c["id"])

        runtime = None
        if c["media_type"] == "movie" and details.get("runtime"):
            runtime = f"{details['runtime']} min"
        elif details.get("episode_run_time"):
            ert = details["episode_run_time"]
            if ert:
                runtime = f"{ert[0]} min/ep"

        recommendations.append(Recommendation(
            title=c["title"],
            media_type=c["media_type"],
            reason=pick["reason"],
            genre=", ".join(g["name"] for g in details.get("genres", [])),
            runtime=runtime,
            age_rating=age_rating,
            rating=details.get("vote_average"),
            where_to_watch=providers,
            poster_url=f"https://image.tmdb.org/t/p/w342{c['poster_path']}" if c.get("poster_path") else None,
        ))

    return RecommendResponse(recommendations=recommendations)