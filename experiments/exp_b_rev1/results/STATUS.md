# Cohort B2 run status

Generated 2026-11-07 18:52:17 Central America Standard Time by `scripts/paper_b_dashboard.py` (no metric values are shown).

```
Paper B rev. 1, cohort B2 - 2026-11-07 18:52:17
Orchestrator: RUNNING (mode quality, workers 6/6, queue 5, admission: 6 workers running (max 6))
Host: CPU 66%  RAM free 5.7/31.4 GB  disk free 359 GB  AC  3000.0 MHz
pilot   : jobs 175/175  rows 700/700  failed rows 0
quality : jobs 564/575  rows 51972/57500  failed rows 4
timing  : cells 0/115
  pid  26720 connect4/svm/33/anchors                  inst 674   1003 s  RSS 1.54 GB (peak 2.00)
  pid  28268 adult/svm/55/shap                        inst 2461    380 s  RSS 0.30 GB (peak 0.30)
  pid  28632 adult/svm/44/anchors                     inst 4410     33 s  RSS 1.11 GB (peak 1.58)
  pid  28160 connect4/rf/33/anchors                   inst 4309    511 s  RSS 1.52 GB (peak 1.84)
  pid  35988 adult/rf/44/anchors                      inst 890      5 s  RSS 0.92 GB (peak 1.78)
  pid  46256 adult/mlp/44/anchors                     inst 3780      1 s  RSS 1.16 GB (peak 2.70)
Sync: last push 15 min ago (70dcc517ae), last commit 15 min ago
```
