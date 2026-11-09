# Post-hoc measurement controls (cohort B2)

Dataset: adult; rows: 12,498; masking rows: 49,912

## Stability by measure and concentration (means over instances)

model,explainer,stab_cosine,stab_cosine_nonzero,stab_spearman,stab_top5_jaccard,zero_vectors,top5_share,entropy_norm
logreg,anchors,0.6303,0.6303,0.6178,0.501,0,0.9356,0.2393
logreg,dice,0.3515,0.3515,0.2264,0.1744,0,0.9976,0.07017
logreg,lime,0.4146,0.4804,0.424,0.3173,1.3,0.8216,0.3956
logreg,lime_full,0.5916,0.6635,0.2531,0.4618,1.15,0.3933,0.8039
logreg,shap,0.8603,0.8603,0.5628,0.6295,0,0.8108,0.4164
mlp,anchors,0.6276,0.6276,0.5821,0.5323,0,0.6991,0.4059
mlp,dice,0.147,0.147,0.08425,0.07127,0,1,0.07375
mlp,lime,0.1887,0.2006,0.2478,0.1356,0.7333,0.7091,0.4573
mlp,lime_full,0.4485,0.5052,0.2795,0.1909,0.9,0.1657,0.9171
mlp,shap,0.3246,0.3246,0.2092,0.1781,0,0.7669,0.4306
rf,anchors,0.6593,0.6593,0.6448,0.5427,0,0.9097,0.2776
rf,dice,0.4952,0.4952,0.3323,0.2524,0,0.9932,0.08666
rf,lime,0.3692,0.4155,0.3495,0.262,0.9,0.8465,0.3793
rf,lime_full,0.5582,0.6354,0.1902,0.4223,1.1,0.3981,0.8104
rf,shap,0.9807,0.9807,0.9967,0.9193,0,0.6411,0.5766
svm,anchors,0.6884,0.6884,0.6778,0.5723,0,0.9218,0.2629
svm,dice,0.4106,0.4106,0.275,0.2125,0,1,0.05354
svm,lime,0.3956,0.4359,0.3833,0.2726,0.7167,0.8537,0.3673
svm,lime_full,0.5913,0.6584,0.2027,0.425,0.85,0.4192,0.79
svm,shap,0.9032,0.9032,0.6389,0.6832,0,0.8224,0.4045
xgb,anchors,0.5656,0.5656,0.5449,0.4499,0,0.8371,0.3019
xgb,dice,0.5829,0.5829,0.3831,0.2846,0,0.9983,0.07009
xgb,lime,0.2409,0.264,0.2591,0.1612,0.7167,0.8863,0.3219
xgb,lime_full,0.5506,0.6071,0.1173,0.3688,0.75,0.3545,0.8276
xgb,shap,0.6149,0.6149,0.9809,0.7449,0,0.7785,0.4773


## Top-5 masking: SHAP minus X, mean of cell means, and cells with SHAP ahead

model,contrast,scheme,gap_mean,cells,cells_shap_ahead
logreg,shap-anchors,grouped_mean,0.1081,5,5
logreg,shap-anchors,marginal,0.1014,5,5
logreg,shap-anchors,mean,0.111,5,5
logreg,shap-anchors,zero,0.1368,5,5
mlp,shap-anchors,grouped_mean,0.149,5,5
mlp,shap-anchors,marginal,0.1402,5,5
mlp,shap-anchors,mean,0.2037,5,5
mlp,shap-anchors,zero,0.1926,5,5
rf,shap-anchors,grouped_mean,0.1274,5,5
rf,shap-anchors,marginal,0.07804,5,5
rf,shap-anchors,mean,0.149,5,5
rf,shap-anchors,zero,0.149,5,5
svm,shap-anchors,grouped_mean,0.0484,5,5
svm,shap-anchors,marginal,0.02651,5,5
svm,shap-anchors,mean,0.05816,5,5
svm,shap-anchors,zero,0.06612,5,5
xgb,shap-anchors,grouped_mean,0.1566,5,5
xgb,shap-anchors,marginal,0.0816,5,5
xgb,shap-anchors,mean,0.1606,5,5
xgb,shap-anchors,zero,0.1606,5,5
logreg,shap-dice,grouped_mean,0.1873,5,5
logreg,shap-dice,marginal,0.1774,5,5
logreg,shap-dice,mean,0.2059,5,5
logreg,shap-dice,zero,0.2328,5,5
mlp,shap-dice,grouped_mean,0.2109,5,5
mlp,shap-dice,marginal,0.2595,5,5
mlp,shap-dice,mean,0.3225,5,5
mlp,shap-dice,zero,0.3143,5,5
rf,shap-dice,grouped_mean,0.1946,5,5
rf,shap-dice,marginal,0.15,5,5
rf,shap-dice,mean,0.2431,5,5
rf,shap-dice,zero,0.2426,5,5
svm,shap-dice,grouped_mean,0.17,5,5
svm,shap-dice,marginal,0.1286,5,5
svm,shap-dice,mean,0.1978,5,5
svm,shap-dice,zero,0.2224,5,5
xgb,shap-dice,grouped_mean,0.1564,5,5
xgb,shap-dice,marginal,0.1195,5,5
xgb,shap-dice,mean,0.1749,5,5
xgb,shap-dice,zero,0.1749,5,5
logreg,shap-lime,grouped_mean,0.0774,5,5
logreg,shap-lime,marginal,0.06062,5,5
logreg,shap-lime,mean,0.06558,5,5
logreg,shap-lime,zero,0.08002,5,5
mlp,shap-lime,grouped_mean,0.1077,5,5
mlp,shap-lime,marginal,0.1605,5,5
mlp,shap-lime,mean,0.1903,5,5
mlp,shap-lime,zero,0.1887,5,5
rf,shap-lime,grouped_mean,0.05298,5,5
rf,shap-lime,marginal,0.06129,5,5
rf,shap-lime,mean,0.08583,5,5
rf,shap-lime,zero,0.08574,5,5
svm,shap-lime,grouped_mean,0.08249,5,5
svm,shap-lime,marginal,0.06033,5,5
svm,shap-lime,mean,0.1098,5,5
svm,shap-lime,zero,0.0848,5,5
xgb,shap-lime,grouped_mean,0.003051,5,3
xgb,shap-lime,marginal,0.03868,5,5
xgb,shap-lime,mean,0.004933,5,4
xgb,shap-lime,zero,0.004933,5,4
logreg,shap-lime_full,grouped_mean,0.08715,5,5
logreg,shap-lime_full,marginal,0.05572,5,5
logreg,shap-lime_full,mean,0.07704,5,5
logreg,shap-lime_full,zero,0.08803,5,5
mlp,shap-lime_full,grouped_mean,0.1448,5,5
mlp,shap-lime_full,marginal,0.2589,5,5
mlp,shap-lime_full,mean,0.3075,5,5
mlp,shap-lime_full,zero,0.2998,5,5
rf,shap-lime_full,grouped_mean,0.08402,5,5
rf,shap-lime_full,marginal,0.06402,5,5
rf,shap-lime_full,mean,0.1142,5,5
rf,shap-lime_full,zero,0.1141,5,5
svm,shap-lime_full,grouped_mean,0.1138,5,5
svm,shap-lime_full,marginal,0.0894,5,5
svm,shap-lime_full,mean,0.1425,5,5
svm,shap-lime_full,zero,0.1175,5,5
xgb,shap-lime_full,grouped_mean,0.01437,5,5
xgb,shap-lime_full,marginal,0.04792,5,5
xgb,shap-lime_full,mean,0.01722,5,5
xgb,shap-lime_full,zero,0.01722,5,5

