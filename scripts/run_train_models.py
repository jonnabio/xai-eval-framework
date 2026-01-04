import argparse
import sys
import logging
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.models.tabular_models import train_random_forest_adult
# Assuming xgboost trainer similar or needing import, check xgboost_trainer.py
from src.models.xgboost_trainer import train_xgboost_adult

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Train models for Experiment 1 (Adult Dataset)")
    parser.add_argument("--model", type=str, choices=["rf", "xgb", "all"], required=True, help="Model to train")
    parser.add_argument("--force", action="store_true", help="Force retraining")
    
    args = parser.parse_args()
    
    try:
        if args.model in ["rf", "all"]:
            logger.info("Training Random Forest...")
            train_random_forest_adult(force_retrain=args.force)
            
        if args.model in ["xgb", "all"]:
            logger.info("Training XGBoost...")
            train_xgboost_adult(force_retrain=args.force)
            
    except Exception as e:
        logger.error(f"Training failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
