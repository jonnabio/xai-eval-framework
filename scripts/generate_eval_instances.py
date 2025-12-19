"""
Script to generate the standardized evaluation dataset for XAI metrics.

This script:
1. Loads the Adult dataset.
2. Loads the trained XGBoost model.
3. Uses EvaluationSampler to select ~200 stratified instances.
4. Saves data/processed/eval_instances.csv.
"""
import logging
import sys
from pathlib import Path
import joblib

# Add src to path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src'))

from data_loading.adult import load_adult
from evaluation.sampler import EvaluationSampler

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    logger.info("Starting Evaluation Dataset Generation...")
    
    # Paths
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parents[1]
    data_dir = project_root / 'data'
    models_dir = project_root / 'experiments/exp1_adult/models'
    output_path = data_dir / 'processed/eval_instances.csv'
    
    # 1. Load Data
    logger.info(f"Loading data from {data_dir}...")
    data_dict = load_adult(data_dir=str(data_dir), random_state=42)
    X_test = data_dict['X_test']
    y_test = data_dict['y_test']
    
    # 2. Load Model (Prefer XGBoost)
    # Check potential paths
    xgb_path = models_dir / 'xgboost/xgboost_model.joblib'
    if not xgb_path.exists():
        xgb_path = models_dir / 'xgboost_model.joblib'
        
    if not xgb_path.exists():
        logger.error(f"XGBoost model not found in {models_dir}. Please run training first.")
        sys.exit(1)
        
    logger.info(f"Loading model from {xgb_path}...")
    model = joblib.load(xgb_path)
    
    # 3. Initialize Sampler
    sampler = EvaluationSampler(
        model=model,
        X_test=X_test,
        y_test=y_test,
        random_state=42
    )
    
    # 4. Generate Samples
    logger.info("Sampling stratified instances (Target: 50 per quadrant)...")
    eval_df = sampler.sample_stratified_by_error(n_per_group=50)
    
    # 5. Save
    sampler.save_instances(eval_df, output_path)
    logger.info("Generation Complete!")
    
    # Print Summary
    print("\n" + "="*40)
    print("Evaluation Dataset Summary")
    print("="*40)
    print(eval_df['quadrant'].value_counts().to_string())
    print("-" * 40)
    print(f"Total: {len(eval_df)}")
    print(f"Path: {output_path}")
    print("="*40)

if __name__ == '__main__':
    main()
