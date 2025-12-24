"""
Configuration management for the XAI Evaluation API.
"""

from pathlib import Path
from typing import List
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """API configuration settings."""
    
    # API Information
    API_VERSION: str = "0.2.0"
    API_TITLE: str = "XAI Evaluation API"
    API_DESCRIPTION: str = """
    API for accessing XAI benchmark experiment results.
    
    This API provides access to:
    - Experiment runs with XAI methods (LIME, SHAP, etc.)
    - Model performance metrics
    - Explainability scores and evaluations
    - Filtering and searching capabilities
    
    Built for the XAI Evaluation Framework PhD research project.
    """
    
    # Server Configuration
    HOST: str = os.getenv("API_HOST", "0.0.0.0")
    PORT: int = int(os.getenv("API_PORT", "8000"))
    DEBUG: bool = os.getenv("API_DEBUG", "true").lower() == "true"
    
    # CORS Configuration
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
    ]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["*"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]
    
    # Paths
    BASE_DIR: Path = Path(__file__).parent.parent.parent
    EXPERIMENTS_DIR: Path = BASE_DIR / "experiments"
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100

settings = Settings()
