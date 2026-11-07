# Cohort B2 run status

Generated 2026-11-07 14:48:33 Central America Standard Time by `scripts/paper_b_dashboard.py` (no metric values are shown).

```
Paper B rev. 1, cohort B2 - 2026-11-07 14:48:33
  !! Throttling suspected: the micro-benchmark is 1.27x its first value (heat or power plan).
Orchestrator: RUNNING (mode quality, workers 6/6, queue 47, admission: 6 workers running (max 6))
Host: CPU 70%  RAM free 9.2/31.4 GB  disk free 359 GB  AC  3000.0 MHz
pilot   : jobs 175/175  rows 700/700  failed rows 0
quality : jobs 522/575  rows 47657/57500  failed rows 1
timing  : cells 0/115
  pid  28088 adult/svm/33/shap                        inst 3938      4 s  RSS 0.30 GB (peak 0.30)
  pid  19312 connect4/svm/33/shap                     inst 2439    489 s  RSS 0.34 GB (peak 0.36)
  pid  24476 adult/svm/33/anchors                     inst 1170     44 s  RSS 1.10 GB (peak 1.70)
  pid  42884 connect4/svm/33/anchors                  inst 3708     37 s  RSS 0.87 GB (peak 1.16)
  pid  44296 adult/svm/44/dice                        inst 27      2 s  RSS 0.33 GB (peak 0.36)
  pid  24712 adult/svm/44/shap                        inst 8324    624 s  RSS 0.30 GB (peak 0.30)
Sync: last push 15 min ago (e78aff45e6), last commit 15 min ago
```
