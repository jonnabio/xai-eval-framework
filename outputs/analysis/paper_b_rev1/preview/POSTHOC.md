# Post-hoc measurement controls (cohort B2)

Dataset: german_credit; rows: 4,405; masking rows: 17,620

## Stability by measure and concentration (means over instances)

model,explainer,stab_cosine,stab_cosine_nonzero,stab_spearman,stab_top5_jaccard,zero_vectors,top5_share,entropy_norm
logreg,anchors,0.7427,0.7427,0.7231,0.6414,0,0.9125,0.3008
logreg,dice,0.3661,0.3661,0.2069,0.1564,0,0.99,0.1349
logreg,lime,0.8261,0.8261,0.7797,0.6015,0,0.6627,0.5374
logreg,lime_full,0.9942,0.9942,0.9651,0.7315,0,0.2573,0.9065
logreg,shap,0.8433,0.8433,0.6806,0.5799,0,0.7358,0.5122
mlp,anchors,0.6563,0.6563,0.6066,0.5392,0,0.7971,0.4115
mlp,dice,0.1937,0.1937,0.1262,0.1069,0,0.9981,0.1089
mlp,lime,0.6983,0.6983,0.6051,0.475,0,0.7077,0.5278
mlp,lime_full,0.9207,0.9207,0.6937,0.6414,0,0.2594,0.9154
mlp,shap,0.7755,0.7755,0.5434,0.4644,0,0.7524,0.4984
rf,anchors,0.714,0.714,0.6313,0.65,0,0.6756,0.4938
rf,dice,0.3511,0.3511,0.2458,0.1888,0,0.9706,0.158
rf,lime,0.9166,0.9166,0.762,0.7161,0,0.7427,0.5139
rf,lime_full,0.9312,0.9312,0.5965,0.7623,0,0.3868,0.8517
rf,shap,0.9851,0.9851,0.9682,0.8446,0,0.4983,0.7618
svm,anchors,0.7138,0.7138,0.6869,0.596,0,0.8171,0.3517
svm,dice,0.3796,0.3796,0.2499,0.1974,0,0.9991,0.07983
svm,lime,0.908,0.908,0.816,0.6996,0,0.7188,0.5208
svm,lime_full,0.9805,0.9805,0.8322,0.8089,0,0.332,0.8869
svm,shap,0.8879,0.8879,0.6864,0.6126,0,0.7491,0.499
xgb,anchors,0.6294,0.6294,0.5817,0.5181,0,0.8375,0.3806
xgb,dice,0.2267,0.2267,0.1503,0.1238,0,0.9935,0.1151
xgb,lime,0.8953,0.8953,0.6824,0.7304,0,0.7806,0.4914
xgb,lime_full,0.8797,0.8797,0.3916,0.7734,0,0.4115,0.8438
xgb,shap,0.6391,0.6391,0.8834,0.5252,0,0.5398,0.7243


## Top-5 masking: SHAP minus X, mean of cell means, and cells with SHAP ahead

