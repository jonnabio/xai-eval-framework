# Paper B revision 1: analysis report (cohort B2)

- Design hash: `9dc6c861fc84c0b8f536f45fde6e6f3985776f20d9c17c868cf0160bb8d8764e`
- Rows: 900; cells: 15
- Complete cells only
- Seed overlap of instances (Jaccard, same dataset and model): mean 0.006, max 0.043

## Table 2: primary effects (Adult)

| endpoint | contrast | confirmatory | n_cells | mean_shap | mean_x | estimate | ci_lo | ci_hi | boot_lo | boot_hi | p_holm | d_z | hl | r_rb | cells_positive | method |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| stability | shap-lime_full | True | 15 | 0.7994 | 0.8974 | -0.09793 | -0.1825 | -0.01332 | -0.1185 | -0.07467 | 0.06988 | -2.632 | -0.09421 | -1 | 0 | mixedlm |
| stability | shap-anchors | True | 15 | 0.7994 | 0.543 | 0.2565 | 0.2103 | 0.3026 | 0.2087 | 0.2866 | 1.1e-26 | 4.025 | 0.2648 | 1 | 15 | mixedlm |
| stability | shap-dice | True | 15 | 0.7994 | 0.3653 | 0.4342 | 0.2369 | 0.6314 | 0.3682 | 0.4899 | 8.02e-05 | 5.146 | 0.4381 | 1 | 15 | mixedlm |
| stability | shap-lime | False | 15 | 0.7994 | 0.8441 | -0.04468 | -0.1338 | 0.04445 | -0.07379 | -0.01514 |  | -0.9639 | -0.04505 | -0.85 | 2 | mixedlm |
| fidelity | shap-lime_full | True | 15 | 0.8246 | 0.4383 | 0.3863 | 0.2531 | 0.5195 | 0.2653 | 0.4779 | 7.968e-08 | 2.711 | 0.3989 | 1 | 15 | mixedlm |
| fidelity | shap-anchors | True | 15 | 0.8246 | 0.408 | 0.4166 | 0.3192 | 0.5141 | 0.3862 | 0.4426 | 3.732e-16 | 7.233 | 0.4226 | 1 | 15 | mixedlm |
| fidelity | shap-dice | True | 15 | 0.8246 | 0.1981 | 0.6265 | 0.4903 | 0.7627 | 0.5006 | 0.7248 | 1.543e-18 | 4.122 | 0.6361 | 1 | 15 | mixedlm |
| fidelity | shap-lime | False | 15 | 0.8246 | 0.5156 | 0.309 | 0.194 | 0.424 | 0.2079 | 0.3989 |  | 2.28 | 0.3297 | 1 | 15 | mixedlm |
| faithfulness_gap | shap-lime_full | True | 15 | 0.3905 | 0.2521 | 0.1385 | 0.01119 | 0.2658 | 0.04421 | 0.2633 | 0.06988 | 0.9436 | 0.1072 | 0.9 | 12 | mixedlm |
| faithfulness_gap | shap-anchors | True | 15 | 0.3905 | 0.2251 | 0.1654 | 0.02143 | 0.3095 | 0.1076 | 0.2305 | 0.06988 | 1.991 | 0.1662 | 1 | 15 | mixedlm |
| faithfulness_gap | shap-dice | True | 15 | 0.3905 | 0.07172 | 0.3188 | 0.1585 | 0.4791 | 0.2621 | 0.4158 | 0.000388 | 2.856 | 0.2914 | 1 | 15 | mixedlm |
| faithfulness_gap | shap-lime | False | 15 | 0.3905 | 0.2969 | 0.09365 | -0.01306 | 0.2004 | 0.03351 | 0.1539 |  | 1.188 | 0.08565 | 0.9 | 12 | mixedlm |
| sparsity | shap-lime_full | False | 15 | 0.2166 | 0.9807 | -0.764 | -0.921 | -0.6071 | -0.8946 | -0.6155 |  | -4.567 | -0.7645 | -1 | 0 | mixedlm |
| sparsity | shap-anchors | False | 15 | 0.2166 | 0.06363 | 0.153 | 0.00308 | 0.3029 | 0.01096 | 0.3094 |  | 0.8601 | 0.1759 | 0.75 | 12 | mixedlm |
| sparsity | shap-dice | False | 15 | 0.2166 | 0.0159 | 0.2007 | 0.06547 | 0.336 | 0.07634 | 0.3419 |  | 1.255 | 0.2103 | 1 | 15 | mixedlm |
| sparsity | shap-lime | False | 15 | 0.2166 | 0.09192 | 0.1247 | -0.01144 | 0.2608 | 0.0006173 | 0.2657 |  | 0.7819 | 0.1337 | 1 | 8 | mixedlm |

## Friedman / Nemenyi (Adult, cell means; rank 1 = highest)

| endpoint | n_cells | chi2 | p | cd_nemenyi | rank_shap | rank_lime_full | rank_anchors | rank_dice |
|---|---|---|---|---|---|---|---|---|
| stability | 15 | 43.88 | 1.6e-09 | 1.211 | 2 | 1 | 3.067 | 3.933 |
| fidelity | 15 | 39.48 | 1.373e-08 | 1.211 | 1 | 2.333 | 2.733 | 3.933 |
| faithfulness_gap | 15 | 36.36 | 6.284e-08 | 1.211 | 1.2 | 2.2 | 2.6 | 4 |

## Table 4: other datasets (mean and SD over seeds of model-averaged means)

_(no data yet)_

## Quality checks

| dataset | explainer | rows | all_zero_share | fidelity_exact_zero_share | stability_rows | stability_zero_vectors_mean | stability_zero_vector_share |
|---|---|---|---|---|---|---|---|
| adult | anchors | 180 | 0 | 0 | 180 | 0 | 0 |
| adult | dice | 180 | 0 | 0 | 180 | 0 | 0 |
| adult | lime | 180 | 0.005556 | 0 | 180 | 0.08889 | 0.005926 |
| adult | lime_full | 180 | 0.005556 | 0 | 180 | 0.08889 | 0.005926 |
| adult | shap | 180 | 0 | 0 | 180 | 0 | 0 |

## Table 3: cost

_(no data yet)_
