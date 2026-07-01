from pydantic import BaseModel
from typing import Literal, Optional

class RecommendRequest(BaseModel):
    media_type: Literal["movie", "tv", "any"] = "any"
    genre: Optional[str] = None
    mood: Optional[str] = None
    watching_with: Optional[str] = None
    similar_title: Optional[str] = None
    free_text: Optional[str] = None

class Recommendation(BaseModel):
    title: str
    media_type: str
    reason: str
    genre: str
    runtime: Optional[str] = None
    age_rating: Optional[str] = None
    rating: Optional[float] = None
    where_to_watch: list[str] = []
    poster_url: Optional[str] = None

class RecommendResponse(BaseModel):
    recommendations: list[Recommendation]