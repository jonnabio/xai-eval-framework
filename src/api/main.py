from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import health

app = FastAPI(
    title="XAI Eval Framework API",
    description="API for accessing XAI experiment results and metrics",
    version="0.1.0"
)

# Enable CORS for dashboard access (localhost:3000)
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.api.main:app", host="0.0.0.0", port=8000, reload=True)
