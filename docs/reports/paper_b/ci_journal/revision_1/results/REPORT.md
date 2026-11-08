# Paper B revision 1: analysis report (cohort B2)

- Design hash: `4ab8673a4a205aaf70ac514a83a21abb59c9ff951a111a6679a85dfe4d97a1fa`
- Rows: 52,740; cells: 115
- Complete cells only
- Seed overlap of instances (Jaccard, same dataset and model): mean 0.220, max 0.691

## Table 2: primary effects (Adult)

| endpoint | contrast | confirmatory | n_cells | mean_shap | mean_x | estimate | ci_lo | ci_hi | boot_lo | boot_hi | p_holm | d_z | hl | r_rb | cells_positive | method |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| stability | shap-lime_full | True | 25 | 0.7367 | 0.5559 | 0.1808 | -0.009963 | 0.3717 | -0.007574 | 0.3392 | 0.2529 | 0.8889 | 0.184 | 0.7723 | 19 | mixedlm |
| stability | shap-anchors | True | 25 | 0.7366 | 0.634 | 0.1024 | -0.07809 | 0.283 | -0.1077 | 0.2638 | 0.3123 | 0.4475 | 0.1455 | 0.4031 | 19 | mixedlm |
| stability | shap-dice | True | 25 | 0.7367 | 0.3974 | 0.3393 | 0.136 | 0.5426 | 0.1532 | 0.4977 | 0.007976 | 1.629 | 0.3362 | 0.9754 | 24 | mixedlm |
| stability | shap-lime | False | 25 | 0.7367 | 0.3283 | 0.4085 | 0.2467 | 0.5702 | 0.2509 | 0.5368 |  | 2.388 | 0.4206 | 1 | 25 | mixedlm |
| fidelity | shap-lime_full | True | 25 | 0.8308 | 0.4464 | 0.3843 | 0.2245 | 0.5441 | 0.2781 | 0.4701 | 2.184e-05 | 3.287 | 0.4019 | 1 | 25 | mixedlm |
| fidelity | shap-anchors | True | 25 | 0.8307 | 0.4116 | 0.4192 | 0.2534 | 0.5849 | 0.395 | 0.439 | 7.136e-06 | 11.79 | 0.4213 | 1 | 25 | mixedlm |
| fidelity | shap-dice | True | 25 | 0.8308 | 0.182 | 0.6488 | 0.4396 | 0.858 | 0.5437 | 0.7291 | 1.461e-08 | 5.83 | 0.6691 | 1 | 25 | mixedlm |
| fidelity | shap-lime | False | 25 | 0.8308 | 0.5165 | 0.3143 | 0.1528 | 0.4758 | 0.2206 | 0.3986 |  | 2.935 | 0.321 | 1 | 25 | mixedlm |
| faithfulness_gap | shap-lime_full | True | 25 | 0.3955 | 0.2641 | 0.1315 | 0.05141 | 0.2115 | 0.05685 | 0.2208 | 0.007976 | 1.332 | 0.1169 | 1 | 25 | mixedlm |
| faithfulness_gap | shap-anchors | True | 25 | 0.3955 | 0.2346 | 0.1609 | -0.0126 | 0.3344 | 0.1015 | 0.2204 | 0.2529 | 2.192 | 0.1598 | 1 | 25 | mixedlm |
| faithfulness_gap | shap-dice | True | 25 | 0.3955 | 0.08095 | 0.3146 | 0.1273 | 0.5019 | 0.2765 | 0.3809 | 0.007976 | 4.476 | 0.2897 | 1 | 25 | mixedlm |
| faithfulness_gap | shap-lime | False | 25 | 0.3955 | 0.3043 | 0.09122 | -0.03427 | 0.2167 | 0.04225 | 0.143 |  | 1.455 | 0.09033 | 0.9938 | 24 | mixedlm |
| sparsity | shap-lime_full | False | 25 | 0.2151 | 0.9814 | -0.7663 | -0.8761 | -0.6566 | -0.8905 | -0.6238 |  | -4.862 | -0.7586 | -1 | 0 | mixedlm |
| sparsity | shap-anchors | False | 25 | 0.2151 | 0.06383 | 0.1513 | 0.03199 | 0.2705 | 0.01643 | 0.3036 |  | 0.9078 | 0.1721 | 0.8708 | 20 | mixedlm |
| sparsity | shap-dice | False | 25 | 0.2151 | 0.01677 | 0.1983 | -0.1512 | 0.5478 | 0.07669 | 0.335 |  | 1.289 | 0.2101 | 1 | 25 | mixedlm |
| sparsity | shap-lime | False | 25 | 0.2151 | 0.09193 | 0.1232 | -0.03062 | 0.2769 | 0.0006148 | 0.2614 |  | 0.7936 | 0.1343 | 1 | 21 | mixedlm |
| wall_ms | shap-lime_full | True | 25 | 3925 | 169.6 | 3756 | 560.9 | 6950 | -0.3456 | 1.124e+04 | 0.1061 | 0.4916 | 21.83 | 0.7477 | 19 | mixedlm |
| wall_ms | shap-anchors | True | 25 | 3925 | 9283 | -5357 | -7208 | -3507 | -7854 | -2861 | 1.522e-07 | -1.272 | -4887 | -1 | 0 | mixedlm |
| wall_ms | shap-dice | True | 25 | 3925 | 1408 | 2517 | -961.5 | 5995 | -1094 | 9702 | 0.3123 | 0.3433 | -1056 | -0.2923 | 5 | mixedlm |
| wall_ms | shap-lime | False | 25 | 3925 | 167.9 | 3757 | 543.7 | 6971 | 1.42 | 1.125e+04 |  | 0.4918 | 23.55 | 0.7538 | 20 | mixedlm |
| cpu_ms | shap-lime_full | False | 25 | 3895 | 169.9 | 3726 | -3558 | 1.101e+04 | -2.094 | 1.116e+04 |  | 0.4912 | 19.92 | 0.76 | 18 | mixedlm |
| cpu_ms | shap-anchors | False | 25 | 3895 | 9209 | -5314 | -8156 | -2471 | -7789 | -2838 |  | -1.27 | -4853 | -1 | 0 | mixedlm |
| cpu_ms | shap-dice | False | 25 | 3895 | 1399 | 2496 | -414.6 | 5407 | -1088 | 9631 |  | 0.343 | -1051 | -0.2923 | 5 | mixedlm |
| cpu_ms | shap-lime | False | 25 | 3895 | 167.5 | 4002 | -6.755e+08 | 6.755e+08 | -0.625 | 1.116e+04 |  | 0.4916 | 23.44 | 0.7538 | 20 | mixedlm |
| rows | shap-lime_full | False | 25 | 1.5e+04 | 1000 | 1.156e+04 | 1.041e+04 | 1.271e+04 | 4000 | 2.4e+04 |  | 1.12 | 1.15e+04 | 0.6615 | 15 | mixedlm |
| rows | shap-anchors | False | 25 | 1.5e+04 | 3e+04 | -1.5e+04 | -5.527e+04 | 2.526e+04 | -2.977e+04 | -241.9 |  | -0.7407 | -1.334e+04 | -0.781 | 5 | mixedlm |
| rows | shap-dice | False | 25 | 1.5e+04 | 2043 | 1.296e+04 | 7048 | 1.887e+04 | 2930 | 2.298e+04 |  | 1.034 | 1.05e+04 | 0.6615 | 15 | mixedlm |
| rows | shap-lime | False | 25 | 1.5e+04 | 1000 | 1.156e+04 | 1.041e+04 | 1.271e+04 | 4000 | 2.4e+04 |  | 1.12 | 1.15e+04 | 0.6615 | 15 | mixedlm |

