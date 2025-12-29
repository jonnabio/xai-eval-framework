#!/usr/bin/env python3
"""
Run LLM Evaluation for EXP1-33.

This script loads existing XAI results, selects a stratified sample of instances,
and uses an LLM to evaluate the quality of the explanations.
"""

import argparse
import json
import logging
import random
import sys
import time
from pathlib import Path
from typing import Dict, List, Any

import pandas as pd
from tqdm import tqdm

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from src.experiment.config import LLMConfig
from src.llm.client import LLMClientFactory
from src.evaluation.evaluator import LLMEvaluator

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(project_root / 'logs/llm_eval.log', mode='a')
    ]
)
logger = logging.getLogger(__name__)

def load_all_results(results_dir: Path) -> List[Dict[str, Any]]:
    """
    Load results from all subdirectories in results_dir.
    Returns a unified list of instances with added metadata (model, explainer).
    """
    all_instances = []
    
    # Expected pattern: results_dir / <experiment_name> / results.json
    for result_file in results_dir.glob("*/results.json"):
        try:
            with open(result_file, 'r') as f:
                data = json.load(f)
                
            model_info = data.get("model_info", {})
            model_name = model_info.get("name", "unknown")
            explainer_method = model_info.get("explainer_method", "unknown")
            
            # Extract instances
            for inst in data.get("instance_evaluations", []):
                # Enrich with experiment metadata
                inst["model"] = model_name
                inst["explainer"] = explainer_method
                inst["source_file"] = str(result_file)
                all_instances.append(inst)
                
        except Exception as e:
            logger.warning(f"Failed to load {result_file}: {e}")
            
    return all_instances

def stratify_and_sample(
    instances: List[Dict], 
    n_per_stratum: int, 
    random_seed: int = 42
) -> List[Dict]:
    """
    Stratify by (Model, Explainer, Quadrant) and sample n_per_stratum.
    """
    random.seed(random_seed)
    
    # helper key generator
    def get_stratum_key(inst):
        return (inst["model"], inst["explainer"], inst["quadrant"])
    
    # Group
    strata = {}
    for inst in instances:
        key = get_stratum_key(inst)
        if key not in strata:
            strata[key] = []
        strata[key].append(inst)
        
    # Sample
    selected = []
    logger.info(f"Stratification Groups found: {len(strata)}")
    
    for key, group in strata.items():
        n_avail = len(group)
        n_select = min(n_per_stratum, n_avail)
        sampled_group = random.sample(group, n_select)
        selected.extend(sampled_group)
        logger.info(f"  Stratum {key}: Selected {n_select}/{n_avail}")
        
    return selected

def main():
    parser = argparse.ArgumentParser(description="Run LLM Evaluation")
    parser.add_argument("--mode", choices=["validation", "full"], default="validation", 
                        help="Mode: validation (1 per stratum) or full (5 per stratum)")
    parser.add_argument("--provider", choices=["openai", "gemini", "dummy", "openrouter"], default="openai",
                        help="LLM Provider")
    parser.add_argument("--model", type=str, default="gpt-4o",
                        help="LLM Model Name")
    parser.add_argument("--results-dir", type=Path, 
                        default=Path("experiments/exp1_adult/results"),
                        help="Directory containing XAI result JSONs")
    parser.add_argument("--output-dir", type=Path,
                        default=Path("experiments/exp1_adult/llm_eval"),
                        help="Output directory for evaluation results")
    parser.add_argument("--cost-limit", type=float, default=5.0,
                        help="Cost limit in USD")
    
    args = parser.parse_args()
    
    # Setup
    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Determine Limit
    n_limit = 1 if args.mode == "validation" else 5
    
    logger.info(f"Starting LLM Evaluation (Mode: {args.mode}, Limit: {n_limit}/stratum)")
    
    # 1. Load Data
    logger.info("Loading XAI results...")
    instances = load_all_results(args.results_dir)
    if not instances:
        logger.error("No instances found. Check --results-dir.")
        return 1
    logger.info(f"Loaded {len(instances)} total instances.")
    
    # 2. Sample
    samples = stratify_and_sample(instances, n_limit)
    logger.info(f"Selected {len(samples)} instances for evaluation.")
    
    # 3. Initialize Evaluator
    llm_config = LLMConfig(
        provider=args.provider,
        model_name=args.model,
        temperature=0.0,
        max_tokens=1000
    )
    
    try:
        client = LLMClientFactory.create(llm_config)
    except Exception as e:
        logger.error(f"Failed to initialize LLM client: {e}")
        logger.error("Ensure API keys are set (OPENAI_API_KEY / GOOGLE_API_KEY).")
        return 1
        
    evaluator = LLMEvaluator(
        client=client, 
        template_dir=project_root / "src/prompts/templates"
    )
    
    # 4. Evaluation Loop
    results = []
    cost_history = []
    
    # Check for existing results to resume? (Simple version: overwrite or append?)
    # For now, we'll just write a new file based on mode.
    output_file = output_dir / f"results_{args.mode}.json"
    
    logger.info("Beginning evaluation loop...")
    for i, instance in enumerate(tqdm(samples)):
        # Check Cost
        current_cost = client.get_cost()
        if current_cost > args.cost_limit:
            logger.warning(f"Cost limit reached (${current_cost:.2f} > ${args.cost_limit}). Stopping.")
            break
            
        try:
            # Enrich instance with 'explanation' string if needed in logic, 
            # but Evaluator handles raw structure now.
            
            # Evaluate
            scores = evaluator.evaluate_instance(instance)
            
            # Combine result
            record = {
                "instance_id": instance["instance_id"],
                "model": instance["model"],
                "explainer": instance["explainer"],
                "quadrant": instance["quadrant"],
                "eval_scores": scores,
                "cost_at_step": client.get_cost()
            }
            results.append(record)
            
        except Exception as e:
            logger.error(f"Error evaluating instance {instance['instance_id']}: {e}")
            
        # Checkpoint every 10
        if (i + 1) % 10 == 0:
            with open(output_file, 'w') as f:
                json.dump(results, f, indent=2)
                
    # Final Save
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
        
    logger.info(f"Evaluation complete. Saved {len(results)} records to {output_file}")
    logger.info(f"Total Cost: ${client.get_cost():.4f}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
