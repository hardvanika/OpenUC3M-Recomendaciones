# ml_service/src/models/registry.py
from src.models.predictor import FeedPredictor

class ModelRegistry:
    _instance: FeedPredictor = None

    @classmethod
    def get_instance(cls) -> FeedPredictor:
        if cls._instance is None:
            cls._instance = FeedPredictor()
        return cls._instance

    @classmethod
    def reload(cls):
        """Reloads weights after 3 AM background training finishes."""
        cls._instance = FeedPredictor()