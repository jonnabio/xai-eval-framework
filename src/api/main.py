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

# Optional monitoring dependencies - fail gracefully if not installed
try:
    import sentry_sdk
    from sentry_sdk.integrations.fastapi import FastApiIntegration
    SENTRY_AVAILABLE = True
except ImportError:
    sentry_sdk = None
    SENTRY_AVAILABLE = False
    print("⚠️  sentry-sdk not available, Sentry monitoring disabled")


try:
    from prometheus_fastapi_instrumentator import Instrumentator
    PROMETHEUS_AVAILABLE = True
except ImportError:
    Instrumentator = None
    PROMETHEUS_AVAILABLE = False
    print("⚠️  prometheus-fastapi-instrumentator not available, metrics disabled")

from src.api.config import settings
from src.api.routes import health, runs, debug, batch, human_eval
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

@app.get("/health", tags=["system"])
async def health_check():
    """Health check endpoint for Render monitoring."""
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "version": settings.API_VERSION
    }

app.include_router(debug.router, prefix="/db")
app.include_router(batch.router, prefix="/api")
app.include_router(human_eval.router, prefix="/human-eval", tags=["Human Evaluation"])
app.include_router(human_eval.router, prefix="/api/human-eval", tags=["Human Evaluation"])

# Startup event
@app.on_event("startup")
async def startup_event():
    """Log startup message and verify configuration."""
    logger.info("=" * 70)
    logger.info(f"🚀 {settings.API_TITLE} v{settings.API_VERSION}")
    logger.info(f"🌍 Environment: {settings.ENVIRONMENT}")
    logger.info("=" * 70)
    
    # Initialize Sentry only if available and configured
    if SENTRY_AVAILABLE and settings.SENTRY_DSN:
        sentry_sdk.init(
            dsn=settings.SENTRY_DSN,
            environment=settings.SENTRY_ENVIRONMENT,
            traces_sample_rate=settings.SENTRY_TRACES_SAMPLE_RATE,
            integrations=[FastApiIntegration()],
        )
        logger.info("✅ Sentry initialized")
    elif settings.SENTRY_DSN and not SENTRY_AVAILABLE:
        logger.warning("⚠️  Sentry DSN set but sentry-sdk not installed")
    else:
        logger.info("ℹ️  Sentry monitoring disabled")

    # Metrics exposed at /metrics by Instrumentator (initialized below)
    if PROMETHEUS_AVAILABLE:
        logger.info("✅ Prometheus metrics exposed at /metrics")
    else:
        logger.warning("⚠️ Prometheus metrics disabled (dependency missing)")

    logger.info(f"📍 Server: http://{settings.HOST}:{settings.PORT}")
    logger.info(f"📚 API Docs: http://{settings.HOST}:{settings.PORT}/docs")
    logger.info(f"📂 Experiments: {settings.EXPERIMENTS_DIR}")
    logger.info(f"🔧 Debug mode: {settings.DEBUG}")


# Initialize Prometheus Instrumentator (Must be done before app startup for middleware)
if PROMETHEUS_AVAILABLE:
    Instrumentator().instrument(app).expose(app)

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
    import os
    import uvicorn
    port = int(os.getenv("PORT", 10000))
    uvicorn.run("src.api.main:app", host="0.0.0.0", port=port, log_level="info")
