#!/usr/bin/env python3
"""
Select stratified samples for human evaluation.

Strategy:
- 4 experiments × 5 samples each = 20 total
- Within each experiment: Stratify by Quadrant (TP/TN/FP/FN) × Fidelity (High/Low)
- Ensure diversity across experiments and performance metrics

Usage:
    python scripts/select_human_eval_samples.py --num-samples 20 --fidelity-threshold 0.7
"""

import argparse
import json
import logging
from pathlib import Path
from typing import List, Dict, Any
from collections import defaultdict
import random

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Constants
BASE_DIR = Path(__file__).parent.parent
EXPERIMENTS_DIR = BASE_DIR / "experiments" / "exp1_adult"
RESULTS_DIR = EXPERIMENTS_DIR / "results"
LLM_EVAL_FILE = EXPERIMENTS_DIR / "llm_eval" / "results_full.json"
OUTPUT_DIR = EXPERIMENTS_DIR / "human_eval"
OUTPUT_FILE = OUTPUT_DIR / "samples.json"

EXPERIMENTS = ["rf_lime", "rf_shap", "xgb_lime", "xgb_shap"]
QUADRANTS = ["TP", "TN", "FP", "FN"]

def load_experiment_results(experiment: str) -> List[Dict]:
    """Load results.json for an experiment."""
    results_file = RESULTS_DIR / experiment / "results.json"

    if not results_file.exists():
        logger.warning(f"Results file not found: {results_file}")
        return []

    with open(results_file, 'r') as f:
        data = json.load(f)

    instances = data.get('instance_evaluations', [])
    logger.info(f"Loaded {len(instances)} instances from {experiment}")

    return instances

def load_llm_scores() -> Dict[str, Dict]:
    """Load LLM evaluation scores."""
    if not LLM_EVAL_FILE.exists():
        logger.warning(f"LLM eval file not found: {LLM_EVAL_FILE}")
        return {}

    with open(LLM_EVAL_FILE, 'r') as f:
        llm_data = json.load(f)

    # Create lookup: (instance_id, model, explainer) -> scores
    lookup = {}
    for item in llm_data:
        key = (item['instance_id'], item['model'], item['explainer'])
        lookup[key] = item.get('eval_scores', {})

    logger.info(f"Loaded LLM scores for {len(lookup)} instances")

    return lookup

def stratify_samples(instances: List[Dict], samples_per_experiment: int, fidelity_threshold: float) -> List[Dict]:
    """
    Stratify samples by Quadrant × Fidelity.

    Args:
        instances: List of instance evaluations
        samples_per_experiment: Number to select from this experiment
        fidelity_threshold: Threshold for high/low fidelity (e.g., 0.7)

    Returns:
        List of selected instances
    """
    # Group by (quadrant, fidelity_level)
    strata = defaultdict(list)

    for inst in instances:
        quadrant = inst.get('quadrant')
        fidelity = inst.get('metrics', {}).get('fidelity', 0)
        fidelity_level = 'high' if fidelity >= fidelity_threshold else 'low'

        strata[(quadrant, fidelity_level)].append(inst)

    logger.info(f"Stratification: {len(strata)} strata")
    for key, items in strata.items():
        logger.debug(f"  {key}: {len(items)} instances")

    # Select samples
    selected = []

    # Strategy: Round-robin through strata, picking one from each until we have enough
    while len(selected) < samples_per_experiment:
        for stratum_key in sorted(strata.keys()):
            if strata[stratum_key]:
                # Pick random instance from this stratum
                inst = random.choice(strata[stratum_key])
                selected.append(inst)
                strata[stratum_key].remove(inst)

                if len(selected) >= samples_per_experiment:
                    break

        # Prevent infinite loop if we run out of samples
        if all(not v for v in strata.values()):
            logger.warning(f"Ran out of samples in strata, got {len(selected)}/{samples_per_experiment}")
            break

    return selected[:samples_per_experiment]

