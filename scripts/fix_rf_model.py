import sys
from pathlib import Path
import logging

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

# Setup logging
logging.basicConfig(level=logging.INFO)

from src.models.tabular_models import AdultRandomForestTrainer

def main():
    print("Starting manual RF training...")
    
    config = {
        'model': {
            'params': {
                'n_estimators': 100, 
                'random_state': 42,
                'n_jobs': -1
            }
        },
        'output': {
            'model_dir': 'experiments/exp1_adult/models',
            'model_filename': 'rf_model.pkl',
            'results_dir': 'experiments/exp1_adult/results',
            'metrics_filename': 'rf_metrics.json'
        },
        'validation': {}
    }
    
    try:
        trainer = AdultRandomForestTrainer(config, verbose=True)
        # Call train without args to trigger internal data loading (per my refactor)
        # OR passed args if I wanted. Explicit is better but cleaner to let it load.
        model, metrics = trainer.train(force_retrain=True)
        print(f"RF Model Trained. Metrics: {metrics.get('test_roc_auc')}")
        
        # Verify file
        p = Path('experiments/exp1_adult/models/rf_model.pkl')
        if p.exists():
            print(f"SUCCESS: Model saved to {p}")
        else:
            print(f"FAILURE: Model file not found at {p}")
            
    except Exception as e:
        print(f"CRITICAL FAILURE: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
