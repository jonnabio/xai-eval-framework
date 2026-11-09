# Post-hoc measurement controls (cohort B2)

Dataset: breast_cancer; rows: 4,035; masking rows: 15,948

## Stability by measure and concentration (means over instances)

model,explainer,stab_cosine,stab_cosine_nonzero,stab_spearman,stab_top5_jaccard,zero_vectors,top5_share,entropy_norm
logreg,anchors,0.4702,0.4702,0.4277,0.3862,0,1,0.2135
logreg,dice,0.2656,0.2806,0.1537,0.1444,0.625,0.9334,0.2772
logreg,lime,0.8869,0.8869,0.8137,0.6635,0,0.6231,0.6618
logreg,lime_full,0.9947,0.9947,0.9704,0.6431,0,0.3078,0.9493
logreg,shap,0.8813,0.8813,0.7333,0.6108,0,0.6405,0.6543
mlp,anchors,0.4105,0.4105,0.3593,0.3116,0,1,0.2223
mlp,dice,0.3194,0.3271,0.1731,0.1548,0.1,0.9579,0.2221
mlp,lime,0.8503,0.8503,0.7719,0.567,0,0.6132,0.6633
mlp,lime_full,0.9891,0.9891,0.9559,0.5444,0,0.3106,0.9363
mlp,shap,0.8282,0.8282,0.6626,0.5661,0,0.6605,0.6486
rf,anchors,0.2511,0.2511,0.1909,0.175,0,1,0.2168
rf,dice,0.2364,0.2398,0.1689,0.1644,0.06061,0.8576,0.4435
rf,lime,0.8764,0.8764,0.7856,0.6891,0,0.732,0.6293
rf,lime_full,0.9865,0.9865,0.9196,0.8025,0,0.4953,0.8624
rf,shap,0.8351,0.8351,0.8333,0.6933,0,0.5538,0.8083
svm,anchors,0.3861,0.3861,0.3364,0.2914,0,1,0.2156
svm,dice,0.159,0.2196,0.1188,0.101,1.958,0.9754,0.1774
svm,lime,0.8592,0.8592,0.7828,0.5718,0,0.599,0.6663
svm,lime_full,0.9956,0.9956,0.9752,0.8232,0,0.3058,0.9331
svm,shap,0.8456,0.8456,0.6896,0.5144,0,0.6222,0.6581
xgb,anchors,0.397,0.397,0.345,0.3128,0,1,0.2172
xgb,dice,0.2448,0.2448,0.1743,0.1682,0,0.9293,0.3557
xgb,lime,0.8681,0.8681,0.7591,0.6934,0,0.7086,0.6394
xgb,lime_full,0.9786,0.9786,0.8395,0.9383,0,0.5186,0.8364
xgb,shap,0.8148,0.8148,0.9418,0.716,0,0.6195,0.7471


## Top-5 masking: SHAP minus X, mean of cell means, and cells with SHAP ahead

model,contrast,scheme,gap_mean,cells,cells_shap_ahead
logreg,shap-anchors,grouped_mean,0.1047,3,3
logreg,shap-anchors,marginal,0.109,3,3
logreg,shap-anchors,mean,0.1047,3,3
logreg,shap-anchors,zero,0.1047,3,3
mlp,shap-anchors,grouped_mean,0.1249,3,3
mlp,shap-anchors,marginal,0.1686,3,3
mlp,shap-anchors,mean,0.1249,3,3
mlp,shap-anchors,zero,0.1249,3,3
rf,shap-anchors,grouped_mean,0.1779,3,3
rf,shap-anchors,marginal,0.167,3,3
rf,shap-anchors,mean,0.1779,3,3
rf,shap-anchors,zero,0.1779,3,3
svm,shap-anchors,grouped_mean,0.0891,3,3
svm,shap-anchors,marginal,0.09619,3,3
svm,shap-anchors,mean,0.0891,3,3
svm,shap-anchors,zero,0.0891,3,3
xgb,shap-anchors,grouped_mean,0.1944,3,3
xgb,shap-anchors,marginal,0.2748,3,3
xgb,shap-anchors,mean,0.1944,3,3
xgb,shap-anchors,zero,0.1944,3,3
logreg,shap-dice,grouped_mean,0.1337,3,3
logreg,shap-dice,marginal,0.1415,3,3
logreg,shap-dice,mean,0.1337,3,3
logreg,shap-dice,zero,0.1337,3,3
mlp,shap-dice,grouped_mean,0.1751,3,3
mlp,shap-dice,marginal,0.203,3,3
mlp,shap-dice,mean,0.1751,3,3
mlp,shap-dice,zero,0.1751,3,3
rf,shap-dice,grouped_mean,0.1392,3,3
rf,shap-dice,marginal,0.1506,3,3
rf,shap-dice,mean,0.1392,3,3
rf,shap-dice,zero,0.1392,3,3
svm,shap-dice,grouped_mean,0.09517,3,3
svm,shap-dice,marginal,0.07772,3,3
svm,shap-dice,mean,0.09517,3,3
svm,shap-dice,zero,0.09517,3,3
xgb,shap-dice,grouped_mean,0.1796,3,3
xgb,shap-dice,marginal,0.2408,3,3
xgb,shap-dice,mean,0.1796,3,3
xgb,shap-dice,zero,0.1796,3,3
logreg,shap-lime,grouped_mean,0.07478,3,3
logreg,shap-lime,marginal,0.0401,3,3
logreg,shap-lime,mean,0.07478,3,3
logreg,shap-lime,zero,0.07478,3,3
mlp,shap-lime,grouped_mean,0.1214,3,3
mlp,shap-lime,marginal,0.1168,3,3
mlp,shap-lime,mean,0.1214,3,3
mlp,shap-lime,zero,0.1214,3,3
rf,shap-lime,grouped_mean,0.02788,3,3
rf,shap-lime,marginal,0.06297,3,3
rf,shap-lime,mean,0.02788,3,3
rf,shap-lime,zero,0.02788,3,3
svm,shap-lime,grouped_mean,0.05524,3,3
svm,shap-lime,marginal,0.05256,3,3
svm,shap-lime,mean,0.05524,3,3
svm,shap-lime,zero,0.05524,3,3
xgb,shap-lime,grouped_mean,0.04864,3,3
xgb,shap-lime,marginal,0.05787,3,2
xgb,shap-lime,mean,0.04864,3,3
xgb,shap-lime,zero,0.04864,3,3
logreg,shap-lime_full,grouped_mean,0.1118,3,3
logreg,shap-lime_full,marginal,0.08619,3,3
logreg,shap-lime_full,mean,0.1118,3,3
logreg,shap-lime_full,zero,0.1118,3,3
mlp,shap-lime_full,grouped_mean,0.1539,3,3
mlp,shap-lime_full,marginal,0.1131,3,3
mlp,shap-lime_full,mean,0.1539,3,3
mlp,shap-lime_full,zero,0.1539,3,3
rf,shap-lime_full,grouped_mean,0.03612,3,3
rf,shap-lime_full,marginal,0.03861,3,2
rf,shap-lime_full,mean,0.03612,3,3
rf,shap-lime_full,zero,0.03612,3,3
svm,shap-lime_full,grouped_mean,0.09319,3,3
svm,shap-lime_full,marginal,0.02406,3,3
svm,shap-lime_full,mean,0.09319,3,3
svm,shap-lime_full,zero,0.09319,3,3
xgb,shap-lime_full,grouped_mean,0.0674,3,3
xgb,shap-lime_full,marginal,0.07148,3,2
xgb,shap-lime_full,mean,0.0674,3,3
xgb,shap-lime_full,zero,0.0674,3,3