model,contrast,scheme,gap_mean,cells,cells_shap_ahead
logreg,shap-anchors,grouped_mean,0.01895,2,2
logreg,shap-anchors,marginal,0.05382,2,2
logreg,shap-anchors,mean,0.03639,2,2
logreg,shap-anchors,zero,0.02296,2,2
mlp,shap-anchors,grouped_mean,0.1105,2,2
mlp,shap-anchors,marginal,0.07459,2,2
mlp,shap-anchors,mean,0.1242,2,2
mlp,shap-anchors,zero,0.1512,2,2
rf,shap-anchors,grouped_mean,0.009572,2,2
rf,shap-anchors,marginal,0.0358,2,2
rf,shap-anchors,mean,0.02407,2,2
rf,shap-anchors,zero,0.04051,2,2
svm,shap-anchors,grouped_mean,0.06312,1,1
svm,shap-anchors,marginal,0.06065,1,1
svm,shap-anchors,mean,0.06727,1,1
svm,shap-anchors,zero,0.07091,1,1
xgb,shap-anchors,grouped_mean,-0.001807,2,1
xgb,shap-anchors,marginal,0.03905,2,2
xgb,shap-anchors,mean,0.005309,2,2
xgb,shap-anchors,zero,0.005309,2,2
logreg,shap-dice,grouped_mean,0.1643,2,2
logreg,shap-dice,marginal,0.1685,2,2
logreg,shap-dice,mean,0.1747,2,2
logreg,shap-dice,zero,0.1706,2,2
mlp,shap-dice,grouped_mean,0.3284,2,2
mlp,shap-dice,marginal,0.2641,2,2
mlp,shap-dice,mean,0.3431,2,2
mlp,shap-dice,zero,0.3815,2,2
rf,shap-dice,grouped_mean,0.05196,1,1
rf,shap-dice,marginal,0.0659,1,1
rf,shap-dice,mean,0.05977,1,1
rf,shap-dice,zero,0.06937,1,1
svm,shap-dice,grouped_mean,0.1353,2,2
svm,shap-dice,marginal,0.1034,2,2
svm,shap-dice,mean,0.1236,2,2
svm,shap-dice,zero,0.1199,2,2
xgb,shap-dice,grouped_mean,0.03738,2,2
xgb,shap-dice,marginal,0.08082,2,2
xgb,shap-dice,mean,0.04323,2,2
xgb,shap-dice,zero,0.04323,2,2
logreg,shap-lime,grouped_mean,0.08438,2,2
logreg,shap-lime,marginal,0.07307,2,2
logreg,shap-lime,mean,0.09042,2,2
logreg,shap-lime,zero,0.08907,2,2
mlp,shap-lime,grouped_mean,0.2435,2,2
mlp,shap-lime,marginal,0.2052,2,2
mlp,shap-lime,mean,0.2724,2,2
mlp,shap-lime,zero,0.3147,2,2
rf,shap-lime,grouped_mean,0.02905,2,2
rf,shap-lime,marginal,0.02447,2,2
rf,shap-lime,mean,0.03056,2,2
rf,shap-lime,zero,0.03645,2,2
svm,shap-lime,grouped_mean,0.09803,2,2
svm,shap-lime,marginal,0.07457,2,2
svm,shap-lime,mean,0.08818,2,2
svm,shap-lime,zero,0.07957,2,2
xgb,shap-lime,grouped_mean,0.09011,2,2
xgb,shap-lime,marginal,0.1214,2,2
xgb,shap-lime,mean,0.09217,2,2
xgb,shap-lime,zero,0.09217,2,2
logreg,shap-lime_full,grouped_mean,0.08433,2,2
logreg,shap-lime_full,marginal,0.09825,2,2
logreg,shap-lime_full,mean,0.1192,2,2
logreg,shap-lime_full,zero,0.1399,2,2
mlp,shap-lime_full,grouped_mean,0.2823,2,2
mlp,shap-lime_full,marginal,0.2483,2,2
mlp,shap-lime_full,mean,0.327,2,2
mlp,shap-lime_full,zero,0.3923,2,2
rf,shap-lime_full,grouped_mean,0.03561,2,2
rf,shap-lime_full,marginal,0.04779,2,2
rf,shap-lime_full,mean,0.03587,2,2
rf,shap-lime_full,zero,0.04545,2,2
svm,shap-lime_full,grouped_mean,0.1144,1,1
svm,shap-lime_full,marginal,0.06645,1,1
svm,shap-lime_full,mean,0.103,1,1
svm,shap-lime_full,zero,0.1005,1,1
xgb,shap-lime_full,grouped_mean,0.1031,1,1
xgb,shap-lime_full,marginal,0.1224,1,1
xgb,shap-lime_full,mean,0.09915,1,1
xgb,shap-lime_full,zero,0.09915,1,1

