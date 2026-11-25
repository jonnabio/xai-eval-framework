# Supplementary material

**Do Explainers Agree on Which Features Matter? Instance-Level Agreement between SHAP and LIME** (revision 1). Every value below is generated from the files of the archive (https://doi.org/10.5281/zenodo.24518192, release `paper-e-aair-2026-11-24-r1`); the code that produces each table is named with it.

## S1. Models

Hyperparameters read from the model binaries used by the study.

| Dataset | Model | Fit | Hyperparameters |
|---|---|---|---|
| Adult | LogisticRegression | seed-42 partition (all seeds) | C = 1.0; penalty = l2; solver = lbfgs; max_iter = 1000 |
| Adult | SVC | seed-42 partition (all seeds) | C = 1.0; kernel = rbf; gamma = scale; probability = True |
| Adult | MLPClassifier | seed-42 partition (all seeds) | hidden_layer_sizes = [100]; activation = relu; alpha = 0.0001; max_iter = 500 |
| Adult | RandomForestClassifier | seed-42 partition (all seeds) | n_estimators = 50; max_depth = 15; min_samples_leaf = 1 |
| Adult | XGBClassifier | seed-42 partition (all seeds) | n_estimators = 100; max_depth = 6; learning_rate = 0.1 |
| German Credit | RandomForestClassifier | seed 42 | n_estimators = 100; max_depth = None; min_samples_leaf = 1 |
| German Credit | RandomForestClassifier | seed 123 | n_estimators = 100; max_depth = None; min_samples_leaf = 1 |
| German Credit | RandomForestClassifier | seed 456 | n_estimators = 100; max_depth = None; min_samples_leaf = 1 |
| German Credit | XGBClassifier | seed 42 | n_estimators = 100; max_depth = 4; learning_rate = 0.1 |
| German Credit | XGBClassifier | seed 123 | n_estimators = 100; max_depth = 4; learning_rate = 0.1 |
| German Credit | XGBClassifier | seed 456 | n_estimators = 100; max_depth = 4; learning_rate = 0.1 |
| Breast Cancer | RandomForestClassifier | seed 42 | n_estimators = 100; max_depth = None; min_samples_leaf = 1 |
| Breast Cancer | RandomForestClassifier | seed 123 | n_estimators = 100; max_depth = None; min_samples_leaf = 1 |
| Breast Cancer | RandomForestClassifier | seed 456 | n_estimators = 100; max_depth = None; min_samples_leaf = 1 |
| Breast Cancer | XGBClassifier | seed 42 | n_estimators = 100; max_depth = 4; learning_rate = 0.1 |
| Breast Cancer | XGBClassifier | seed 123 | n_estimators = 100; max_depth = 4; learning_rate = 0.1 |
| Breast Cancer | XGBClassifier | seed 456 | n_estimators = 100; max_depth = 4; learning_rate = 0.1 |

## S2. Explainer configurations

| Explainer | Settings | Source |
|---|---|---|
| SHAP (RF, XGB) | TreeSHAP, interventional, probability of class 1; 50 background instances from the training data | configs/experiments/exp2_comparative/*_shap.yaml; src/xai/shap_tabular.py |
| SHAP (LR, SVM, MLP) | KernelSHAP, probability of class 1; 50 background instances | configs/experiments/exp2_comparative/*_shap.yaml; src/xai/shap_tabular.py |
| LIME (study) | kernel width 3; 1000 samples; ten features; discretize_continuous = False; auto feature selection | configs/experiments/exp2_comparative/*_lime.yaml; src/xai/lime_tabular.py |
| LIME (settings analysis) | w3_5k, w3_10k: width 3, no discretisation, 5000 / 10000 samples; wd_5k: default width 0.75*sqrt(p), no discretisation, 5000; package: default width, quartile discretisation, 5000; random states 1001 and 2002 | docs/reports/paper_e/scripts/paper_e_lime_settings.py |
| Anchors (Adult) | precision threshold 0.95 | configs/experiments/exp2_comparative/*_anchors.yaml; src/xai/anchors_wrapper.py |
| DiCE (Adult) | method random; one counterfactual; desired class opposite | src/xai/dice_wrapper.py |

## S3. Agreement measures

For one instance, $S_k$ and $L_k$ are the sets of the $k$ features with the largest absolute SHAP and LIME values. **Top-k Jaccard** $J_k = |S_k \cap L_k| / |S_k \cup L_k|$, $k = 5$ (primary) and $k = 10$. **Kendall's $\tau_b$** on the union of the two top-10 lists, absent features at rank 11, ties as midranks. **Sign agreement**: share of the features of $S_5 \cap L_5$ with both values non-zero whose signs agree; post hoc, the LIME slope $w_j$ converted into a contribution $c_j = w_j (x_j - m_j)/s_j$. **Permutation reference**: the SHAP list of an instance against the LIME list of another instance of the same run (20 draws per instance), and, in S5, of the same predicted class. **Self-agreement**: two runs of a method with different random states on the same instance. Aggregation: run means; mean of run means; 95% interval from a percentile bootstrap over seeds (2000 resamples). Code: `scripts/analyze_paper_e.py` (`primary_agreement`).

## S4. Adult: primary measures on held-out instances (post hoc)

Held-out: instances that are not rows of the seed-42 training partition; a run enters a cell with at least 10 instances. Code: `paper_e_revision1_analyses.py`.

| Model | Subset | Runs | Pairs | Top-5 Jaccard | Top-10 Jaccard | Kendall τb |
|---|---|---|---|---|---|---|
| LR | all | 15 | 7000 | 0.485 [0.464, 0.505] | 0.617 [0.587, 0.638] | 0.263 [0.221, 0.304] |
| LR | heldout | 15 | 2526 | 0.478 [0.447, 0.509] | 0.624 [0.596, 0.650] | 0.256 [0.201, 0.309] |
| LR | train | 12 | 4474 | 0.480 [0.464, 0.499] | 0.607 [0.573, 0.628] | 0.252 [0.204, 0.300] |
| SVM | all | 14 | 2064 | 0.395 [0.387, 0.404] | 0.516 [0.487, 0.539] | 0.171 [0.148, 0.187] |
| SVM | heldout | 12 | 852 | 0.395 [0.378, 0.410] | 0.515 [0.500, 0.529] | 0.168 [0.140, 0.193] |
| SVM | train | 11 | 1212 | 0.394 [0.384, 0.407] | 0.507 [0.473, 0.546] | 0.162 [0.144, 0.177] |
| MLP | all | 15 | 7000 | 0.335 [0.325, 0.341] | 0.441 [0.435, 0.448] | 0.043 [0.029, 0.054] |
| MLP | heldout | 15 | 2817 | 0.331 [0.324, 0.338] | 0.438 [0.433, 0.440] | 0.040 [0.032, 0.049] |
| MLP | train | 12 | 4183 | 0.335 [0.322, 0.346] | 0.442 [0.434, 0.454] | 0.043 [0.023, 0.061] |
| RF | all | 15 | 6603 | 0.389 [0.363, 0.415] | 0.560 [0.530, 0.590] | 0.129 [0.089, 0.168] |
| RF | heldout | 15 | 4248 | 0.402 [0.372, 0.434] | 0.550 [0.511, 0.589] | 0.133 [0.088, 0.178] |
| RF | train | 12 | 2355 | 0.364 [0.335, 0.389] | 0.566 [0.542, 0.586] | 0.110 [0.082, 0.142] |
| XGB | all | 15 | 7000 | 0.363 [0.328, 0.399] | 0.404 [0.384, 0.422] | 0.028 [−0.019, 0.071] |
| XGB | heldout | 15 | 2568 | 0.364 [0.328, 0.399] | 0.408 [0.394, 0.423] | 0.029 [−0.013, 0.068] |
| XGB | train | 12 | 4432 | 0.355 [0.313, 0.397] | 0.398 [0.376, 0.419] | 0.017 [−0.033, 0.068] |
| All | all | 74 | 29667 | 0.393 [0.377, 0.410] | 0.507 [0.488, 0.525] | 0.126 [0.098, 0.153] |
| All | heldout | 72 | 13011 | 0.394 [0.372, 0.415] | 0.507 [0.488, 0.523] | 0.123 [0.091, 0.155] |
| All | train | 59 | 16656 | 0.385 [0.371, 0.399] | 0.504 [0.485, 0.521] | 0.116 [0.093, 0.139] |

## S5. Permutation reference within the predicted class (post hoc)

| Dataset | Model | Paired | Other (any class) | Other (same class) | Instance-specific (same class) |
|---|---|---|---|---|---|
| Breast Cancer | RF | 0.738 | 0.653 | 0.655 | 0.082 [0.058, 0.115] |
| Breast Cancer | XGB | 0.690 | 0.647 | 0.647 | 0.043 [0.039, 0.047] |
| Adult | LR | 0.485 | 0.261 | 0.268 | 0.217 [0.205, 0.231] |
| Adult | MLP | 0.335 | 0.129 | 0.131 | 0.204 [0.196, 0.212] |
| Adult | RF | 0.389 | 0.201 | 0.204 | 0.185 [0.175, 0.195] |
| Adult | SVM | 0.395 | 0.209 | 0.209 | 0.186 [0.174, 0.195] |
| Adult | XGB | 0.363 | 0.219 | 0.224 | 0.139 [0.128, 0.148] |
| German Credit | RF | 0.464 | 0.339 | 0.337 | 0.127 [0.112, 0.156] |
| German Credit | XGB | 0.309 | 0.235 | 0.238 | 0.071 [0.060, 0.080] |
| Breast Cancer | All | 0.714 | 0.650 | 0.651 | 0.063 [0.052, 0.080] |
| Adult | All | 0.393 | 0.204 | 0.207 | 0.186 [0.180, 0.191] |
| German Credit | All | 0.387 | 0.287 | 0.288 | 0.099 [0.086, 0.115] |

## S6. Leave one seed out (post hoc)

All seeds, and in parentheses the smallest and largest estimate with one seed left out.

| Dataset | Model | Seeds | Top-5 Jaccard | Top-10 Jaccard | Kendall τb |
|---|---|---|---|---|---|
| Breast Cancer | RF | 3 | 0.738 (0.712 to 0.767) | 0.665 (0.652 to 0.676) | 0.526 (0.504 to 0.543) |
| Breast Cancer | XGB | 3 | 0.690 (0.638 to 0.730) | 0.673 (0.669 to 0.676) | 0.507 (0.485 to 0.532) |
| Adult | LR | 5 | 0.485 (0.478 to 0.492) | 0.617 (0.609 to 0.631) | 0.263 (0.249 to 0.282) |
| Adult | MLP | 5 | 0.335 (0.333 to 0.339) | 0.441 (0.437 to 0.442) | 0.043 (0.038 to 0.049) |
| Adult | RF | 5 | 0.389 (0.378 to 0.401) | 0.560 (0.550 to 0.574) | 0.129 (0.117 to 0.143) |
| Adult | SVM | 5 | 0.395 (0.391 to 0.398) | 0.516 (0.505 to 0.524) | 0.171 (0.163 to 0.178) |
| Adult | XGB | 5 | 0.363 (0.351 to 0.376) | 0.404 (0.398 to 0.412) | 0.028 (0.016 to 0.048) |
| German Credit | RF | 3 | 0.464 (0.461 to 0.471) | 0.542 (0.527 to 0.553) | 0.237 (0.229 to 0.249) |
| German Credit | XGB | 3 | 0.309 (0.273 to 0.346) | 0.419 (0.408 to 0.430) | 0.008 (−0.036 to 0.063) |
| Breast Cancer | All | 3 | 0.714 (0.675 to 0.735) | 0.669 (0.663 to 0.676) | 0.517 (0.495 to 0.537) |
| Adult | All | 5 | 0.393 (0.388 to 0.399) | 0.507 (0.501 to 0.516) | 0.126 (0.117 to 0.136) |
| German Credit | All | 3 | 0.387 (0.367 to 0.409) | 0.480 (0.467 to 0.492) | 0.122 (0.098 to 0.156) |

## S7. LIME settings (post hoc)

Top-5 Jaccard on the self-agreement subsample (760 instances). LIME self: two LIME runs with different random states; SHAP–LIME: mean of the four pairs of a SHAP and a LIME run; vs study: against the stored LIME list of the study. SHAP self-agreement for reference: Adult 0.782; German Credit 0.708; Breast Cancer 0.939. Code: `paper_e_lime_settings.py`.

| Dataset | Model | Setting | LIME self | SHAP–LIME | vs study |
|---|---|---|---|---|---|
| Adult | LR | Width 3, 1000 (study) | 0.774 | 0.475 | 0.736 |
| Adult | LR | Width 3, 5000 | 0.857 | 0.488 | 0.664 |
| Adult | LR | Width 3, 10000 | 0.921 | 0.480 | 0.611 |
| Adult | LR | Default width, 5000 | 0.967 | 0.494 | 0.462 |
| Adult | LR | Package defaults | 0.360 | 0.195 | 0.223 |
| Adult | MLP | Width 3, 1000 (study) | 0.526 | 0.346 | 0.507 |
| Adult | MLP | Width 3, 5000 | 0.593 | 0.339 | 0.500 |
| Adult | MLP | Width 3, 10000 | 0.688 | 0.340 | 0.444 |
| Adult | MLP | Default width, 5000 | 0.694 | 0.270 | 0.293 |
| Adult | MLP | Package defaults | 0.267 | 0.028 | 0.013 |
| Adult | RF | Width 3, 1000 (study) | 0.783 | 0.353 | 0.739 |
| Adult | RF | Width 3, 5000 | 0.853 | 0.467 | 0.570 |
| Adult | RF | Width 3, 10000 | 0.887 | 0.479 | 0.497 |
| Adult | RF | Default width, 5000 | 0.923 | 0.550 | 0.305 |
| Adult | RF | Package defaults | 0.516 | 0.319 | 0.236 |
| Adult | XGB | Width 3, 1000 (study) | 0.676 | 0.360 | 0.670 |
| Adult | XGB | Width 3, 5000 | 0.798 | 0.506 | 0.641 |
| Adult | XGB | Width 3, 10000 | 0.848 | 0.536 | 0.608 |
| Adult | XGB | Default width, 5000 | 0.808 | 0.577 | 0.364 |
| Adult | XGB | Package defaults | 0.200 | 0.113 | 0.147 |
| Adult | All | Width 3, 1000 (study) | 0.690 | 0.383 | 0.663 |
| Adult | All | Width 3, 5000 | 0.775 | 0.450 | 0.594 |
| Adult | All | Width 3, 10000 | 0.836 | 0.459 | 0.540 |
| Adult | All | Default width, 5000 | 0.848 | 0.473 | 0.356 |
| Adult | All | Package defaults | 0.336 | 0.164 | 0.155 |
| German Credit | RF | Width 3, 1000 (study) | 0.642 | 0.461 | 0.640 |
| German Credit | RF | Width 3, 5000 | 0.801 | 0.466 | 0.649 |
| German Credit | RF | Width 3, 10000 | 0.824 | 0.463 | 0.651 |
| German Credit | RF | Default width, 5000 | 0.827 | 0.440 | 0.568 |
| German Credit | RF | Package defaults | 0.801 | 0.331 | 0.360 |
| German Credit | XGB | Width 3, 1000 (study) | 0.643 | 0.309 | 0.664 |
| German Credit | XGB | Width 3, 5000 | 0.805 | 0.302 | 0.658 |
| German Credit | XGB | Width 3, 10000 | 0.816 | 0.301 | 0.633 |
| German Credit | XGB | Default width, 5000 | 0.863 | 0.304 | 0.556 |
| German Credit | XGB | Package defaults | 0.878 | 0.208 | 0.151 |
| German Credit | All | Width 3, 1000 (study) | 0.642 | 0.385 | 0.652 |
| German Credit | All | Width 3, 5000 | 0.803 | 0.384 | 0.653 |
| German Credit | All | Width 3, 10000 | 0.820 | 0.382 | 0.642 |
| German Credit | All | Default width, 5000 | 0.845 | 0.372 | 0.562 |
| German Credit | All | Package defaults | 0.839 | 0.269 | 0.256 |
| Breast Cancer | RF | Width 3, 1000 (study) | 0.825 | 0.733 | 0.812 |
| Breast Cancer | RF | Width 3, 5000 | 0.919 | 0.760 | 0.857 |
| Breast Cancer | RF | Width 3, 10000 | 0.933 | 0.759 | 0.855 |
| Breast Cancer | RF | Default width, 5000 | 0.931 | 0.757 | 0.856 |
| Breast Cancer | RF | Package defaults | 0.858 | 0.695 | 0.707 |
| Breast Cancer | XGB | Width 3, 1000 (study) | 0.847 | 0.696 | 0.872 |
| Breast Cancer | XGB | Width 3, 5000 | 0.919 | 0.702 | 0.884 |
| Breast Cancer | XGB | Width 3, 10000 | 0.933 | 0.703 | 0.886 |
| Breast Cancer | XGB | Default width, 5000 | 0.915 | 0.720 | 0.882 |
| Breast Cancer | XGB | Package defaults | 0.883 | 0.711 | 0.702 |
| Breast Cancer | All | Width 3, 1000 (study) | 0.836 | 0.715 | 0.842 |
| Breast Cancer | All | Width 3, 5000 | 0.919 | 0.731 | 0.870 |
| Breast Cancer | All | Width 3, 10000 | 0.933 | 0.731 | 0.871 |
| Breast Cancer | All | Default width, 5000 | 0.923 | 0.738 | 0.869 |
| Breast Cancer | All | Package defaults | 0.870 | 0.703 | 0.704 |

## S8. Reproduction

From the repository root, with the archive of the release:

```
python docs/reports/paper_e/scripts/paper_e_revision1_analyses.py
python scripts/train_exp3_models.py --model-root <dir> --data-cache-dir data
python docs/reports/paper_e/scripts/paper_e_lime_settings.py --exp3-model-root <dir>
python docs/reports/paper_e/aair_journal/scripts/build_paper_e_aair_docx.py
python docs/reports/paper_e/aair_journal/revision_1/scripts/build_supplement.py --exp3-model-root <dir>
```
