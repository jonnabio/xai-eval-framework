# Cohort B2 run status

Generated 2026-11-07 01:23:00 Central America Standard Time by `scripts/paper_b_dashboard.py` (no metric values are shown).

```
Paper B rev. 1, cohort B2 - 2026-11-07 01:23:00
  !! Throttling suspected: the micro-benchmark is 1.51x its first value (heat or power plan).
Orchestrator: RUNNING (mode quality, workers 6/6, queue 395, admission: 6 workers running (max 6))
Host: CPU 68%  RAM free 9.6/31.4 GB  disk free 359 GB  AC  3000.0 MHz
pilot   : jobs 175/175  rows 700/700  failed rows 0
quality : jobs 174/575  rows 16104/57500  failed rows 0
timing  : cells 0/115
  pid  40356 connect4/svm/11/shap                     inst 7953     31 s  RSS 0.34 GB (peak 0.36)
  pid  22332 connect4/svm/11/anchors                  inst 8319   1852 s  RSS 1.41 GB (peak 1.86)
  pid  48188 adult/svm/11/shap                        inst 2569     71 s  RSS 0.30 GB (peak 0.31)
  pid  31456 phishing/svm/11/anchors                  inst 2106    223 s  RSS 0.89 GB (peak 1.36)
  pid  26756 adult/rf/22/dice                         inst 7971      1 s  RSS 0.33 GB (peak 0.34)
  pid  28380 breast_cancer/mlp/22/dice                inst 4      9 s  RSS 0.26 GB (peak 0.26)
Sync: last push 15 min ago (5785fce15c), last commit 15 min ago
```
