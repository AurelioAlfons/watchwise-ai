import json
import re
import httpx

from app.config import settings
from app.schemas import RecommendRequest


class AIServiceError(Exception):
    def __init__(self, message: str, status_code: int = 503):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


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

Choose exactly 5 from this list only.
Prioritize thematic/vibe variety.
Avoid sequels or entries from the same franchise as "{prefs.similar_title}".

Candidates:
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

        if r.status_code == 429:
            raise AIServiceError("AI service is busy. Please wait a moment and try again.", 429)

        if r.status_code == 400:
            print(f"[OPENAI 400] {r.text}", flush=True)
            raise AIServiceError("AI service rejected the request.", 502)

        if r.status_code >= 500:
            raise AIServiceError("AI service is temporarily unavailable. Please try again soon.", 503)

        r.raise_for_status()
        text = r.json()["choices"][0]["message"]["content"]
        return _safe_parse(text)


async def _call_gemini(prompt: str):
    async with httpx.AsyncClient(timeout=20.0) as client:
        r = await client.post(
            "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent",
            headers={"x-goog-api-key": settings.GEMINI_API_KEY},
            json={
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {
                    "temperature": 0.4,
                    "maxOutputTokens": 600,
                    "thinkingConfig": {"thinkingBudget": 0},
                },
            },
        )

        if r.status_code == 429:
            raise AIServiceError("AI service is busy. Please wait a moment and try again.", 429)

        if r.status_code == 400:
            # Log the response body (not headers/URL) so we see *why* without ever
            # risking the key — the key now lives only in headers, which we don't log.
            print(f"[GEMINI 400] {r.text}", flush=True)
            raise AIServiceError("AI service rejected the request.", 502)

        if r.status_code >= 500:
            raise AIServiceError("AI service is temporarily unavailable. Please try again soon.", 503)

        r.raise_for_status()
        text = r.json()["candidates"][0]["content"]["parts"][0]["text"]
        return _safe_parse(text)


def _safe_parse(text: str):
    match = re.search(r"\[.*\]", text, re.DOTALL)

    if not match:
        print("[AI PARSE FAILED] no JSON array found")
        return []

    try:
        return json.loads(match.group(0))
    except json.JSONDecodeError as e:
        print(f"[AI PARSE FAILED] error={e}")
        return []