## Friedman / Nemenyi (Adult, cell means; rank 1 = highest)

| endpoint | n_cells | chi2 | p | cd_nemenyi | rank_shap | rank_lime_full | rank_anchors | rank_dice |
|---|---|---|---|---|---|---|---|---|
| stability | 25 | 42.46 | 3.211e-09 | 0.9381 | 1.52 | 2.8 | 1.96 | 3.72 |
| fidelity | 25 | 64.06 | 7.985e-14 | 0.9381 | 1 | 2.52 | 2.56 | 3.92 |
| faithfulness_gap | 25 | 67.61 | 1.388e-14 | 0.9381 | 1 | 2.44 | 2.56 | 4 |

## Table 4: other datasets (mean and SD over seeds of model-averaged means)

| dataset | explainer | stability_mean | stability_std | fidelity_mean | fidelity_std | faithfulness_gap_mean | faithfulness_gap_std | sparsity_mean | sparsity_std |
|---|---|---|---|---|---|---|---|---|---|
| breast_cancer | anchors | 0.383 | 0.03458 | 0.2544 | 0.007367 | 0.08484 | 0.006151 | 0.0705 | 0.0005422 |
| breast_cancer | dice | 0.2451 | 0.01937 | 0.1479 | 0.01838 | 0.07016 | 0.001607 | 0.1485 | 0.008238 |
| breast_cancer | lime | 0.8682 | 0.01235 | 0.632 | 0.0119 | 0.1432 | 0.007557 | 0.3332 | 0.000148 |
| breast_cancer | lime_full | 0.9889 | 0.0005569 | 0.4977 | 0.007417 | 0.1163 | 0.001114 | 0.994 | 0.00244 |
| breast_cancer | shap | 0.841 | 0.006536 | 0.6875 | 0.005221 | 0.2088 | 0.01336 | 0.574 | 0.0004816 |
| connect4 | anchors | 0.7141 | 0.01246 | 0.4887 | 0.01114 | 0.3654 | 0.0131 | 0.05991 | 0.0007826 |
| connect4 | dice | 0.1032 | 0.01286 | 0.09109 | 0.01011 | 0.07761 | 0.007334 | 0.01859 | 0.001092 |
| connect4 | lime | 0.6084 | 0.01385 | 0.4959 | 0.003894 | 0.223 | 0.001665 | 0.07913 | 0.0001273 |
| connect4 | lime_full | 0.85 | 0.006475 | 0.3614 | 0.003142 | 0.1746 | 0.00693 | 0.9856 | 0.002016 |
| connect4 | shap | 0.6962 | 0.008756 | 0.7982 | 0.006425 | 0.3673 | 0.001488 | 0.3092 | 0.000468 |
| diabetes | anchors | 0.8164 | 0.01162 | 0.3678 | 0.01307 | 0.2875 | 0.004143 | 0.4047 | 0.002002 |
| diabetes | dice | 0.3222 | 0.005186 | 0.2666 | 0.02789 | 0.2192 | 0.009186 | 0.1972 | 0.001073 |
| diabetes | lime | 0.9963 | 0.0002694 | 0.4899 | 0.01047 | 0.2802 | 0.003129 | 0.9984 | 0.0004337 |
| diabetes | lime_full | 0.9963 | 0.0002805 | 0.4899 | 0.01047 | 0.2802 | 0.003129 | 0.9984 | 0.0004337 |
| diabetes | shap | 0.9475 | 0.002446 | 0.7969 | 0.007934 | 0.2982 | 0.002742 | 0.9974 | 0.000164 |
| german_credit | anchors | 0.6755 | 0.01772 | 0.4275 | 0.008561 | 0.2167 | 0.00446 | 0.1085 | 0.001757 |
| german_credit | dice | 0.3006 | 0.01136 | 0.1776 | 0.008325 | 0.1011 | 0.004226 | 0.03719 | 0.0003209 |
| german_credit | lime | 0.8512 | 0.006311 | 0.5218 | 0.001828 | 0.1926 | 0.003039 | 0.1639 | 2.004e-05 |
| german_credit | lime_full | 0.9419 | 0.001221 | 0.4428 | 0.001701 | 0.1686 | 0.0008105 | 0.9929 | 0.0005162 |
| german_credit | shap | 0.8263 | 0.008058 | 0.7729 | 0.005872 | 0.3057 | 0.00564 | 0.448 | 0.0002719 |
| phishing | anchors | 0.8902 | 0.006598 | 0.5094 | 0.0006257 | 0.3257 | 0.01131 | 0.05475 | 0.002279 |
| phishing | dice | 0.2503 | 0.01451 | 0.2638 | 0.01436 | 0.2021 | 0.005991 | 0.04642 | 0.0009159 |
| phishing | lime | 0.8902 | 0.002725 | 0.5667 | 0.002745 | 0.2912 | 0.008135 | 0.1471 | 0 |
| phishing | lime_full | 0.9544 | 0.00014 | 0.5429 | 0.002335 | 0.2755 | 0.006707 | 0.994 | 0.0002586 |
| phishing | shap | 0.7482 | 0.01279 | 0.6983 | 0.002169 | 0.4609 | 0.008325 | 0.3814 | 0.001024 |
| spambase | anchors | 0.2988 | 0.02134 | 0.2424 | 0.002922 | 0.2462 | 0.003514 | 0.0591 | 0.0001735 |
| spambase | dice | 0.1094 | 0.009317 | 0.1303 | 0.006056 | 0.1812 | 0.001534 | 0.03579 | 0.001623 |
| spambase | lime | 0.7815 | 0.01694 | 0.5058 | 0.006837 | 0.2505 | 0.006118 | 0.1733 | 0.0003755 |
| spambase | lime_full | 0.9464 | 0.008007 | 0.4578 | 0.00761 | 0.2457 | 0.009258 | 0.9802 | 0.00247 |
| spambase | shap | 0.6912 | 0.01898 | 0.6409 | 0.007268 | 0.457 | 0.01189 | 0.4459 | 0.0006107 |

