import logging
import uuid
import threading
from typing import List, Dict, Optional, Any
from pathlib import Path
from datetime import datetime
import pandas as pd

from src.experiment.batch_runner import BatchExperimentRunner

logger = logging.getLogger(__name__)

class BatchJobManager:
    """
    Manages asynchronous batch experiment execution.
    Stores job state in-memory (reset on restart).
    """
    
    def __init__(self, config_root: Path):
        self.config_root = config_root
        self._jobs: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.Lock()
        
    def submit_job(self, config_names: List[str]) -> str:
        """
        Submit a new batch job.
        
        Args:
            config_names: List of config filenames (e.g. ['exp1.yaml'])
            
        Returns:
            Job ID
        """
        job_id = str(uuid.uuid4())
        
        # Resolve paths
        config_paths = []
        for name in config_names:
            p = self.config_root / name
            if p.exists():
                config_paths.append(p)
            else:
                logger.warning(f"Config not found: {name}")

        with self._lock:
            self._jobs[job_id] = {
                "id": job_id,
                "status": "queued",
                "submitted_at": datetime.now().isoformat(),
                "config_count": len(config_paths),
                "configs": [p.name for p in config_paths],
                "error": None,
                "manifest": None
            }
            
        # Start in background thread to not block API
        thread = threading.Thread(
            target=self._run_job_thread,
            args=(job_id, config_paths),
            daemon=True
        )
        thread.start()
        
        return job_id
        
    def get_job(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Get current job status."""
        with self._lock:
            return self._jobs.get(job_id)

    def list_jobs(self) -> List[Dict[str, Any]]:
        """List all jobs."""
        with self._lock:
            return list(self._jobs.values())

    def _run_job_thread(self, job_id: str, config_paths: List[Path]):
        """Worker thread execution."""
        logger.info(f"Starting batch job {job_id}")
        
        with self._lock:
             self._jobs[job_id]["status"] = "running"
             self._jobs[job_id]["started_at"] = datetime.now().isoformat()
             
        try:
            if not config_paths:
                raise ValueError("No valid configuration files provided.")
                
            runner = BatchExperimentRunner(config_paths)
            
            # Run (blocking call, hence why we are in a thread)
            # Parallel execution is safe here as runner uses ProcessPoolExecutor
            # and we are in a Thread.
            df, manifest = runner.run(parallel=True, max_workers=2)
            
            with self._lock:
                self._jobs[job_id]["status"] = "completed"
                self._jobs[job_id]["completed_at"] = datetime.now().isoformat()
                self._jobs[job_id]["manifest"] = manifest
                self._jobs[job_id]["results_summary"] = {
                    "total": len(manifest["executions"]),
                    "passed": sum(1 for e in manifest["executions"] if e["status"] == "success"),
                    "failed": sum(1 for e in manifest["executions"] if e["status"] == "failed")
                }
                
        except Exception as e:
            logger.error(f"Job {job_id} failed: {e}", exc_info=True)
            with self._lock:
                self._jobs[job_id]["status"] = "failed"
                self._jobs[job_id]["error"] = str(e)
                self._jobs[job_id]["completed_at"] = datetime.now().isoformat()

# Singleton instance (initialized in dependencies)?
# Or just global variable?
# We'll rely on the routes to initialize it properly or use a dependency injection pattern.
