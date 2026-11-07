# Cohort B2 run status

Generated 2026-11-07 09:44:17 Central America Standard Time by `scripts/paper_b_dashboard.py` (no metric values are shown).

```
Paper B rev. 1, cohort B2 - 2026-11-07 09:44:17
  !! Throttling suspected: the micro-benchmark is 1.20x its first value (heat or power plan).
Orchestrator: RUNNING (mode quality, workers 6/6, queue 198, admission: 6 workers running (max 6))
Host: CPU 65%  RAM free 8.5/31.4 GB  disk free 359 GB  AC  3000.0 MHz
pilot   : jobs 175/175  rows 700/700  failed rows 0
quality : jobs 371/575  rows 34065/57500  failed rows 1
timing  : cells 0/115
  pid  30040 connect4/svm/22/anchors                  inst 10593    675 s  RSS 1.25 GB (peak 1.91)
  pid  30684 adult/svm/22/shap                        inst 3040     21 s  RSS 0.30 GB (peak 0.31)
  pid  35004 connect4/mlp/33/anchors                  inst 4489     20 s  RSS 1.90 GB (peak 2.62)
  pid  23000 phishing/svm/33/shap                     inst 802      3 s  RSS 0.26 GB (peak 0.26)
  pid  35924 breast_cancer/xgb/33/anchors             inst 44     41 s  RSS 0.73 GB (peak 0.84)
  pid  27072 connect4/rf/33/dice                      inst 4309      8 s  RSS 0.38 GB (peak 0.42)
Sync: last push 15 min ago (187144bb93), last commit 15 min ago
```
