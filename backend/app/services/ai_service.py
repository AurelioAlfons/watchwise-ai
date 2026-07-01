import json
import httpx
from app.config import settings
from app.schemas import RecommendRequest

async def rank_and_explain(prefs: RecommendRequest, candidates: list[dict]) -> list[dict]:
    """
    candidates: list of {id, title, media_type, overview, genre_names}
    Returns list of {id, reason} for the top 5, picked by the LLM.
    """
    candidate_text = "\n".join(
        f"- id:{c['id']} | {c['title']} ({c['media_type']}) | genres: {c['genre_names']} | {c['overview'][:200]}"
        for c in candidates
    )

    prompt = f"""You are a movie/anime recommendation assistant.
User preferences:
- Type: {prefs.media_type}
- Genre: {prefs.genre}
- Mood: {prefs.mood}
- Watching with: {prefs.watching_with}
- Similar to: {prefs.similar_title}
- Notes: {prefs.free_text}

Here are candidate titles (only choose from this list, do not invent new titles):
{candidate_text}

Pick the best 5 matches and explain briefly (1-2 sentences) why each fits the user's mood and context.
Respond ONLY with valid JSON, no markdown, in this exact format:
[{{"id": <id>, "reason": "<short reason>"}}, ...]
"""

    if settings.AI_PROVIDER == "openai":
        return await _call_openai(prompt)
    return await _call_gemini(prompt)


async def _call_openai(prompt: str):
    async with httpx.AsyncClient(timeout=30.0) as client:
        r = await client.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {settings.OPENAI_API_KEY}"},
            json={
                "model": "gpt-4o-mini",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.6,
            },
        )
        r.raise_for_status()
        text = r.json()["choices"][0]["message"]["content"]
        return _safe_parse(text)


async def _call_gemini(prompt: str):
    async with httpx.AsyncClient(timeout=30.0) as client:
        r = await client.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={settings.GEMINI_API_KEY}",
            json={"contents": [{"parts": [{"text": prompt}]}]},
        )
        r.raise_for_status()
        text = r.json()["candidates"][0]["content"]["parts"][0]["text"]
        return _safe_parse(text)


def _safe_parse(text: str):
    text = text.strip().strip("```json").strip("```").strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return []