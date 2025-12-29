"""
Data loader service for XAI experiments.

Handles discovery and loading of experiment results from filesystem.
"""

import json
import logging
from pathlib import Path
from functools import lru_cache
from typing import List, Dict, Any, Optional, Tuple

from src.api.config import settings
from src.api.models.schemas import ExperimentResult, InstanceEvaluation
from src.api.services.transformer import transform_experiment_to_run, transform_experiment_to_result

logger = logging.getLogger(__name__)

def get_experiments_dir() -> Path:
    """Get path to experiments directory."""
    return settings.EXPERIMENTS_DIR

def discover_experiment_directories() -> List[Path]:
    """
    Discover all experiment directories.
    
    Returns:
        List of Path objects for experiment directories
    """
    base_dir = get_experiments_dir()
    if not base_dir.exists():
        logger.warning(f"Experiments directory not found: {base_dir}")
        return []
        
    # Valid experiment directory has a 'results' folder
    exp_dirs = []
    for p in base_dir.iterdir():
        if p.is_dir() and (p / "results").exists():
            exp_dirs.append(p)
            
    return sorted(exp_dirs)

def find_result_files(experiment_dir: Path) -> List[Path]:
    """
    Find all JSON result files in experiment directory.
    
    Args:
        experiment_dir: Path to experiment directory
        
    Returns:
        Sorted list of Path objects for JSON files
    """
    results_dir = experiment_dir / "results"
    if not results_dir.exists():
        return []
    
    # Policy: 
    # 1. Look for *.json in results/ (files like rf_metrics.json)
    # 2. Look for results.json in immediate subdirectories of results/ (files like rf_shap/results.json)
    
    json_files = list(results_dir.glob("*.json"))
    
    # Also include nested results.json if specific subdirs structure is used
    json_files.extend(results_dir.glob("*/results.json"))
    
    return sorted(json_files, key=lambda p: p.name)

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

def load_all_experiments() -> List[Dict[str, Any]]:
    """
    Load all experiment results from filesystem.
    
    Returns:
        List of experiment data dictionaries
    """
    experiments = []
    
    exp_dirs = discover_experiment_directories()
    logger.info(f"Found {len(exp_dirs)} experiment directories")
    
    for exp_dir in exp_dirs:
        result_files = find_result_files(exp_dir)
        for file_path in result_files:
            data = load_json_file(file_path)
            if data:
                # Augment with useful metadata if not present
                # This helps if JSON is missing context
                if isinstance(data, dict):
                    if "experiment_dir_name" not in data:
                        data["_meta_experiment_dir"] = exp_dir.name
                    experiments.append(data)
    
    logger.info(f"Loaded {len(experiments)} experiment result files")
    return experiments

def filter_experiments(
    experiments: List[Dict[str, Any]],
    **filters
) -> List[Dict[str, Any]]:
    """
    Filter experiments by criteria.
    
    Args:
        experiments: List of experiment data
        **filters: Filtering criteria (dataset, method, model_type, model_name)
        
    Returns:
        Filtered list of experiments
    """
    if not filters:
        return experiments
        
    filtered = []
    for exp in experiments:
        match = True
        for key, value in filters.items():
            if not value: 
                continue
                
            # Mapping filter keys to potential json keys
            # exp data keys might be snake_case or whatever the file has
            
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
            filtered.append(exp)
            
    return filtered

def load_experiments_with_filters(**filters) -> List[Dict[str, Any]]:
    """
    Load and filter experiments in one call.
    
    Args:
        **filters: Same as filter_experiments
        
    Returns:
        Filtered list of experiment data
    """
    all_experiments = load_all_experiments()
    return filter_experiments(all_experiments, **filters)


@lru_cache(maxsize=32)
def get_experiment_result(run_id: str) -> Optional[ExperimentResult]:
    """
    Locate and load complete experiment result by run ID.
    Cached to improve performance on repeated access.
    """
    # 1. Load all raw experiments (this could be optimized to metadata only scan if needed)
    all_experiments = load_all_experiments()
    
    # 2. Iterate and match ID
    for exp_data in all_experiments:
        try:
            # We generate the ID to check for match
            # This relies on transformer logic being deterministic
            run = transform_experiment_to_run(exp_data)
            
            if run.id == run_id:
                # 3. Found match, transform to detailed result
                return transform_experiment_to_result(exp_data)
                
        except Exception as e:
            logger.warning(f"Error checking experiment for ID match: {e}")
            continue
            
    return None


def get_instances_paginated(
    run_id: str,
    offset: int = 0,
    limit: int = 50
) -> Tuple[List[InstanceEvaluation], int]:
    """
    Get paginated instance evaluations for a run.
    
    Returns:
        Tuple[List[InstanceEvaluation], int]: (page_items, total_count)
    """
    result = get_experiment_result(run_id)
    if not result:
        return [], 0
        
    total = len(result.instance_evaluations)
    
    # Slice
    start = offset
    end = min(offset + limit, total)
    
    if start >= total:
        return [], total
        
    return result.instance_evaluations[start:end], total
