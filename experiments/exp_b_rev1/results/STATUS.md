# Cohort B2 run status

Generated 2026-11-06 20:56:24 Central America Standard Time by `scripts/paper_b_dashboard.py` (no metric values are shown).

```
Paper B rev. 1, cohort B2 - 2026-11-06 20:56:24
  !! Throttling suspected: the micro-benchmark is 1.65x its first value (heat or power plan).
Orchestrator: RUNNING (mode quality, workers 6/6, queue 496, admission: 6 workers running (max 6))
Host: CPU 75%  RAM free 8.9/31.4 GB  disk free 359 GB  AC  3000.0 MHz
pilot   : jobs 175/175  rows 700/700  failed rows 0
quality : jobs 73/575  rows 6805/57500  failed rows 0
timing  : cells 0/115
  pid  18748 adult/svm/11/anchors                     inst 6631    736 s  RSS 1.16 GB (peak 1.87)
  pid  33280 connect4/logreg/11/anchors               inst 6766     66 s  RSS 1.15 GB (peak 2.04)
  pid  17976 phishing/mlp/11/anchors                  inst 1110     97 s  RSS 1.03 GB (peak 1.17)
  pid  50124 connect4/rf/11/dice                      inst 3972     28 s  RSS 0.39 GB (peak 0.39)
  pid  27440 connect4/xgb/11/dice                     inst 5755      7 s  RSS 0.47 GB (peak 0.47)
  pid  25896 connect4/svm/11/lime                     inst 163     28 s  RSS 0.31 GB (peak 0.31)
Sync: last push 15 min ago (9152d989b2), last commit 15 min ago
```
