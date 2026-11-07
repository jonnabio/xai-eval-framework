# Cohort B2 run status

Generated 2026-11-06 21:50:31 Central America Standard Time by `scripts/paper_b_dashboard.py` (no metric values are shown).

```
Paper B rev. 1, cohort B2 - 2026-11-06 21:50:31
Orchestrator: RUNNING (mode quality, workers 5/6, queue 456, admission: RAM available 7.8 GB minus expected peak 3.4 GB < reserve 6.0 GB)
Host: CPU 60%  RAM free 7.8/31.4 GB  disk free 359 GB  AC  3000.0 MHz
pilot   : jobs 175/175  rows 700/700  failed rows 0
quality : jobs 114/575  rows 10329/57500  failed rows 0
timing  : cells 0/115
  pid  18748 adult/svm/11/anchors                     inst 7050     79 s  RSS 1.22 GB (peak 1.87)
  pid  36276 connect4/mlp/11/anchors                  inst 5345    582 s  RSS 2.27 GB (peak 3.05)
  pid  40356 connect4/svm/11/shap                     inst 163    564 s  RSS 0.34 GB (peak 0.34)
  pid  20440 spambase/rf/11/anchors                   inst 829     83 s  RSS 0.58 GB (peak 0.68)
  pid  16236 adult/xgb/11/anchors                     inst 6358      5 s  RSS 1.21 GB (peak 2.12)
Sync: last push 15 min ago (4137cfdddf), last commit 15 min ago
```
