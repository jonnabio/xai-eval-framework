
import argparse
import pandas as pd
import json
import logging
from pathlib import Path
import sys

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def load_metrics(path: Path) -> pd.DataFrame:
    try:
        csv_path = path / "metrics.csv"
        if not csv_path.exists():
            return None
        return pd.read_csv(csv_path)
    except Exception as e:
        logger.warning(f"Failed to read {csv_path}: {e}")
        return None

def load_metadata(path: Path) -> dict:
    try:
        json_path = path / "results.json"
        if not json_path.exists():
            return {}
        with open(json_path) as f:
            return json.load(f).get("experiment_metadata", {})
    except Exception as e:
        return {}

def main():
    parser = argparse.ArgumentParser(description="Compare Recovery Run vs Baseline")
    parser.add_argument("--baseline", type=str, required=True, help="Path to baseline results dir")
    parser.add_argument("--recovery", type=str, required=True, help="Path to recovery results dir")
    args = parser.parse_args()

    baseline_root = Path(args.baseline)
    recovery_root = Path(args.recovery)

    if not baseline_root.exists() or not recovery_root.exists():
        logger.error("Paths must verify existing directories.")
        sys.exit(1)

    # Find matching experiments (by folder name structure? or just list all)
    # We expect recovery to have "rec_p1_" prefix perhaps, or different folder structure.
    # Let's scan for result directories (contain metrics.csv)
    
    logger.info(f"Scanning recovery results in {recovery_root}...")
    rec_results = list(recovery_root.rglob("metrics.csv"))
    
    report_data = []

    for rec_csv in rec_results:
        rec_dir = rec_csv.parent
        # Infer corresponding baseline dir
        # Recovery: experiments/recovery/phase1/results/mlp_shap/seed_42/n_100
        # Baseline: experiments/exp2_scaled/results/mlp_shap/seed_42/n_100
        
        rel_path = rec_dir.relative_to(recovery_root)
        # Check if same structure exists in baseline
        base_dir = baseline_root / rel_path
        
        # Load Data
        df_rec = pd.read_csv(rec_csv)
        meta_rec = load_metadata(rec_dir)
        
        df_base = load_metrics(base_dir)
        meta_base = load_metadata(base_dir) if df_base is not None else {}
        
        # Compare Time
        time_rec = meta_rec.get("duration_seconds", 0)
        time_base = meta_base.get("duration_seconds", float('nan'))
        
        # Compare Fidelity (Faithfulness)
        fid_rec = df_rec['metric_faithfulness'].mean() if 'metric_faithfulness' in df_rec else float('nan')
        fid_base = df_base['metric_faithfulness'].mean() if df_base is not None and 'metric_faithfulness' in df_base else float('nan')
        
        report_data.append({
            "Experiment": rel_path,
            "Rec_Time(s)": time_rec,
            "Base_Time(s)": time_base,
            "Speedup": time_base / time_rec if time_rec > 0 and pd.notna(time_base) else "N/A",
            "Rec_Fidelity": fid_rec,
            "Base_Fidelity": fid_base,
            "Fidelity_Delta": fid_rec - fid_base if pd.notna(fid_rec) and pd.notna(fid_base) else "N/A"
        })

    # Print Report
    if not report_data:
        logger.warning("No matching results found to compare.")
        return

    df_report = pd.DataFrame(report_data)
    print("\n=== Phase 1 Recovery Comparison Report ===\n")
    print(df_report.to_markdown(index=False, floatfmt=".2f"))
    
    # Save
    out_file = "phase1_comparison_report.csv"
    df_report.to_csv(out_file, index=False)
    print(f"\nReport saved to {out_file}")

if __name__ == "__main__":
    main()
