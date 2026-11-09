# Cohort B2 run status

Generated 2026-11-09 00:03:26 Central America Standard Time by `scripts/paper_b_dashboard.py` (no metric values are shown).

```
Paper B rev. 1, cohort B2 - 2026-11-09 00:03:26
Orchestrator: RUNNING (mode quality, workers 6/6, queue 50, admission: 6 workers running (max 6))
Host: CPU 59%  RAM free 7.8/31.4 GB  disk free 358 GB  AC  3000.0 MHz
pilot   : jobs 0/25  rows 0/100  failed rows 0
quality : jobs 19/75  rows 264/7500  failed rows 0
timing  : cells 0/15
  pid  28840 adult/mlp/11/anchors                     inst 2058    291 s  RSS 2.52 GB (peak 3.06)
  pid  27620 adult/rf/11/anchors                      inst 9040      9 s  RSS 0.99 GB (peak 1.73)
  pid  28504 adult/svm/11/shap                        inst 6631     83 s  RSS 0.30 GB (peak 0.30)
  pid  33756 adult/svm/11/anchors                     inst 5558    853 s  RSS 1.27 GB (peak 1.54)
  pid  40188 adult/svm/11/lime_full                   inst 7459     11 s  RSS 0.28 GB (peak 0.28)
  pid  17116 adult/xgb/11/dice                        inst 8072      2 s  RSS 0.44 GB (peak 0.44)
Sync: last push 15 min ago (8df6a6de62), last commit 15 min ago
```
