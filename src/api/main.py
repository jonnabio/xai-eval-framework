"""
Main Entry Point for the XAI Evaluation API.
Configures FastAPI application, CORS, Middleware, and Routes.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.config import settings
from src.api.routes import health
# TODO: Import runs router in INT-09
# from src.api.routes import runs 

app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup/Shutdown Events
@app.on_event("startup")
async def startup_event():
    """Initialize resources on startup."""
    print(f"Starting {settings.API_TITLE} v{settings.API_VERSION}")
    # TODO: Initialize logging middleware in INT-10

# Routes
app.include_router(health.router, prefix="/api")
# TODO: Include runs router in INT-09
# app.include_router(runs.router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.api.main:app", host=settings.HOST, port=settings.PORT, reload=True)
