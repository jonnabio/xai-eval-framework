"""
Generate experiment configuration files for Phase I (Experiment 2: Comparative Evaluation).

Matrix:
- Models (5): RF, XGB, SVM, MLP, LogReg
- Explainers (4): SHAP, LIME, Anchors, DiCE
- Replicates: 5 (via random seeds? No, usually distinct configs or loop in runner. 
             We will treat each config as one "Main" run for now, runner handles internal validation CV/seeds if configured.
             Wait, publication strategy says "10 independent runs". 
             However, creating 200 config files is messy.
             Ideally, the config has 'n_runs' or we use runner to do it.
             The current runner does ONE run per config.
             For now, let's generate the base matrix (20 configs). Replicates can be handled by running the same config multiple times? 
             No, deterministic. We need different seeds.
             
             Let's stick to the BASE 20 Configs first. We can add seed variations later or update Config schema to support multiple runs.
             Actually, let's just do ONE run for this phase to get the pipeline working, then expand.
"""
import yaml
from pathlib import Path

# Constants
MODELS = ['rf', 'xgb', 'svm', 'mlp', 'logreg']
EXPLAINERS = ['shap', 'lime', 'anchors', 'dice']

OUTPUT_DIR = Path("configs/experiments/exp2_comparative")
MODEL_DIR = Path("experiments/exp1_adult/models")

def generate_configs():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    count = 0
    for model in MODELS:
        for explainer in EXPLAINERS:
            
            # Construct Config Dictionary
            config = {
                "name": f"exp2_{model}_{explainer}",
                "version": "1.0",
                "dataset": "adult",
                "random_seed": 42,
                
                "model": {
                    "name": f"adult_{model}",
                    "path": str(MODEL_DIR / f"{model}.joblib"),
                    "type": model
                },
                
                "explainer": {
                    "method": explainer,
                    "params": {} # Default params
                },
                
                "sampling": {
                    "strategy": "stratified",
                    "samples_per_class": 10, # 40 total per run (small for dev, increase for real paper)
                    "random_seed": 42
                },
                
                "metrics": {
                    "fidelity": True,
                    "stability": True,
                    "sparsity": True,
                    "cost": True,
                    "domain": False, # Requires prior knowledge setup
                    "counterfactual": False # DiCE handles this internally if explainer IS DiCE
                },
                
                "output_dir": f"experiments/exp2_comparative/results/{model}_{explainer}"
            }
            
            # Special Explainer Params
            if explainer == "shap":
                config['explainer']['params'] = {
                    "n_background_samples": 50
                }
                # Tree vs Kernel
                if model in ['rf', 'xgb']:
                     config['explainer']['explainer_type'] = "tree"
                else:
                     config['explainer']['explainer_type'] = "kernel"
                     
            elif explainer == "lime":
                config['explainer']['params'] = {
                    "kernel_width": 3.0
                }
                
            elif explainer == "anchors":
                config['explainer']['params'] = {
                    "threshold": 0.95
                }
                # Anchors needs 'alibi' installed
                
            elif explainer == "dice":
                 config['metrics']['counterfactual'] = True
                 # DiCE params if any
            
            # Write to file
            filename = OUTPUT_DIR / f"{model}_{explainer}.yaml"
            with open(filename, 'w') as f:
                yaml.dump(config, f, sort_keys=False)
            
            count += 1
            
    print(f"Generated {count} configuration files in {OUTPUT_DIR}")

if __name__ == "__main__":
    generate_configs()
