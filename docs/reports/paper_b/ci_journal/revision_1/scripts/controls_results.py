"""Validity controls (no noise, valid one-hot) against the main protocol, matched instances."""
import json, sys
from pathlib import Path
import pandas as pd

CTL = Path(sys.argv[1]); MAIN = sys.argv[2]; OUT = Path(sys.argv[3])
rows = []
for study in ("controls_nonoise", "controls_onehot"):
    for f in (CTL / study / "results/quality/adult").rglob("*.jsonl"):
        model, seed, expl = f.parts[-3], int(f.parts[-2].split("_")[1]), f.stem
        for l in f.read_text().splitlines():
            d = json.loads(l)
            rows.append(dict(study=study, model=model, seed=seed, explainer=expl,
                             instance_id=d["instance_id"], stability=d.get("stability"),
                             zero=d.get("stability_zero_vectors", 0)))
c = pd.DataFrame(rows)
m = pd.read_csv(MAIN, low_memory=False)
m = m[(m.dataset == "adult")][["model", "seed", "explainer", "instance_id", "stability"]].dropna()
m["study"] = "main"
key = ["model", "seed", "explainer", "instance_id"]
inst = c[key].drop_duplicates()
mm = m.merge(inst, on=key)
print("control rows", len(c), "matched main rows", len(mm), "fails", c.stability.isna().sum())
a = pd.concat([mm, c[mm.columns]])
t = a.groupby(["study", "model", "explainer"]).stability.mean().unstack("study")
t = t[["main", "controls_nonoise", "controls_onehot"]]
OUT.mkdir(parents=True, exist_ok=True)
t.round(3).to_csv(OUT / "controls_stability.csv")
print(t.round(3).to_string())
# SHAP minus X per cell (model, seed), number of cells SHAP ahead, by study
cell = a.groupby(["study", "model", "seed", "explainer"]).stability.mean().unstack("explainer")
res = []
for x in ("lime", "lime_full", "anchors", "dice"):
    d = (cell["shap"] - cell[x]).rename("d").reset_index()
    for st, g in d.groupby("study"):
        res.append(dict(study=st, contrast=f"shap-{x}", mean=g.d.mean(), cells=len(g),
                        shap_ahead=int((g.d > 0).sum()),
                        models_ahead=int((g.groupby("model").d.mean() > 0).sum())))
r = pd.DataFrame(res)
r.round(3).to_csv(OUT / "controls_contrasts.csv", index=False)
print(r.round(3).to_string())
# share of LIME's instability that is its own sampling: (1 - nonoise) / (1 - main)
for x in ("lime", "lime_full", "shap", "anchors", "dice"):
    s = t.xs(x, level="explainer")
    share = (1 - s.controls_nonoise) / (1 - s.main)
    print(x, "own-sampling share by model:", share.round(2).to_dict(),
          "pooled", round((1 - s.controls_nonoise.mean()) / (1 - s.main.mean()), 2))
