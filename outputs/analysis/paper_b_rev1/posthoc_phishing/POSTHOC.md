# Post-hoc measurement controls (cohort B2)

Dataset: phishing; rows: 7,440; masking rows: 29,760

## Stability by measure and concentration (means over instances)

model,explainer,stab_cosine,stab_cosine_nonzero,stab_spearman,stab_top5_jaccard,zero_vectors,top5_share,entropy_norm
logreg,anchors,0.9374,0.9374,0.9337,0.9062,0,0.9953,0.2445
logreg,dice,0.2535,0.2535,0.1773,0.1389,0,0.9402,0.2042
logreg,lime,0.8709,0.8709,0.7012,0.5412,0,0.7442,0.4982
logreg,lime_full,0.9889,0.9889,0.8811,0.9965,0,0.3448,0.8652
logreg,shap,0.8314,0.8314,0.5886,0.4555,0,0.7507,0.4801
mlp,anchors,0.8136,0.8136,0.7907,0.7249,0,0.9217,0.3128
mlp,dice,0.2045,0.2045,0.144,0.1148,0,0.97,0.1771
mlp,lime,0.8566,0.8566,0.6656,0.6455,0,0.7724,0.4901
mlp,lime_full,0.9624,0.9624,0.7027,0.9535,0,0.3765,0.8605
mlp,shap,0.6476,0.6476,0.455,0.4275,0,0.7441,0.4879
rf,anchors,0.8553,0.8553,0.846,0.7804,0,0.9724,0.2875
rf,dice,0.2837,0.2837,0.2166,0.1703,0,0.9842,0.1703
rf,lime,0.9214,0.9214,0.6242,0.6349,0,0.784,0.4765
rf,lime_full,0.932,0.932,0.4766,0.7097,0,0.4111,0.8316
rf,shap,1,1,1,1,0,0.5272,0.7194
svm,anchors,0.9554,0.9554,0.9524,0.9318,0,0.9937,0.2454
svm,dice,0.3065,0.3065,0.2105,0.1634,0,0.9144,0.2368
svm,lime,0.9029,0.9029,0.7081,0.5449,0,0.7488,0.4936
svm,lime_full,0.9886,0.9886,0.8935,0.8114,0,0.3419,0.8653
svm,shap,0.8559,0.8559,0.6206,0.5134,0,0.7587,0.4773
xgb,anchors,0.8893,0.8893,0.8792,0.8327,0,0.9755,0.2575
xgb,dice,0.2033,0.2033,0.2013,0.1507,0,0.9963,0.1279
xgb,lime,0.8992,0.8992,0.4676,0.4767,0,0.856,0.4137
xgb,lime_full,0.9,0.9,0.1903,0.5462,0,0.4594,0.803
xgb,shap,0.4063,0.4063,0.9506,0.5138,0,0.6238,0.6245


## Top-5 masking: SHAP minus X, mean of cell means, and cells with SHAP ahead

