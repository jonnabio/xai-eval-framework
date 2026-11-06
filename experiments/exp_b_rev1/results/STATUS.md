# Cohort B2 run status

Generated 2026-11-06 15:53:42 Central America Standard Time by `scripts/paper_b_dashboard.py` (no metric values are shown).

```
Paper B rev. 1, cohort B2 - 2026-11-06 15:53:42
  !! Throttling suspected: the micro-benchmark is 1.25x its first value (heat or power plan).
Orchestrator: RUNNING (mode pilot, workers 4/4, queue 1, admission: 4 workers running (max 4))
Host: CPU 42%  RAM free 8.3/31.4 GB  disk free 359 GB  AC  3000.0 MHz
pilot   : jobs 170/175  rows 688/700  failed rows 0
quality : jobs 0/575  rows 0/57500  failed rows 0
timing  : cells 0/115
  pid   4152 connect4/svm/11/shap                     inst 9079   1555 s  RSS 0.43 GB (peak 0.48)
  pid  10976 connect4/svm/11/anchors                  inst 12120   1329 s  RSS 1.82 GB (peak 2.47)
  pid  35816 adult/svm/11/shap                        inst 7316    750 s  RSS 0.38 GB (peak 0.38)
  pid  41416 phishing/svm/11/anchors                  inst 1998    127 s  RSS 0.89 GB (peak 1.25)
Sync: last push 15 min ago (76ade4f901), last commit 15 min ago
```
