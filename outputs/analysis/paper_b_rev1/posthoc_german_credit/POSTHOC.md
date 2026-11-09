# Post-hoc measurement controls (cohort B2)

Dataset: german_credit; rows: 7,155; masking rows: 28,620

## Stability by measure and concentration (means over instances)

model,explainer,stab_cosine,stab_cosine_nonzero,stab_spearman,stab_top5_jaccard,zero_vectors,top5_share,entropy_norm
logreg,anchors,0.737,0.737,0.7167,0.6312,0,0.9118,0.3017
logreg,dice,0.3686,0.3686,0.2082,0.1631,0,0.9881,0.1397
logreg,lime,0.8365,0.8365,0.7813,0.6147,0,0.6619,0.5376
logreg,lime_full,0.9941,0.9941,0.9643,0.7346,0,0.2572,0.9065
logreg,shap,0.844,0.844,0.6799,0.5832,0,0.7349,0.5128
mlp,anchors,0.6643,0.6643,0.6173,0.55,0,0.7919,0.4153
mlp,dice,0.2217,0.2217,0.1426,0.1182,0,0.9988,0.1021
mlp,lime,0.7034,0.7034,0.6039,0.4796,0,0.7063,0.5283
mlp,lime_full,0.9211,0.9211,0.6955,0.6448,0,0.2595,0.9153
mlp,shap,0.7761,0.7761,0.5467,0.4647,0,0.7547,0.4973
rf,anchors,0.6924,0.6924,0.6092,0.612,0,0.6753,0.495
rf,dice,0.3132,0.3132,0.2113,0.1673,0,0.9732,0.166
rf,lime,0.916,0.916,0.7682,0.7133,0,0.741,0.5146
rf,lime_full,0.9309,0.9309,0.5947,0.7624,0,0.3854,0.8526
rf,shap,0.9855,0.9855,0.9679,0.8403,0,0.4997,0.7611
svm,anchors,0.6651,0.6651,0.6332,0.5603,0,0.8318,0.3485
svm,dice,0.3811,0.3811,0.2467,0.1943,0,0.9994,0.08092
svm,lime,0.9029,0.9029,0.8114,0.7067,0,0.7177,0.5211
svm,lime_full,0.981,0.981,0.8345,0.8169,0,0.3322,0.8861
svm,shap,0.8895,0.8895,0.6911,0.6035,0,0.7509,0.4973
xgb,anchors,0.6188,0.6188,0.5738,0.5102,0,0.8343,0.3817
xgb,dice,0.2183,0.2183,0.1443,0.1205,0,0.9936,0.115
xgb,lime,0.8975,0.8975,0.6883,0.7335,0,0.7791,0.4918
xgb,lime_full,0.8826,0.8826,0.3905,0.7815,0,0.4134,0.8428
xgb,shap,0.6364,0.6364,0.8869,0.5255,0,0.5382,0.7253


## Top-5 masking: SHAP minus X, mean of cell means, and cells with SHAP ahead

