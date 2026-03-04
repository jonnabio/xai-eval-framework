"""
Business logic for human evaluation system.

Handles:
- Loading samples from filesystem
- Saving annotations with file locking
- Progress tracking
- Admin statistics
"""

import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
from filelock import FileLock
from functools import lru_cache

from src.api.config import settings
from src.api.models.schemas import (
    HumanEvalSample, HumanAnnotationSubmission, AnnotationProgress
)

logger = logging.getLogger(__name__)

# =============================================================================
# PATH UTILITIES
# =============================================================================

def get_human_eval_dir() -> Path:
    """Get human evaluation directory, create if doesn't exist."""
    path = settings.HUMAN_EVAL_DIR
    path.mkdir(parents=True, exist_ok=True)
    return path

def get_samples_file() -> Path:
    """Get path to samples.json."""
    return get_human_eval_dir() / settings.HUMAN_EVAL_SAMPLES_FILE

def get_annotations_dir() -> Path:
    """Get annotations directory, create if doesn't exist."""
    path = get_human_eval_dir() / settings.HUMAN_EVAL_ANNOTATIONS_DIR
    path.mkdir(parents=True, exist_ok=True)
    return path

def get_metadata_file() -> Path:
    """Get path to metadata.json."""
    return get_human_eval_dir() / settings.HUMAN_EVAL_METADATA_FILE

