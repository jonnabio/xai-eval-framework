# Post-hoc measurement controls (cohort B2)

Dataset: german_credit; rows: 831; masking rows: 3,324

## Stability by measure and concentration (means over instances)

model,explainer,stab_cosine,stab_cosine_nonzero,stab_spearman,stab_top5_jaccard,zero_vectors,top5_share,entropy_norm
mlp,dice,0.2156,0.2156,0.1259,0.1052,0,0.9969,0.1193
mlp,shap,0.7608,0.7608,0.5368,0.4589,0,0.7525,0.4989
rf,anchors,0.7076,0.7076,0.6171,0.6409,0,0.6766,0.4909
rf,lime,0.9097,0.9097,0.7642,0.7005,0,0.7439,0.5135
rf,shap,0.9845,0.9845,0.9685,0.8158,0,0.4967,0.7628
svm,anchors,0.7138,0.7138,0.6869,0.596,0,0.8171,0.3517
svm,dice,0.3024,0.3024,0.1949,0.1585,0,0.9982,0.08233
svm,lime,0.892,0.892,0.8044,0.667,0,0.7202,0.5209
svm,lime_full,0.9805,0.9805,0.8322,0.8089,0,0.332,0.8869


## Top-5 masking: SHAP minus X, mean of cell means, and cells with SHAP ahead

model,contrast,scheme,gap_mean,cells,cells_shap_ahead
rf,shap-anchors,grouped_mean,0.01204,1,1
rf,shap-anchors,marginal,0.02662,1,1
rf,shap-anchors,mean,0.02952,1,1
rf,shap-anchors,zero,0.0458,1,1
mlp,shap-dice,grouped_mean,0.2779,1,1
mlp,shap-dice,marginal,0.2483,1,1
mlp,shap-dice,mean,0.308,1,1
mlp,shap-dice,zero,0.358,1,1
rf,shap-lime,grouped_mean,0.03002,1,1
rf,shap-lime,marginal,0.006404,1,1
rf,shap-lime,mean,0.03558,1,1
rf,shap-lime,zero,0.0404,1,1