## Quality checks

| dataset | explainer | rows | all_zero_share | fidelity_exact_zero_share | stability_rows | stability_zero_vectors_mean | stability_zero_vector_share |
|---|---|---|---|---|---|---|---|
| adult | anchors | 2498 | 0 | 0.0008006 | 298 | 0 | 0 |
| adult | dice | 2500 | 0 | 0.0004 | 300 | 0 | 0 |
| adult | lime | 2500 | 0.004 | 0.0004 | 300 | 0.8767 | 0.05844 |
| adult | lime_full | 2500 | 0.004 | 0.0004 | 300 | 0.95 | 0.06333 |
| adult | shap | 2500 | 0 | 0.0004 | 300 | 0 | 0 |
| breast_cancer | anchors | 807 | 0 | 0.03346 | 144 | 0 | 0 |
| breast_cancer | dice | 807 | 0.05948 | 0.08674 | 144 | 0.4653 | 0.03102 |
| breast_cancer | lime | 807 | 0 | 0.03346 | 144 | 0 | 0 |
| breast_cancer | lime_full | 807 | 0 | 0.03346 | 144 | 0 | 0 |
| breast_cancer | shap | 807 | 0 | 0.03346 | 144 | 0 | 0 |
| connect4 | anchors | 1497 | 0 | 0.00334 | 177 | 0 | 0 |
| connect4 | dice | 1500 | 0 | 0.002667 | 180 | 0 | 0 |
| connect4 | lime | 1500 | 0 | 0.002667 | 180 | 0.1167 | 0.007778 |
| connect4 | lime_full | 1500 | 0 | 0.002667 | 180 | 0.1167 | 0.007778 |
| connect4 | shap | 1500 | 0 | 0.002667 | 180 | 0 | 0 |
| diabetes | anchors | 1347 | 0 | 0.01411 | 180 | 0 | 0 |
| diabetes | dice | 1347 | 0 | 0 | 180 | 0 | 0 |
| diabetes | lime | 1347 | 0 | 0 | 180 | 0 | 0 |
| diabetes | lime_full | 1347 | 0 | 0 | 180 | 0 | 0 |
| diabetes | shap | 1347 | 0 | 0 | 180 | 0 | 0 |
| german_credit | anchors | 1431 | 0 | 0 | 180 | 0 | 0 |
| german_credit | dice | 1431 | 0 | 0 | 180 | 0 | 0 |
| german_credit | lime | 1431 | 0 | 0 | 180 | 0 | 0 |
| german_credit | lime_full | 1431 | 0 | 0 | 180 | 0 | 0 |
| german_credit | shap | 1431 | 0 | 0 | 180 | 0 | 0 |
| phishing | anchors | 1488 | 0 | 0.01411 | 180 | 0 | 0 |
| phishing | dice | 1488 | 0 | 0.01411 | 180 | 0 | 0 |
| phishing | lime | 1488 | 0 | 0.01411 | 180 | 0 | 0 |
| phishing | lime_full | 1488 | 0 | 0.01411 | 180 | 0 | 0 |
| phishing | shap | 1488 | 0 | 0.01411 | 180 | 0 | 0 |
| spambase | anchors | 1476 | 0 | 0.0122 | 180 | 0 | 0 |
| spambase | dice | 1476 | 0.006098 | 0.01829 | 180 | 0.07778 | 0.005185 |
| spambase | lime | 1476 | 0.00271 | 0.0122 | 180 | 0.01667 | 0.001111 |
| spambase | lime_full | 1476 | 0.00271 | 0.0122 | 180 | 0.01667 | 0.001111 |
| spambase | shap | 1476 | 0 | 0.0122 | 180 | 0 | 0 |