def get_annotation_filename(annotator_id: str, sample_id: str) -> str:
    """Generate filename for an annotation."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{annotator_id}_{sample_id}_{timestamp}.json"

# =============================================================================
# SAMPLE LOADING
# =============================================================================

@lru_cache(maxsize=1)
def load_samples_from_file() -> List[Dict[str, Any]]:
    """
    Load samples from samples.json file.

    Cached to avoid re-reading file on every request.
    Clear cache if samples.json is regenerated.

    Returns:
        List of sample dictionaries

    Raises:
        FileNotFoundError: If samples.json doesn't exist
        json.JSONDecodeError: If samples.json is invalid
    """
    samples_file = get_samples_file()

    if not samples_file.exists():
        logger.error(f"Samples file not found: {samples_file}")
        raise FileNotFoundError(
            "Samples file not found. Please run: "
            "python scripts/select_human_eval_samples.py"
        )

    try:
        with open(samples_file, 'r') as f:
            data = json.load(f)

        logger.info(f"Loaded {len(data)} samples from {samples_file}")
        return data

    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in samples file: {e}")
        raise

def get_all_samples() -> List[HumanEvalSample]:
    """
    Get all samples as Pydantic models.

    Returns:
        List of HumanEvalSample objects
    """
    # Note: If cache becomes stale, we might need a way to invalidate it
    raw_samples = load_samples_from_file()

    samples = []
    for raw in raw_samples:
        try:
            # Remove llm_scores if present (enforce blindness)
            sample_data = {k: v for k, v in raw.items() if k != 'llm_scores'}
            sample = HumanEvalSample(**sample_data)
            samples.append(sample)
        except Exception as e:
            logger.warning(f"Failed to parse sample {raw.get('sample_id')}: {e}")
            continue

    return samples

def get_samples_for_annotator(
    annotator_id: str,
    include_completed: bool = False
) -> List[HumanEvalSample]:
    """
    Get samples assigned to a specific annotator.

    Args:
        annotator_id: Annotator identifier
        include_completed: If False, exclude completed samples

    Returns:
        List of samples for this annotator
    """
    all_samples = get_all_samples()

    # Get completed sample IDs for this annotator
    completed_ids = set()
    if not include_completed:
        completed_ids = get_completed_sample_ids(annotator_id)

    # Filter samples
    filtered = []
    for sample in all_samples:
        # Check assignment (None = assigned to all)
        if sample.assigned_to and sample.assigned_to != annotator_id:
            continue

        # Check completion status
        if not include_completed and sample.sample_id in completed_ids:
            continue

        filtered.append(sample)

    logger.info(f"Found {len(filtered)} samples for annotator '{annotator_id}'")
    return filtered

# =============================================================================
# ANNOTATION STORAGE
# =============================================================================

def save_annotation(submission: HumanAnnotationSubmission) -> Tuple[bool, str, str]:
    """
    Save an annotation to filesystem with file locking.

    Args:
        submission: Annotation data

    Returns:
        Tuple of (success, annotation_id, message)
    """
    try:
        # Validate sample exists
        all_samples = load_samples_from_file()
        sample_ids = {s['sample_id'] for s in all_samples}

        if submission.sample_id not in sample_ids:
            return False, "", f"Invalid sample_id: {submission.sample_id}"

        # Check for duplicate (idempotency)
        existing = find_existing_annotation(
            submission.annotator_id,
            submission.sample_id
        )
        if existing:
            logger.info(f"Annotation already exists: {existing}")
            return True, existing, "Annotation already submitted (idempotent)"

        # Generate annotation data
        annotation_id = f"anno_{submission.annotator_id}_{submission.sample_id}_{int(datetime.now().timestamp())}"

        annotation_data = {
            "annotation_id": annotation_id,
            "sample_id": submission.sample_id,
            "annotator_id": submission.annotator_id,
            "ratings": submission.ratings.model_dump(),
            "comments": submission.comments,
            "time_spent_seconds": submission.time_spent_seconds,
            "timestamp": datetime.now().isoformat(),
            "version": "1.0"
        }

        # Save to file with locking
        annotations_dir = get_annotations_dir()
        filename = get_annotation_filename(submission.annotator_id, submission.sample_id)
        filepath = annotations_dir / filename
        lockfile = filepath.with_suffix('.lock')

        with FileLock(str(lockfile), timeout=10):
            with open(filepath, 'w') as f:
                json.dump(annotation_data, f, indent=2)

        logger.info(f"Saved annotation: {filepath}")

        # Update metadata
        update_metadata(submission.annotator_id)

        return True, annotation_id, "Annotation saved successfully"

    except Exception as e:
        logger.error(f"Error saving annotation: {e}", exc_info=True)
        return False, "", f"Error saving annotation: {str(e)}"

def find_existing_annotation(annotator_id: str, sample_id: str) -> Optional[str]:
    """
    Check if annotation already exists for this annotator/sample pair.

    Returns:
        annotation_id if exists, None otherwise
    """
    annotations_dir = get_annotations_dir()
    pattern = f"{annotator_id}_{sample_id}_*.json"

    matches = list(annotations_dir.glob(pattern))
    if matches:
        # Load and return annotation_id
        try:
            with open(matches[0], 'r') as f:
                data = json.load(f)
            return data.get('annotation_id')
        except Exception:
            return None

    return None

def get_completed_sample_ids(annotator_id: str) -> set:
    """Get set of sample_ids this annotator has completed."""
    annotations_dir = get_annotations_dir()
    pattern = f"{annotator_id}_*.json"

    completed = set()
    for filepath in annotations_dir.glob(pattern):
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            completed.add(data['sample_id'])
        except Exception as e:
            logger.warning(f"Error reading {filepath}: {e}")

    return completed

# =============================================================================
# PROGRESS TRACKING
# =============================================================================

def get_annotator_progress(annotator_id: str) -> AnnotationProgress:
    """
    Calculate progress for an annotator.

    Args:
        annotator_id: Annotator identifier

    Returns:
        AnnotationProgress object
    """
    # Get assigned samples
    all_samples = get_samples_for_annotator(annotator_id, include_completed=True)
    total_assigned = len(all_samples)

    # Get completed
    completed_ids = get_completed_sample_ids(annotator_id)
    completed = len(completed_ids)

    # Calculate stats
    pending = total_assigned - completed
    completion_rate = completed / total_assigned if total_assigned > 0 else 0.0

    # Get average time
    avg_time = calculate_average_time(annotator_id)

    return AnnotationProgress(
        annotator_id=annotator_id,
        total_assigned=total_assigned,
        completed=completed,
        in_progress=0,  # Not tracking this state currently
        pending=pending,
        completion_rate=completion_rate,
        avg_time_per_annotation=avg_time
    )

def calculate_average_time(annotator_id: str) -> Optional[float]:
    """Calculate average annotation time for annotator."""
    annotations_dir = get_annotations_dir()
    pattern = f"{annotator_id}_*.json"

    times = []
    for filepath in annotations_dir.glob(pattern):
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            if data.get('time_spent_seconds'):
                times.append(data['time_spent_seconds'])
        except Exception:
            continue

    if times:
        return sum(times) / len(times)
    return None

# =============================================================================
# METADATA MANAGEMENT
# =============================================================================

def update_metadata(annotator_id: str):
    """Update metadata.json with latest stats."""
    metadata_file = get_metadata_file()
    lockfile = metadata_file.with_suffix('.lock')

    try:
        with FileLock(str(lockfile), timeout=10):
            # Load existing
            if metadata_file.exists():
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)
            else:
                metadata = {
                    "created_at": datetime.now().isoformat(),
                    "annotators": {}
                }

            # Update for this annotator
            progress = get_annotator_progress(annotator_id)
            metadata['annotators'][annotator_id] = {
                "total_assigned": progress.total_assigned,
                "completed": progress.completed,
                "pending": progress.pending,
                "completion_rate": progress.completion_rate,
                "last_updated": datetime.now().isoformat()
            }

            metadata['last_updated'] = datetime.now().isoformat()

            # Save
            with open(metadata_file, 'w') as f:
                json.dump(metadata, f, indent=2)

    except Exception as e:
        logger.error(f"Error updating metadata: {e}")

# =============================================================================
# ADMIN FUNCTIONS
# =============================================================================

def get_admin_stats() -> Dict[str, Any]:
    """Get overall system statistics for admin dashboard."""
    all_samples = get_all_samples()
    total_samples = len(all_samples)

    # Get all annotators
    annotations_dir = get_annotations_dir()
    annotators = set()
    for filepath in annotations_dir.glob("*.json"):
        parts = filepath.stem.split('_')
        if parts:
            annotators.add(parts[0])

    # Get stats per annotator
    annotator_stats = []
    total_completed = 0

    for annotator_id in annotators:
        progress = get_annotator_progress(annotator_id)
        annotator_stats.append({
            "annotator_id": annotator_id,
            "completed": progress.completed,
            "pending": progress.pending,
            "completion_rate": progress.completion_rate,
            "avg_time": progress.avg_time_per_annotation
        })
        total_completed += progress.completed

    # Overall completion (accounting for overlaps)
    unique_completed = len(get_all_completed_samples())
    overall_completion = unique_completed / total_samples if total_samples > 0 else 0.0

    # By experiment
    by_experiment = {}
    for sample in all_samples:
        exp = sample.experiment
        if exp not in by_experiment:
            by_experiment[exp] = {"total": 0, "completed": 0}
        by_experiment[exp]["total"] += 1

        # Check if completed by any annotator
        if is_sample_completed(sample.sample_id):
            by_experiment[exp]["completed"] += 1

    return {
        "total_samples": total_samples,
        "total_annotators": len(annotators),
        "overall_completion": overall_completion,
        "unique_completed_samples": unique_completed,
        "total_annotations": total_completed,
        "by_annotator": annotator_stats,
        "by_experiment": by_experiment,
        "last_updated": datetime.now().isoformat()
    }

def get_all_completed_samples() -> set:
    """Get set of all sample_ids that have been completed by anyone."""
    annotations_dir = get_annotations_dir()
    completed = set()

    for filepath in annotations_dir.glob("*.json"):
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            completed.add(data['sample_id'])
        except Exception:
            continue

    return completed

def is_sample_completed(sample_id: str) -> bool:
    """Check if a sample has been completed by any annotator."""
    annotations_dir = get_annotations_dir()
    pattern = f"*_{sample_id}_*.json"
    matches = list(annotations_dir.glob(pattern))
    return len(matches) > 0

def get_all_annotations_with_llm_scores() -> List[Dict[str, Any]]:
    """
    Export all annotations with LLM scores for analysis.

    Returns:
        List of dicts with human ratings + LLM scores
    """
    # Load raw samples (with LLM scores)
    raw_samples = load_samples_from_file()
    llm_scores_map = {s['sample_id']: s.get('llm_scores', {}) for s in raw_samples}

    # Load all annotations
    annotations_dir = get_annotations_dir()
    results = []

    for filepath in annotations_dir.glob("*.json"):
        try:
            with open(filepath, 'r') as f:
                annotation = json.load(f)

            sample_id = annotation.get('sample_id')
            if not sample_id:
                continue

            # Merge with LLM scores
            combined = {
                **annotation,
                "llm_scores": llm_scores_map.get(sample_id, {}),
                "filepath": str(filepath)
            }

            results.append(combined)
        except Exception as e:
            logger.warning(f"Error loading {filepath}: {e}")

    return results

def export_annotations_csv() -> str:
    """Export annotations as CSV string."""
    import csv
    from io import StringIO

    data = get_all_annotations_with_llm_scores()

    if not data:
        return ""

    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=[
        'annotation_id', 'sample_id', 'annotator_id',
        'human_coherence', 'human_faithfulness', 'human_usefulness',
        'llm_coherence', 'llm_faithfulness', 'llm_usefulness',
        'comments', 'time_spent_seconds', 'timestamp'
    ])

    writer.writeheader()

    for item in data:
        llm = item.get('llm_scores', {})
        ratings = item.get('ratings', {})

        writer.writerow({
            'annotation_id': item.get('annotation_id'),
            'sample_id': item.get('sample_id'),
            'annotator_id': item.get('annotator_id'),
            'human_coherence': ratings.get('coherence'),
            'human_faithfulness': ratings.get('faithfulness'),
            'human_usefulness': ratings.get('usefulness'),
            'llm_coherence': llm.get('coherence'),
            'llm_faithfulness': llm.get('faithfulness'),
            'llm_usefulness': llm.get('usefulness'),
            'comments': item.get('comments', ''),
            'time_spent_seconds': item.get('time_spent_seconds'),
            'timestamp': item.get('timestamp')
        })

    return output.getvalue()
