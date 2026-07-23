# FastAPI Side: src/api/schemas.py
from pydantic import BaseModel, Field
from typing import List, Optional

class CandidatePost(BaseModel):
    post_id: int
    text: Optional[str] = ""
    is_author_my_connection: int = 0
    number_of_comments: float = 0.0
    likes_count: float = 0.0
    freshness: float = 0.0
    same_campus: int = 0
    is_author_verified: int = 0
    is_author_shadowbanned: int = 0

class RankedFeedRequest(BaseModel):
    user_id: int
    candidates: List[CandidatePost]
    limit: int = 20

class RankedFeedResponse(BaseModel):
    user_id: int
    ranked_post_ids: List[int]
    fallback_used: bool = False

class HealthCheckResponse(BaseModel):
    status: str
    model_loaded: bool