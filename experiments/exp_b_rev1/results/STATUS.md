# Cohort B2 run status

Generated 2026-11-07 11:30:47 Central America Standard Time by `scripts/paper_b_dashboard.py` (no metric values are shown).

```
Paper B rev. 1, cohort B2 - 2026-11-07 11:30:47
  !! Throttling suspected: the micro-benchmark is 1.35x its first value (heat or power plan).
Orchestrator: RUNNING (mode quality, workers 6/6, queue 138, admission: 6 workers running (max 6))
Host: CPU 70%  RAM free 7.4/31.4 GB  disk free 359 GB  AC  3000.0 MHz
pilot   : jobs 175/175  rows 700/700  failed rows 0
quality : jobs 431/575  rows 39463/57500  failed rows 1
timing  : cells 0/115
  pid  30040 connect4/svm/22/anchors                  inst 2804     12 s  RSS 1.21 GB (peak 2.11)
  pid  34664 connect4/xgb/33/anchors                  inst 1653    294 s  RSS 2.36 GB (peak 2.73)
  pid   3568 spambase/svm/33/anchors                  inst 905     97 s  RSS 0.63 GB (peak 1.56)
  pid  33620 phishing/xgb/33/anchors                  inst 1920     53 s  RSS 1.04 GB (peak 1.17)
  pid  36384 connect4/svm/33/dice                     inst 3589    331 s  RSS 0.36 GB (peak 0.36)
  pid  39388 breast_cancer/mlp/33/anchors             inst 5      1 s  RSS 0.55 GB (peak 0.65)
Sync: last push 15 min ago (28b67d05d3), last commit 15 min ago
```
