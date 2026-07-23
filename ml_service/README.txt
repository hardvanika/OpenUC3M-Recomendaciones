ml_service/
├── config/
│   └── settings.py          # Environment variables & hyperparameter configs
├── data/                    # Storage for raw CSV dumps and training Parquet files
├── models/                  # Offline trained PyTorch checkpoints (.pt / .pkl)
├── src/
│   ├── api/                 # HTTP Transport Layer (FastAPI)
│   │   ├── main.py          # FastAPI application startup & router registration
│   │   ├── registry.py      # Singleton pattern to manage in-memory model state
│   │   ├── routes.py        # REST API endpoints (/feed/ranked, /health, etc.)
│   │   └── schemas.py       # Pydantic data validation schemas
│   └── training/            # Model training loops, loss functions & evaluators
├── Dockerfile               # Container build definition for production deployment
├── main.py                  # Entrypoint to launch the Uvicorn ASGI server
└── train.py                 # Standalone script to trigger offline model retraining