# Post-hoc measurement controls (cohort B2)

Dataset: spambase; rows: 7,380; masking rows: 29,452

## Stability by measure and concentration (means over instances)

model,explainer,stab_cosine,stab_cosine_nonzero,stab_spearman,stab_top5_jaccard,zero_vectors,top5_share,entropy_norm
logreg,anchors,0.307,0.307,0.2803,0.234,0,0.9708,0.2739
logreg,dice,0.05662,0.05662,0.02681,0.03915,0,1,0.06903
logreg,lime,0.8007,0.8007,0.601,0.4519,0,0.7313,0.5145
logreg,lime_full,0.978,0.978,0.8294,0.5513,0,0.3182,0.8753
logreg,shap,0.7847,0.7847,0.5326,0.4822,0,0.7821,0.4693
mlp,anchors,0.3187,0.3187,0.2913,0.241,0,0.9592,0.2976
mlp,dice,0.05294,0.05294,0.02363,0.0377,0,1,0.0736
mlp,lime,0.7079,0.7079,0.5177,0.396,0,0.7329,0.5177
mlp,lime_full,0.9532,0.9532,0.7823,0.6681,0,0.31,0.8898
mlp,shap,0.7218,0.7218,0.4911,0.4219,0,0.7443,0.4919
rf,anchors,0.2852,0.2852,0.2543,0.2138,0,0.9994,0.2627
rf,dice,0.1653,0.1653,0.1273,0.11,0,0.9724,0.1492
rf,lime,0.8338,0.8338,0.7004,0.6794,0,0.7414,0.5195
rf,lime_full,0.9308,0.9308,0.6821,0.8231,0,0.3824,0.8557
rf,shap,0.598,0.598,0.8075,0.527,0,0.523,0.7305
svm,anchors,0.3391,0.3391,0.3122,0.2516,0,0.9886,0.268
svm,dice,0.09736,0.1001,0.07153,0.0791,0.3889,1,0.07604
svm,lime,0.8102,0.8102,0.734,0.616,0,0.6873,0.5378
svm,lime_full,0.9875,0.9875,0.9375,0.8208,0,0.2578,0.9246
svm,shap,0.9,0.9,0.6552,0.5509,0,0.7425,0.4839
xgb,anchors,0.244,0.244,0.213,0.1835,0,0.9962,0.2714
xgb,dice,0.175,0.175,0.1322,0.106,0,0.9875,0.1207
xgb,lime,0.7547,0.7535,0.5685,0.4519,0.08333,0.7459,0.5072
xgb,lime_full,0.8826,0.8813,0.557,0.5682,0.08333,0.3561,0.8675
xgb,shap,0.4516,0.4516,0.828,0.4622,0,0.5413,0.7196


## Top-5 masking: SHAP minus X, mean of cell means, and cells with SHAP ahead

model,contrast,scheme,gap_mean,cells,cells_shap_ahead
logreg,shap-anchors,grouped_mean,0.1404,3,3
logreg,shap-anchors,marginal,0.1038,3,3
logreg,shap-anchors,mean,0.1404,3,3
logreg,shap-anchors,zero,0.1404,3,3
mlp,shap-anchors,grouped_mean,0.3218,3,3
mlp,shap-anchors,marginal,0.1726,3,3
mlp,shap-anchors,mean,0.3218,3,3
mlp,shap-anchors,zero,0.3218,3,3
rf,shap-anchors,grouped_mean,0.1861,3,3
rf,shap-anchors,marginal,0.09517,3,3
rf,shap-anchors,mean,0.1861,3,3
rf,shap-anchors,zero,0.1861,3,3
svm,shap-anchors,grouped_mean,0.14,3,3
svm,shap-anchors,marginal,0.1204,3,3
svm,shap-anchors,mean,0.14,3,3
svm,shap-anchors,zero,0.14,3,3
xgb,shap-anchors,grouped_mean,0.3385,3,3
xgb,shap-anchors,marginal,0.1085,3,3
xgb,shap-anchors,mean,0.3385,3,3
xgb,shap-anchors,zero,0.3385,3,3
logreg,shap-dice,grouped_mean,0.3061,3,3
logreg,shap-dice,marginal,0.2713,3,3
logreg,shap-dice,mean,0.3061,3,3
logreg,shap-dice,zero,0.3061,3,3
mlp,shap-dice,grouped_mean,0.5113,3,3
mlp,shap-dice,marginal,0.3833,3,3
mlp,shap-dice,mean,0.5113,3,3
mlp,shap-dice,zero,0.5113,3,3
rf,shap-dice,grouped_mean,0.1114,3,3
rf,shap-dice,marginal,0.2011,3,3
rf,shap-dice,mean,0.1114,3,3
rf,shap-dice,zero,0.1114,3,3
svm,shap-dice,grouped_mean,0.2859,3,3
svm,shap-dice,marginal,0.2567,3,3
svm,shap-dice,mean,0.2859,3,3
svm,shap-dice,zero,0.2859,3,3
xgb,shap-dice,grouped_mean,0.3315,3,3
xgb,shap-dice,marginal,0.2874,3,3
xgb,shap-dice,mean,0.3315,3,3
xgb,shap-dice,zero,0.3315,3,3
logreg,shap-lime,grouped_mean,0.1385,3,3
logreg,shap-lime,marginal,0.1777,3,3
logreg,shap-lime,mean,0.1385,3,3
logreg,shap-lime,zero,0.1385,3,3
mlp,shap-lime,grouped_mean,0.3469,3,3
mlp,shap-lime,marginal,0.2693,3,3
mlp,shap-lime,mean,0.3469,3,3
mlp,shap-lime,zero,0.3469,3,3
rf,shap-lime,grouped_mean,0.1066,3,3
rf,shap-lime,marginal,0.1031,3,3
rf,shap-lime,mean,0.1066,3,3
rf,shap-lime,zero,0.1066,3,3
svm,shap-lime,grouped_mean,0.2392,3,3
svm,shap-lime,marginal,0.1693,3,3
svm,shap-lime,mean,0.2392,3,3
svm,shap-lime,zero,0.2392,3,3
xgb,shap-lime,grouped_mean,0.1975,3,3
xgb,shap-lime,marginal,0.1697,3,3
xgb,shap-lime,mean,0.1975,3,3
xgb,shap-lime,zero,0.1975,3,3
logreg,shap-lime_full,grouped_mean,0.1502,3,3
logreg,shap-lime_full,marginal,0.1554,3,3
logreg,shap-lime_full,mean,0.1502,3,3
logreg,shap-lime_full,zero,0.1502,3,3
mlp,shap-lime_full,grouped_mean,0.3486,3,3
mlp,shap-lime_full,marginal,0.3092,3,3
mlp,shap-lime_full,mean,0.3486,3,3
mlp,shap-lime_full,zero,0.3486,3,3
rf,shap-lime_full,grouped_mean,0.1117,3,3
rf,shap-lime_full,marginal,0.0839,3,3
rf,shap-lime_full,mean,0.1117,3,3
rf,shap-lime_full,zero,0.1117,3,3
svm,shap-lime_full,grouped_mean,0.2425,3,3
svm,shap-lime_full,marginal,0.1579,3,3
svm,shap-lime_full,mean,0.2425,3,3
svm,shap-lime_full,zero,0.2425,3,3
xgb,shap-lime_full,grouped_mean,0.2,3,3
xgb,shap-lime_full,marginal,0.2109,3,3
xgb,shap-lime_full,mean,0.2,3,3
xgb,shap-lime_full,zero,0.2,3,3

