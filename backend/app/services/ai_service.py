import json
import re
import httpx

from app.config import settings
from app.schemas import RecommendRequest


async def rank_and_explain(prefs: RecommendRequest, candidates: list[dict]) -> list[dict]:
    candidates = candidates[:20]

    candidate_text = "\n".join(
        f"- id:{c['id']} | {c['title']} ({c['media_type']}) | {c.get('overview', '')[:120]}"
        for c in candidates
    )

    prompt = f"""You recommend movies/anime.

User:
Type: {prefs.media_type}
Genre: {prefs.genre}
Mood: {prefs.mood}
Watching with: {prefs.watching_with}
Similar to: {prefs.similar_title}
Notes: {prefs.free_text}

Choose exactly 5 from this list only:
{candidate_text}

Return only valid JSON in this format:
[
  {{"id": 123, "reason": "short reason"}},
  {{"id": 456, "reason": "short reason"}}
]
"""

    if settings.AI_PROVIDER == "openai":
        return await _call_openai(prompt)

    return await _call_gemini(prompt)


async def _call_openai(prompt: str):
    async with httpx.AsyncClient(timeout=20.0) as client:
        r = await client.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {settings.OPENAI_API_KEY}"},
            json={
                "model": "gpt-4o-mini",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.4,
                "max_tokens": 600,
            },
        )
        r.raise_for_status()
        text = r.json()["choices"][0]["message"]["content"]
        return _safe_parse(text)


async def _call_gemini(prompt: str):
    async with httpx.AsyncClient(timeout=20.0) as client:
        r = await client.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={settings.GEMINI_API_KEY}",
            json={
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {
                    "temperature": 0.4,
                    "maxOutputTokens": 600,
                    "thinkingConfig": {"thinkingBudget": 0},
                },
            },
        )
        r.raise_for_status()
        text = r.json()["candidates"][0]["content"]["parts"][0]["text"]
        return _safe_parse(text)


def _safe_parse(text: str):
    match = re.search(r"\[.*\]", text, re.DOTALL)

    if not match:
        print(f"[AI PARSE FAILED] no JSON array found in: {text!r}")
        return []

    try:
        return json.loads(match.group(0))
    except json.JSONDecodeError as e:
        print(f"[AI PARSE FAILED] error={e}")
        print(f"[AI RAW OUTPUT] {text!r}")
        return []