def create_sample_object(instance: Dict, experiment: str, llm_scores_lookup: Dict) -> Dict:
    """
    Create a sample object for annotation.

    Includes classical metrics but excludes LLM scores (for blind evaluation).
    LLM scores are stored separately for later unblinding.
    """
    instance_id = instance['instance_id']

    # Parse experiment name to get model and explainer
    parts = experiment.split('_')
    model = parts[0]  # rf or xgb (but actually maps to 'random_forest' or 'xgboost')
    explainer = parts[1]  # lime or shap

    # Map model names
    model_map = {'rf': 'rf', 'xgb': 'xgboost'}
    model_key = model_map.get(model, model)

    # Get LLM scores
    llm_key = (instance_id, model_key, explainer)
    llm_scores = llm_scores_lookup.get(llm_key, {})

    sample = {
        "sample_id": f"{experiment}_{instance_id}",
        "experiment": experiment,
        "instance_id": instance_id,
        "quadrant": instance.get('quadrant'),
        "prediction": instance.get('prediction'),
        "true_label": instance.get('true_label'),
        "prediction_correct": instance.get('prediction_correct'),
        "explanation": instance.get('explanation', {}),
        "classical_metrics": instance.get('metrics', {}),
        "llm_scores": llm_scores,  # Store but don't expose via API
        "assigned_to": None,  # Can manually assign later
        "status": "pending",
        "stratification": {
            "quadrant": instance.get('quadrant'),
            "fidelity": instance.get('metrics', {}).get('fidelity', 0),
            "fidelity_level": "high" if instance.get('metrics', {}).get('fidelity', 0) >= 0.7 else "low"
        }
    }

    return sample

def main():
    parser = argparse.ArgumentParser(description="Select samples for human evaluation")
    parser.add_argument('--num-samples', type=int, default=20, help="Total number of samples to select")
    parser.add_argument('--fidelity-threshold', type=float, default=0.7, help="Threshold for high/low fidelity")
    parser.add_argument('--random-seed', type=int, default=42, help="Random seed for reproducibility")
    parser.add_argument('--output', type=Path, default=OUTPUT_FILE, help="Output file path")

    args = parser.parse_args()

    # Set random seed
    random.seed(args.random_seed)

    # Calculate samples per experiment
    samples_per_experiment = args.num_samples // len(EXPERIMENTS)
    logger.info(f"Selecting {samples_per_experiment} samples from each of {len(EXPERIMENTS)} experiments")

    # Load LLM scores
    llm_scores_lookup = load_llm_scores()

    # Select samples from each experiment
    all_samples = []

    for experiment in EXPERIMENTS:
        logger.info(f"\nProcessing experiment: {experiment}")

        # Load instances
        instances = load_experiment_results(experiment)
        if not instances:
            logger.error(f"No instances found for {experiment}, skipping")
            continue

        # Stratify and select
        selected = stratify_samples(instances, samples_per_experiment, args.fidelity_threshold)

        logger.info(f"Selected {len(selected)} samples from {experiment}")

        # Convert to sample objects
        for inst in selected:
            sample = create_sample_object(inst, experiment, llm_scores_lookup)
            all_samples.append(sample)

    # Summary
    logger.info("\n=== Summary ===")
    logger.info(f"Total samples selected: {len(all_samples)}")

    # Breakdown by quadrant
    quadrant_counts = defaultdict(int)
    for s in all_samples:
        quadrant_counts[s['quadrant']] += 1
    logger.info(f"By quadrant: {dict(quadrant_counts)}")

    # Breakdown by experiment
    exp_counts = defaultdict(int)
    for s in all_samples:
        exp_counts[s['experiment']] += 1
    logger.info(f"By experiment: {dict(exp_counts)}")

    # Save to file
    args.output.parent.mkdir(parents=True, exist_ok=True)

    with open(args.output, 'w') as f:
        json.dump(all_samples, f, indent=2)

    logger.info(f"\n✓ Saved {len(all_samples)} samples to: {args.output}")
    logger.info("\nNext steps:")
    logger.info(f"  1. Review samples: cat {args.output} | jq '.[] | .sample_id'")
    logger.info("  2. Start API server: python -m src.api.main")
    logger.info("  3. Test endpoint: curl http://localhost:8000/api/human-eval/samples")

if __name__ == "__main__":
    main()
