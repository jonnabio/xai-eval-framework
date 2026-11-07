# Cohort B2 run status

Generated 2026-11-06 20:10:56 Central America Standard Time by `scripts/paper_b_dashboard.py` (no metric values are shown).

```
Paper B rev. 1, cohort B2 - 2026-11-06 20:10:56
  !! Throttling suspected: the micro-benchmark is 1.25x its first value (heat or power plan).
Orchestrator: RUNNING (mode quality, workers 6/6, queue 527, admission: 6 workers running (max 6))
Host: CPU 76%  RAM free 7.3/31.4 GB  disk free 359 GB  AC  3000.0 MHz
pilot   : jobs 175/175  rows 700/700  failed rows 0
quality : jobs 42/575  rows 3995/57500  failed rows 0
timing  : cells 0/115
  pid  39372 connect4/xgb/11/anchors                  inst 4730    290 s  RSS 1.74 GB (peak 2.73)
  pid  41052 breast_cancer/svm/11/dice                inst 16     28 s  RSS 0.26 GB (peak 0.26)
  pid  10152 adult/logreg/11/dice                     inst 8387     33 s  RSS 0.32 GB (peak 0.32)
  pid  47728 german_credit/mlp/11/dice                inst 101      1 s  RSS 0.26 GB (peak 0.26)
  pid  18748 adult/svm/11/anchors                     inst 5558    130 s  RSS 0.74 GB (peak 0.74)
  pid  24180 phishing/logreg/11/dice                  inst 538      3 s  RSS 0.27 GB (peak 0.27)
Sync: last push 15 min ago (4ce6590a8b), last commit 15 min ago
```