model,contrast,scheme,gap_mean,cells,cells_shap_ahead
logreg,shap-anchors,grouped_mean,0.01534,3,3
logreg,shap-anchors,marginal,0.05439,3,3
logreg,shap-anchors,mean,0.03068,3,3
logreg,shap-anchors,zero,0.01593,3,3
mlp,shap-anchors,grouped_mean,0.1141,3,3
mlp,shap-anchors,marginal,0.08512,3,3
mlp,shap-anchors,mean,0.1309,3,3
mlp,shap-anchors,zero,0.16,3,3
rf,shap-anchors,grouped_mean,0.009245,3,3
rf,shap-anchors,marginal,0.03915,3,3
rf,shap-anchors,mean,0.02271,3,3
rf,shap-anchors,zero,0.04163,3,3
svm,shap-anchors,grouped_mean,0.06081,3,3
svm,shap-anchors,marginal,0.05677,3,3
svm,shap-anchors,mean,0.06759,3,3
svm,shap-anchors,zero,0.06635,3,3
xgb,shap-anchors,grouped_mean,0.005442,3,2
xgb,shap-anchors,marginal,0.03236,3,3
xgb,shap-anchors,mean,0.01198,3,3
xgb,shap-anchors,zero,0.01198,3,3
logreg,shap-dice,grouped_mean,0.1686,3,3
logreg,shap-dice,marginal,0.1686,3,3
logreg,shap-dice,mean,0.1744,3,3
logreg,shap-dice,zero,0.1683,3,3
mlp,shap-dice,grouped_mean,0.3183,3,3
mlp,shap-dice,marginal,0.2545,3,3
mlp,shap-dice,mean,0.333,3,3
mlp,shap-dice,zero,0.3655,3,3
rf,shap-dice,grouped_mean,0.06191,3,3
rf,shap-dice,marginal,0.08687,3,3
rf,shap-dice,mean,0.06731,3,3
rf,shap-dice,zero,0.07816,3,3
svm,shap-dice,grouped_mean,0.1423,3,3
svm,shap-dice,marginal,0.1131,3,3
svm,shap-dice,mean,0.1296,3,3
svm,shap-dice,zero,0.126,3,3
xgb,shap-dice,grouped_mean,0.04281,3,3
xgb,shap-dice,marginal,0.07982,3,3
xgb,shap-dice,mean,0.0497,3,3
xgb,shap-dice,zero,0.0497,3,3
logreg,shap-lime,grouped_mean,0.08105,3,3
logreg,shap-lime,marginal,0.08878,3,3
logreg,shap-lime,mean,0.08446,3,3
logreg,shap-lime,zero,0.08467,3,3
mlp,shap-lime,grouped_mean,0.2352,3,3
mlp,shap-lime,marginal,0.2177,3,3
mlp,shap-lime,mean,0.2659,3,3
mlp,shap-lime,zero,0.3093,3,3
rf,shap-lime,grouped_mean,0.02753,3,3
rf,shap-lime,marginal,0.02626,3,3
rf,shap-lime,mean,0.02657,3,3
rf,shap-lime,zero,0.03148,3,3
svm,shap-lime,grouped_mean,0.105,3,3
svm,shap-lime,marginal,0.06967,3,3
svm,shap-lime,mean,0.09559,3,3
svm,shap-lime,zero,0.08662,3,3
xgb,shap-lime,grouped_mean,0.09004,3,3
xgb,shap-lime,marginal,0.1191,3,3
xgb,shap-lime,mean,0.09289,3,3
xgb,shap-lime,zero,0.09289,3,3
logreg,shap-lime_full,grouped_mean,0.08254,3,3
logreg,shap-lime_full,marginal,0.1049,3,3
logreg,shap-lime_full,mean,0.117,3,3
logreg,shap-lime_full,zero,0.1339,3,3
mlp,shap-lime_full,grouped_mean,0.2782,3,3
mlp,shap-lime_full,marginal,0.2515,3,3
mlp,shap-lime_full,mean,0.3217,3,3
mlp,shap-lime_full,zero,0.3815,3,3
rf,shap-lime_full,grouped_mean,0.03495,3,3
rf,shap-lime_full,marginal,0.04314,3,3
rf,shap-lime_full,mean,0.0326,3,3
rf,shap-lime_full,zero,0.04263,3,3
svm,shap-lime_full,grouped_mean,0.1161,3,3
svm,shap-lime_full,marginal,0.08653,3,3
svm,shap-lime_full,mean,0.1078,3,3
svm,shap-lime_full,zero,0.1045,3,3
xgb,shap-lime_full,grouped_mean,0.1045,3,3
xgb,shap-lime_full,marginal,0.1313,3,3
xgb,shap-lime_full,mean,0.1062,3,3
xgb,shap-lime_full,zero,0.1062,3,3

