# Post-hoc measurement controls (cohort B2)

Dataset: connect4; rows: 7,497; masking rows: 29,988

## Stability by measure and concentration (means over instances)

model,explainer,stab_cosine,stab_cosine_nonzero,stab_spearman,stab_top5_jaccard,zero_vectors,top5_share,entropy_norm
logreg,anchors,0.7383,0.7383,0.7267,0.5969,0,0.8538,0.296
logreg,dice,0.05781,0.05781,0.03758,0.03453,0,0.9932,0.1102
logreg,lime,0.6051,0.6051,0.6243,0.3581,0,0.6815,0.4525
logreg,lime_full,0.9815,0.9815,0.8806,0.8825,0,0.1739,0.9018
logreg,shap,0.7298,0.7298,0.4409,0.4634,0,0.7813,0.4178
mlp,anchors,0.6687,0.6687,0.6419,0.4821,0,0.6582,0.4098
mlp,dice,0.05122,0.05122,0.03219,0.03108,0,0.9985,0.09242
mlp,lime,0.4467,0.4467,0.3908,0.2554,0,0.711,0.4457
mlp,lime_full,0.8298,0.8298,0.5341,0.4791,0,0.1542,0.9199
mlp,shap,0.4845,0.4845,0.2597,0.2455,0,0.7656,0.4177
rf,anchors,0.6761,0.6761,0.6586,0.514,0,0.723,0.3821
rf,dice,0.1927,0.1927,0.1482,0.1133,0,0.9717,0.1403
rf,lime,0.7185,0.7192,0.5467,0.4525,0.2222,0.6851,0.45
rf,lime_full,0.8249,0.8251,0.4257,0.4333,0.25,0.1998,0.8888
rf,shap,1,1,1,1,0,0.4155,0.7146
svm,anchors,0.7666,0.7666,0.756,0.6225,0,0.8041,0.3375
svm,dice,0.1305,0.1305,0.09127,0.07231,0,0.9837,0.1308
svm,lime,0.6653,0.6653,0.6644,0.386,0,0.6785,0.4536
svm,lime_full,0.963,0.963,0.7961,0.6046,0,0.161,0.8976
svm,shap,0.7888,0.7888,0.5228,0.5306,0,0.7584,0.4254
xgb,anchors,0.7183,0.7183,0.7024,0.5581,0,0.7505,0.3646
xgb,dice,0.08374,0.08374,0.06032,0.04959,0,0.9781,0.1342
xgb,lime,0.6063,0.5792,0.4584,0.39,0.3611,0.7425,0.4387
xgb,lime_full,0.6507,0.6379,0.2599,0.6223,0.3333,0.2118,0.9032
xgb,shap,0.4777,0.4777,0.926,0.4052,0,0.4159,0.7083


## Top-5 masking: SHAP minus X, mean of cell means, and cells with SHAP ahead

model,contrast,scheme,gap_mean,cells,cells_shap_ahead
logreg,shap-anchors,grouped_mean,-0.1005,3,0
logreg,shap-anchors,marginal,-0.06633,3,0
logreg,shap-anchors,mean,-0.1111,3,0
logreg,shap-anchors,zero,-0.1008,3,0
mlp,shap-anchors,grouped_mean,0.17,3,3
mlp,shap-anchors,marginal,0.1738,3,3
mlp,shap-anchors,mean,0.1625,3,3
mlp,shap-anchors,zero,0.1966,3,3
rf,shap-anchors,grouped_mean,0.01669,3,2
rf,shap-anchors,marginal,0.002853,3,2
rf,shap-anchors,mean,0.02462,3,3
rf,shap-anchors,zero,0.02233,3,3
svm,shap-anchors,grouped_mean,-0.03887,3,1
svm,shap-anchors,marginal,-0.03832,3,0
svm,shap-anchors,mean,-0.06743,3,0
svm,shap-anchors,zero,-0.04439,3,0
xgb,shap-anchors,grouped_mean,-0.05141,3,0
xgb,shap-anchors,marginal,-0.04259,3,0
xgb,shap-anchors,mean,-0.05375,3,0
xgb,shap-anchors,zero,-0.05375,3,0
logreg,shap-dice,grouped_mean,0.1827,3,3
logreg,shap-dice,marginal,0.1765,3,3
logreg,shap-dice,mean,0.184,3,3
logreg,shap-dice,zero,0.2272,3,3
mlp,shap-dice,grouped_mean,0.4444,3,3
mlp,shap-dice,marginal,0.4746,3,3
mlp,shap-dice,mean,0.5152,3,3
mlp,shap-dice,zero,0.5477,3,3
rf,shap-dice,grouped_mean,0.07455,3,3
rf,shap-dice,marginal,0.07309,3,3
rf,shap-dice,mean,0.1121,3,3
rf,shap-dice,zero,0.1084,3,3
svm,shap-dice,grouped_mean,0.2601,3,3
svm,shap-dice,marginal,0.2319,3,3
svm,shap-dice,mean,0.2665,3,3
svm,shap-dice,zero,0.3196,3,3
xgb,shap-dice,grouped_mean,0.04803,3,3
xgb,shap-dice,marginal,0.07004,3,3
xgb,shap-dice,mean,0.07947,3,3
xgb,shap-dice,zero,0.07947,3,3
logreg,shap-lime,grouped_mean,0.09464,3,3
logreg,shap-lime,marginal,0.05811,3,3
logreg,shap-lime,mean,0.07727,3,3
logreg,shap-lime,zero,0.1089,3,3
mlp,shap-lime,grouped_mean,0.3112,3,3
mlp,shap-lime,marginal,0.285,3,3
mlp,shap-lime,mean,0.3706,3,3
mlp,shap-lime,zero,0.3641,3,3
rf,shap-lime,grouped_mean,0.02867,3,3
rf,shap-lime,marginal,0.02654,3,3
rf,shap-lime,mean,0.03877,3,3
rf,shap-lime,zero,0.03604,3,3
svm,shap-lime,grouped_mean,0.1826,3,3
svm,shap-lime,marginal,0.1214,3,3
svm,shap-lime,mean,0.1507,3,3
svm,shap-lime,zero,0.1769,3,3
xgb,shap-lime,grouped_mean,0.06834,3,3
xgb,shap-lime,marginal,0.07711,3,3
xgb,shap-lime,mean,0.08408,3,3
xgb,shap-lime,zero,0.08408,3,3
logreg,shap-lime_full,grouped_mean,0.167,3,3
logreg,shap-lime_full,marginal,0.1214,3,3
logreg,shap-lime_full,mean,0.1391,3,3
logreg,shap-lime_full,zero,0.1967,3,3
mlp,shap-lime_full,grouped_mean,0.3972,3,3
mlp,shap-lime_full,marginal,0.4491,3,3
mlp,shap-lime_full,mean,0.4332,3,3
mlp,shap-lime_full,zero,0.5494,3,3
rf,shap-lime_full,grouped_mean,0.04457,3,3
rf,shap-lime_full,marginal,0.04109,3,3
rf,shap-lime_full,mean,0.06569,3,3
rf,shap-lime_full,zero,0.06295,3,3
svm,shap-lime_full,grouped_mean,0.2522,3,3
svm,shap-lime_full,marginal,0.1771,3,3
svm,shap-lime_full,mean,0.2258,3,3
svm,shap-lime_full,zero,0.2797,3,3
xgb,shap-lime_full,grouped_mean,0.07443,3,3
xgb,shap-lime_full,marginal,0.1115,3,3
xgb,shap-lime_full,mean,0.09994,3,3
xgb,shap-lime_full,zero,0.09994,3,3

