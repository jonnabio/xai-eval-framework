# Cohort B2 run status

Generated 2026-11-06 15:08:13 Central America Standard Time by `scripts/paper_b_dashboard.py` (no metric values are shown).

```
Paper B rev. 1, cohort B2 - 2026-11-06 15:08:13
  !! Throttling suspected: the micro-benchmark is 1.43x its first value (heat or power plan).
Orchestrator: RUNNING (mode pilot, workers 4/4, queue 24, admission: 4 workers running (max 4))
Host: CPU 54%  RAM free 9.8/31.4 GB  disk free 359 GB  AC  3000.0 MHz
pilot   : jobs 147/175  rows 590/700  failed rows 0
quality : jobs 0/575  rows 0/57500  failed rows 0
timing  : cells 0/115
  pid   4152 connect4/svm/11/shap                     inst 5432   2218 s  RSS 0.43 GB (peak 0.48)
  pid  10976 connect4/svm/11/anchors                  inst 9079     80 s  RSS 1.06 GB (peak 1.11)
  pid  35816 adult/svm/11/shap                        inst 5558    265 s  RSS 0.38 GB (peak 0.38)
  pid  41216 adult/logreg/11/anchors                  inst 8387      7 s  RSS 0.89 GB (peak 1.58)
Sync: last push 15 min ago (b93e679fb2), last commit 15 min ago
```
