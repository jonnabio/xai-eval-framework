import sys
import json
import hashlib
import importlib
import argparse
from pathlib import Path
import math

class ReproducibilityChecker:
    def __init__(self, expected_results_path):
        self.errors = []
        self.warnings = []
        self.base_dir = Path(__file__).resolve().parent.parent.parent.parent
        
        try:
            with open(expected_results_path) as f:
                self.config = json.load(f)
        except Exception as e:
            self.fail(f"Could not load expected results from {expected_results_path}: {e}")

    def fail(self, msg):
        print(f"❌ CRITICAL ERROR: {msg}")
        sys.exit(1)

    def check_environment(self):
        """Verify Python version and verification of key packages."""
        print("[1/7] Checking environment...")
        
        # Python
        v = sys.version_info
        if v.major != 3 or v.minor != 11:
            self.warnings.append(f"Python version mismatch: expected 3.11, got {v.major}.{v.minor}")

        required = {
            'sklearn': '1.8.0',
            'xgboost': '3.1.2',
            'shap': '0.50.0',
            'lime': '0.2.0.1' 
        }
        
        for pkg, expected in required.items():
            try:
                mod = importlib.import_module(pkg)
                actual = getattr(mod, '__version__', 'unknown')
                if not actual.startswith(expected.rpartition('.')[0]): 
                     self.warnings.append(f"Package {pkg} version mismatch: expected ~{expected}, got {actual}")
            except ImportError:
                self.errors.append(f"Missing package: {pkg}")

    def check_data(self):
        """Verify dataset integrity."""
        print("[2/7] Checking data...")
        data_checksums = self.config.get('data_checksums', {})
        
        for filename, expected_hash in data_checksums.items():
            file_path = self.base_dir / "data" / "adult" / filename
            if not file_path.exists():
                self.errors.append(f"Missing data file: {file_path}")
                continue
                
            with open(file_path, "rb") as f:
                md5 = hashlib.md5(f.read()).hexdigest()
            
            if md5 != expected_hash:
                self.errors.append(f"Data corruption: {filename} hash mismatch.")

    def check_models(self):
        """Verify model existence."""
        print("[3/7] Checking models...")
        # Corrected paths
        models = [
            "experiments/exp1_adult/models/rf_model.pkl",
            "experiments/exp1_adult/models/xgboost/xgb_model.pkl"
        ]
        
        for m in models:
            p = self.base_dir / m
            if not p.exists():
                self.errors.append(f"Missing model: {m}")

    def check_results(self):
        """Verify result JSONs exist."""
        print("[4/7] Checking results files...")
        experiments = ['rf_lime', 'rf_shap', 'xgb_lime', 'xgb_shap']
        
        for exp in experiments:
            p = self.base_dir / f"experiments/exp1_adult/results/{exp}/results.json"
            if not p.exists():
                self.errors.append(f"Missing results for {exp}")
            else:
                 # Check for basic content (instances)
                try:
                    with open(p) as f:
                         data = json.load(f)
                    if 'instance_evaluations' not in data:
                        self.warnings.append(f"Results for {exp} missing instance_evaluations")
                except json.JSONDecodeError:
                    self.errors.append(f"Corrupt results JSON for {exp}")

    def check_metrics(self):
        """Compare quantitative metrics against expected ranges using metadata artifact."""
        print("[5/7] Checking metrics (from results_metadata.json)...")
        expected = self.config.get('expected_metrics', {})
        
        meta_path = self.base_dir / "docs/thesis/results_metadata.json"
        if not meta_path.exists():
            self.errors.append("results_metadata.json missing. Cannot verify metrics.")
            return

        try:
            with open(meta_path) as f:
                metadata = json.load(f)
        except Exception as e:
            self.errors.append(f"Corrupt results_metadata.json: {e}")
            return
        
        for exp_name, metrics in expected.items():
            # In metadata.json, keys are matched to what we have in config
            if exp_name not in metadata:
                self.warnings.append(f"Experiment {exp_name} not found in metadata.")
                continue
            
            # Metadata structure: metadata[exp_name]['xai_metrics'][metric]['mean']
            xai_metrics = metadata[exp_name].get('xai_metrics', {})
            
            for m_name, criteria in metrics.items():
                target = criteria['mean']
                tol = criteria['tolerance']
                
                # Handling 'fidelity' vs 'Fidelity' if case mismatch exists?
                # Usually keys are lowercase in our pipeline.
                actual_dict = xai_metrics.get(m_name, {})
                actual = actual_dict.get('mean')
                
                if actual is None:
                    self.warnings.append(f"{exp_name}: Metric {m_name} missing from metadata.")
                    continue
                    
                if abs(actual - target) > tol:
                    self.warnings.append(f"{exp_name} {m_name}: {actual:.3f} outside expected range {target} ± {tol}")

    def check_artifacts(self):
        """Verify generated LaTeX artifacts."""
        print("[6/7] Checking artifacts...")
        required = [
            "docs/thesis/chapter_5_results.tex",
            "docs/thesis/tables/model_performance.tex",
            "docs/thesis/tables/xai_metrics_comparison.tex",
            "docs/thesis/interpretation.tex"
        ]
        
        for r in required:
            p = self.base_dir / r
            if not p.exists():
                self.errors.append(f"Missing artifact: {r}")

    def run(self):
        print("="*60)
        print("REPRODUCIBILITY VERIFICATION")
        print("="*60)
        
        self.check_environment()
        self.check_data()
        self.check_models()
        self.check_results()
        self.check_metrics()
        self.check_artifacts()
        
        print("\n" + "="*60)
        if not self.errors and not self.warnings:
            print("✅ VERIFICATION PASSED: Experiment is fully reproducible.")
            return 0
        
        if self.warnings:
            print(f"⚠️  PASSED WITH WARNINGS ({len(self.warnings)}):")
            for w in self.warnings: print(f"  - {w}")
            
        if self.errors:
            print(f"❌ FAILED ({len(self.errors)} errors):")
            for e in self.errors: print(f"  - {e}")
            return 1
            
        return 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    default_config = Path(__file__).parent / "expected_results.json"
    parser.add_argument("--config", default=str(default_config))
    args = parser.parse_args()
    
    checker = ReproducibilityChecker(args.config)
    sys.exit(checker.run())
