#!/usr/bin/env python3
"""Paper B revision 1: write the configuration files of the auxiliary studies.

    py scripts/paper_b_studies.py            # (re)writes experiments/exp_b_rev1/studies/*.toml
    py scripts/paper_b_studies.py --budget   # also prints a CPU-hour estimate from the pilot

Each study is the main design (cohort.toml) with only the stated changes, run by the same
runner with PAPER_B_CONFIG=<file> (own live folder, state, logs and stop file):

- sweep.toml            WP5  configuration sweep on Adult: LIME kernel width x samples (full
                        vector); KernelSHAP samples and background one factor at a time, on
                        every model (KernelSHAP forced on the tree models too); TreeSHAP
                        background on the tree models. 1 instance per stratum, 3 seeds.
- controls_nonoise.toml WP4a sigma = 0: the explainer's own variance.
- controls_onehot.toml  WP4b noise that keeps one-hot rows valid.
                        Both controls use the main cohort's instances and compute only its
                        stability subset (3 per stratum, 3 seeds).
- matched.toml          WP2b random forest and XGBoost at matched depth (rf_d6, xgb_d15) next
                        to the main ones; for the timing pass (cost against total leaves).

Run order (after the main quality pass, never during the timing pass):
  set PAPER_B_CONFIG=experiments\\exp_b_rev1\\studies\\<file>; py scripts\\paper_b_run.py launch
  (matched: `prepare --keep-data` first, then `launch-timing`; sweep: `launch` then
  `launch-timing`.)
"""
from __future__ import annotations

import argparse
import copy
import sys
import tomllib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paper_b_lib as lib  # noqa: E402

STUDIES = lib.COHORT_DIR / "studies"
ADULT_SEEDS = [11, 22, 33]
LIME_KW = [0.75, 1.5, 3.0, 5.0, "default", 10.0, 15.0]
LIME_NS = [250, 500, 1000, 2000, 5000]
KSHAP = [(100, 50), (250, 50), (500, 50), (1000, 50), ("auto", 50), (500, 10), (500, 25),
         (500, 100)]
TREE_BG = [10, 25, 50, 100]


def emit(v) -> str:
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return repr(v)
    if isinstance(v, str):
        return '"' + v.replace("\\", "\\\\").replace('"', '\\"') + '"'
    if isinstance(v, list):
        return "[" + ", ".join(emit(x) for x in v) + "]"
    if isinstance(v, dict):
        return "{ " + ", ".join(f"{k} = {emit(x)}" for k, x in v.items()) + " }"
    raise TypeError(type(v))


def dump(cfg: dict, header: str) -> str:
    out = [f"# {line}".rstrip() for line in header.strip().splitlines()] + [""]
    for top, val in cfg.items():
        if all(isinstance(x, dict) for x in val.values()) and val:
            for name, sub in val.items():
                out.append(f"[{top}.{name}]")
                out += [f"{k} = {emit(x)}" for k, x in sub.items()]
                out.append("")
        else:
            out.append(f"[{top}]")
            out += [f"{k} = {emit(x)}" for k, x in val.items()]
            out.append("")
    return "\n".join(out)


def base(main: dict, study: str) -> dict:
    c = copy.deepcopy(main)
    c["cohort"]["name"] = f"B2-{study}"
    c["datasets"] = {"adult": c["datasets"]["adult"]}
    c["seeds"] = {"adult": ADULT_SEEDS, "other": ADULT_SEEDS}
    c["sync"]["results_prefix"] = f"experiments/exp_b_rev1/studies_results/{study}"
    c["sync"]["also_push"] = []
    return c


def sweep(main: dict) -> dict:
    c = base(main, "sweep")
    c["sampling"].update({"per_stratum": 1, "stability_per_stratum": 1})
    ex = {}
    for kw in LIME_KW:
        for ns in LIME_NS:
            tag = "def" if kw == "default" else str(kw).replace(".", "p")
            ex[f"lime_kw{tag}_ns{ns}"] = {"method": "lime", "num_samples": ns,
                                         "num_features": "all", "kernel_width": kw}
    for ns, bg in KSHAP:
        ex[f"kshap_ns{ns}_bg{bg}"] = {"method": "shap", "algorithm": "kernel",
                                       "n_background_samples": bg, "kernel_nsamples": ns,
                                       "kernel_nsamples_by_model": {}}
    for bg in TREE_BG:
        ex[f"tshap_bg{bg}"] = {"method": "shap", "n_background_samples": bg,
                               "kernel_nsamples": "auto", "kernel_nsamples_by_model": {},
                               "models": ["rf", "xgb"]}
    c["explainers"] = ex
    c["timing"].update({"per_stratum": 1})
    return c


def controls(main: dict, study: str, metrics: dict) -> dict:
    c = base(main, study)
    c["sampling"].update({"stability_only": True})      # same instances as the main cohort
    c["metrics"].update(metrics)
    return c


def matched(main: dict) -> dict:
    c = base(main, "matched")
    rf, xgb = main["models"]["rf"], main["models"]["xgb"]
    c["models"] = {
        "rf": rf, "xgb": xgb,
        "rf_d6": {"class": rf["class"], "params": {**rf["params"], "max_depth": 6}},
        "xgb_d15": {"class": xgb["class"], "params": {**xgb["params"], "max_depth": 15}},
    }
    c["explainers"] = {k: main["explainers"][k] for k in ("shap", "lime_full")}
    return c


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--budget", action="store_true")
    a = ap.parse_args(argv)
    with open(lib.MAIN_CONFIG, "rb") as fh:
        m = tomllib.load(fh)
    STUDIES.mkdir(parents=True, exist_ok=True)
    head = ("GENERATED by scripts/paper_b_studies.py from cohort.toml: do not edit by hand.\n"
            "Run with PAPER_B_CONFIG=<this file> (see the script's docstring).")
    files = {
        "sweep": sweep(m),
        "controls_nonoise": controls(m, "controls_nonoise", {"stability_sigma": 0.0}),
        "controls_onehot": controls(m, "controls_onehot",
                                    {"stability_noise": "onehot_valid", "onehot_resample_p": 0.1}),
        "matched": matched(m),
    }
    for name, cfg in files.items():
        text = dump(cfg, f"Study '{name}' of Paper B revision 1 (cohort B2).\n{head}")
        path = STUDIES / f"{name}.toml"
        path.write_text(text, encoding="utf-8")
        with open(path, "rb") as fh:
            back = tomllib.load(fh)
        assert back == cfg, f"{name}: round trip changed the configuration"
        n = len(lib.all_quality_jobs(cfg))
        print(f"{path.relative_to(lib.ROOT)}: {len(cfg['explainers'])} explainer variants, "
              f"{len(cfg['models'])} models, {n} quality jobs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
