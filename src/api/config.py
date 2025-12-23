"""
Configuration settings for the XAI Evaluation API.
Centralizes environment variables, file paths, and server settings.
"""
from pydantic import BaseSettings
from pathlib import Path
from typing import List

class Settings(BaseSettings):
    API_VERSION: str = "0.2.0"
    API_TITLE: str = "XAI Evaluation API"
    API_DESCRIPTION: str = "REST API for serving XAI experiment results to the dashboard."
    
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    LOG_LEVEL: str = "INFO"
    
    # CORS Configuration
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ]
    
    # Paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    EXPERIMENTS_DIR: Path = BASE_DIR / "experiments"

    class Config:
        env_file = ".env"

settings = Settings()
