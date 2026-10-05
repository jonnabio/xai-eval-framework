# Human-rated subset

Plan: `../PLAN.md`, sections 6, 14.3 and 15.5.

The sheets show the record of the **clean condition**: dataset, model family, explainer,
prediction and the explanation. They show no technical metrics, no outcome of the
prediction and no true label. They were rebuilt on 2026-10-04, before any sheet was sent;
the sample of 56 cases did not change.

| File | What it is |
|---|---|
| `sample_cases.csv` | The 56 cases: 7 from each of the 8 dataset-by-explainer cells of the 192-case EXP4 inventory, drawn with seed 20261004 |
| `rating_sheet_rater_A.html`, `rating_sheet_rater_B.html` | One self-contained sheet per rater, with the cases in a different order. Opens in any browser, needs no connection |
| `ratings/` | Where the returned files `ratings_rater_A.json` and `ratings_rater_B.json` go (not yet received) |

Regenerate the sample and the sheets with
`python docs/reports/paper_c/scripts/draw_human_sample.py`. The output is the same on every
run. Do not regenerate after a sheet has been sent.

## What to send each rater

Send one sheet to each rater, with this text:

> Open the attached file in a browser (Chrome, Edge or Firefox). It shows 56 explanations of
> predictions made by machine-learning classifiers. Read the instructions at the top and rate
> each explanation from 1 to 5 on the seven dimensions. Please work alone and do not discuss
> the cases with anyone. Your answers are saved in the browser, so you can stop and continue
> later on the same computer and browser. When all 56 cases are complete, press "Export
> ratings" and send me the downloaded file. It takes about two hours.

## Rules

- A rater sees no judge score and no rating of the other rater.
- Each rater uses one browser on one computer from start to end; the answers are stored
  there until they are exported.
- A returned file is kept as received. Corrections are made in a new file, with the reason.
- Rater names are not stored in this public repository; the files use "A" and "B".
