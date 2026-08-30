"""
Run the 12 SHAP-only exp3_cross_dataset configs (rf/xgb x breast_cancer/german_credit
x 3 seeds). These don't need alibi/dice-ml, unlike the 12 Anchors configs in the same
experiment set, which remain blocked by a numpy<2.0 vs. Python 3.13 environment
incompatibility (see paper_a_quality_assessment.md).
"""
import json
import sys
import time
from datetime import datetime
from pathlib import Path
import logging

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.experiment.config import load_config
from src.experiment.runner import ExperimentRunner

REPO_ROOT = Path(__file__).resolve().parents[1]
LOG_FILE = REPO_ROOT / "logs/run_exp3_shap_configs.log"
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger("run_exp3_shap_configs")

STATUS_PATH = REPO_ROOT / "logs/run_exp3_shap_configs_status.json"


def main() -> None:
    status: dict = {}
    if STATUS_PATH.exists():
        status = json.loads(STATUS_PATH.read_text())

    configs = sorted((REPO_ROOT / "configs/experiments/exp3_cross_dataset").glob("*/*shap*.yaml"))
    logger.info(f"Found {len(configs)} SHAP-only exp3 configs")

    for p in configs:
        name = f"{p.parent.name}/{p.stem}"
        if status.get(name, {}).get("status") == "ok":
            logger.info(f"Skipping already-completed {name}")
            continue
        logger.info(f"=== Starting {name} ===")
        t0 = time.time()
        try:
            config = load_config(p)
            runner = ExperimentRunner(config)
            runner.max_workers = 1
            results = runner.run()
            n_evals = len(results.get("instance_evaluations", []))
            elapsed = time.time() - t0
            status[name] = {
                "status": "ok" if n_evals > 0 else "still_empty",
                "n_instance_evaluations": n_evals,
                "elapsed_seconds": elapsed,
                "finished_at": datetime.now().isoformat(),
            }
            logger.info(f"=== Finished {name}: {n_evals} evaluations in {elapsed:.1f}s ===")
        except Exception as e:
            elapsed = time.time() - t0
            status[name] = {"status": "error", "error": str(e), "elapsed_seconds": elapsed}
            logger.error(f"=== FAILED {name}: {e} ===")
        STATUS_PATH.write_text(json.dumps(status, indent=2))

    n_ok = sum(1 for v in status.values() if v.get("status") == "ok")
    n_bad = sum(1 for v in status.values() if v.get("status") != "ok")
    logger.info(f"DONE. {n_ok} succeeded, {n_bad} failed/empty.")


if __name__ == "__main__":
    main()
