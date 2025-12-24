"""
Health check endpoint.

Provides simple health status for monitoring and deployment verification.
"""

from fastapi import APIRouter
from datetime import datetime

from src.api.models.schemas import HealthResponse
from src.api.config import settings

router = APIRouter()

@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check",
    description="Check if the API is running and responsive",
    tags=["Health"]
)
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        HealthResponse with status, version, and timestamp
    """
    return HealthResponse(
        status="healthy",
        version=settings.API_VERSION,
        timestamp=datetime.now()
    )

@router.get(
    "/health/detailed",
    summary="Detailed Health Check",
    description="Detailed health information including system stats",
    tags=["Health"]
)
async def detailed_health_check():
    """
    Detailed health check with system information.
    
    Returns:
        Detailed health status including experiments availability
    """
    from src.api.services.data_loader import get_experiments_dir
    import os
    
    experiments_dir = get_experiments_dir()
    experiments_exists = experiments_dir.exists()
    
    return {
        "status": "healthy",
        "version": settings.API_VERSION,
        "timestamp": datetime.now().isoformat(),
        "system": {
            "experiments_directory": str(experiments_dir),
            "experiments_directory_exists": experiments_exists,
            "api_host": settings.HOST,
            "api_port": settings.PORT,
        }
    }
