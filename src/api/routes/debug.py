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

@router.get("/loader")
async def debug_loader():
    """Debug the data loader logic."""
    try:
        from src.api.services import data_loader
        
        exp_dirs = data_loader.discover_experiment_directories()
        
        details = []
        for d in exp_dirs:
            files = data_loader.find_result_files(d)
            details.append({
                "dir": str(d),
                "has_results_dir": (d / "results").exists(),
                "found_files": [str(f) for f in files]
            })
            
        raw_experiments = data_loader.load_all_experiments()
        
        return {
            "experiments_dir": str(data_loader.get_experiments_dir()),
            "discovered_dirs": [str(d) for d in exp_dirs],
            "details": details,
            "loaded_experiments_count": len(raw_experiments),
            "sample_experiment": raw_experiments[0] if raw_experiments else None
        }
    except Exception as e:
        return {"error": str(e)}
