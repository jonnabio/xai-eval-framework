# Cohort B2 run status

Generated 2026-11-07 00:52:38 Central America Standard Time by `scripts/paper_b_dashboard.py` (no metric values are shown).

```
Paper B rev. 1, cohort B2 - 2026-11-07 00:52:38
  !! Throttling suspected: the micro-benchmark is 1.40x its first value (heat or power plan).
Orchestrator: RUNNING (mode quality, workers 6/6, queue 400, admission: 6 workers running (max 6))
Host: CPU 70%  RAM free 8.8/31.4 GB  disk free 359 GB  AC  3000.0 MHz
pilot   : jobs 175/175  rows 700/700  failed rows 0
quality : jobs 169/575  rows 15557/57500  failed rows 0
timing  : cells 0/115
  pid  40356 connect4/svm/11/shap                     inst 6936    544 s  RSS 0.34 GB (peak 0.36)
  pid  22332 connect4/svm/11/anchors                  inst 8319     29 s  RSS 1.21 GB (peak 1.53)
  pid  48188 adult/svm/11/shap                        inst 7213    192 s  RSS 0.30 GB (peak 0.30)
  pid   9700 adult/mlp/11/anchors                     inst 9120      4 s  RSS 1.54 GB (peak 3.74)
  pid  31456 phishing/svm/11/anchors                  inst 539     10 s  RSS 0.79 GB (peak 1.08)
  pid  37904 spambase/svm/11/shap                     inst 713     10 s  RSS 0.25 GB (peak 0.25)
Sync: last push 15 min ago (67e8b778df), last commit 15 min ago
```
