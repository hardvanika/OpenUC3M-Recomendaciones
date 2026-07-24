# main.py
from fastapi import FastAPI
from src.api.routes import router
from src.api.registry import ModelRegistry

app = FastAPI(title="Feed Recommendation Service")

app.include_router(router)

@app.on_event("startup")
async def startup():
    """Initializes and loads PyTorch model weights into RAM when app starts."""
    ModelRegistry.get_instance()