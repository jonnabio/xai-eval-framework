# Cohort B2 run status

Generated 2026-11-07 05:10:55 Central America Standard Time by `scripts/paper_b_dashboard.py` (no metric values are shown).

```
Paper B rev. 1, cohort B2 - 2026-11-07 05:10:55
  !! Throttling suspected: the micro-benchmark is 1.15x its first value (heat or power plan).
Orchestrator: RUNNING (mode quality, workers 6/6, queue 301, admission: 6 workers running (max 6))
Host: CPU 67%  RAM free 8.7/31.4 GB  disk free 359 GB  AC  3000.0 MHz
pilot   : jobs 175/175  rows 700/700  failed rows 0
quality : jobs 268/575  rows 24512/57500  failed rows 0
timing  : cells 0/115
  pid  14416 connect4/svm/22/shap                     inst 8985     36 s  RSS 0.34 GB (peak 0.34)
  pid  29420 adult/svm/22/anchors                     inst 4511    459 s  RSS 1.27 GB (peak 1.81)
  pid  17848 german_credit/rf/22/anchors              inst 36      7 s  RSS 1.25 GB (peak 2.13)
  pid  31016 connect4/svm/22/anchors                  inst 5500    139 s  RSS 0.83 GB (peak 1.14)
  pid  31416 connect4/rf/22/dice                      inst 13083     13 s  RSS 0.38 GB (peak 0.38)
  pid  31968 diabetes/mlp/22/dice                     inst 126      1 s  RSS 0.24 GB (peak 0.24)
Sync: last push 15 min ago (f374691ade), last commit 15 min ago
```
