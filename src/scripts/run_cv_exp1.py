"""
Script to run Cross-Validation for EXP1 experiments.

Usage:
    python src/scripts/run_cv_exp1.py --folds 5 --experiments rf_lime xgb_shap
    python src/scripts/run_cv_exp1.py --folds 2 --experiments rf_lime (Pilot)
"""

import argparse
import logging
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from src.experiment.config import load_config
from src.experiment.cv_runner import CrossValidationRunner

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Map experiment keys to config files
EXP_CONFIGS = {
    "rf_lime": "configs/experiments/exp1_adult_rf_lime.yaml",
    "rf_shap": "configs/experiments/exp1_adult_rf_shap.yaml",
    "xgb_lime": "configs/experiments/exp1_adult_xgb_lime.yaml",
    "xgb_shap": "configs/experiments/exp1_adult_xgb_shap.yaml"
}

def main():
    parser = argparse.ArgumentParser(description="Run EXP1 Cross-Validation")
    parser.add_argument("--folds", type=int, default=5, help="Number of folds (default: 5)")
    parser.add_argument(
        "--experiments", 
        nargs="+", 
        default=["rf_lime", "rf_shap", "xgb_lime", "xgb_shap"],
        choices=EXP_CONFIGS.keys(),
        help="Experiments to run"
    )
    
    args = parser.parse_args()
    
    logger.info(f"Starting CV Run with {args.folds} folds for: {args.experiments}")
    
    for exp_key in args.experiments:
        config_path = Path(EXP_CONFIGS[exp_key])
        if not config_path.exists():
            logger.error(f"Config file not found: {config_path}")
            continue
            
        try:
            logger.info(f"Loading config: {config_path}")
            config = load_config(config_path)
            
            # Update name to indicate CV
            # e.g. "exp1_adult_rf_lime" -> "exp1_cv_adult_rf_lime"
            # This ensures output goes to outputs/cv/exp1_cv_...
            if not config.name.startswith("exp1_cv_"):
                config.name = config.name.replace("exp1_", "exp1_cv_")
                
            runner = CrossValidationRunner(config, n_folds=args.folds)
            runner.run()
            
        except Exception as e:
            logger.error(f"Failed to run CV for {exp_key}: {e}", exc_info=True)

if __name__ == "__main__":
    main()
