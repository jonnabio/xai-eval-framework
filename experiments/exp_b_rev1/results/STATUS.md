# Cohort B2 run status

Generated 2026-11-07 15:03:48 Central America Standard Time by `scripts/paper_b_dashboard.py` (no metric values are shown).

```
Paper B rev. 1, cohort B2 - 2026-11-07 15:03:48
Orchestrator: RUNNING (mode quality, workers 6/6, queue 40, admission: 6 workers running (max 6))
Host: CPU 63%  RAM free 8.0/31.4 GB  disk free 359 GB  AC  3000.0 MHz
pilot   : jobs 175/175  rows 700/700  failed rows 0
quality : jobs 529/575  rows 48275/57500  failed rows 1
timing  : cells 0/115
  pid  19312 connect4/svm/33/shap                     inst 9518    467 s  RSS 0.34 GB (peak 0.36)
  pid  24476 adult/svm/33/anchors                     inst 7747     87 s  RSS 1.08 GB (peak 1.70)
  pid  42884 connect4/svm/33/anchors                  inst 5786    534 s  RSS 1.88 GB (peak 1.88)
  pid  24712 adult/svm/44/shap                        inst 5721    320 s  RSS 0.30 GB (peak 0.30)
  pid  13668 adult/logreg/44/dice                     inst 9596     19 s  RSS 0.32 GB (peak 0.32)
  pid  40036 adult/xgb/44/dice                        inst 6502     57 s  RSS 0.44 GB (peak 0.44)
Sync: last push 15 min ago (41ace4d264), last commit 15 min ago
```
