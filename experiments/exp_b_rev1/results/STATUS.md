# Cohort B2 run status

Generated 2026-11-06 20:41:15 Central America Standard Time by `scripts/paper_b_dashboard.py` (no metric values are shown).

```
Paper B rev. 1, cohort B2 - 2026-11-06 20:41:15
  !! Throttling suspected: the micro-benchmark is 1.60x its first value (heat or power plan).
Orchestrator: RUNNING (mode quality, workers 6/6, queue 503, admission: 6 workers running (max 6))
Host: CPU 66%  RAM free 8.2/31.4 GB  disk free 359 GB  AC  3000.0 MHz
pilot   : jobs 175/175  rows 700/700  failed rows 0
quality : jobs 66/575  rows 6090/57500  failed rows 0
timing  : cells 0/115
  pid  18748 adult/svm/11/anchors                     inst 4714    803 s  RSS 1.35 GB (peak 1.87)
  pid  47004 breast_cancer/xgb/11/anchors             inst 96     64 s  RSS 0.73 GB (peak 0.82)
  pid  26760 diabetes/svm/11/dice                     inst 134     23 s  RSS 0.26 GB (peak 0.26)
  pid  33280 connect4/logreg/11/anchors               inst 2277     10 s  RSS 1.06 GB (peak 1.15)
  pid  40132 adult/xgb/11/dice                        inst 8065     20 s  RSS 0.44 GB (peak 0.44)
  pid  39372 spambase/xgb/11/anchors                  inst 642      4 s  RSS 0.67 GB (peak 0.75)
Sync: last push 15 min ago (fe5cefcac1), last commit 15 min ago
```
