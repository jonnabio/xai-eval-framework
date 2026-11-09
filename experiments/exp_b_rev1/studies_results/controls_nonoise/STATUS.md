# Cohort B2 run status

Generated 2026-11-09 01:34:18 Central America Standard Time by `scripts/paper_b_dashboard.py` (no metric values are shown).

```
Paper B rev. 1, cohort B2 - 2026-11-09 01:34:18
Orchestrator: RUNNING (mode quality, workers 6/6, queue 17, admission: 6 workers running (max 6))
Host: CPU 54%  RAM free 8.4/31.4 GB  disk free 358 GB  AC  3000.0 MHz
pilot   : jobs 0/25  rows 0/100  failed rows 0
quality : jobs 52/75  rows 653/7500  failed rows 0
timing  : cells 0/15
  pid  33756 adult/svm/11/anchors                     inst 5367     36 s  RSS 0.95 GB (peak 1.81)
  pid  30624 adult/svm/22/shap                        inst 2170    275 s  RSS 0.30 GB (peak 0.30)
  pid  14024 adult/mlp/22/anchors                     inst 1867    815 s  RSS 2.61 GB (peak 3.26)
  pid  46892 adult/svm/22/dice                        inst 3082     60 s  RSS 0.33 GB (peak 0.33)
  pid  19724 adult/logreg/22/dice                     inst 7118     23 s  RSS 0.32 GB (peak 0.32)
  pid  14248 adult/mlp/33/dice                        inst 7655      2 s  RSS 0.32 GB (peak 0.32)
Sync: last push 15 min ago (58b21f6c20), last commit 15 min ago
```
