"""
One-off driver to rerun Paper A's known result gaps after installing the
missing alibi/dice-ml dependencies:

  - the 25 present-but-empty Anchors/DiCE artifacts in experiments/exp2_scaled
  - the 24 not-yet-run exp3_cross_dataset external-validation configs

Existing empty exp2 results.json files are backed up (not deleted) before
being cleared, so the runner will re-execute those cells instead of skipping
them. Runs are sequential (max_workers=1) to respect this machine's limited
free RAM. No auto-commit/auto-push: this script only writes result artifacts;
committing is left to a manual review step afterward.
"""
import json
import logging
import shutil
import sys
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.experiment.config import load_config
from src.experiment.runner import ExperimentRunner

LOG_FILE = Path(__file__).resolve().parents[1] / "logs/rerun_paper_a_gaps.log"
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger("rerun_paper_a_gaps")

REPO_ROOT = Path(__file__).resolve().parents[1]
EXP2_EMPTY_NAMES = [
    "logreg_anchors_s123_n200", "logreg_anchors_s123_n50", "logreg_anchors_s42_n200",
    "logreg_anchors_s42_n50", "logreg_anchors_s456_n100", "logreg_anchors_s789_n200",
    "logreg_anchors_s999_n200", "logreg_anchors_s999_n50", "logreg_dice_s123_n50",
    "logreg_dice_s999_n50", "mlp_anchors_s123_n200", "mlp_anchors_s42_n100",
    "mlp_anchors_s42_n50", "mlp_anchors_s456_n100", "mlp_anchors_s456_n50",
    "mlp_anchors_s789_n200", "mlp_anchors_s789_n50", "mlp_anchors_s999_n200",
    "mlp_dice_s456_n200", "mlp_dice_s456_n50", "svm_dice_s123_n50",
    "svm_dice_s456_n100", "xgb_anchors_s123_n50", "xgb_anchors_s42_n200",
    "xgb_dice_s789_n100",
]
EXP2_CONFIG_DIR = REPO_ROOT / "configs/experiments/exp2_scaled"
EXP3_CONFIG_DIR = REPO_ROOT / "configs/experiments/exp3_cross_dataset"
BACKUP_DIR = REPO_ROOT / "experiments/exp2_scaled/_empty_artifact_backup_20260722"
STATUS_PATH = REPO_ROOT / "logs/rerun_paper_a_gaps_status.json"


def backup_and_clear(config_path: Path) -> None:
    config = load_config(config_path)
    result_file = Path(config.output_dir) / "results.json"
    if not result_file.exists():
        return
    dest = BACKUP_DIR / config.name
    dest.mkdir(parents=True, exist_ok=True)
    shutil.copy2(result_file, dest / "results.json")
    result_file.unlink()
    logger.info(f"Backed up and cleared {result_file}")


def run_one(config_path: Path, status: dict) -> None:
    name = config_path.stem
    logger.info(f"=== Starting {name} ===")
    t0 = time.time()
    try:
        config = load_config(config_path)
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
        status[name] = {
            "status": "error",
            "error": str(e),
            "elapsed_seconds": elapsed,
            "finished_at": datetime.now().isoformat(),
        }
        logger.error(f"=== FAILED {name}: {e} ===")
    STATUS_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATUS_PATH.write_text(json.dumps(status, indent=2))


def main() -> None:
    status: dict = {}
    if STATUS_PATH.exists():
        status = json.loads(STATUS_PATH.read_text())

    exp2_configs = [EXP2_CONFIG_DIR / f"{n}.yaml" for n in EXP2_EMPTY_NAMES]
    missing = [p for p in exp2_configs if not p.exists()]
    if missing:
        raise SystemExit(f"Missing expected config files: {missing}")

    exp3_configs = sorted(EXP3_CONFIG_DIR.glob("*/*.yaml"))

    logger.info(f"Clearing {len(exp2_configs)} empty exp2 artifacts (backed up to {BACKUP_DIR})...")
    for p in exp2_configs:
        if status.get(p.stem, {}).get("status") == "ok":
            continue
        backup_and_clear(p)

    all_configs = exp2_configs + exp3_configs
    logger.info(f"Total configs to process: {len(all_configs)} (exp2 gaps: {len(exp2_configs)}, exp3: {len(exp3_configs)})")

    for p in all_configs:
        if status.get(p.stem, {}).get("status") == "ok":
            logger.info(f"Skipping already-completed {p.stem}")
            continue
        run_one(p, status)

    n_ok = sum(1 for v in status.values() if v.get("status") == "ok")
    n_bad = sum(1 for v in status.values() if v.get("status") != "ok")
    logger.info(f"DONE. {n_ok} succeeded, {n_bad} still failed/empty. Status file: {STATUS_PATH}")


if __name__ == "__main__":
    main()
