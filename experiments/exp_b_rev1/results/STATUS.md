# Cohort B2 run status

Generated 2026-11-07 19:07:31 Central America Standard Time by `scripts/paper_b_dashboard.py` (no metric values are shown).

```
Paper B rev. 1, cohort B2 - 2026-11-07 19:07:31
Orchestrator: RUNNING (mode quality, workers 6/6, queue 5, admission: 6 workers running (max 6))
Host: CPU 75%  RAM free 6.8/31.4 GB  disk free 359 GB  AC  3000.0 MHz
pilot   : jobs 175/175  rows 700/700  failed rows 0
quality : jobs 564/575  rows 52055/57500  failed rows 4
timing  : cells 0/115
  pid  26720 connect4/svm/33/anchors                  inst 674   1916 s  RSS 1.87 GB (peak 2.14)
  pid  28268 adult/svm/55/shap                        inst 1794     23 s  RSS 0.30 GB (peak 0.30)
  pid  28632 adult/svm/44/anchors                     inst 2917      8 s  RSS 0.80 GB (peak 2.00)
  pid  28160 connect4/rf/33/anchors                   inst 10002    400 s  RSS 2.01 GB (peak 2.07)
  pid  35988 adult/rf/44/anchors                      inst 3958      3 s  RSS 1.13 GB (peak 2.85)
  pid  46256 adult/mlp/44/anchors                     inst 519    383 s  RSS 1.33 GB (peak 2.90)
Sync: last push 15 min ago (044992028d), last commit 15 min ago
```
