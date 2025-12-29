"""
FastAPI application entry point.

This module:
- Creates the FastAPI application instance
- Configures CORS middleware
- Sets up error handling
- Includes routers
- Defines startup/shutdown events
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from datetime import datetime
import logging

from src.api.config import settings
from src.api.routes import health, runs, debug, batch
from src.api.middleware.exceptions import (
    validation_exception_handler,
    general_exception_handler
)

# Configure logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format=settings.LOG_FORMAT
)
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

# Register exception handlers
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)
# Include routers
# Mount runs at root AND /api to support both conventions and fix frontend 404s
app.include_router(runs.router)
app.include_router(runs.router, prefix="/api")

# Mount health at root AND /api
app.include_router(health.router)
app.include_router(health.router, prefix="/api")

app.include_router(debug.router, prefix="/db")
app.include_router(batch.router, prefix="/api")

# Startup event
@app.on_event("startup")
async def startup_event():
    """Log startup message and verify configuration."""
    logger.info("=" * 70)
    logger.info(f"🚀 {settings.API_TITLE} v{settings.API_VERSION}")
    logger.info("=" * 70)
    logger.info(f"📍 Server: http://{settings.HOST}:{settings.PORT}")
    logger.info(f"📚 API Docs: http://{settings.HOST}:{settings.PORT}/docs")
    logger.info(f"📂 Experiments: {settings.EXPERIMENTS_DIR}")
    logger.info(f"🔧 Debug mode: {settings.DEBUG}")
    logger.info("=" * 70)

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Log shutdown message."""
    logger.info("=" * 70)
    logger.info("👋 API shutting down...")
    logger.info("=" * 70)

# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint with API information.
    
    Returns basic API info and useful links.
    """
    return {
        "name": settings.API_TITLE,
        "version": settings.API_VERSION,
        "status": "running",
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "docs": "/docs",
            "redoc": "/redoc",
            "health": "/api/health",
            "openapi": "/openapi.json"
        }
    }

# Run with uvicorn if executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT,
        log_level=settings.LOG_LEVEL.lower()
    )
