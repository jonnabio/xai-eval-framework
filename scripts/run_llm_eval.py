#!/usr/bin/env python3
"""
Script to run LLM-based evaluation on XAI experiment results.

Usage:
    python scripts/run_llm_eval.py \
        --input_dir experiments/exp1_adult/results/rf_shap \
        --provider openai \
        --model gpt-4 \
        --output_file llm_eval_results.json
"""

import argparse
import json
import logging
import sys
from pathlib import Path
from tqdm import tqdm

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from src.experiment.config import LLMConfig
from src.llm.client import LLMClientFactory
from src.prompts.engine import PromptEngine

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def parse_args():
    parser = argparse.ArgumentParser(description="Run LLM evaluation on XAI results.")
    
    parser.add_argument(
        '--input_dir',
        type=Path,
        required=True,
        help='Directory containing results.json from an experiment run'
    )
    
    parser.add_argument(
        '--provider',
        type=str,
        default='openai',
        choices=['openai', 'gemini'],
        help='LLM provider'
    )
    
    parser.add_argument(
        '--model',
        type=str,
        default='gpt-4',
        help='LLM model name'
    )
    
    parser.add_argument(
        '--output_file',
        type=str,
        default='llm_eval.json',
        help='Filename for output results (saved in input_dir)'
    )
    
    parser.add_argument(
        '--limit',
        type=int,
        default=None,
        help='Limit number of instances to evaluate (for testing)'
    )
    
    return parser.parse_args()

def main():
    args = parse_args()
    
    # 1. Load Experiment Results
    results_path = args.input_dir / "results.json"
    if not results_path.exists():
        logger.error(f"Results file not found: {results_path}")
        sys.exit(1)
        
    logger.info(f"Loading results from {results_path}")
    with open(results_path, 'r') as f:
        data = json.load(f)
        
    instances = data.get('instance_evaluations', [])
    if not instances:
        logger.warning("No instances found in results file.")
        sys.exit(0)
        
    # Metadata for context
    model_name = data.get('model_info', {}).get('name', 'Unknown')
    method_name = data.get('model_info', {}).get('explainer_method', 'Unknown')
    
    # 2. Initialize LLM Client
    llm_config = LLMConfig(
        provider=args.provider,
        model_name=args.model,
        temperature=0.0
    )
    
    try:
        client = LLMClientFactory.create(llm_config)
    except Exception as e:
        logger.error(f"Failed to initialize LLM client: {e}")
        sys.exit(1)
        
    # 3. Initialize Prompt Engine
    prompt_engine = PromptEngine()
    
    # 4. Evaluation Loop
    eval_results = []
    
    count = 0
    limit = args.limit if args.limit is not None else len(instances)
    
    logger.info(f"Starting evaluation of {limit} instances...")
    
    for inst in tqdm(instances[:limit]):
        try:
            # Prepare context
            explanation_str = "\n".join(inst.get('explanation', {}).get('top_features', []))
            if not explanation_str:
                explanation_str = "No explanation details available."
            
            context = {
                "model_name": model_name,
                "method_name": method_name,
                "prediction_label": ">50K" if inst['prediction'] == 1 else "<=50K",
                "true_label": ">50K" if inst['true_label'] == 1 else "<=50K",
                "explanation_text": explanation_str
            }
            
            # Render Prompt
            prompt = prompt_engine.render("eval_instruction.j2", **context)
            
            # Call LLM
            response_text = client.generate(prompt)
            
            # Parse Response (naive JSON extraction)
            # LLMs might wrap JSON in ```json ... ``` given the prompt instructions?
            # Or just raw text. The prompt asks for JSON.
            # Let's try to clean it up lightly.
            clean_resp = response_text.replace("```json", "").replace("```", "").strip()
            
            try:
                scores = json.loads(clean_resp)
            except json.JSONDecodeError:
                logger.warning(f"Failed to parse JSON for instance {inst['instance_id']}. Raw: {response_text[:50]}...")
                scores = {"error": "JSON parse error", "raw_response": response_text}
                
            # Store result
            eval_record = {
                "instance_id": inst['instance_id'],
                "llm_eval": scores
            }
            eval_results.append(eval_record)
            
        except Exception as e:
            logger.error(f"Error evaluating instance {inst['instance_id']}: {e}")
            
    # 5. Save Results
    output_path = args.input_dir / args.output_file
    with open(output_path, 'w') as f:
        json.dump({
            "llm_config": llm_config.model_dump(),
            "results": eval_results
        }, f, indent=2)
        
    logger.info(f"Saved LLM evaluation results to {output_path}")

if __name__ == "__main__":
    main()
