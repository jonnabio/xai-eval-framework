# Cohort B2 run status

Generated 2026-11-07 08:58:39 Central America Standard Time by `scripts/paper_b_dashboard.py` (no metric values are shown).

```
Paper B rev. 1, cohort B2 - 2026-11-07 08:58:39
Orchestrator: RUNNING (mode quality, workers 6/6, queue 222, admission: 6 workers running (max 6))
Host: CPU 71%  RAM free 7.5/31.4 GB  disk free 359 GB  AC  3000.0 MHz
pilot   : jobs 175/175  rows 700/700  failed rows 0
quality : jobs 347/575  rows 31767/57500  failed rows 1
timing  : cells 0/115
  pid  30040 connect4/svm/22/anchors                  inst 7527    465 s  RSS 1.01 GB (peak 1.91)
  pid  30680 connect4/rf/22/anchors                   inst 3715     51 s  RSS 1.65 GB (peak 3.07)
  pid  30684 adult/svm/22/shap                        inst 5421     26 s  RSS 0.30 GB (peak 0.30)
  pid  47344 spambase/xgb/22/dice                     inst 433     24 s  RSS 0.38 GB (peak 0.38)
  pid  35004 connect4/mlp/33/anchors                  inst 6348    126 s  RSS 2.21 GB (peak 2.32)
  pid  49532 breast_cancer/logreg/33/dice             inst 105     44 s  RSS 0.26 GB (peak 0.26)
Sync: last push 15 min ago (7dafe48aba), last commit 15 min ago
```
