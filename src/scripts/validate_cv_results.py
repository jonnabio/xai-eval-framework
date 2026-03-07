
import json
import logging
import numpy as np
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)

def validate_results():
    base_dir = Path("outputs/cv")
    orig_base_dir = Path("experiments/exp1_adult/results")
    
    experiments = {
        "exp1_cv_rf_lime": "rf_lime",
        "exp1_cv_rf_shap": "rf_shap",
        "exp1_cv_xgb_lime": "xgb_lime",
        "exp1_cv_xgb_shap": "xgb_shap"
    }
    
    validation_report = "# Cross-Validation Validation Report\n\n"
    
    for cv_name, orig_name in experiments.items():
        logger.info(f"Validating {cv_name} against {orig_name}...")
        validation_report += f"## {cv_name} vs {orig_name}\n\n"
        
        cv_path = base_dir / cv_name / "cv_summary.json"
        orig_path = orig_base_dir / orig_name / "results.json"
        
        if not cv_path.exists():
            logger.warning(f"CV Validation skipped: {cv_path} not found")
            validation_report += "Result: **SKIPPED** (CV File missing)\n\n"
            continue
            
        if not orig_path.exists():
            logger.warning(f"CV Validation skipped: {orig_path} not found")
            validation_report += "Result: **SKIPPED** (Original File missing)\n\n"
            continue
            
        with open(cv_path, 'r') as f:
            cv_data = json.load(f)
            
        with open(orig_path, 'r') as f:
            orig_data = json.load(f)
            
        validations = {}
        comp_metrics = {}
        
        # Validate Metrics
        table_rows = []
        table_rows.append("| Metric | CV Mean | CV Std | Orig Mean | 95% CI | Pass? | Delta % |")
        table_rows.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
        
        all_passed = True
        
        for metric in ['fidelity', 'stability', 'sparsity', 'cost']:
            if metric not in cv_data["aggregated_metrics"]:
                continue
            
            stats = cv_data["aggregated_metrics"][metric]
            cv_mean = stats['mean']
            cv_std = stats['std']
            
            # Original structure check
            # original might have 'aggregated_metrics' or just 'metrics' depending on runner version
            # Assuming 'aggregated_metrics' since it was ExperimentRunner output
            orig_stats = orig_data.get('aggregated_metrics', {}).get(metric, {})
            # If orig results are from single run, it might be in 'metrics' if not aggregated?
            # ExperimentRunner.evaluate_instance -> ... -> results["aggregated_metrics"]
            if not orig_stats:
                 orig_stats = orig_data.get('metrics', {}).get(metric, {})
            
            orig_mean = orig_stats.get('mean')
            
            if orig_mean is not None:
                ci_lower = cv_mean - 1.96 * cv_std
                ci_upper = cv_mean + 1.96 * cv_std
                is_within = ci_lower <= orig_mean <= ci_upper
                
                # Loose check for stability (CV < 0.05 implies very stable)
                # But here we check consistency with baseline
                
                delta_pct = ((cv_mean - orig_mean)/orig_mean * 100) if orig_mean != 0 else 0
                
                validations[f"{metric}_consistent"] = is_within
                comp_metrics[metric] = {
                    "cv_mean": cv_mean,
                    "orig_mean": orig_mean,
                    "within_95_ci": is_within,
                    "diff_pct": delta_pct
                }
                
                status_icon = "✅" if is_within else "❌"
                if not is_within:
                    all_passed = False
                
                row = f"| {metric} | {cv_mean:.4f} | {cv_std:.4f} | {orig_mean:.4f} | [{ci_lower:.4f}, {ci_upper:.4f}] | {status_icon} | {delta_pct:.2f}% |"
                table_rows.append(row)
            else:
                table_rows.append(f"| {metric} | {cv_mean:.4f} | {cv_std:.4f} | N/A | - | ❓ | - |")

        validation_report += "\n".join(table_rows) + "\n\n"
        
        if all_passed:
            validation_report += "**Overall Status**: ✅ PASSED\n\n"
        else:
            validation_report += "**Overall Status**: ⚠️ WARNINGS\n\n"
            
        # Update CV Summary
        cv_data["validation"] = validations
        cv_data["comparison_with_original"] = {
            "original_path": str(orig_path),
            "metrics": comp_metrics
        }
        
        with open(cv_path, 'w') as f:
            json.dump(cv_data, f, indent=2, cls=NpEncoder)
            
        logger.info(f"Updated {cv_path}")

    # Write Report
    with open("outputs/cv/validation_report.md", 'w') as f:
        f.write(validation_report)
    logger.info("Validation report saved to outputs/cv/validation_report.md")

if __name__ == "__main__":
    validate_results()
