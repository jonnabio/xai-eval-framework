# Cohort B2 run status

Generated 2026-11-07 03:09:21 Central America Standard Time by `scripts/paper_b_dashboard.py` (no metric values are shown).

```
Paper B rev. 1, cohort B2 - 2026-11-07 03:09:21
  !! Throttling suspected: the micro-benchmark is 1.21x its first value (heat or power plan).
Orchestrator: RUNNING (mode quality, workers 6/6, queue 348, admission: 6 workers running (max 6))
Host: CPU 64%  RAM free 7.9/31.4 GB  disk free 359 GB  AC  3000.0 MHz
pilot   : jobs 175/175  rows 700/700  failed rows 0
quality : jobs 221/575  rows 20264/57500  failed rows 0
timing  : cells 0/115
  pid  22332 connect4/svm/11/anchors                  inst 12120    796 s  RSS 1.75 GB (peak 2.47)
  pid  14416 connect4/svm/22/shap                     inst 94     24 s  RSS 0.34 GB (peak 0.34)
  pid  36656 phishing/svm/22/anchors                  inst 771    220 s  RSS 0.94 GB (peak 1.24)
  pid  21488 phishing/mlp/22/anchors                  inst 1142     67 s  RSS 1.25 GB (peak 1.72)
  pid  49008 breast_cancer/svm/22/anchors             inst 55     43 s  RSS 0.54 GB (peak 0.61)
  pid  27732 german_credit/xgb/22/anchors             inst None      9 s  RSS 0.34 GB (peak 0.34)
Sync: last push 15 min ago (66609ca7dc), last commit 15 min ago
```
