# Cohort B2 run status

Generated 2026-11-06 21:20:08 Central America Standard Time by `scripts/paper_b_dashboard.py` (no metric values are shown).

```
Paper B rev. 1, cohort B2 - 2026-11-06 21:20:08
  !! Throttling suspected: the micro-benchmark is 1.60x its first value (heat or power plan).
Orchestrator: RUNNING (mode quality, workers 6/6, queue 473, admission: 6 workers running (max 6))
Host: CPU 66%  RAM free 8.1/31.4 GB  disk free 359 GB  AC  3000.0 MHz
pilot   : jobs 175/175  rows 700/700  failed rows 0
quality : jobs 96/575  rows 8771/57500  failed rows 0
timing  : cells 0/115
  pid  18748 adult/svm/11/anchors                     inst 3253      6 s  RSS 0.83 GB (peak 1.87)
  pid  36276 connect4/mlp/11/anchors                  inst 11082    192 s  RSS 2.03 GB (peak 2.58)
  pid  40956 breast_cancer/svm/11/anchors             inst 73      9 s  RSS 0.62 GB (peak 0.68)
  pid  29292 breast_cancer/rf/11/dice                 inst 20    216 s  RSS 0.26 GB (peak 0.26)
  pid  25016 german_credit/logreg/11/anchors          inst 162     13 s  RSS 0.78 GB (peak 0.86)
  pid  35524 phishing/xgb/11/dice                     inst 1009     13 s  RSS 0.39 GB (peak 0.39)
Sync: last push 15 min ago (88c4c8915b), last commit 15 min ago
```
