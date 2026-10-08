"""Paper F: order of the jobs of the launcher and choice of the seeds of a launch.

No data are read and no job is started.
"""
from __future__ import annotations

import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
import paper_f_chain as chain  # noqa: E402
import paper_f_run as run  # noqa: E402

DATASETS = ["adult", "churn", "pc3"]
MODELS = ["logreg", "rf"]
EXPLAINERS = ["lime", "shap", "anchors", "dice"]


def test_one_seed_keeps_the_order_of_the_first_part():
    """Seed 42 was run with one shuffle of its jobs; a launch of one seed must not change it."""
    old = [(d, m, s, e) for d in DATASETS for m in MODELS for s in [42] for e in EXPLAINERS]
    random.Random(20261005).shuffle(old)
    assert run.ordered_jobs(DATASETS, MODELS, [42], EXPLAINERS) == old


def test_seeds_in_order_with_the_same_shuffle_inside():
    seeds = [123, 456, 789]
    jobs = run.ordered_jobs(DATASETS, MODELS, seeds, EXPLAINERS)
    per_seed = len(DATASETS) * len(MODELS) * len(EXPLAINERS)
    assert len(jobs) == len(set(jobs)) == per_seed * len(seeds)
    assert [j[2] for j in jobs] == [s for s in seeds for _ in range(per_seed)]
    parts = [[(d, m, e) for d, m, s, e in jobs if s == seed] for seed in seeds]
    assert parts[0] == parts[1] == parts[2]


def test_requeue_stays_inside_its_seed():
    seeds = [123, 456]
    queue = [("a", "rf", 123, "lime"), ("b", "rf", 456, "lime"), ("c", "rf", 456, "shap")]
    run.requeue(queue, ("x", "rf", 123, "dice"), seeds)
    assert [j[0] for j in queue] == ["a", "x", "b", "c"]
    run.requeue(queue, ("y", "rf", 456, "dice"), seeds)
    assert [j[0] for j in queue] == ["a", "x", "b", "c", "y"]
    empty: list[tuple] = []
    run.requeue(empty, ("z", "rf", 123, "dice"), seeds)
    assert empty == [("z", "rf", 123, "dice")]


def test_seeds_to_launch_skips_complete_and_given_up():
    seeds = [42, 123, 456, 789]
    counts = {42: 256, 123: 3, 456: 2, 789: 0}
    assert chain.seeds_to_launch(seeds, counts, 256, {"42": 1}) == [123, 456, 789]
    given_up = {"123": chain.MAX_RELAUNCH}
    assert chain.seeds_to_launch(seeds, counts, 256, given_up) == [456, 789]
    assert chain.seeds_to_launch(seeds, dict.fromkeys(seeds, 256), 256, {}) == []
