# Cohort B2 run status

Generated 2026-11-08 23:48:18 Central America Standard Time by `scripts/paper_b_dashboard.py` (no metric values are shown).

```
Paper B rev. 1, cohort B2 - 2026-11-08 23:48:18
Orchestrator: RUNNING (mode quality, workers 6/6, queue 57, admission: 6 workers running (max 6))
Host: CPU 55%  RAM free 9.2/31.4 GB  disk free 358 GB  AC  3000.0 MHz
pilot   : jobs 0/25  rows 0/100  failed rows 0
quality : jobs 12/75  rows 173/7500  failed rows 0
timing  : cells 0/15
  pid  28840 adult/mlp/11/anchors                     inst 5563    281 s  RSS 2.20 GB (peak 2.84)
  pid  27620 adult/rf/11/anchors                      inst 2527    243 s  RSS 0.91 GB (peak 1.60)
  pid  22876 adult/logreg/11/dice                     inst 1854     19 s  RSS 0.32 GB (peak 0.32)
  pid  22552 adult/rf/11/dice                         inst 2527     12 s  RSS 0.33 GB (peak 0.35)
  pid  28504 adult/svm/11/shap                        inst 5558     34 s  RSS 0.30 GB (peak 0.30)
  pid  37076 adult/rf/11/shap                         inst 8593      1 s  RSS 0.31 GB (peak 0.31)
Sync: last push 15 min ago (fe637cbc7f), last commit 15 min ago
```
