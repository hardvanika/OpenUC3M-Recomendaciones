import yaml
from pathlib import Path
from pydantic import BaseModel

CONFIG_PATH = Path(__file__).parent / "config.yaml"

class Settings(BaseModel):
    project_name: str
    environment: str
    paths: dict
    model: dict
    training: dict
    api: dict

def load_settings() -> Settings:
    """Loads and validates the YAML config file."""
    with open(CONFIG_PATH, "r") as f:
        config_data = yaml.safe_load(f)
    return Settings(**config_data)

# Global settings instance
SETTINGS = load_settings()