"""
Batch execution of XAI experiments.

Handles orchestration, parallel execution, checkpointing, and result aggregation
for multiple experiment configurations.
"""

import logging
import json
import time
import os
import multiprocessing
from pathlib import Path
from typing import List, Dict, Any, Optional
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime
import pandas as pd
try:
    import git
except ImportError:
    git = None

from src.experiment.config import load_config
from src.experiment.runner import ExperimentRunner

logger = logging.getLogger(__name__)

import threading
import subprocess

def _auto_commit_worker(interval_seconds: int):
    """Background worker that commits the experiments directory periodically."""
    last_push_time = time.time()
    # 6 hours = 21600 seconds
    push_interval = 21600
    
    while True:
        time.sleep(interval_seconds)
        try:
            logger.info("Running automatic git commit for experiment progress...")
            # We add everything in experiments/ and configs/ (just in case)
            subprocess.run(["git", "add", "experiments/", "configs/"], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            res = subprocess.run(
                ["git", "commit", "-m", "Auto-commit: Checkpointing experiment progress"],
                check=False,
                capture_output=True,
                text=True
            )
            
            commit_made = res.returncode == 0
            if commit_made:
                logger.info("Auto-commit successful.")
            
            # Check if it's time to push (regardless of whether we JUST committed, 
            # to capture any pending commits from previous iterations)
            current_time = time.time()
            if current_time - last_push_time >= push_interval:
                logger.info(f"Pushing to remote (6-hour interval reached)...")
                push_res = subprocess.run(["git", "push"], check=False, capture_output=True, text=True)
                if push_res.returncode == 0:
                    logger.info("Push successful.")
                    last_push_time = current_time
                else:
                    logger.warning(f"Push failed: {push_res.stderr}")
                    
        except Exception as e:
            logger.error(f"Auto-commit thread encountered an error: {e}")

def _run_single_experiment(config_path: Path) -> Dict[str, Any]:
    """
    Worker function for parallel execution.
    Must be top-level for pickling on Windows.
    """
    try:
        # Re-load config in worker process to ensure clean state
        # (Pass path instead of object to avoid pickling complex config objects if possible,
        # though Pydantic models usually pickle fine. Path is safer.)
        config = load_config(config_path)
        
        # Checkpoint check (double check to be safe, though runner check happens before submit)
        if (config.output_dir / "results.json").exists():
            return {
                "status": "skipped",
                "config_path": str(config_path),
                "experiment_name": config.name,
                "message": "Results already exist"
            }

        runner = ExperimentRunner(config)
        # CRITICAL FIX: Force sequential execution within the worker to prevent
        # nested parallelism explosion (Process Bomb) on MacOS/Spawn.
        # This ensures 4 batch workers = 4 total processes.
        runner.max_workers = 1 
        results = runner.run()
        
        return {
            "status": "success",
            "config_path": str(config_path),
            "experiment_name": config.name,
            "results": results
        }
        
    except Exception as e:
        # Capture error but don't crash worker
        return {
            "status": "failed",
            "config_path": str(config_path),
            "error": str(e),
            "experiment_name": config_path.stem # Fallback name
        }

class BatchExperimentRunner:
    """
    Orchestrates execution of multiple experiment configurations.
    """
    
    def __init__(self, config_paths: List[Path]):
        """
        Initialize with list of configuration files.
        """
        self.config_paths = [Path(p).resolve() for p in config_paths]
        self._validate_paths()
        
    def _validate_paths(self):
        """Ensure all paths exist and are unique."""
        seen = set()
        valid = []
        for p in self.config_paths:
            if not p.exists():
                logger.warning(f"Config not found: {p}")
                continue
            if p in seen:
                continue
            seen.add(p)
            valid.append(p)
        self.config_paths = valid
        
    def run(self, parallel: bool = True, max_workers: int = 2, auto_commit_interval: int = 1800) -> pd.DataFrame:
        """
        Execute experiments in batch.
        
        Args:
            parallel: Whether to run in parallel
            max_workers: Number of worker processes
            auto_commit_interval: Seconds between automatic git commits (0 to disable)
            
        Returns:
            DataFrame containing aggregated results
        """
        if auto_commit_interval > 0:
            logger.info(f"Starting auto-commit thread (interval: {auto_commit_interval}s)")
            commit_thread = threading.Thread(
                target=_auto_commit_worker, 
                args=(auto_commit_interval,), 
                daemon=True
            )
            commit_thread.start()
            
        start_time = time.time()
        results_list = []
        
        # Metadata for manifest
        manifest = {
            "timestamp": datetime.now().isoformat(),
            "git_hash": self._get_git_hash(),
            "executions": []
        }
        
        # 1. Identify work
        todo_configs = []
        skipped_configs = []
        
        logger.info(f"Scanning {len(self.config_paths)} configurations...")
        
        for p in self.config_paths:
            try:
                # Quick load to check output dir
                # We assume standard naming convention or load fully
                # Loading fully is safer to get output_dir
                cfg = load_config(p)
                result_file = cfg.output_dir / "results.json"
                
                if result_file.exists():
                    logger.info(f"Skipping {cfg.name} (results exist)")
                    # Load existing for aggregation
                    with open(result_file, 'r') as f:
                        res = json.load(f)
                    
                    # Flatten for dataframe
                    flat = self._flatten_result(res)
                    if flat:
                        results_list.append(flat)
                        
                    manifest["executions"].append({
                        "id": cfg.name,
                        "status": "skipped",
                        "path": str(p)
                    })
                    skipped_configs.append(p)
                else:
                    todo_configs.append(p)
                    
            except Exception as e:
                logger.error(f"Failed to load config {p}: {e}")
                manifest["executions"].append({
                    "id": p.stem,
                    "status": "config_error",
                    "error": str(e)
                })

        logger.info(f"Found {len(todo_configs)} experiments to run ({len(skipped_configs)} skipped).")
        
        # 2. Execute
        if todo_configs:
            if parallel:
                new_results = self._run_parallel(todo_configs, max_workers)
            else:
                new_results = self._run_sequential(todo_configs)
                
            # Process results
            for res in new_results:
                manifest_entry = {
                    "path": res["config_path"],
                    "status": res["status"]
                }
                
                if res["status"] == "success":
                    manifest_entry["id"] = res["experiment_name"]
                    # Add to dataframe list
                    flat = self._flatten_result(res["results"])
                    if flat:
                        results_list.append(flat)
                elif res["status"] == "failed":
                    manifest_entry["error"] = res.get("error")
                    manifest_entry["id"] = res.get("experiment_name", "unknown")
                    logger.error(f"Experiment failed: {manifest_entry['id']} - {manifest_entry['error']}")
                    
                manifest["executions"].append(manifest_entry)

        # 3. Aggregate
        if results_list:
            df = pd.DataFrame(results_list)
        else:
            df = pd.DataFrame()
            
        return df, manifest
        
    def _run_parallel(self, configs: List[Path], max_workers: int) -> List[Dict]:
        """Run experiments using ProcessPoolExecutor."""
        results = []
        ctx = multiprocessing.get_context('spawn') if os.name == 'nt' else None
        
        logger.info(f"Starting parallel execution with {max_workers} workers...")
        
        with ProcessPoolExecutor(max_workers=max_workers, mp_context=ctx) as executor:
            future_to_config = {
                executor.submit(_run_single_experiment, p): p 
                for p in configs
            }
            
            for future in as_completed(future_to_config):
                p = future_to_config[future]
                try:
                    res = future.result()
                    results.append(res)
                    status = res['status']
                    name = res.get('experiment_name', p.stem)
                    logger.info(f"Finished {name}: {status}")
                except Exception as e:
                    logger.error(f"Worker exception for {p}: {e}")
                    results.append({
                        "status": "failed",
                        "config_path": str(p),
                        "error": f"Worker Exception: {str(e)}"
                    })
                    
        return results

    def _run_sequential(self, configs: List[Path]) -> List[Dict]:
        """Run experiments sequentially."""
        results = []
        for p in configs:
            logger.info(f"Running {p.stem}...")
            res = _run_single_experiment(p)
            results.append(res)
        return results

    def _flatten_result(self, res_dict: Dict) -> Optional[Dict]:
        """Convert complex result dict to flat row for DataFrame."""
        try:
            row = {}
            # Metadata
            meta = res_dict.get("experiment_metadata", {})
            row["experiment_name"] = meta.get("name")
            row["dataset"] = meta.get("dataset")
            row["duration"] = meta.get("duration_seconds")
            
            # Model Info
            model = res_dict.get("model_info", {})
            row["model"] = model.get("name")
            row["explainer"] = model.get("explainer_method")
            
            # Aggregated Metrics
            aggs = res_dict.get("aggregated_metrics", {})
            for metric, stats in aggs.items():
                row[f"{metric}_mean"] = stats.get("mean")
                row[f"{metric}_std"] = stats.get("std")
                
            return row
        except Exception as e:
            logger.warning(f"Error flattening results: {e}")
            return None

    def _get_git_hash(self) -> str:
        """Get current git commit hash for provenance."""
        if git is None:
            return "unknown (git not available)"
        try:
            repo = git.Repo(search_parent_directories=True)
            return repo.head.object.hexsha
        except Exception:
            return "unknown"
