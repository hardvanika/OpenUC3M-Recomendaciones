# ml_service/src/api/routes.py
import os
import csv
import io
from fastapi import APIRouter, status, File, UploadFile, HTTPException
from .schemas import RankedFeedRequest, RankedFeedResponse, HealthCheckResponse, DatasetIngestResponse
from .registry import ModelRegistry
    
router = APIRouter()

# --- NEW ROUTE: Receive CSV Dataset ---
@router.post(
    "/api/v1/dataset/ingest", 
    response_model=DatasetIngestResponse,
    status_code=status.HTTP_201_CREATED
)
async def ingest_dataset(file: UploadFile = File(...)):
    """Receives CSV dataset sent from Django and stores it on disk."""
    if not file.filename.endswith('.csv'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Only CSV files are accepted"
        )

    # Directory where datasets will be stored
    save_dir = os.path.join(os.getcwd(), "data")
    os.makedirs(save_dir, exist_ok=True)
    destination_path = os.path.join(save_dir, file.filename)

    # Read content to process/save
    contents = await file.read()
    
    # Save the received file to disk
    with open(destination_path, "wb") as f:
        f.write(contents)

    # Count rows in CSV for confirmation
    decoded_content = contents.decode('utf-8')
    csv_reader = csv.reader(io.StringIO(decoded_content))
    total_rows = max(0, sum(1 for row in csv_reader) - 1)  # Subtract header row

    return {
        "status": "success",
        "filename": file.filename,
        "rows_processed": total_rows,
        "message": f"Successfully ingested {total_rows} records into FastAPI storage."
    }

# --- Existing Routes ---
@router.post(
    "/api/v1/feed/ranked", 
    response_model=RankedFeedResponse,
    status_code=status.HTTP_200_OK
)
async def rank_home_feed(payload: RankedFeedRequest):
    try:
        predictor = ModelRegistry.get_instance()
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