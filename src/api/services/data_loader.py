"""
Data loader service for XAI experiments.

Handles discovery and loading of experiment results from filesystem.
"""

import json
import logging
from pathlib import Path
from functools import lru_cache
from typing import List, Dict, Any, Optional, Tuple, Iterator, Iterable
from datetime import datetime, timedelta

from src.api.config import settings
from src.api.models.schemas import ExperimentResult, InstanceEvaluation, Run
from src.api.services.transformer import transform_experiment_to_run, transform_experiment_to_result
from src.api.utils.pagination import paginate_list

logger = logging.getLogger(__name__)

def get_experiments_dir() -> Path:
    """Get path to experiments directory."""
    return settings.EXPERIMENTS_DIR

def discover_experiment_directories() -> List[Path]:
    """
    Discover all experiment directories.
    
    Returns:
        List containing the root experiments directory.
        We return a list to maintain compatibility with the calling signature,
        but we now treat the experiment root as the base, allowing recursive
        search for result files across all subdirectories and depth levels.
    """
    base_dir = get_experiments_dir()
    if not base_dir.exists():
        logger.warning(f"Experiments directory not found: {base_dir}")
        return []
        
    return [base_dir]

def find_result_files(experiment_dir: Path) -> List[Path]:
    """
    Recursively find all result JSON files in directory.
    
    Args:
        experiment_dir: Path to directory to search (usually experiments root)
        
    Returns:
        Sorted list of Path objects for JSON files
    """
    if not experiment_dir.exists():
        return []

    json_files = list(experiment_dir.rglob("results.json"))
    json_files.extend(experiment_dir.rglob("*_metrics.json"))
    
    return sorted(json_files, key=lambda p: str(p))

def load_json_file(file_path: Path) -> Optional[Dict[str, Any]]:
    """
    Load and parse JSON file.
    
    Args:
        file_path: Path to JSON file
        
    Returns:
        Parsed JSON data or None if error
    """
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.warning(f"File not found: {file_path}")
        return None
    except json.JSONDecodeError as e:
        logger.warning(f"Invalid JSON in {file_path}: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error loading {file_path}: {e}")
        return None

def iter_all_experiments() -> Iterator[Dict[str, Any]]:
    """
    Yield all experiment results from filesystem one by one.
    This prevents loading all files into memory at once.
    
    Yields:
        Experiment data dictionary
    """
    exp_dirs = discover_experiment_directories()
    logger.info(f"Scanning {len(exp_dirs)} experiment directories")
    
    count = 0
    for exp_dir in exp_dirs:
        result_files = find_result_files(exp_dir)
        for file_path in result_files:
            data = load_json_file(file_path)
            if data:
                # Augment with useful metadata if not present
                if isinstance(data, dict):
                    if "experiment_dir_name" not in data:
                        data["_meta_experiment_dir"] = exp_dir.name
                    yield data
                    count += 1
    
    logger.info(f"Finished scanning {count} experiment result files")

def filter_experiments(
    experiments: Iterable[Dict[str, Any]],
    **filters
) -> Iterator[Dict[str, Any]]:
    """
    Filter experiments by criteria using lazy evaluation.
    
    Args:
        experiments: Iterable of experiment data
        **filters: Filtering criteria (dataset, method, model_type, model_name)
        
    Yields:
        Filtered experiment data
    """
    if not filters:
        yield from experiments
        return

    for exp in experiments:
        match = True
        for key, value in filters.items():
            if not value: 
                continue
                
            # Mapping filter keys to potential json keys
            exp_val = None
            
            # Helper to find values case-insensitively or by common keys
            if key == 'dataset':
                exp_val = exp.get('dataset') or exp.get('experiment_metadata', {}).get('dataset')
            elif key == 'method':
                exp_val = exp.get('xai_method') or exp.get('method') or exp.get('model_info', {}).get('explainer_method')
            elif key == 'model_type':
                exp_val = exp.get('model_type')
            elif key == 'model_name':
                exp_val = exp.get('model_name') or exp.get('model_info', {}).get('name')
                
            # Logic: If field missing in exp, we can't match it -> Fail
            if not exp_val:
                match = False
                break
                
            # Comparison
            val_str = str(value).lower()
            exp_str = str(exp_val).lower()
            
            # Exact match for most, partial for model_name
            if key == 'model_name':
                if val_str not in exp_str:
                    match = False
                    break
            else:
                if val_str != exp_str:
                    match = False
                    break
        
        if match:
            yield exp

def iter_experiments_with_filters(**filters) -> Iterator[Dict[str, Any]]:
    """
    Load and filter experiments lazily.
    
    Args:
        **filters: Same as filter_experiments
        
    Returns:
        Iterator of filtered experiment data
    """
    all_experiments = iter_all_experiments()
    return filter_experiments(all_experiments, **filters)

