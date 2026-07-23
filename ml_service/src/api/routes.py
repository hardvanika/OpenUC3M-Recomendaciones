# ml_service/src/api/routes.py
from fastapi import APIRouter, status
from .schemas import RankedFeedRequest, RankedFeedResponse, HealthCheckResponse
from .registry import ModelRegistry
    
router = APIRouter()

@router.post(
    "/api/v1/feed/ranked", 
    response_model=RankedFeedResponse,
    status_code=status.HTTP_200_OK
)
async def rank_home_feed(payload: RankedFeedRequest):
    """
    HTTP route handler: Receives Pydantic payload and delegates 
    inference directly to the model in src/models/.
    """
    try:
        # 1. Fetch trained model instance from RAM
        predictor = ModelRegistry.get_instance()

        # 2. Execute actual model predictions inside src/models/
        ranked_ids = predictor.predict_and_rank(
            user_id=payload.user_id,
            candidates=payload.candidates
        )

        return {
            "user_id": payload.user_id,
            "ranked_post_ids": ranked_ids[:payload.limit],
            "fallback_used": False
        }

    except Exception as e:
        # Graceful fallback: return unranked candidate IDs on error
        fallback_ids = [c.post_id for c in payload.candidates]
        return {
            "user_id": payload.user_id,
            "ranked_post_ids": fallback_ids[:payload.limit],
            "fallback_used": True
        }

@router.get("/health", response_model=HealthCheckResponse)
async def health_check():
    return {"status": "ok", "model_loaded": ModelRegistry._instance is not None}

@router.post("/admin/reload-model")
async def reload_model():
    ModelRegistry.reload()
    return {"status": "Model successfully reloaded"}