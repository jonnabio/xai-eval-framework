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
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
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
    PORT: int = int(os.getenv("PORT", "8000"))  # Render provides PORT
    DEBUG: bool = os.getenv("API_DEBUG", "true").lower() == "true"
    
    # Monitoring
    SENTRY_DSN: str | None = os.getenv("SENTRY_DSN")
    SENTRY_ENVIRONMENT: str = os.getenv("SENTRY_ENVIRONMENT", "production")
    SENTRY_TRACES_SAMPLE_RATE: float = float(os.getenv("SENTRY_TRACES_SAMPLE_RATE", "0.1"))
    
    # CORS Configuration
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
        "https://xai-benchmark.onrender.com",
        "https://xai-benchmark-frontend.onrender.com",
    ]
    
    # Allow overriding/appending CORS via environment variable
    if os.getenv("CORS_ORIGINS"):
        CORS_ORIGINS.extend(os.getenv("CORS_ORIGINS").split(","))
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["*"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]
    
    # Paths
    BASE_DIR: Path = Path(__file__).parent.parent.parent
    EXPERIMENTS_DIR: Path = BASE_DIR / "experiments"
    CONFIGS_DIR: Path = BASE_DIR / "configs/experiments"
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Pagination
    DEFAULT_PAGE_SIZE: int = 100
    MAX_PAGE_SIZE: int = 5000

    # Results API Configuration
    RESULTS_CACHE_TTL_SECONDS: int = 300  # 5 minutes
    RESULTS_DEFAULT_PAGE_SIZE: int = 50
    RESULTS_MAX_INSTANCES_PER_REQUEST: int = 100

    # Human Evaluation Configuration
    HUMAN_EVAL_DIR: Path = EXPERIMENTS_DIR / "exp1_adult" / "human_eval"
    HUMAN_EVAL_SAMPLES_FILE: str = "samples.json"
    HUMAN_EVAL_ANNOTATIONS_DIR: str = "annotations"
    HUMAN_EVAL_METADATA_FILE: str = "metadata.json"
    HUMAN_EVAL_MAX_ANNOTATORS: int = 10
    HUMAN_EVAL_REQUIRE_AUTH: bool = os.getenv("HUMAN_EVAL_REQUIRE_AUTH", "True").lower() == "true"

    # Authentication Configuration
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "insecure-debug-key-change-me")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_HOURS: int = 24

settings = Settings()
