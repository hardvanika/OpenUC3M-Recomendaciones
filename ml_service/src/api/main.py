from fastapi import FastAPI
from src.api.routes import router

app = FastAPI(title="Feed Recommendation Service")

app.include_router(router)

@app.on_event("startup")
async def startup():
    """
    Initializes and loads PyTorch model weights into RAM when container boots[cite: 304].
    """
    pass