# Cohort B2 run status

Generated 2026-11-07 01:07:49 Central America Standard Time by `scripts/paper_b_dashboard.py` (no metric values are shown).

```
Paper B rev. 1, cohort B2 - 2026-11-07 01:07:49
  !! Throttling suspected: the micro-benchmark is 1.24x its first value (heat or power plan).
Orchestrator: RUNNING (mode quality, workers 6/6, queue 399, admission: 6 workers running (max 6))
Host: CPU 70%  RAM free 8.0/31.4 GB  disk free 359 GB  AC  3000.0 MHz
pilot   : jobs 175/175  rows 700/700  failed rows 0
quality : jobs 170/575  rows 15724/57500  failed rows 0
timing  : cells 0/115
  pid  40356 connect4/svm/11/shap                     inst 1428    591 s  RSS 0.34 GB (peak 0.36)
  pid  22332 connect4/svm/11/anchors                  inst 8319    940 s  RSS 1.56 GB (peak 1.84)
  pid  48188 adult/svm/11/shap                        inst 9566     25 s  RSS 0.30 GB (peak 0.31)
  pid   9700 adult/mlp/11/anchors                     inst 3353      7 s  RSS 1.73 GB (peak 3.74)
  pid  31456 phishing/svm/11/anchors                  inst 193     13 s  RSS 0.72 GB (peak 1.08)
  pid  48896 connect4/svm/22/lime_full                inst 13240     34 s  RSS 0.31 GB (peak 0.31)
Sync: last push 15 min ago (510f866bea), last commit 15 min ago
```
