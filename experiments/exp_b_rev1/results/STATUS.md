# Cohort B2 run status

Generated 2026-11-06 19:10:22 Central America Standard Time by `scripts/paper_b_dashboard.py` (no metric values are shown).

```
Paper B rev. 1, cohort B2 - 2026-11-06 19:10:22
  !! Throttling suspected: the micro-benchmark is 1.43x its first value (heat or power plan).
Orchestrator: RUNNING (mode quality, workers 4/4, queue 558, admission: 4 workers running (max 4))
Host: CPU 57%  RAM free 8.9/31.4 GB  disk free 359 GB  AC  3000.0 MHz
pilot   : jobs 175/175  rows 700/700  failed rows 0
quality : jobs 13/575  rows 1325/57500  failed rows 0
timing  : cells 0/115
  pid  39868 phishing/svm/11/dice                     inst 2022      2 s  RSS 0.27 GB (peak 0.27)
  pid  26092 phishing/xgb/11/anchors                  inst 2182     52 s  RSS 0.96 GB (peak 1.19)
  pid  12608 german_credit/rf/11/anchors              inst 189     14 s  RSS 0.82 GB (peak 0.86)
  pid  35028 spambase/logreg/11/anchors               inst 143     13 s  RSS 0.50 GB (peak 0.52)
Sync: last push 15 min ago (0fe3dc9ce4), last commit 15 min ago
```
