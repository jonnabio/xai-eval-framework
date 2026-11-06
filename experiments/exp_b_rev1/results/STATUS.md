# Cohort B2 run status

Generated 2026-11-06 15:23:23 Central America Standard Time by `scripts/paper_b_dashboard.py` (no metric values are shown).

```
Paper B rev. 1, cohort B2 - 2026-11-06 15:23:23
  !! Throttling suspected: the micro-benchmark is 1.56x its first value (heat or power plan).
Orchestrator: RUNNING (mode pilot, workers 4/4, queue 17, admission: 4 workers running (max 4))
Host: CPU 62%  RAM free 7.6/31.4 GB  disk free 359 GB  AC  3000.0 MHz
pilot   : jobs 154/175  rows 619/700  failed rows 0
quality : jobs 0/575  rows 0/57500  failed rows 0
timing  : cells 0/115
  pid   4152 connect4/svm/11/shap                     inst 5432   3127 s  RSS 0.43 GB (peak 0.48)
  pid  10976 connect4/svm/11/anchors                  inst 9079    989 s  RSS 1.07 GB (peak 1.39)
  pid  35816 adult/svm/11/shap                        inst 5558   1175 s  RSS 0.38 GB (peak 0.38)
  pid  40160 adult/mlp/11/anchors                     inst 5563    447 s  RSS 2.41 GB (peak 2.84)
Sync: last push 15 min ago (dbcea8c444), last commit 15 min ago
```
