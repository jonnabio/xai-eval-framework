# Cohort B2 run status

Generated 2026-11-06 13:52:27 Central America Standard Time by `scripts/paper_b_dashboard.py` (no metric values are shown).

```
Paper B rev. 1, cohort B2 - 2026-11-06 13:52:27
  !! Throttling suspected: the micro-benchmark is 1.73x its first value (heat or power plan).
Orchestrator: RUNNING (mode pilot, workers 4/4, queue 137, admission: 4 workers running (max 4))
Host: CPU 55%  RAM free 9.1/31.4 GB  disk free 360 GB  AC  3000.0 MHz
pilot   : jobs 34/175  rows 143/700  failed rows 0
quality : jobs 0/575  rows 0/57500  failed rows 0
timing  : cells 0/115
  pid  34604 german_credit/rf/11/anchors              inst 95    265 s  RSS 0.98 GB (peak 1.25)
  pid  45096 breast_cancer/rf/11/anchors              inst 3    106 s  RSS 0.65 GB (peak 0.70)
  pid  33716 phishing/svm/11/shap                     inst 1072     73 s  RSS 0.30 GB (peak 0.30)
  pid  19256 connect4/xgb/11/anchors                  inst 4839      8 s  RSS 1.07 GB (peak 1.07)
Sync: last push 15 min ago (b145bf1366), last commit 15 min ago
```
