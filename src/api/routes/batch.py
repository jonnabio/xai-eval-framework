from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

from src.api.config import settings
from src.api.services.batch_service import BatchJobManager

router = APIRouter(prefix="/experiments/batch", tags=["Batch Experiments"])

# Dependency-ish pattern (singleton)
batch_manager = BatchJobManager(settings.CONFIGS_DIR)

class BatchSubmitRequest(BaseModel):
    configs: List[str]

class BatchJobResponse(BaseModel):
    job_id: str
    status: str
    submitted_at: str

@router.post("/", response_model=BatchJobResponse)
async def submit_batch(request: BatchSubmitRequest):
    """
    Trigger a new batch execution.
    
    Args:
        configs: List of configuration filenames (e.g. ["exp1.yaml"])
    """
    if not request.configs:
        raise HTTPException(status_code=400, detail="Config list cannot be empty")
        
    job_id = batch_manager.submit_job(request.configs)
    job = batch_manager.get_job(job_id)
    return {
        "job_id": job_id,
        "status": job["status"],
        "submitted_at": job["submitted_at"]
    }

@router.get("/{job_id}")
async def get_batch_status(job_id: str):
    """Get status of a specific batch job."""
    job = batch_manager.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.get("/{job_id}/results")
async def get_batch_results(job_id: str):
    """Get results validation/manifest for a completed job."""
    job = batch_manager.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
        
    if job["status"] != "completed":
        raise HTTPException(status_code=400, detail=f"Job is {job['status']}, results not ready")
        
    return {
        "job_id": job_id,
        "manifest": job.get("manifest"),
        "summary": job.get("results_summary")
    }

@router.get("/")
async def list_batch_jobs():
    """List all batch jobs in current session."""
    return batch_manager.list_jobs()
