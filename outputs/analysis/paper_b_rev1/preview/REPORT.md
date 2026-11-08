# Paper B revision 1: analysis report (cohort B2)

- Design hash: `4ab8673a4a205aaf70ac514a83a21abb59c9ff951a111a6679a85dfe4d97a1fa`
- Rows: 3,738; cells: 25
- PARTIAL: the run is not finished; numbers will change
- Seed overlap of instances (Jaccard, same dataset and model): mean nan, max nan

## Table 2: primary effects (Adult)

_(no data yet)_

## Friedman / Nemenyi (Adult, cell means; rank 1 = highest)

_(no data yet)_

## Table 4: other datasets (mean and SD over seeds of model-averaged means)

| dataset | explainer | stability_mean | stability_std | fidelity_mean | fidelity_std | faithfulness_gap_mean | faithfulness_gap_std | sparsity_mean | sparsity_std |
|---|---|---|---|---|---|---|---|---|---|
| breast_cancer | anchors | 0.2491 |  | 0.2557 |  | 0.1122 |  | 0.0703 |  |
| breast_cancer | dice | 0.07806 |  | 0.07176 |  | 0.03331 |  | 0.06667 |  |
| breast_cancer | lime | 0.8621 |  | 0.5685 |  | 0.1145 |  | 0.3333 |  |
| breast_cancer | lime_full | 0.9865 |  | 0.6314 |  | 0.2278 |  | 0.9891 |  |
| breast_cancer | shap | 0.8284 |  | 0.6615 |  | 0.272 |  | 0.7336 |  |
| connect4 | anchors | 0.6754 |  | 0.4519 |  | 0.3055 |  | 0.04473 |  |
| connect4 | lime | 0.5699 |  | 0.6797 |  | 0.1996 |  | 0.07929 |  |
| connect4 | lime_full | 0.6549 |  | 0.2379 |  | 0.1685 |  | 0.9815 |  |
| connect4 | shap | 0.6554 |  | 0.7622 |  | 0.388 |  | 0.4618 |  |
| diabetes | anchors | 0.8069 |  | 0.3337 |  | 0.3156 |  | 0.4694 |  |
| diabetes | dice | 0.3538 |  | 0.4078 |  | 0.2116 |  | 0.1908 |  |
| diabetes | lime | 0.9978 |  | 0.5349 |  | 0.253 |  | 1 |  |
| diabetes | lime_full | 0.9961 |  | 0.3953 |  | 0.246 |  | 1 |  |
| diabetes | shap | 0.9112 |  | 0.7621 |  | 0.3426 |  | 0.9987 |  |
| german_credit | anchors | 0.7107 |  | 0.3634 |  | 0.1199 |  | 0.1329 |  |
| german_credit | dice | 0.1899 |  | 0.1823 |  | 0.1439 |  | 0.0231 |  |
| german_credit | lime | 0.9097 |  | 0.4019 |  | 0.1357 |  | 0.1639 |  |
| german_credit | lime_full | 0.9805 |  | 0.5738 |  | 0.1519 |  | 0.9957 |  |
| german_credit | shap | 0.8726 |  | 0.758 |  | 0.3337 |  | 0.5371 |  |
| phishing | anchors | 0.8928 |  | 0.3269 |  | 0.3179 |  | 0.05235 |  |
| phishing | dice | 0.3568 |  | 0.3567 |  | 0.1147 |  | 0.07029 |  |
| phishing | lime | 0.9037 |  | 0.6337 |  | 0.3629 |  | 0.1471 |  |
| phishing | shap | 0.8288 |  | 0.8621 |  | 0.4144 |  | 0.1471 |  |
| spambase | anchors | 0.386 |  | 0.3477 |  | 0.2063 |  | 0.05912 |  |
| spambase | dice | 0.1947 |  | 0.3226 |  | 0.301 |  | 0.0615 |  |
| spambase | lime | 0.8482 |  | 0.5935 |  | 0.2295 |  | 0.1719 |  |
| spambase | lime_full | 0.9656 |  | 0.3898 |  | 0.2279 |  | 0.9925 |  |

## Quality checks

| dataset | explainer | rows | all_zero_share | fidelity_exact_zero_share | stability_rows | stability_zero_vectors_mean |
|---|---|---|---|---|---|---|
| adult | dice | 100 | 0 | 0 | 12 | 0 |
| adult | shap | 188 | 0 | 0.005319 | 24 | 0 |
| breast_cancer | anchors | 55 | 0 | 0 | 11 | 0 |
| breast_cancer | dice | 2 | 0 | 0 | 2 | 0 |
| breast_cancer | lime | 54 | 0 | 0.1296 | 10 | 0 |
| breast_cancer | lime_full | 55 | 0 | 0 | 11 | 0 |
| breast_cancer | shap | 165 | 0 | 0.04242 | 32 | 0 |
| connect4 | anchors | 77 | 0 | 0 | 11 | 0 |
| connect4 | lime | 100 | 0 | 0 | 12 | 0 |
| connect4 | lime_full | 100 | 0 | 0 | 12 | 0 |
| connect4 | shap | 300 | 0 | 0.006667 | 36 | 0 |
| diabetes | anchors | 182 | 0 | 0.005495 | 25 | 0 |
| diabetes | dice | 181 | 0 | 0 | 24 | 0 |
| diabetes | lime | 181 | 0 | 0 | 24 | 0 |
| diabetes | lime_full | 88 | 0 | 0 | 12 | 0 |
| diabetes | shap | 180 | 0 | 0 | 24 | 0 |
| german_credit | anchors | 181 | 0 | 0 | 24 | 0 |
| german_credit | dice | 89 | 0 | 0 | 13 | 0 |
| german_credit | lime | 93 | 0 | 0 | 12 | 0 |
| german_credit | lime_full | 88 | 0 | 0 | 12 | 0 |
| german_credit | shap | 193 | 0 | 0 | 24 | 0 |
| phishing | anchors | 100 | 0 | 0 | 12 | 0 |
| phishing | dice | 100 | 0 | 0 | 12 | 0 |
| phishing | lime | 200 | 0 | 0 | 24 | 0 |
| phishing | shap | 200 | 0 | 0 | 24 | 0 |
| spambase | anchors | 100 | 0 | 0 | 12 | 0 |
| spambase | dice | 93 | 0 | 0 | 12 | 0 |
| spambase | lime | 93 | 0 | 0 | 12 | 0 |
| spambase | lime_full | 200 | 0 | 0.04 | 24 | 0 |

## Table 3: cost

_(no data yet)_