model,contrast,scheme,gap_mean,cells,cells_shap_ahead
logreg,shap-anchors,grouped_mean,-0.02288,3,1
logreg,shap-anchors,marginal,0.1013,3,3
logreg,shap-anchors,mean,0.06544,3,3
logreg,shap-anchors,zero,0.03586,3,3
mlp,shap-anchors,grouped_mean,0.09715,3,3
mlp,shap-anchors,marginal,0.1335,3,3
mlp,shap-anchors,mean,0.166,3,3
mlp,shap-anchors,zero,0.09849,3,3
rf,shap-anchors,grouped_mean,-0.001123,3,1
rf,shap-anchors,marginal,0.08863,3,3
rf,shap-anchors,mean,0.09199,3,3
rf,shap-anchors,zero,0.009147,3,3
svm,shap-anchors,grouped_mean,-0.01054,3,0
svm,shap-anchors,marginal,0.08184,3,3
svm,shap-anchors,mean,0.08553,3,3
svm,shap-anchors,zero,0.02221,3,3
xgb,shap-anchors,grouped_mean,0.3008,3,3
xgb,shap-anchors,marginal,0.1102,3,3
xgb,shap-anchors,mean,0.3159,3,3
xgb,shap-anchors,zero,0.3159,3,3
logreg,shap-dice,grouped_mean,0.1865,3,3
logreg,shap-dice,marginal,0.2218,3,3
logreg,shap-dice,mean,0.2869,3,3
logreg,shap-dice,zero,0.2128,3,3
mlp,shap-dice,grouped_mean,0.303,3,3
mlp,shap-dice,marginal,0.2583,3,3
mlp,shap-dice,mean,0.34,3,3
mlp,shap-dice,zero,0.2539,3,3
rf,shap-dice,grouped_mean,0.1408,3,3
rf,shap-dice,marginal,0.2364,3,3
rf,shap-dice,mean,0.2391,3,3
rf,shap-dice,zero,0.1484,3,3
svm,shap-dice,grouped_mean,0.1867,3,3
svm,shap-dice,marginal,0.2191,3,3
svm,shap-dice,mean,0.3084,3,3
svm,shap-dice,zero,0.2488,3,3
xgb,shap-dice,grouped_mean,0.1483,3,3
xgb,shap-dice,marginal,0.2568,3,3
xgb,shap-dice,mean,0.1663,3,3
xgb,shap-dice,zero,0.1663,3,3
logreg,shap-lime,grouped_mean,0.1024,3,3
logreg,shap-lime,marginal,0.03951,3,2
logreg,shap-lime,mean,0.1555,3,3
logreg,shap-lime,zero,0.0756,3,3
mlp,shap-lime,grouped_mean,0.2285,3,3
mlp,shap-lime,marginal,0.1067,3,3
mlp,shap-lime,mean,0.2839,3,3
mlp,shap-lime,zero,0.2106,3,3
rf,shap-lime,grouped_mean,0.05514,3,3
rf,shap-lime,marginal,0.08385,3,3
rf,shap-lime,mean,0.09709,3,3
rf,shap-lime,zero,0.04722,3,3
svm,shap-lime,grouped_mean,0.1278,3,3
svm,shap-lime,marginal,0.02265,3,1
svm,shap-lime,mean,0.1807,3,3
svm,shap-lime,zero,0.09873,3,3
xgb,shap-lime,grouped_mean,0.1208,3,3
xgb,shap-lime,marginal,0.0807,3,3
xgb,shap-lime,mean,0.1312,3,3
xgb,shap-lime,zero,0.1312,3,3
logreg,shap-lime_full,grouped_mean,0.09596,3,3
logreg,shap-lime_full,marginal,0.0386,3,2
logreg,shap-lime_full,mean,0.1656,3,3
logreg,shap-lime_full,zero,0.1268,3,3
mlp,shap-lime_full,grouped_mean,0.2215,3,3
mlp,shap-lime_full,marginal,0.1158,3,3
mlp,shap-lime_full,mean,0.2908,3,3
mlp,shap-lime_full,zero,0.2237,3,3
rf,shap-lime_full,grouped_mean,0.07027,3,3
rf,shap-lime_full,marginal,0.06425,3,3
rf,shap-lime_full,mean,0.123,3,3
rf,shap-lime_full,zero,0.04889,3,3
svm,shap-lime_full,grouped_mean,0.1265,3,3
svm,shap-lime_full,marginal,0.07927,3,3
svm,shap-lime_full,mean,0.2151,3,3
svm,shap-lime_full,zero,0.1401,3,3
xgb,shap-lime_full,grouped_mean,0.1221,3,3
xgb,shap-lime_full,marginal,0.08686,3,3
xgb,shap-lime_full,mean,0.1326,3,3
xgb,shap-lime_full,zero,0.1326,3,3

