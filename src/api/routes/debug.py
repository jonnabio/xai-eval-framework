from fastapi import APIRouter
from pathlib import Path
import os
from src.api.config import settings

router = APIRouter(prefix="/debug", tags=["Debug"])

@router.get("/files")
async def list_files():
    """List files in experiments directory."""
    try:
        exp_dir = settings.EXPERIMENTS_DIR
        
        if not exp_dir.exists():
            return {"error": f"Experiments directory not found: {exp_dir}"}
            
        tree = {}
        for root, dirs, files in os.walk(exp_dir):
            rel_root = os.path.relpath(root, exp_dir)
            tree[rel_root] = {"dirs": dirs, "files": files}
            
        return {
            "base_dir": str(settings.BASE_DIR),
            "experiments_dir": str(exp_dir),
            "exists": exp_dir.exists(),
            "tree": tree
        }
    except Exception as e:
        return {"error": str(e)}