## Table 3: cost

| dataset | model | explainer | cpu_ms_median | wall_ms_median | rows_median | calls_median | n |
|---|---|---|---|---|---|---|---|
| adult | logreg | anchors | 742.2 | 748.9 | 5501 | 56 | 100 |
| adult | logreg | dice | 1062 | 1064 | 2004 | 6 | 100 |
| adult | logreg | lime | 15.62 | 7.806 | 1000 | 1 | 100 |
| adult | logreg | lime_full | 15.62 | 9.443 | 1000 | 1 | 100 |
| adult | logreg | shap | 31.25 | 29.62 | 2.5e+04 | 2 | 100 |
| adult | mlp | anchors | 2750 | 2776 | 2.32e+04 | 233 | 100 |
| adult | mlp | dice | 1094 | 1094 | 2004 | 6 | 100 |
| adult | mlp | lime | 15.62 | 9.167 | 1000 | 1 | 100 |
| adult | mlp | lime_full | 15.62 | 11.03 | 1000 | 1 | 100 |
| adult | mlp | shap | 46.88 | 52.17 | 2.5e+04 | 2 | 100 |
| adult | rf | anchors | 1320 | 1323 | 6551 | 66.5 | 100 |
| adult | rf | dice | 1109 | 1107 | 2004 | 6 | 100 |
| adult | rf | lime | 15.62 | 20.5 | 1000 | 1 | 100 |
| adult | rf | lime_full | 15.62 | 22.29 | 1000 | 1 | 100 |
| adult | rf | shap | 15.62 | 23 | 0 | 0 | 100 |
| adult | svm | anchors | 5617 | 5640 | 6351 | 64.5 | 100 |
| adult | svm | dice | 2609 | 2627 | 2004 | 6 | 100 |
| adult | svm | lime | 781.2 | 788.5 | 1000 | 1 | 100 |
| adult | svm | lime_full | 781.2 | 786.2 | 1000 | 1 | 100 |
| adult | svm | shap | 1.936e+04 | 1.949e+04 | 2.5e+04 | 2 | 100 |
| adult | xgb | anchors | 921.9 | 918.8 | 0 | 0 | 100 |
| adult | xgb | dice | 1094 | 1107 | 2004 | 6 | 100 |
| adult | xgb | lime | 15.62 | 11.46 | 1000 | 1 | 100 |
| adult | xgb | lime_full | 15.62 | 13.33 | 1000 | 1 | 100 |
| adult | xgb | shap | 0 | 1.429 | 0 | 0 | 100 |
| breast_cancer | logreg | anchors | 1523 | 1534 | 6.4e+04 | 641 | 36 |
| breast_cancer | logreg | dice | 234.4 | 228.4 | 2004 | 6 | 36 |
| breast_cancer | logreg | lime | 0 | 3.815 | 1000 | 1 | 36 |
| breast_cancer | logreg | lime_full | 0 | 3.756 | 1000 | 1 | 36 |
| breast_cancer | logreg | shap | 15.62 | 18.04 | 2.5e+04 | 2 | 36 |
| breast_cancer | rf | anchors | 5328 | 5367 | 8.65e+04 | 866 | 45 |
| breast_cancer | rf | dice | 296.9 | 294.9 | 2004 | 6 | 45 |
| breast_cancer | rf | lime | 15.62 | 10.97 | 1000 | 1 | 45 |
| breast_cancer | rf | lime_full | 15.62 | 11.09 | 1000 | 1 | 45 |
| breast_cancer | rf | shap | 0 | 2.632 | 0 | 0 | 45 |
| breast_cancer | xgb | anchors | 2000 | 2021 | 0 | 0 | 33 |
| breast_cancer | xgb | dice | 250 | 250.2 | 2004 | 6 | 34 |
| breast_cancer | xgb | lime | 0 | 5.421 | 1000 | 1 | 33 |
| breast_cancer | xgb | lime_full | 0 | 5.574 | 1000 | 1 | 33 |
| breast_cancer | xgb | shap | 0 | 0.6831 | 0 | 0 | 34 |
