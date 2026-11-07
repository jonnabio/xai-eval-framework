# Cohort B2 run status

Generated 2026-11-07 00:37:27 Central America Standard Time by `scripts/paper_b_dashboard.py` (no metric values are shown).

```
Paper B rev. 1, cohort B2 - 2026-11-07 00:37:27
Orchestrator: RUNNING (mode quality, workers 5/6, queue 402, admission: RAM available 8.8 GB minus expected peak 3.2 GB < reserve 6.0 GB)
Host: CPU 56%  RAM free 8.8/31.4 GB  disk free 359 GB  AC  3000.0 MHz
pilot   : jobs 175/175  rows 700/700  failed rows 0
quality : jobs 168/575  rows 15414/57500  failed rows 0
timing  : cells 0/115
  pid  40356 connect4/svm/11/shap                     inst 12120    494 s  RSS 0.34 GB (peak 0.36)
  pid  22332 connect4/svm/11/anchors                  inst 10533   1357 s  RSS 1.38 GB (peak 1.53)
  pid  48188 adult/svm/11/shap                        inst 7316    402 s  RSS 0.30 GB (peak 0.30)
  pid   9700 adult/mlp/11/anchors                     inst 2058    502 s  RSS 2.07 GB (peak 2.80)
  pid  49052 spambase/svm/11/dice                     inst 454      7 s  RSS 0.27 GB (peak 0.27)
Sync: last push 15 min ago (1e7e708a82), last commit 15 min ago
```
