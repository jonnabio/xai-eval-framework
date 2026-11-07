# Cohort B2 run status

Generated 2026-11-07 09:29:04 Central America Standard Time by `scripts/paper_b_dashboard.py` (no metric values are shown).

```
Paper B rev. 1, cohort B2 - 2026-11-07 09:29:04
Orchestrator: RUNNING (mode quality, workers 6/6, queue 200, admission: 6 workers running (max 6))
Host: CPU 71%  RAM free 9.1/31.4 GB  disk free 359 GB  AC  3000.0 MHz
pilot   : jobs 175/175  rows 700/700  failed rows 0
quality : jobs 369/575  rows 33776/57500  failed rows 1
timing  : cells 0/115
  pid  30040 connect4/svm/22/anchors                  inst 4630     10 s  RSS 1.03 GB (peak 1.91)
  pid  30684 adult/svm/22/shap                        inst 4511    154 s  RSS 0.30 GB (peak 0.31)
  pid  35004 connect4/mlp/33/anchors                  inst 1536     82 s  RSS 1.81 GB (peak 2.57)
  pid  23000 phishing/svm/33/shap                     inst 495     63 s  RSS 0.26 GB (peak 0.26)
  pid  25244 breast_cancer/svm/33/anchors             inst 12     28 s  RSS 0.62 GB (peak 0.62)
  pid  43748 german_credit/svm/33/shap                inst 112      8 s  RSS 0.25 GB (peak 0.25)
Sync: last push 15 min ago (674512719a), last commit 15 min ago
```
