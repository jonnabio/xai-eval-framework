import json
import argparse
import sys
import os
import yaml
import inspect
import importlib
from pathlib import Path

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.data_loading.adult import load_adult
from src.metrics.fidelity import FidelityMetric
from src.metrics.stability import StabilityMetric
from src.metrics.sparsity import SparsityMetric

# Import other metrics as needed
# from src.metrics.domain import DomainAlignmentMetric
# from src.metrics.counterfactual import CounterfactualSensitivityMetric

def extract_dataset_stats():
    """Extracts statistics from the Adult dataset."""
    try:
        X_train, X_test, y_train, y_test, feature_names, _ = load_adult()
        
        # Calculate class balance on full dataset approximation (train+test)
        total_samples = len(X_train) + len(X_test)
        total_pos = sum(y_train) + sum(y_test)
        balance_ratio = total_pos / total_samples

        return {
            'name': 'UCI Adult Income',
            'n_train': len(X_train),
            'n_test': len(X_test),
            'n_total': total_samples,
            'n_features': len(feature_names),
            'feature_names': feature_names,
            'target': 'income (>50K / <=50K)',
            'class_balance_pos_ratio': float(balance_ratio)
        }
    except Exception as e:
        print(f"Warning: Could not load dataset stats: {e}")
        return {}

def extract_model_configs(config_dir="configs/experiments"):
    """Extracts hyperparameters from YAML config files."""
    configs = []
    config_path = Path(config_dir)
    
    if not config_path.exists():
        print(f"Warning: Config directory {config_dir} not found.")
        return configs

    for config_file in config_path.glob("exp1_*.yaml"):
        try:
            with open(config_file, 'r') as f:
                config = yaml.safe_load(f)
            
            # Extract basic info
            model_info = config.get('model', {})
            hyperparameters = model_info.get('params', {})
            
            # If params are empty, try to load from model file
            if not hyperparameters and 'path' in model_info:
                model_path = Path(model_info['path'])
                # Handle relative path from project root
                if not model_path.is_absolute():
                    model_path = Path(__file__).resolve().parents[2] / model_path
                
                if model_path.exists():
                    try:
                        import joblib
                        model = joblib.load(model_path)
                        
                        # Extract params based on model type
                        if hasattr(model, 'get_params'):
                            # Scikit-learn style
                            all_params = model.get_params()
                            # Filter for interesting ones to avoid clutter
                            interesting_keys = ['n_estimators', 'max_depth', 'learning_rate', 'random_state', 'criterion', 'min_samples_leaf']
                            hyperparameters = {k: all_params[k] for k in interesting_keys if k in all_params}
                        elif hasattr(model, 'save_config'):
                            # XGBoost style
                             import json
                             conf = json.loads(model.save_config())
                             # This structure is complex, keep it simple for now or extract specific keys
                             hyperparameters = {'learner': conf.get('learner', {})}
                    except Exception as e:
                        print(f"Warning: Failed to load model from {model_path}: {e}")
            
            configs.append({
                'filename': config_file.name,
                'name': config.get('name', 'Unknown'),
                'model': model_info.get('name', 'Unknown'),
                'explainer': config.get('explainer', {}).get('method', 'Unknown'),
                'hyperparameters': hyperparameters,
                'explainer_params': config.get('explainer', {}).get('params', {}),
                'sampling': config.get('sampling', {})
            })
        except Exception as e:
            print(f"Warning: Error parsing {config_file}: {e}")
            
    return configs

def extract_metric_definitions():
    """Extracts metric descriptions and formulas from docstrings."""
    metrics = {}
    
    # List of metric classes to document
    metric_classes = [
        ('Fidelity', FidelityMetric),
        ('Stability', StabilityMetric),
        ('Sparsity', SparsityMetric)
    ]

    for name, cls in metric_classes:
        doc = cls.__doc__ if cls.__doc__ else "No description available."
        # Simple extraction logic: Assume first paragraph is description
        description = doc.strip().split('\n')[0]
        
        metrics[name] = {
            'description': description,
            # In a real scenario, we might parse more specific fields from docstrings
            'class_name': cls.__name__
        }
        
    return metrics

def extract_env_info():
    """Extracts version information of key libraries."""
    import sklearn
    import shap
    import lime
    import xgboost
    
    lime_version = getattr(lime, '__version__', 'Unknown')
    if lime_version == 'Unknown':
        # Try getting version from package metadata if available or installed
        try:
             from importlib.metadata import version
             lime_version = version('lime')
        except:
             pass

    return {
        'python': sys.version.split()[0],
        'scikit-learn': sklearn.__version__,
        'shap': shap.__version__,
        'lime': lime_version,
        'xgboost': xgboost.__version__
    }

def main():
    parser = argparse.ArgumentParser(description="Extract methodology metadata to JSON.")
    parser.add_argument("--output", default="docs/thesis/metadata.json", help="Output JSON file path")
    args = parser.parse_args()

    metadata = {
        'dataset': extract_dataset_stats(),
        'experiments': extract_model_configs(),
        'metrics': extract_metric_definitions(),
        'environment': extract_env_info()
    }

    # Ensure output directory exists
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)

    with open(args.output, 'w') as f:
        json.dump(metadata, f, indent=4)
    
    print(f"Metadata extracted to {args.output}")

if __name__ == "__main__":
    main()
