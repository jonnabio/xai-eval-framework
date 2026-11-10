# Paper B revision 1: analysis report (cohort B2)

- Design hash: `3ec2dfac99d0c8dfda185fc14a711379b905dff961bfe9acbd01e14128c3c7b9`
- Rows: 899; cells: 15
- Complete cells only
- Seed overlap of instances (Jaccard, same dataset and model): mean 0.006, max 0.043

## Table 2: primary effects (Adult)

| endpoint | contrast | confirmatory | n_cells | mean_shap | mean_x | estimate | ci_lo | ci_hi | boot_lo | boot_hi | p_holm | d_z | hl | r_rb | cells_positive | method |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| stability | shap-lime_full | True | 15 | 0.9774 | 0.9038 | 0.07363 | 0.02506 | 0.1222 | 0.03029 | 0.117 | 0.008907 | 1.418 | 0.07161 | 1 | 15 | mixedlm |
| stability | shap-anchors | True | 15 | 0.9774 | 0.7588 | 0.2185 | 0.1492 | 0.2879 | 0.1928 | 0.2468 | 4.651e-09 | 5.638 | 0.217 | 1 | 15 | mixedlm |
| stability | shap-dice | True | 15 | 0.9774 | 0.3789 | 0.5985 | 0.3951 | 0.8019 | 0.5254 | 0.691 | 4.843e-08 | 5.238 | 0.5978 | 1 | 15 | mixedlm |
| stability | shap-lime | False | 15 | 0.9774 | 0.9432 | 0.03417 | -0.02267 | 0.091 | -0.001068 | 0.09188 |  | 0.5507 | 0.01382 | 0.6667 | 10 | mixedlm |
| fidelity | shap-lime_full | True | 15 | 0.8246 | 0.4383 | 0.3863 | 0.2531 | 0.5195 | 0.2653 | 0.4779 | 6.64e-08 | 2.711 | 0.3989 | 1 | 15 | mixedlm |
| fidelity | shap-anchors | True | 15 | 0.8246 | 0.4087 | 0.4158 | 0.3633 | 0.4682 | 0.3825 | 0.4431 | 2.019e-53 | 6.766 | 0.421 | 1 | 15 | mixedlm |
| fidelity | shap-dice | True | 15 | 0.8246 | 0.1981 | 0.6265 | 0.4903 | 0.7627 | 0.5006 | 0.7248 | 1.543e-18 | 4.122 | 0.6361 | 1 | 15 | mixedlm |
| fidelity | shap-lime | False | 15 | 0.8246 | 0.5156 | 0.309 | 0.194 | 0.424 | 0.2079 | 0.3989 |  | 2.28 | 0.3297 | 1 | 15 | mixedlm |
| faithfulness_gap | shap-lime_full | True | 15 | 0.3905 | 0.2521 | 0.1385 | 0.01119 | 0.2658 | 0.04421 | 0.2633 | 0.03299 | 0.9436 | 0.1072 | 0.9 | 12 | mixedlm |
| faithfulness_gap | shap-anchors | True | 15 | 0.3897 | 0.2288 | 0.1608 | 0.04277 | 0.2788 | 0.09742 | 0.23 | 0.01516 | 1.853 | 0.1578 | 1 | 15 | mixedlm |
| faithfulness_gap | shap-dice | True | 15 | 0.3905 | 0.07172 | 0.3188 | 0.1585 | 0.4791 | 0.2621 | 0.4158 | 0.000388 | 2.856 | 0.2914 | 1 | 15 | mixedlm |
| faithfulness_gap | shap-lime | False | 15 | 0.3905 | 0.2969 | 0.09365 | -0.01306 | 0.2004 | 0.03351 | 0.1539 |  | 1.188 | 0.08565 | 0.9 | 12 | mixedlm |
| sparsity | shap-lime_full | False | 15 | 0.2166 | 0.9807 | -0.764 | -0.921 | -0.6071 | -0.8946 | -0.6155 |  | -4.567 | -0.7645 | -1 | 0 | mixedlm |
| sparsity | shap-anchors | False | 15 | 0.2166 | 0.06351 | 0.1531 | -0.01483 | 0.321 | 0.01092 | 0.3095 |  | 0.8624 | 0.1746 | 0.7667 | 12 | mixedlm |
| sparsity | shap-dice | False | 15 | 0.2166 | 0.0159 | 0.2007 | 0.06547 | 0.336 | 0.07634 | 0.3419 |  | 1.255 | 0.2103 | 1 | 15 | mixedlm |
| sparsity | shap-lime | False | 15 | 0.2166 | 0.09192 | 0.1247 | -0.01144 | 0.2608 | 0.0006173 | 0.2657 |  | 0.7819 | 0.1337 | 1 | 8 | mixedlm |

## Friedman / Nemenyi (Adult, cell means; rank 1 = highest)

| endpoint | n_cells | chi2 | p | cd_nemenyi | rank_shap | rank_lime_full | rank_anchors | rank_dice |
|---|---|---|---|---|---|---|---|---|
| stability | 15 | 45 | 9.253e-10 | 1.211 | 1 | 2 | 3 | 4 |
| fidelity | 15 | 39.48 | 1.373e-08 | 1.211 | 1 | 2.333 | 2.733 | 3.933 |
| faithfulness_gap | 15 | 35.96 | 7.636e-08 | 1.211 | 1.2 | 2.267 | 2.533 | 4 |

## Table 4: other datasets (mean and SD over seeds of model-averaged means)

_(no data yet)_

## Quality checks

| dataset | explainer | rows | all_zero_share | fidelity_exact_zero_share | stability_rows | stability_zero_vectors_mean | stability_zero_vector_share |
|---|---|---|---|---|---|---|---|
| adult | anchors | 179 | 0 | 0 | 179 | 0 | 0 |
| adult | dice | 180 | 0 | 0 | 180 | 0 | 0 |
| adult | lime | 180 | 0.005556 | 0 | 180 | 0.08333 | 0.005556 |
| adult | lime_full | 180 | 0.005556 | 0 | 180 | 0.08333 | 0.005556 |
| adult | shap | 180 | 0 | 0 | 180 | 0 | 0 |

## Table 3: cost

_(no data yet)_
