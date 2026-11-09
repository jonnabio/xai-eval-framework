# Post-hoc measurement controls (cohort B2)

Dataset: diabetes; rows: 6,735; masking rows: 26,940

## Stability by measure and concentration (means over instances)

model,explainer,stab_cosine,stab_cosine_nonzero,stab_spearman,stab_top5_jaccard,zero_vectors,top5_share,entropy_norm
logreg,anchors,0.8937,0.8937,0.8405,0.833,0,0.989,0.3237
logreg,dice,0.3633,0.3633,0.1964,0.2608,0,1,0.1523
logreg,lime,0.9995,0.9995,0.9908,0.8943,0,0.8779,0.8321
logreg,lime_full,0.9995,0.9995,0.9912,0.8974,0,0.8779,0.8321
logreg,shap,0.9829,0.9829,0.9086,0.8867,0,0.9255,0.7206
mlp,anchors,0.8109,0.8109,0.6653,0.6959,0,0.9865,0.4245
mlp,dice,0.2789,0.2789,0.1104,0.2121,0,1,0.1364
mlp,lime,0.9959,0.9959,0.9498,0.9321,0,0.897,0.823
mlp,lime_full,0.9958,0.9958,0.9506,0.933,0,0.897,0.823
mlp,shap,0.9782,0.9782,0.8826,0.8511,0,0.9206,0.7214
rf,anchors,0.8152,0.8152,0.5765,0.6835,0,0.9501,0.6081
rf,dice,0.3677,0.3677,0.2146,0.279,0,1,0.1656
rf,lime,0.9956,0.9956,0.9469,0.9322,0,0.9288,0.7896
rf,lime_full,0.9956,0.9956,0.9475,0.9306,0,0.9288,0.7896
rf,shap,0.9355,0.9355,0.7985,0.7757,0,0.9195,0.7538
svm,anchors,0.7754,0.7754,0.6211,0.6578,0,0.983,0.4861
svm,dice,0.2817,0.2817,0.1078,0.2112,0,1,0.15
svm,lime,0.9966,0.9966,0.9593,0.9788,0,0.9486,0.7795
svm,lime_full,0.9966,0.9966,0.9563,0.9725,0,0.9486,0.7795
svm,shap,0.9817,0.9817,0.8939,0.8395,0,0.9346,0.7189
xgb,anchors,0.7867,0.7867,0.4912,0.6289,0,0.9332,0.6413
xgb,dice,0.3197,0.3197,0.167,0.2491,0,1,0.1693
xgb,lime,0.9939,0.9939,0.9283,0.8258,0,0.9326,0.7691
xgb,lime_full,0.9939,0.9939,0.929,0.8247,0,0.9326,0.7691
xgb,shap,0.8592,0.8592,0.7232,0.7317,0,0.917,0.7435


## Top-5 masking: SHAP minus X, mean of cell means, and cells with SHAP ahead

model,contrast,scheme,gap_mean,cells,cells_shap_ahead
logreg,shap-anchors,grouped_mean,0.02226,3,3
logreg,shap-anchors,marginal,0.05739,3,3
logreg,shap-anchors,mean,0.02226,3,3
logreg,shap-anchors,zero,0.02226,3,3
mlp,shap-anchors,grouped_mean,0.01903,3,3
mlp,shap-anchors,marginal,0.005318,3,2
mlp,shap-anchors,mean,0.01903,3,3
mlp,shap-anchors,zero,0.01903,3,3
rf,shap-anchors,grouped_mean,0.01246,3,3
rf,shap-anchors,marginal,0.01613,3,2
rf,shap-anchors,mean,0.01246,3,3
rf,shap-anchors,zero,0.01246,3,3
svm,shap-anchors,grouped_mean,0.01707,3,2
svm,shap-anchors,marginal,0.03492,3,3
svm,shap-anchors,mean,0.01707,3,2
svm,shap-anchors,zero,0.01707,3,2
xgb,shap-anchors,grouped_mean,-0.0006074,3,2
xgb,shap-anchors,marginal,0.04411,3,3
xgb,shap-anchors,mean,-0.0006074,3,2
xgb,shap-anchors,zero,-0.0006074,3,2
logreg,shap-dice,grouped_mean,0.0434,3,3
logreg,shap-dice,marginal,0.057,3,3
logreg,shap-dice,mean,0.0434,3,3
logreg,shap-dice,zero,0.0434,3,3
mlp,shap-dice,grouped_mean,0.04386,3,3
mlp,shap-dice,marginal,0.02664,3,3
mlp,shap-dice,mean,0.04386,3,3
mlp,shap-dice,zero,0.04386,3,3
rf,shap-dice,grouped_mean,0.04248,3,3
rf,shap-dice,marginal,0.07154,3,3
rf,shap-dice,mean,0.04248,3,3
rf,shap-dice,zero,0.04248,3,3
svm,shap-dice,grouped_mean,0.04306,3,3
svm,shap-dice,marginal,0.03958,3,3
svm,shap-dice,mean,0.04306,3,3
svm,shap-dice,zero,0.04306,3,3
xgb,shap-dice,grouped_mean,0.04136,3,3
xgb,shap-dice,marginal,0.04391,3,3
xgb,shap-dice,mean,0.04136,3,3
xgb,shap-dice,zero,0.04136,3,3
logreg,shap-lime,grouped_mean,0.00721,3,3
logreg,shap-lime,marginal,0.006278,3,1
logreg,shap-lime,mean,0.00721,3,3
logreg,shap-lime,zero,0.00721,3,3
mlp,shap-lime,grouped_mean,0.005526,3,2
mlp,shap-lime,marginal,-0.01517,3,1
mlp,shap-lime,mean,0.005526,3,2
mlp,shap-lime,zero,0.005526,3,2
rf,shap-lime,grouped_mean,0.0168,3,3
rf,shap-lime,marginal,0.01314,3,2
rf,shap-lime,mean,0.0168,3,3
rf,shap-lime,zero,0.0168,3,3
svm,shap-lime,grouped_mean,0.0144,3,3
svm,shap-lime,marginal,0.03156,3,3
svm,shap-lime,mean,0.0144,3,3
svm,shap-lime,zero,0.0144,3,3
xgb,shap-lime,grouped_mean,0.04642,3,3
xgb,shap-lime,marginal,0.008599,3,2
xgb,shap-lime,mean,0.04642,3,3
xgb,shap-lime,zero,0.04642,3,3
logreg,shap-lime_full,grouped_mean,0.00721,3,3
logreg,shap-lime_full,marginal,0.03843,3,3
logreg,shap-lime_full,mean,0.00721,3,3
logreg,shap-lime_full,zero,0.00721,3,3
mlp,shap-lime_full,grouped_mean,0.005526,3,2
mlp,shap-lime_full,marginal,-0.03427,3,1
mlp,shap-lime_full,mean,0.005526,3,2
mlp,shap-lime_full,zero,0.005526,3,2
rf,shap-lime_full,grouped_mean,0.0168,3,3
rf,shap-lime_full,marginal,0.01008,3,2
rf,shap-lime_full,mean,0.0168,3,3
rf,shap-lime_full,zero,0.0168,3,3
svm,shap-lime_full,grouped_mean,0.0144,3,3
svm,shap-lime_full,marginal,0.02752,3,1
svm,shap-lime_full,mean,0.0144,3,3
svm,shap-lime_full,zero,0.0144,3,3
xgb,shap-lime_full,grouped_mean,0.04642,3,3
xgb,shap-lime_full,marginal,0.02174,3,2
xgb,shap-lime_full,mean,0.04642,3,3
xgb,shap-lime_full,zero,0.04642,3,3

