# Cohort B2 run status

Generated 2026-11-07 12:16:25 Central America Standard Time by `scripts/paper_b_dashboard.py` (no metric values are shown).

```
Paper B rev. 1, cohort B2 - 2026-11-07 12:16:25
Orchestrator: RUNNING (mode quality, workers 6/6, queue 109, admission: 6 workers running (max 6))
Host: CPU 64%  RAM free 9.4/31.4 GB  disk free 359 GB  AC  3000.0 MHz
pilot   : jobs 175/175  rows 700/700  failed rows 0
quality : jobs 460/575  rows 41826/57500  failed rows 1
timing  : cells 0/115
  pid  33456 german_credit/svm/33/anchors             inst 48    146 s  RSS 0.99 GB (peak 1.23)
  pid  49144 german_credit/rf/33/anchors              inst 45    227 s  RSS 1.84 GB (peak 2.30)
  pid  29884 spambase/svm/33/shap                     inst 460     49 s  RSS 0.25 GB (peak 0.25)
  pid  18180 adult/svm/33/dice                        inst 5233     46 s  RSS 0.33 GB (peak 0.37)
  pid  10516 adult/rf/33/anchors                      inst 8816    120 s  RSS 0.95 GB (peak 1.37)
  pid   2696 adult/svm/33/shap                        inst 4189    214 s  RSS 0.30 GB (peak 0.30)
Sync: last push 15 min ago (121383769f), last commit 15 min ago
```