# Legacy support alias (deprecated, use iter_ version)
def load_experiments_with_filters(**filters) -> List[Dict[str, Any]]:
    """
    Legacy list-based loader. 
    WARNING: May cause OOM with large datasets. Use iter_experiments_with_filters instead.
    """
    return list(iter_experiments_with_filters(**filters))

def load_all_experiments() -> List[Dict[str, Any]]:
    """
    Legacy list-based loader.
    WARNING: May cause OOM. Use iter_all_experiments instead.
    """
    return list(iter_all_experiments())


# Global in-memory index mapping run_id to file_path
_RUN_ID_INDEX: Dict[str, Path] = {}

def build_run_id_index():
    """
    Build index of run_id -> file_path on startup.
    This enables O(1) lookups instead of O(n) scanning.
    """
    global _RUN_ID_INDEX
    
    exp_dirs = discover_experiment_directories()
    count = 0
    
    for exp_dir in exp_dirs:
        result_files = find_result_files(exp_dir)
        for file_path in result_files:
            try:
                # We need to peek at the file to generate the ID
                # This happens once on startup
                data = load_json_file(file_path)
                if data:
                    run = transform_experiment_to_run(data)
                    _RUN_ID_INDEX[run.id] = file_path
                    count += 1
            except Exception as e:
                logger.warning(f"Failed to index {file_path}: {e}")
                
    logger.info(f"Built in-memory index with {count} experiments")


@lru_cache(maxsize=256)
def get_experiment_result(run_id: str) -> Optional[ExperimentResult]:
    """
    Locate and load complete experiment result by run ID.
    Uses in-memory index for O(1) lookup.
    Cached to improve performance on repeated access.
    """
    # 1. Try improved O(1) lookup via index
    file_path = _RUN_ID_INDEX.get(run_id)
    
    if file_path:
        data = load_json_file(file_path)
        if data:
            return transform_experiment_to_result(data)
    
    # 2. Fallback to slow scan (in case index is out of sync or empty)
    # This ensures robustness if new files are added without restart
    logger.debug(f"Index miss for {run_id}, falling back to scan")
    
    all_experiments = load_all_experiments()
    
    for exp_data in all_experiments:
        try:
            run = transform_experiment_to_run(exp_data)
            if run.id == run_id:
                # Update index with found item for next time
                # (Note: we can't easily get filepath here without refactoring load_all_experiments)
                return transform_experiment_to_result(exp_data)
        except Exception as e:
            continue
            
    return None


# Global In-Memory Cache for Run Objects
# This avoids re-parsing 100+ MB of JSON on every request
_RUNS_CACHE: List[Run] = []
_LAST_CACHE_UPDATE: Optional[datetime] = None
CACHE_TTL_SECONDS = 300  # 5 minutes

def get_all_run_models(force_refresh: bool = False) -> List[Run]:
    """
    Get all runs as validated objects, using in-memory cache.
    Refreshes cache if empty, expired, or forced.
    """
    global _RUNS_CACHE, _LAST_CACHE_UPDATE
    
    now = datetime.now()
    is_expired = (
        _LAST_CACHE_UPDATE is None or 
        (now - _LAST_CACHE_UPDATE).total_seconds() > CACHE_TTL_SECONDS
    )
    
    if is_expired or force_refresh or not _RUNS_CACHE:
        logger.info("Refreshing runs cache...")
        runs = []
        count = 0
        failed = 0
        
        # Use generator to load one by one
        for exp_data in iter_all_experiments():
            try:
                run = transform_experiment_to_run(exp_data)
                runs.append(run)
                count += 1
            except Exception as e:
                # logger.warning(f"Failed to transform experiment during cache refresh: {e}")
                failed += 1
                
        _RUNS_CACHE = runs
        _LAST_CACHE_UPDATE = now
        logger.info(f"Cache refreshed. Loaded {count} runs ({failed} failed).")
        
    return _RUNS_CACHE

def get_instances_paginated(
    run_id: str,
    offset: int = 0,
    limit: int = 50
) -> Tuple[List[InstanceEvaluation], Dict[str, Any]]:
    """
    Get paginated instance evaluations for a run.
    
    Returns:
        Tuple[List[InstanceEvaluation], Dict[str, Any]]: (page_items, pagination_metadata)
    """
    result = get_experiment_result(run_id)
    if not result:
        # Return empty list and basic zero-metadata if not found (or handle as error generally)
        # Re-using paginate_list on empty list to get consistent struct
        return paginate_list([], offset, limit)
        
    return paginate_list(result.instance_evaluations, offset, limit)
