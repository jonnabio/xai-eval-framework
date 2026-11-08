# Supplementary material

*When Does SHAP Outperform LIME? Model- and Configuration-Dependent Results from a Paired Tabular Benchmark.* Manuscript 2067810, *Computers and Informatics*, revision 1.

This file is independent of the paper: it states the whole design and every result at the level of dataset, model and seed, so that each number in the paper can be checked. Repository and archive addresses are withheld for masked review.

Design fingerprint (SHA-256 of the design configuration): `4ab8673a4a205aaf70ac514a83a21abb59c9ff951a111a6679a85dfe4d97a1fa`. Every result row carries it; the analysis refuses rows of another design.

## S1. Design

| Item | Setting |
|---|---|
| Split | one stratified split per dataset, test share 0.2, seed 42; shared by preprocessing, training and every seed |
| Training cap | 20,000 rows (stratified subsample of the training split) |
| Seeds | Adult: (11, 22, 33, 44, 55); other datasets: (11, 22, 33) |
| Instances | up to 25 per stratum (TP, TN, FP, FN) of the test split; smaller strata taken whole |
| Stability subset | first 3 instances per stratum |
| Stability | T = 15 perturbed copies, Gaussian noise sigma = 0.1 on the encoded features |
| Faithfulness gap | top k = 5 features masked together |
| Sparsity threshold | 0.0001 |
| Timing subset | 5 instances per stratum, 3 repetitions, 1 warm-up per explainer, one process, one thread, pinned to one core |

## S2. Datasets

| Dataset | Source | Train rows | Test rows | Encoded features | Positive share | Role |
|---|---|---:|---:|---:|---:|---|
| Adult | UCI | 39,032 | 9,758 | 108 | 0.239 | primary |
| Breast Cancer | UCI | 455 | 114 | 30 | 0.627 | further |
| German Credit | UCI | 800 | 200 | 61 | 0.700 | further |
| Diabetes | OpenML 37 | 614 | 154 | 8 | 0.349 | numeric, lower dimension |
| Spambase | OpenML 44 | 3,680 | 921 | 57 | 0.394 | numeric, higher dimension |
| Phishing | OpenML 4534 | 8,844 | 2,211 | 68 | 0.557 | categorical, lower dimension |
| Connect-4 | OpenML 40668 | 54,045 | 13,512 | 126 | 0.658 | categorical, higher dimension |

Train rows are those available before the training cap. Connect-4: a win is the positive class; loss and draw are the negative class.

## S3. Models

| Model | Class | Hyperparameters |
|---|---|---|
| Logistic regression | `sklearn.linear_model.LogisticRegression` | solver=lbfgs, max_iter=1000, random_state=42 |
| Random forest | `sklearn.ensemble.RandomForestClassifier` | n_estimators=100, max_depth=15, random_state=42, n_jobs=1 |
| XGBoost | `xgboost.XGBClassifier` | n_estimators=100, max_depth=6, learning_rate=0.1, objective=binary:logistic, eval_metric=logloss, random_state=42, n_jobs=1 |
| SVM (RBF) | `sklearn.svm.SVC` | C=1.0, kernel=rbf, probability=True, random_state=42 |
| MLP | `sklearn.neural_network.MLPClassifier` | hidden_layer_sizes=(100), max_iter=500, random_state=42 |

Test accuracy of the frozen models:

| Dataset | Logistic regression | Random forest | XGBoost | SVM (RBF) | MLP |
|---|---:|---:|---:|---:|---:|
| Adult | 0.8500 | 0.8580 | 0.8666 | 0.8526 | 0.8240 |
| Breast Cancer | 0.9825 | 0.9561 | 0.9474 | 0.9825 | 0.9649 |
| German Credit | 0.7050 | 0.7400 | 0.7400 | 0.7400 | 0.7400 |
| Diabetes | 0.7143 | 0.7532 | 0.7662 | 0.7532 | 0.7078 |
| Spambase | 0.9294 | 0.9425 | 0.9468 | 0.9273 | 0.9392 |
| Phishing | 0.9398 | 0.9715 | 0.9665 | 0.9593 | 0.9742 |
| Connect-4 | 0.7979 | 0.8290 | 0.8529 | 0.8490 | 0.8676 |

## S4. Explainers

| Variant | Settings |
|---|---|
| shap | method=shap, n_background_samples=50, kernel_nsamples=500 |
| lime | method=lime, num_samples=1000, num_features=10, kernel_width=default |
| lime_full | method=lime, num_samples=1000, num_features=all, kernel_width=default |
| anchors | method=anchors, threshold=0.95 |
| dice | method=dice, num_counterfactuals=1 |

SHAP uses TreeSHAP for the random forest and XGBoost and KernelSHAP otherwise. LIME's default kernel width is 0.75 times the square root of the number of encoded features. Anchors: the attribution vector marks the anchor's features with 1. DiCE: the attribution of a feature is the absolute change in the counterfactual.

## S5. Computing environment

One laptop for every run: AMD Ryzen 5 4600H (6 cores, 12 threads, 3.0 GHz base), 31.4 GB RAM, Windows 11 Home 10.0.26300, on mains power. CPython 3.11.11; scikit-learn 1.7.1, XGBoost 3.1.2, SHAP 0.50.0, LIME 0.2.0.1, NumPy 2.2.6, pandas 2.3.3, SciPy 1.16.3, alibi 0.9.6, dice-ml 0.12. The full frozen environment is part of the artifacts.

## S6. Model and data fingerprints

Each run checks the model file against these hashes before it starts.

| Dataset | Model | Model SHA-256 (first 16) | Data SHA-256 (first 16) |
|---|---|---|---|
| Adult | Logistic regression | `c06174920a8dfa75` | `18b42fcbbcf14068` |
| Adult | MLP | `329f273fa5d5688a` | `18b42fcbbcf14068` |
| Adult | Random forest | `a2dd7551756486ea` | `18b42fcbbcf14068` |
| Adult | rf_d6 | `48e5d53de3368649` | `18b42fcbbcf14068` |
| Adult | SVM (RBF) | `2b0a0c6b236bd11d` | `18b42fcbbcf14068` |
| Adult | XGBoost | `6fa7994e30549e68` | `18b42fcbbcf14068` |
| Adult | xgb_d15 | `deef8fd516743635` | `18b42fcbbcf14068` |
| Breast Cancer | Logistic regression | `571aaf8bb37da91f` | `765348e4109f0b13` |
| Breast Cancer | MLP | `9e7838f9c2a4616e` | `765348e4109f0b13` |
| Breast Cancer | Random forest | `ece4da48e4fcc84d` | `765348e4109f0b13` |
| Breast Cancer | SVM (RBF) | `273b476e04b1f1dd` | `765348e4109f0b13` |
| Breast Cancer | XGBoost | `1d03c4d9da6ab8a9` | `765348e4109f0b13` |
| Connect-4 | Logistic regression | `873e0b72df24adfc` | `e438bafb45e36a75` |
| Connect-4 | MLP | `d737986b44181bc3` | `e438bafb45e36a75` |
| Connect-4 | Random forest | `213c98dad25a4fc7` | `e438bafb45e36a75` |
| Connect-4 | SVM (RBF) | `0cbc54c363e606c5` | `e438bafb45e36a75` |
| Connect-4 | XGBoost | `6d0ea32aa008aa18` | `e438bafb45e36a75` |
| Diabetes | Logistic regression | `a991171cff6e2c47` | `f9f1195b4e6a9677` |
| Diabetes | MLP | `6e2d11ebedfcff6c` | `f9f1195b4e6a9677` |
| Diabetes | Random forest | `006d37382f8dfe45` | `f9f1195b4e6a9677` |
| Diabetes | SVM (RBF) | `82d2e966fea86ace` | `f9f1195b4e6a9677` |
| Diabetes | XGBoost | `51545d5ae1130e5a` | `f9f1195b4e6a9677` |
| German Credit | Logistic regression | `f94432191bc002cf` | `04b09e7ae7547830` |
| German Credit | MLP | `4c406969284f6c6c` | `04b09e7ae7547830` |
| German Credit | Random forest | `fdbf9f1e3859d9c7` | `04b09e7ae7547830` |
| German Credit | SVM (RBF) | `0814b148809bf258` | `04b09e7ae7547830` |
| German Credit | XGBoost | `15ed0d95627e82d3` | `04b09e7ae7547830` |
| Phishing | Logistic regression | `b691431585152391` | `9d93cc662c21ea41` |
| Phishing | MLP | `11980a4dcd44ab8e` | `9d93cc662c21ea41` |
| Phishing | Random forest | `552a74bafd59aa88` | `9d93cc662c21ea41` |
| Phishing | SVM (RBF) | `b5ef782a7937d841` | `9d93cc662c21ea41` |
| Phishing | XGBoost | `c3583f6aef8d7f67` | `9d93cc662c21ea41` |
| Spambase | Logistic regression | `df2e6e9f26ecdc5b` | `89f80a488462e60e` |
| Spambase | MLP | `ec3acdf8a11764f8` | `89f80a488462e60e` |
| Spambase | Random forest | `b788ed367089fd13` | `89f80a488462e60e` |
| Spambase | SVM (RBF) | `9c3450727360d61a` | `89f80a488462e60e` |
| Spambase | XGBoost | `0b808e596faf5ff0` | `89f80a488462e60e` |

## S7. Realized instances

Quality pass: 575 of 575 jobs, 52,740 instance rows. Instances per stratum of the test split, for each dataset, model and seed (a stratum with fewer than 25 instances is taken whole), and the instances with stability computed:

| Dataset | Model | Seed | TP | TN | FP | FN | Stability |
|---|---|---:|---:|---:|---:|---:|---:|
| Adult | Logistic regression | 11 | 25 | 25 | 25 | 25 | 12 |
| Adult | Logistic regression | 22 | 25 | 25 | 25 | 25 | 12 |
| Adult | Logistic regression | 33 | 25 | 25 | 25 | 25 | 12 |
| Adult | Logistic regression | 44 | 25 | 25 | 25 | 25 | 12 |
| Adult | Logistic regression | 55 | 25 | 25 | 25 | 25 | 12 |
| Adult | Random forest | 11 | 25 | 25 | 25 | 25 | 12 |
| Adult | Random forest | 22 | 25 | 25 | 25 | 25 | 12 |
| Adult | Random forest | 33 | 25 | 25 | 25 | 25 | 12 |
| Adult | Random forest | 44 | 25 | 25 | 25 | 25 | 12 |
| Adult | Random forest | 55 | 25 | 25 | 25 | 25 | 12 |
| Adult | XGBoost | 11 | 25 | 25 | 25 | 25 | 12 |
| Adult | XGBoost | 22 | 25 | 25 | 25 | 25 | 12 |
| Adult | XGBoost | 33 | 25 | 25 | 25 | 25 | 12 |
| Adult | XGBoost | 44 | 25 | 25 | 25 | 25 | 12 |
| Adult | XGBoost | 55 | 25 | 25 | 25 | 25 | 12 |
| Adult | SVM (RBF) | 11 | 25 | 25 | 25 | 25 | 12 |
| Adult | SVM (RBF) | 22 | 25 | 25 | 25 | 25 | 12 |
| Adult | SVM (RBF) | 33 | 25 | 25 | 25 | 25 | 12 |
| Adult | SVM (RBF) | 44 | 25 | 25 | 25 | 25 | 12 |
| Adult | SVM (RBF) | 55 | 25 | 25 | 25 | 25 | 12 |
| Adult | MLP | 11 | 25 | 25 | 25 | 25 | 12 |
| Adult | MLP | 22 | 25 | 25 | 25 | 25 | 12 |
| Adult | MLP | 33 | 25 | 25 | 25 | 25 | 12 |
| Adult | MLP | 44 | 25 | 25 | 25 | 25 | 12 |
| Adult | MLP | 55 | 25 | 25 | 25 | 25 | 12 |
| Breast Cancer | Logistic regression | 11 | 25 | 25 | 1 | 1 | 8 |
| Breast Cancer | Logistic regression | 22 | 25 | 25 | 1 | 1 | 8 |
| Breast Cancer | Logistic regression | 33 | 25 | 25 | 1 | 1 | 8 |
| Breast Cancer | Random forest | 11 | 25 | 25 | 3 | 2 | 11 |
| Breast Cancer | Random forest | 22 | 25 | 25 | 3 | 2 | 11 |
| Breast Cancer | Random forest | 33 | 25 | 25 | 3 | 2 | 11 |
| Breast Cancer | XGBoost | 11 | 25 | 25 | 4 | 2 | 11 |
| Breast Cancer | XGBoost | 22 | 25 | 25 | 4 | 2 | 11 |
| Breast Cancer | XGBoost | 33 | 25 | 25 | 4 | 2 | 11 |
| Breast Cancer | SVM (RBF) | 11 | 25 | 25 | 1 | 1 | 8 |
| Breast Cancer | SVM (RBF) | 22 | 25 | 25 | 1 | 1 | 8 |
| Breast Cancer | SVM (RBF) | 33 | 25 | 25 | 1 | 1 | 8 |
| Breast Cancer | MLP | 11 | 25 | 25 | 1 | 3 | 10 |
| Breast Cancer | MLP | 22 | 25 | 25 | 1 | 3 | 10 |
| Breast Cancer | MLP | 33 | 25 | 25 | 1 | 3 | 10 |
| German Credit | Logistic regression | 11 | 25 | 25 | 25 | 25 | 12 |
| German Credit | Logistic regression | 22 | 25 | 25 | 25 | 25 | 12 |
| German Credit | Logistic regression | 33 | 25 | 25 | 25 | 25 | 12 |
| German Credit | Random forest | 11 | 25 | 25 | 25 | 18 | 12 |
| German Credit | Random forest | 22 | 25 | 25 | 25 | 18 | 12 |
| German Credit | Random forest | 33 | 25 | 25 | 25 | 18 | 12 |
| German Credit | XGBoost | 11 | 25 | 25 | 25 | 21 | 12 |
| German Credit | XGBoost | 22 | 25 | 25 | 25 | 21 | 12 |
| German Credit | XGBoost | 33 | 25 | 25 | 25 | 21 | 12 |
| German Credit | SVM (RBF) | 11 | 25 | 23 | 25 | 15 | 12 |
| German Credit | SVM (RBF) | 22 | 25 | 23 | 25 | 15 | 12 |
| German Credit | SVM (RBF) | 33 | 25 | 23 | 25 | 15 | 12 |
| German Credit | MLP | 11 | 25 | 25 | 25 | 25 | 12 |
| German Credit | MLP | 22 | 25 | 25 | 25 | 25 | 12 |
| German Credit | MLP | 33 | 25 | 25 | 25 | 25 | 12 |
| Diabetes | Logistic regression | 11 | 25 | 25 | 18 | 25 | 12 |
| Diabetes | Logistic regression | 22 | 25 | 25 | 18 | 25 | 12 |
| Diabetes | Logistic regression | 33 | 25 | 25 | 18 | 25 | 12 |
| Diabetes | Random forest | 11 | 25 | 25 | 15 | 23 | 12 |
| Diabetes | Random forest | 22 | 25 | 25 | 15 | 23 | 12 |
| Diabetes | Random forest | 33 | 25 | 25 | 15 | 23 | 12 |
| Diabetes | XGBoost | 11 | 25 | 25 | 16 | 20 | 12 |
| Diabetes | XGBoost | 22 | 25 | 25 | 16 | 20 | 12 |
| Diabetes | XGBoost | 33 | 25 | 25 | 16 | 20 | 12 |
| Diabetes | SVM (RBF) | 11 | 25 | 25 | 17 | 21 | 12 |
| Diabetes | SVM (RBF) | 22 | 25 | 25 | 17 | 21 | 12 |
| Diabetes | SVM (RBF) | 33 | 25 | 25 | 17 | 21 | 12 |
| Diabetes | MLP | 11 | 25 | 25 | 19 | 25 | 12 |
| Diabetes | MLP | 22 | 25 | 25 | 19 | 25 | 12 |
| Diabetes | MLP | 33 | 25 | 25 | 19 | 25 | 12 |
| Spambase | Logistic regression | 11 | 25 | 25 | 25 | 25 | 12 |
| Spambase | Logistic regression | 22 | 25 | 25 | 25 | 25 | 12 |
| Spambase | Logistic regression | 33 | 25 | 25 | 25 | 25 | 12 |
| Spambase | Random forest | 11 | 25 | 25 | 18 | 25 | 12 |
| Spambase | Random forest | 22 | 25 | 25 | 18 | 25 | 12 |
| Spambase | Random forest | 33 | 25 | 25 | 18 | 25 | 12 |
| Spambase | XGBoost | 11 | 25 | 25 | 24 | 25 | 12 |
| Spambase | XGBoost | 22 | 25 | 25 | 24 | 25 | 12 |
| Spambase | XGBoost | 33 | 25 | 25 | 24 | 25 | 12 |
| Spambase | SVM (RBF) | 11 | 25 | 25 | 25 | 25 | 12 |
| Spambase | SVM (RBF) | 22 | 25 | 25 | 25 | 25 | 12 |
| Spambase | SVM (RBF) | 33 | 25 | 25 | 25 | 25 | 12 |
| Spambase | MLP | 11 | 25 | 25 | 25 | 25 | 12 |
| Spambase | MLP | 22 | 25 | 25 | 25 | 25 | 12 |
| Spambase | MLP | 33 | 25 | 25 | 25 | 25 | 12 |
| Phishing | Logistic regression | 11 | 25 | 25 | 25 | 25 | 12 |
| Phishing | Logistic regression | 22 | 25 | 25 | 25 | 25 | 12 |
| Phishing | Logistic regression | 33 | 25 | 25 | 25 | 25 | 12 |
| Phishing | Random forest | 11 | 25 | 25 | 25 | 24 | 12 |
| Phishing | Random forest | 22 | 25 | 25 | 25 | 24 | 12 |
| Phishing | Random forest | 33 | 25 | 25 | 25 | 24 | 12 |
| Phishing | XGBoost | 11 | 25 | 25 | 25 | 25 | 12 |
| Phishing | XGBoost | 22 | 25 | 25 | 25 | 25 | 12 |
| Phishing | XGBoost | 33 | 25 | 25 | 25 | 25 | 12 |
| Phishing | SVM (RBF) | 11 | 25 | 25 | 25 | 25 | 12 |
| Phishing | SVM (RBF) | 22 | 25 | 25 | 25 | 25 | 12 |
| Phishing | SVM (RBF) | 33 | 25 | 25 | 25 | 25 | 12 |
| Phishing | MLP | 11 | 25 | 25 | 25 | 22 | 12 |
| Phishing | MLP | 22 | 25 | 25 | 25 | 22 | 12 |
| Phishing | MLP | 33 | 25 | 25 | 25 | 22 | 12 |
| Connect-4 | Logistic regression | 11 | 25 | 25 | 25 | 25 | 12 |
| Connect-4 | Logistic regression | 22 | 25 | 25 | 25 | 25 | 12 |
| Connect-4 | Logistic regression | 33 | 25 | 25 | 25 | 25 | 12 |
| Connect-4 | Random forest | 11 | 25 | 25 | 25 | 25 | 12 |
| Connect-4 | Random forest | 22 | 25 | 25 | 25 | 25 | 12 |
| Connect-4 | Random forest | 33 | 25 | 25 | 25 | 25 | 12 |
| Connect-4 | XGBoost | 11 | 25 | 25 | 25 | 25 | 12 |
| Connect-4 | XGBoost | 22 | 25 | 25 | 25 | 25 | 12 |
| Connect-4 | XGBoost | 33 | 25 | 25 | 25 | 25 | 12 |
| Connect-4 | SVM (RBF) | 11 | 25 | 25 | 25 | 25 | 12 |
| Connect-4 | SVM (RBF) | 22 | 25 | 25 | 25 | 25 | 12 |
| Connect-4 | SVM (RBF) | 33 | 25 | 25 | 25 | 25 | 12 |
| Connect-4 | MLP | 11 | 25 | 25 | 25 | 25 | 12 |
| Connect-4 | MLP | 22 | 25 | 25 | 25 | 25 | 12 |
| Connect-4 | MLP | 33 | 25 | 25 | 25 | 25 | 12 |

Overlap of the instance sets between seeds (Jaccard index over all pairs of seeds of the same dataset and model):

| Dataset | Model | Mean | Maximum |
|---|---|---:|---:|
| Adult | Logistic regression | 0.01 | 0.04 |
| Adult | Random forest | 0.01 | 0.02 |
| Adult | XGBoost | 0.02 | 0.03 |
| Adult | SVM (RBF) | 0.01 | 0.03 |
| Adult | MLP | 0.01 | 0.02 |
| Breast Cancer | Logistic regression | 0.32 | 0.37 |
| Breast Cancer | Random forest | 0.39 | 0.41 |
| Breast Cancer | XGBoost | 0.39 | 0.42 |
| Breast Cancer | SVM (RBF) | 0.32 | 0.37 |
| Breast Cancer | MLP | 0.33 | 0.35 |
| German Credit | Logistic regression | 0.54 | 0.55 |
| German Credit | Random forest | 0.53 | 0.55 |
| German Credit | XGBoost | 0.53 | 0.55 |
| German Credit | SVM (RBF) | 0.53 | 0.54 |
| German Credit | MLP | 0.55 | 0.57 |
| Diabetes | Logistic regression | 0.66 | 0.69 |
| Diabetes | Random forest | 0.57 | 0.57 |
| Diabetes | XGBoost | 0.55 | 0.58 |
| Diabetes | SVM (RBF) | 0.58 | 0.61 |
| Diabetes | MLP | 0.65 | 0.66 |
| Spambase | Logistic regression | 0.29 | 0.31 |
| Spambase | Random forest | 0.26 | 0.27 |
| Spambase | XGBoost | 0.34 | 0.35 |
| Spambase | SVM (RBF) | 0.29 | 0.31 |
| Spambase | MLP | 0.31 | 0.32 |
| Phishing | Logistic regression | 0.12 | 0.14 |
| Phishing | Random forest | 0.26 | 0.27 |
| Phishing | XGBoost | 0.23 | 0.24 |
| Phishing | SVM (RBF) | 0.19 | 0.20 |
| Phishing | MLP | 0.26 | 0.27 |
| Connect-4 | Logistic regression | 0.00 | 0.01 |
| Connect-4 | Random forest | 0.01 | 0.02 |
| Connect-4 | XGBoost | 0.01 | 0.01 |
| Connect-4 | SVM (RBF) | 0.01 | 0.02 |
| Connect-4 | MLP | 0.02 | 0.03 |

Over all 140 pairs of seeds: mean 0.22, maximum 0.69 (the values of §3.2 of the paper).


Degenerate explanations per dataset and explainer: share of all-zero attribution vectors, share of instances with undefined fidelity, and share of all-zero vectors among the 15 perturbed explanations of each stability instance:

| Dataset | Explainer | Rows | All-zero | Fidelity undefined | Zero among perturbed |
|---|---|---:|---:|---:|---:|
| Adult | SHAP | 2,500 | 0.0% | 0.0% | 0.0% |
| Adult | LIME (10) | 2,500 | 0.4% | 0.0% | 5.8% |
| Adult | LIME (full) | 2,500 | 0.4% | 0.0% | 6.3% |
| Adult | Anchors | 2,498 | 0.0% | 0.1% | 0.0% |
| Adult | DiCE | 2,500 | 0.0% | 0.0% | 0.0% |
| Breast Cancer | SHAP | 807 | 0.0% | 3.3% | 0.0% |
| Breast Cancer | LIME (10) | 807 | 0.0% | 3.3% | 0.0% |
| Breast Cancer | LIME (full) | 807 | 0.0% | 3.3% | 0.0% |
| Breast Cancer | Anchors | 807 | 0.0% | 3.3% | 0.0% |
| Breast Cancer | DiCE | 807 | 5.9% | 8.7% | 3.1% |
| German Credit | SHAP | 1,431 | 0.0% | 0.0% | 0.0% |
| German Credit | LIME (10) | 1,431 | 0.0% | 0.0% | 0.0% |
| German Credit | LIME (full) | 1,431 | 0.0% | 0.0% | 0.0% |
| German Credit | Anchors | 1,431 | 0.0% | 0.0% | 0.0% |
| German Credit | DiCE | 1,431 | 0.0% | 0.0% | 0.0% |
| Diabetes | SHAP | 1,347 | 0.0% | 0.0% | 0.0% |
| Diabetes | LIME (10) | 1,347 | 0.0% | 0.0% | 0.0% |
| Diabetes | LIME (full) | 1,347 | 0.0% | 0.0% | 0.0% |
| Diabetes | Anchors | 1,347 | 0.0% | 1.4% | 0.0% |
| Diabetes | DiCE | 1,347 | 0.0% | 0.0% | 0.0% |
| Spambase | SHAP | 1,476 | 0.0% | 1.2% | 0.0% |
| Spambase | LIME (10) | 1,476 | 0.3% | 1.2% | 0.1% |
| Spambase | LIME (full) | 1,476 | 0.3% | 1.2% | 0.1% |
| Spambase | Anchors | 1,476 | 0.0% | 1.2% | 0.0% |
| Spambase | DiCE | 1,476 | 0.6% | 1.8% | 0.5% |
| Phishing | SHAP | 1,488 | 0.0% | 1.4% | 0.0% |
| Phishing | LIME (10) | 1,488 | 0.0% | 1.4% | 0.0% |
| Phishing | LIME (full) | 1,488 | 0.0% | 1.4% | 0.0% |
| Phishing | Anchors | 1,488 | 0.0% | 1.4% | 0.0% |
| Phishing | DiCE | 1,488 | 0.0% | 1.4% | 0.0% |
| Connect-4 | SHAP | 1,500 | 0.0% | 0.3% | 0.0% |
| Connect-4 | LIME (10) | 1,500 | 0.0% | 0.3% | 0.8% |
| Connect-4 | LIME (full) | 1,500 | 0.0% | 0.3% | 0.8% |
| Connect-4 | Anchors | 1,497 | 0.0% | 0.3% | 0.0% |
| Connect-4 | DiCE | 1,500 | 0.0% | 0.3% | 0.0% |

## S8. Primary benchmark (Adult): per model and seed

Mean of each endpoint per cell (model, seed) and explainer. LIME (10) uses the 10-feature budget, LIME (full) the full vector; the confirmatory contrasts use LIME (full).

| Model | Seed | Explainer | Stability | Fidelity | Faithfulness gap | Sparsity |
|---|---:|---|---:|---:|---:|---:|
| Logistic regression | 11 | SHAP | 0.88 | 0.96 | 0.33 | 0.09 |
| Logistic regression | 11 | LIME (10) | 0.45 | 0.61 | 0.26 | 0.09 |
| Logistic regression | 11 | LIME (full) | 0.61 | 0.57 | 0.25 | 0.98 |
| Logistic regression | 11 | Anchors | 0.63 | 0.54 | 0.25 | 0.03 |
| Logistic regression | 11 | DiCE | 0.41 | 0.16 | 0.06 | 0.02 |
| Logistic regression | 22 | SHAP | 0.88 | 0.95 | 0.35 | 0.09 |
| Logistic regression | 22 | LIME (10) | 0.35 | 0.62 | 0.28 | 0.09 |
| Logistic regression | 22 | LIME (full) | 0.62 | 0.59 | 0.28 | 0.98 |
| Logistic regression | 22 | Anchors | 0.61 | 0.49 | 0.22 | 0.04 |
| Logistic regression | 22 | DiCE | 0.35 | 0.20 | 0.07 | 0.02 |
| Logistic regression | 33 | SHAP | 0.84 | 0.96 | 0.35 | 0.09 |
| Logistic regression | 33 | LIME (10) | 0.42 | 0.62 | 0.28 | 0.09 |
| Logistic regression | 33 | LIME (full) | 0.58 | 0.59 | 0.27 | 0.99 |
| Logistic regression | 33 | Anchors | 0.66 | 0.55 | 0.25 | 0.03 |
| Logistic regression | 33 | DiCE | 0.38 | 0.17 | 0.06 | 0.02 |
| Logistic regression | 44 | SHAP | 0.84 | 0.96 | 0.35 | 0.09 |
| Logistic regression | 44 | LIME (10) | 0.48 | 0.61 | 0.29 | 0.09 |
| Logistic regression | 44 | LIME (full) | 0.62 | 0.58 | 0.27 | 0.97 |
| Logistic regression | 44 | Anchors | 0.64 | 0.51 | 0.22 | 0.04 |
| Logistic regression | 44 | DiCE | 0.30 | 0.18 | 0.06 | 0.02 |
| Logistic regression | 55 | SHAP | 0.86 | 0.96 | 0.36 | 0.09 |
| Logistic regression | 55 | LIME (10) | 0.44 | 0.65 | 0.30 | 0.09 |
| Logistic regression | 55 | LIME (full) | 0.57 | 0.62 | 0.29 | 0.98 |
| Logistic regression | 55 | Anchors | 0.60 | 0.50 | 0.24 | 0.03 |
| Logistic regression | 55 | DiCE | 0.32 | 0.20 | 0.07 | 0.02 |
| Random forest | 11 | SHAP | 0.99 | 0.81 | 0.35 | 0.44 |
| Random forest | 11 | LIME (10) | 0.38 | 0.36 | 0.26 | 0.09 |
| Random forest | 11 | LIME (full) | 0.54 | 0.33 | 0.24 | 0.98 |
| Random forest | 11 | Anchors | 0.66 | 0.43 | 0.20 | 0.05 |
| Random forest | 11 | DiCE | 0.61 | 0.13 | 0.06 | 0.02 |
| Random forest | 22 | SHAP | 0.96 | 0.79 | 0.34 | 0.44 |
| Random forest | 22 | LIME (10) | 0.46 | 0.35 | 0.28 | 0.09 |
| Random forest | 22 | LIME (full) | 0.64 | 0.31 | 0.24 | 0.96 |
| Random forest | 22 | Anchors | 0.60 | 0.40 | 0.20 | 0.05 |
| Random forest | 22 | DiCE | 0.43 | 0.17 | 0.08 | 0.02 |
| Random forest | 33 | SHAP | 0.98 | 0.81 | 0.34 | 0.44 |
| Random forest | 33 | LIME (10) | 0.34 | 0.37 | 0.26 | 0.09 |
| Random forest | 33 | LIME (full) | 0.58 | 0.33 | 0.23 | 0.95 |
| Random forest | 33 | Anchors | 0.66 | 0.40 | 0.21 | 0.06 |
| Random forest | 33 | DiCE | 0.43 | 0.16 | 0.06 | 0.02 |
| Random forest | 44 | SHAP | 0.99 | 0.84 | 0.38 | 0.44 |
| Random forest | 44 | LIME (10) | 0.34 | 0.38 | 0.29 | 0.09 |
| Random forest | 44 | LIME (full) | 0.59 | 0.34 | 0.25 | 0.97 |
| Random forest | 44 | Anchors | 0.75 | 0.42 | 0.23 | 0.04 |
| Random forest | 44 | DiCE | 0.53 | 0.14 | 0.06 | 0.02 |
| Random forest | 55 | SHAP | 0.99 | 0.83 | 0.36 | 0.44 |
| Random forest | 55 | LIME (10) | 0.35 | 0.36 | 0.27 | 0.09 |
| Random forest | 55 | LIME (full) | 0.50 | 0.33 | 0.25 | 0.99 |
| Random forest | 55 | Anchors | 0.62 | 0.39 | 0.18 | 0.04 |
| Random forest | 55 | DiCE | 0.48 | 0.15 | 0.07 | 0.02 |
| XGBoost | 11 | SHAP | 0.63 | 0.76 | 0.45 | 0.36 |
| XGBoost | 11 | LIME (10) | 0.28 | 0.62 | 0.44 | 0.09 |
| XGBoost | 11 | LIME (full) | 0.54 | 0.58 | 0.43 | 0.99 |
| XGBoost | 11 | Anchors | 0.58 | 0.33 | 0.22 | 0.05 |
| XGBoost | 11 | DiCE | 0.50 | 0.35 | 0.17 | 0.02 |
| XGBoost | 22 | SHAP | 0.63 | 0.77 | 0.41 | 0.36 |
| XGBoost | 22 | LIME (10) | 0.22 | 0.60 | 0.41 | 0.09 |
| XGBoost | 22 | LIME (full) | 0.52 | 0.57 | 0.39 | 0.98 |
| XGBoost | 22 | Anchors | 0.59 | 0.32 | 0.20 | 0.07 |
| XGBoost | 22 | DiCE | 0.71 | 0.32 | 0.16 | 0.02 |
| XGBoost | 33 | SHAP | 0.61 | 0.76 | 0.44 | 0.36 |
| XGBoost | 33 | LIME (10) | 0.19 | 0.64 | 0.43 | 0.09 |
| XGBoost | 33 | LIME (full) | 0.63 | 0.60 | 0.41 | 0.99 |
| XGBoost | 33 | Anchors | 0.50 | 0.32 | 0.21 | 0.05 |
| XGBoost | 33 | DiCE | 0.59 | 0.34 | 0.16 | 0.02 |
| XGBoost | 44 | SHAP | 0.65 | 0.77 | 0.45 | 0.36 |
| XGBoost | 44 | LIME (10) | 0.27 | 0.63 | 0.44 | 0.09 |
| XGBoost | 44 | LIME (full) | 0.57 | 0.60 | 0.43 | 0.99 |
| XGBoost | 44 | Anchors | 0.59 | 0.34 | 0.21 | 0.07 |
| XGBoost | 44 | DiCE | 0.58 | 0.29 | 0.18 | 0.02 |
| XGBoost | 55 | SHAP | 0.56 | 0.78 | 0.42 | 0.36 |
| XGBoost | 55 | LIME (10) | 0.25 | 0.62 | 0.42 | 0.09 |
| XGBoost | 55 | LIME (full) | 0.51 | 0.59 | 0.42 | 0.99 |
| XGBoost | 55 | Anchors | 0.57 | 0.31 | 0.18 | 0.07 |
| XGBoost | 55 | DiCE | 0.53 | 0.27 | 0.15 | 0.02 |
| SVM (RBF) | 11 | SHAP | 0.91 | 0.89 | 0.35 | 0.09 |
| SVM (RBF) | 11 | LIME (10) | 0.33 | 0.50 | 0.23 | 0.09 |
| SVM (RBF) | 11 | LIME (full) | 0.54 | 0.47 | 0.19 | 0.99 |
| SVM (RBF) | 11 | Anchors | 0.67 | 0.53 | 0.28 | 0.05 |
| SVM (RBF) | 11 | DiCE | 0.46 | 0.22 | 0.06 | 0.01 |
| SVM (RBF) | 22 | SHAP | 0.93 | 0.90 | 0.35 | 0.09 |
| SVM (RBF) | 22 | LIME (10) | 0.40 | 0.51 | 0.25 | 0.09 |
| SVM (RBF) | 22 | LIME (full) | 0.61 | 0.48 | 0.22 | 0.99 |
| SVM (RBF) | 22 | Anchors | 0.74 | 0.52 | 0.30 | 0.04 |
| SVM (RBF) | 22 | DiCE | 0.53 | 0.27 | 0.08 | 0.02 |
| SVM (RBF) | 33 | SHAP | 0.90 | 0.89 | 0.35 | 0.09 |
| SVM (RBF) | 33 | LIME (10) | 0.44 | 0.55 | 0.24 | 0.09 |
| SVM (RBF) | 33 | LIME (full) | 0.60 | 0.52 | 0.20 | 0.99 |
| SVM (RBF) | 33 | Anchors | 0.65 | 0.49 | 0.26 | 0.04 |
| SVM (RBF) | 33 | DiCE | 0.31 | 0.25 | 0.06 | 0.02 |
| SVM (RBF) | 44 | SHAP | 0.90 | 0.90 | 0.36 | 0.09 |
| SVM (RBF) | 44 | LIME (10) | 0.40 | 0.54 | 0.26 | 0.09 |
| SVM (RBF) | 44 | LIME (full) | 0.61 | 0.51 | 0.22 | 0.99 |
| SVM (RBF) | 44 | Anchors | 0.68 | 0.49 | 0.29 | 0.04 |
| SVM (RBF) | 44 | DiCE | 0.39 | 0.22 | 0.06 | 0.01 |
| SVM (RBF) | 55 | SHAP | 0.88 | 0.89 | 0.35 | 0.09 |
| SVM (RBF) | 55 | LIME (10) | 0.42 | 0.51 | 0.23 | 0.09 |
| SVM (RBF) | 55 | LIME (full) | 0.62 | 0.49 | 0.20 | 0.98 |
| SVM (RBF) | 55 | Anchors | 0.70 | 0.57 | 0.28 | 0.04 |
| SVM (RBF) | 55 | DiCE | 0.37 | 0.23 | 0.06 | 0.01 |
| MLP | 11 | SHAP | 0.26 | 0.72 | 0.49 | 0.09 |
| MLP | 11 | LIME (10) | 0.18 | 0.44 | 0.30 | 0.09 |
| MLP | 11 | LIME (full) | 0.45 | 0.23 | 0.20 | 0.99 |
| MLP | 11 | Anchors | 0.63 | 0.31 | 0.28 | 0.12 |
| MLP | 11 | DiCE | 0.11 | 0.02 | 0.04 | 0.02 |
| MLP | 22 | SHAP | 0.38 | 0.74 | 0.53 | 0.09 |
| MLP | 22 | LIME (10) | 0.21 | 0.44 | 0.32 | 0.09 |
| MLP | 22 | LIME (full) | 0.45 | 0.22 | 0.19 | 1.00 |
| MLP | 22 | Anchors | 0.65 | 0.34 | 0.27 | 0.12 |
| MLP | 22 | DiCE | 0.16 | 0.02 | 0.04 | 0.02 |
| MLP | 33 | SHAP | 0.38 | 0.74 | 0.52 | 0.09 |
| MLP | 33 | LIME (10) | 0.20 | 0.43 | 0.30 | 0.09 |
| MLP | 33 | LIME (full) | 0.48 | 0.23 | 0.19 | 0.97 |
| MLP | 33 | Anchors | 0.62 | 0.27 | 0.22 | 0.15 |
| MLP | 33 | DiCE | 0.20 | 0.03 | 0.03 | 0.02 |
| MLP | 44 | SHAP | 0.28 | 0.72 | 0.49 | 0.09 |
| MLP | 44 | LIME (10) | 0.17 | 0.47 | 0.30 | 0.09 |
| MLP | 44 | LIME (full) | 0.46 | 0.25 | 0.19 | 0.98 |
| MLP | 44 | Anchors | 0.62 | 0.27 | 0.21 | 0.13 |
| MLP | 44 | DiCE | 0.13 | 0.05 | 0.07 | 0.02 |
| MLP | 55 | SHAP | 0.32 | 0.69 | 0.42 | 0.09 |
| MLP | 55 | LIME (10) | 0.23 | 0.46 | 0.30 | 0.09 |
| MLP | 55 | LIME (full) | 0.47 | 0.24 | 0.16 | 0.98 |
| MLP | 55 | Anchors | 0.62 | 0.26 | 0.24 | 0.13 |
| MLP | 55 | DiCE | 0.12 | 0.01 | 0.04 | 0.02 |

Paired effects SHAP − X on Adult, every endpoint and contrast (confirmatory rows marked C; Holm correction over the 12 confirmatory tests). Mixed model with random intercepts for model and for seed within model; variance components of the model (between models, seeds within models, residual); cluster bootstrap over models; number of the 25 cells with a positive difference.

| Endpoint | X | | Estimate [95% CI] | p | p Holm | Bootstrap 95% CI | Var. model | Var. seed | Var. residual | Cells > 0 |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Stability | LIME (full) | C | 0.181 [−0.010, 0.372] | 0.063 | 0.253 | [−0.008, 0.339] | 0.0465 | 0.0000 | 0.0506 | 19 |
| Stability | Anchors | C | 0.102 [−0.078, 0.283] | 0.266 | 0.312 | [−0.108, 0.264] | 0.0417 | 0.0012 | 0.0317 | 19 |
| Stability | DiCE | C | 0.339 [0.136, 0.543] | 0.001 | 0.008 | [0.153, 0.498] | 0.0521 | 0.0002 | 0.0965 | 24 |
| Stability | LIME (10) |  | 0.408 [0.247, 0.570] | <0.001 | — | [0.251, 0.537] | 0.0331 | 0.0017 | 0.0375 | 25 |
| Fidelity | LIME (full) | C | 0.384 [0.225, 0.544] | <0.001 | <0.001 | [0.278, 0.470] | 0.0331 | 0.0000 | 0.0425 | 25 |
| Fidelity | Anchors | C | 0.419 [0.253, 0.585] | <0.001 | <0.001 | [0.395, 0.439] | 0.0356 | 0.0003 | 0.0523 | 25 |
| Fidelity | DiCE | C | 0.649 [0.440, 0.858] | <0.001 | <0.001 | [0.544, 0.729] | 0.0568 | 0.0001 | 0.0776 | 25 |
| Fidelity | LIME (10) |  | 0.314 [0.153, 0.476] | <0.001 | — | [0.221, 0.399] | 0.0338 | 0.0000 | 0.0444 | 25 |
| Faithfulness gap | LIME (full) | C | 0.131 [0.051, 0.212] | 0.001 | 0.008 | [0.057, 0.221] | 0.0083 | 0.0000 | 0.0341 | 25 |
| Faithfulness gap | Anchors | C | 0.161 [−0.013, 0.334] | 0.069 | 0.253 | [0.101, 0.220] | 0.0391 | 0.0001 | 0.0547 | 25 |
| Faithfulness gap | DiCE | C | 0.315 [0.127, 0.502] | <0.001 | 0.008 | [0.276, 0.381] | 0.0455 | 0.0001 | 0.0643 | 25 |
| Faithfulness gap | LIME (10) |  | 0.091 [−0.034, 0.217] | 0.154 | — | [0.042, 0.143] | 0.0204 | 0.0000 | 0.0282 | 24 |
| Sparsity | LIME (full) |  | −0.766 [−0.876, −0.657] | <0.001 | — | [−0.891, −0.624] | 0.0157 | 0.0000 | 0.0080 | 0 |
| Sparsity | Anchors |  | 0.151 [0.032, 0.271] | 0.013 | — | [0.016, 0.304] | 0.0185 | 0.0000 | 0.0124 | 20 |
| Sparsity | DiCE |  | 0.198 [−0.151, 0.548] | 0.266 | — | [0.077, 0.335] | 0.1590 | 0.0000 | 0.0004 | 25 |
| Sparsity | LIME (10) |  | 0.123 [−0.031, 0.277] | 0.116 | — | [0.001, 0.261] | 0.0308 | 0.0000 | 0.0003 | 21 |
| Wall time (ms) | LIME (full) | C | 3,756 [561, 6,950] | 0.021 | 0.106 | [−0, 11,244] | 13,282,976 | 235.1689 | 9,937 | 19 |
| Wall time (ms) | Anchors | C | -5,357 [-7,208, -3,507] | <0.001 | <0.001 | [-7,854, -2,861] | 725.9988 | 3,507,119 | 375,329,671 | 0 |
| Wall time (ms) | DiCE | C | 2,517 [−961, 5,995] | 0.156 | 0.312 | [-1,094, 9,702] | 15,745,746 | 3,142 | 10,603 | 5 |
| Wall time (ms) | LIME (10) |  | 3,757 [544, 6,971] | 0.022 | — | [1, 11,246] | 13,440,870 | 314.8729 | 9,953 | 20 |
| CPU time (ms) | LIME (full) |  | 3,726 [-3,558, 11,009] | 0.316 | — | [−2, 11,159] | 69,042,926 | 368.1309 | 5,255 | 18 |
| CPU time (ms) | Anchors |  | -5,314 [-8,156, -2,471] | <0.001 | — | [-7,789, -2,838] | 6,188,102 | 3,358,922 | 365,431,338 | 0 |
| CPU time (ms) | DiCE |  | 2,496 [−415, 5,407] | 0.093 | — | [-1,088, 9,631] | 11,027,902 | 5.1734 | 6,459 | 5 |
| CPU time (ms) | LIME (10) |  | 4,002 [-675,519,485, 675,527,489] | 1.000 | — | [−1, 11,162] | 61,751,436 | 0.0000 | 5,803 | 20 |
| Rows evaluated | LIME (full) |  | 11,561 [10,413, 12,708] | <0.001 | — | [4,000, 24,001] | 1,626,351 | 19.4509 | 0.0000 | 15 |
| Rows evaluated | Anchors |  | -15,004 [-55,272, 25,263] | 0.465 | — | [-29,767, −242] | 2,071,701,154 | 41,208,886 | 3,053,769,993 | 5 |
| Rows evaluated | DiCE |  | 12,958 [7,048, 18,868] | <0.001 | — | [2,930, 22,984] | 45,458,742 | 14,769 | 80,076 | 15 |
| Rows evaluated | LIME (10) |  | 11,561 [10,413, 12,708] | <0.001 | — | [4,000, 24,001] | 1,626,351 | 19.4509 | 0.0000 | 15 |

Distribution of the instance-level paired differences SHAP − X (quantiles over all Adult instances, and per model):

| Endpoint | X | Model | n | Mean | Share > 0 | Min | P10 | Q1 | Median | Q3 | P90 | Max |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Stability | LIME (full) | All | 300 | 0.18 | 73% | −0.60 | −0.29 | −0.02 | 0.24 | 0.41 | 0.52 | 0.80 |
| Stability | LIME (full) | Logistic regression | 60 | 0.26 | 93% | −0.27 | 0.04 | 0.14 | 0.28 | 0.40 | 0.45 | 0.80 |
| Stability | LIME (full) | MLP | 60 | −0.14 | 30% | −0.60 | −0.42 | −0.36 | −0.17 | 0.04 | 0.23 | 0.54 |
| Stability | LIME (full) | Random forest | 60 | 0.41 | 100% | 0.11 | 0.18 | 0.29 | 0.42 | 0.53 | 0.60 | 0.73 |
| Stability | LIME (full) | SVM (RBF) | 60 | 0.31 | 92% | −0.32 | 0.02 | 0.20 | 0.34 | 0.42 | 0.52 | 0.71 |
| Stability | LIME (full) | XGBoost | 60 | 0.06 | 52% | −0.47 | −0.29 | −0.16 | 0.02 | 0.32 | 0.43 | 0.66 |
| Stability | Anchors | All | 298 | 0.10 | 71% | −0.81 | −0.35 | −0.06 | 0.20 | 0.32 | 0.38 | 0.66 |
| Stability | Anchors | Logistic regression | 60 | 0.23 | 93% | −0.23 | 0.05 | 0.15 | 0.25 | 0.33 | 0.38 | 0.47 |
| Stability | Anchors | MLP | 60 | −0.30 | 12% | −0.81 | −0.55 | −0.45 | −0.35 | −0.14 | 0.01 | 0.19 |
| Stability | Anchors | Random forest | 60 | 0.32 | 100% | 0.02 | 0.15 | 0.26 | 0.34 | 0.38 | 0.44 | 0.66 |
| Stability | Anchors | SVM (RBF) | 58 | 0.21 | 88% | −0.24 | −0.02 | 0.11 | 0.26 | 0.33 | 0.39 | 0.45 |
| Stability | Anchors | XGBoost | 60 | 0.05 | 65% | −0.39 | −0.22 | −0.13 | 0.08 | 0.22 | 0.27 | 0.47 |
| Stability | DiCE | All | 300 | 0.34 | 81% | −0.64 | −0.06 | 0.03 | 0.29 | 0.71 | 0.84 | 0.96 |
| Stability | DiCE | Logistic regression | 60 | 0.51 | 83% | −0.09 | −0.05 | 0.18 | 0.71 | 0.80 | 0.84 | 0.88 |
| Stability | DiCE | MLP | 60 | 0.18 | 83% | −0.36 | −0.03 | 0.05 | 0.12 | 0.30 | 0.48 | 0.82 |
| Stability | DiCE | Random forest | 60 | 0.49 | 98% | −0.03 | 0.01 | 0.09 | 0.63 | 0.80 | 0.88 | 0.96 |
| Stability | DiCE | SVM (RBF) | 60 | 0.49 | 83% | −0.13 | −0.04 | 0.17 | 0.57 | 0.82 | 0.87 | 0.93 |
| Stability | DiCE | XGBoost | 60 | 0.03 | 55% | −0.64 | −0.32 | −0.14 | 0.02 | 0.21 | 0.38 | 0.55 |
| Fidelity | LIME (full) | All | 2,500 | 0.38 | 95% | −0.63 | 0.05 | 0.23 | 0.41 | 0.55 | 0.65 | 1.08 |
| Fidelity | LIME (full) | Logistic regression | 500 | 0.37 | 100% | 0.01 | 0.21 | 0.32 | 0.39 | 0.44 | 0.50 | 0.77 |
| Fidelity | LIME (full) | MLP | 500 | 0.49 | 98% | −0.45 | 0.22 | 0.34 | 0.47 | 0.64 | 0.77 | 1.08 |
| Fidelity | LIME (full) | Random forest | 500 | 0.49 | 99% | −0.23 | 0.21 | 0.45 | 0.52 | 0.60 | 0.64 | 0.90 |
| Fidelity | LIME (full) | SVM (RBF) | 500 | 0.40 | 96% | −0.16 | 0.05 | 0.17 | 0.47 | 0.60 | 0.66 | 0.91 |
| Fidelity | LIME (full) | XGBoost | 500 | 0.18 | 82% | −0.63 | −0.09 | 0.03 | 0.18 | 0.29 | 0.53 | 0.83 |
| Fidelity | Anchors | All | 2,498 | 0.42 | 97% | −0.59 | 0.13 | 0.27 | 0.41 | 0.58 | 0.72 | 1.25 |
| Fidelity | Anchors | Logistic regression | 500 | 0.44 | 100% | 0.03 | 0.19 | 0.31 | 0.42 | 0.58 | 0.70 | 0.96 |
| Fidelity | Anchors | MLP | 500 | 0.43 | 95% | −0.59 | 0.13 | 0.28 | 0.44 | 0.59 | 0.71 | 1.25 |
| Fidelity | Anchors | Random forest | 500 | 0.41 | 94% | −0.31 | 0.08 | 0.26 | 0.39 | 0.58 | 0.78 | 0.96 |
| Fidelity | Anchors | SVM (RBF) | 498 | 0.37 | 98% | −0.53 | 0.12 | 0.22 | 0.36 | 0.51 | 0.66 | 0.95 |
| Fidelity | Anchors | XGBoost | 500 | 0.44 | 97% | −0.29 | 0.14 | 0.29 | 0.46 | 0.61 | 0.74 | 0.98 |
| Fidelity | DiCE | All | 2,500 | 0.65 | 97% | −0.63 | 0.21 | 0.45 | 0.73 | 0.90 | 0.96 | 1.02 |
| Fidelity | DiCE | Logistic regression | 500 | 0.77 | 100% | −0.00 | 0.45 | 0.67 | 0.81 | 0.96 | 0.99 | 1.02 |
| Fidelity | DiCE | MLP | 500 | 0.69 | 98% | −0.14 | 0.42 | 0.59 | 0.74 | 0.85 | 0.92 | 1.01 |
| Fidelity | DiCE | Random forest | 500 | 0.66 | 100% | −0.07 | 0.25 | 0.41 | 0.79 | 0.91 | 0.94 | 1.00 |
| Fidelity | DiCE | SVM (RBF) | 500 | 0.66 | 99% | −0.04 | 0.20 | 0.39 | 0.73 | 0.93 | 0.98 | 1.01 |
| Fidelity | DiCE | XGBoost | 500 | 0.45 | 88% | −0.63 | −0.02 | 0.22 | 0.49 | 0.74 | 0.87 | 0.99 |
| Faithfulness gap | LIME (full) | All | 2,500 | 0.13 | 74% | −0.65 | −0.03 | 0.00 | 0.06 | 0.21 | 0.39 | 1.00 |
| Faithfulness gap | LIME (full) | Logistic regression | 500 | 0.08 | 73% | −0.22 | −0.07 | −0.00 | 0.06 | 0.15 | 0.24 | 0.57 |
| Faithfulness gap | LIME (full) | MLP | 500 | 0.30 | 86% | −0.65 | −0.04 | 0.04 | 0.26 | 0.56 | 0.78 | 1.00 |
| Faithfulness gap | LIME (full) | Random forest | 500 | 0.12 | 87% | −0.09 | −0.00 | 0.02 | 0.11 | 0.20 | 0.25 | 0.40 |
| Faithfulness gap | LIME (full) | SVM (RBF) | 500 | 0.14 | 81% | −0.26 | −0.04 | 0.01 | 0.08 | 0.26 | 0.39 | 0.79 |
| Faithfulness gap | LIME (full) | XGBoost | 500 | 0.02 | 42% | −0.08 | −0.03 | −0.01 | 0.00 | 0.01 | 0.03 | 0.88 |
| Faithfulness gap | Anchors | All | 2,498 | 0.16 | 80% | −0.81 | −0.06 | 0.01 | 0.11 | 0.28 | 0.48 | 0.99 |
| Faithfulness gap | Anchors | Logistic regression | 500 | 0.11 | 75% | −0.35 | −0.08 | −0.00 | 0.09 | 0.21 | 0.35 | 0.77 |
| Faithfulness gap | Anchors | MLP | 500 | 0.24 | 80% | −0.81 | −0.17 | 0.02 | 0.21 | 0.48 | 0.72 | 0.98 |
| Faithfulness gap | Anchors | Random forest | 500 | 0.15 | 89% | −0.19 | 0.00 | 0.03 | 0.15 | 0.23 | 0.35 | 0.73 |
| Faithfulness gap | Anchors | SVM (RBF) | 498 | 0.07 | 71% | −0.58 | −0.11 | −0.00 | 0.05 | 0.12 | 0.27 | 0.86 |
| Faithfulness gap | Anchors | XGBoost | 500 | 0.23 | 86% | −0.32 | −0.00 | 0.02 | 0.15 | 0.38 | 0.56 | 0.99 |
| Faithfulness gap | DiCE | All | 2,500 | 0.31 | 93% | −0.80 | 0.01 | 0.07 | 0.30 | 0.50 | 0.68 | 0.99 |
| Faithfulness gap | DiCE | Logistic regression | 500 | 0.28 | 93% | −0.25 | 0.02 | 0.09 | 0.27 | 0.46 | 0.58 | 0.80 |
| Faithfulness gap | DiCE | MLP | 500 | 0.44 | 95% | −0.80 | 0.02 | 0.16 | 0.45 | 0.73 | 0.89 | 0.99 |
| Faithfulness gap | DiCE | Random forest | 500 | 0.29 | 98% | −0.08 | 0.02 | 0.12 | 0.31 | 0.43 | 0.53 | 0.74 |
| Faithfulness gap | DiCE | SVM (RBF) | 500 | 0.29 | 90% | −0.49 | −0.00 | 0.04 | 0.25 | 0.53 | 0.68 | 0.86 |
| Faithfulness gap | DiCE | XGBoost | 500 | 0.27 | 89% | −0.16 | −0.00 | 0.02 | 0.24 | 0.46 | 0.61 | 0.99 |

![Figure S1. Instance-level paired differences SHAP − X on Adult, by model (LR logistic regression, RF random forest, XGB XGBoost, SVM, MLP). Dashed line: no difference.](fig_s1_paired_differences.png){width=100%}

## S9. Cost

Timing pass: 5 instances per stratum (20 per cell), 3 repetitions (median used), 1 warm-up explanation per explainer, explainers interleaved per instance, one process and one thread pinned to logical CPU 2, measurements paused while any other process used more than 10% of a core. Wall time from the high-resolution performance counter; CPU time from the process clock (15.6 ms steps on Windows). FLOPs per explanation for logistic regression (2p + 2 per row) and the MLP (one hidden layer of 100 units), with p the number of encoded features.

*Timing pass at this build: 73 of 115 cells finished. Not complete: Spambase, Phishing, Connect-4. Rows marked * rest on fewer seeds than planned; rows of models not started are absent.*

| Dataset | Model | Explainer | n | Wall (ms) | CPU (ms) | Rows | Model calls | MFLOPs |
|---|---|---|---:|---:|---:|---:|---:|---:|
| Adult | Logistic regression | SHAP | 100 | 29.6 | 31.2 | 25,001 | 2 | 5.45 |
| Adult | Logistic regression | LIME (10) | 100 | 7.8 | 15.6 | 1,000 | 1 | 0.22 |
| Adult | Logistic regression | LIME (full) | 100 | 9.4 | 15.6 | 1,000 | 1 | 0.22 |
| Adult | Logistic regression | Anchors | 100 | 748.9 | 742.2 | 5,501 | 56 | 1.20 |
| Adult | Logistic regression | DiCE | 100 | 1,064 | 1,062 | 2,004 | 6 | 0.44 |
| Adult | Random forest | SHAP | 100 | 23.0 | 15.6 | 0 | 0 | — |
| Adult | Random forest | LIME (10) | 100 | 20.5 | 15.6 | 1,000 | 1 | — |
| Adult | Random forest | LIME (full) | 100 | 22.3 | 15.6 | 1,000 | 1 | — |
| Adult | Random forest | Anchors | 100 | 1,323 | 1,320 | 6,551 | 66 | — |
| Adult | Random forest | DiCE | 100 | 1,107 | 1,109 | 2,004 | 6 | — |
| Adult | XGBoost | SHAP | 100 | 1.4 | 0.0 | 0 | 0 | — |
| Adult | XGBoost | LIME (10) | 100 | 11.5 | 15.6 | 1,000 | 1 | — |
| Adult | XGBoost | LIME (full) | 100 | 13.3 | 15.6 | 1,000 | 1 | — |
| Adult | XGBoost | Anchors | 100 | 918.8 | 921.9 | not counted | not counted | — |
| Adult | XGBoost | DiCE | 100 | 1,107 | 1,094 | 2,004 | 6 | — |
| Adult | SVM (RBF) | SHAP | 100 | 19,492 | 19,359 | 25,001 | 2 | — |
| Adult | SVM (RBF) | LIME (10) | 100 | 788.5 | 781.2 | 1,000 | 1 | — |
| Adult | SVM (RBF) | LIME (full) | 100 | 786.2 | 781.2 | 1,000 | 1 | — |
| Adult | SVM (RBF) | Anchors | 100 | 5,640 | 5,617 | 6,351 | 64 | — |
| Adult | SVM (RBF) | DiCE | 100 | 2,627 | 2,609 | 2,004 | 6 | — |
| Adult | MLP | SHAP | 100 | 52.2 | 46.9 | 25,001 | 2 | 555.02 |
| Adult | MLP | LIME (10) | 100 | 9.2 | 15.6 | 1,000 | 1 | 22.20 |
| Adult | MLP | LIME (full) | 100 | 11.0 | 15.6 | 1,000 | 1 | 22.20 |
| Adult | MLP | Anchors | 100 | 2,776 | 2,750 | 23,201 | 233 | 515.06 |
| Adult | MLP | DiCE | 100 | 1,094 | 1,094 | 2,004 | 6 | 44.49 |
| Breast Cancer | Logistic regression | SHAP | 36 | 18.0 | 15.6 | 25,001 | 2 | 1.55 |
| Breast Cancer | Logistic regression | LIME (10) | 36 | 3.8 | 0.0 | 1,000 | 1 | 0.06 |
| Breast Cancer | Logistic regression | LIME (full) | 36 | 3.8 | 0.0 | 1,000 | 1 | 0.06 |
| Breast Cancer | Logistic regression | Anchors | 36 | 1,534 | 1,523 | 64,001 | 641 | 3.97 |
| Breast Cancer | Logistic regression | DiCE | 36 | 228.4 | 234.4 | 2,004 | 6 | 0.12 |
| Breast Cancer | Random forest | SHAP | 45 | 2.6 | 0.0 | 0 | 0 | — |
| Breast Cancer | Random forest | LIME (10) | 45 | 11.0 | 15.6 | 1,000 | 1 | — |
| Breast Cancer | Random forest | LIME (full) | 45 | 11.1 | 15.6 | 1,000 | 1 | — |
| Breast Cancer | Random forest | Anchors | 45 | 5,367 | 5,328 | 86,501 | 866 | — |
| Breast Cancer | Random forest | DiCE | 45 | 294.9 | 296.9 | 2,004 | 6 | — |
| Breast Cancer | XGBoost | SHAP | 48 | 0.7 | 0.0 | 0 | 0 | — |
| Breast Cancer | XGBoost | LIME (10) | 48 | 5.5 | 0.0 | 1,000 | 1 | — |
| Breast Cancer | XGBoost | LIME (full) | 48 | 5.6 | 0.0 | 1,000 | 1 | — |
| Breast Cancer | XGBoost | Anchors | 48 | 2,071 | 2,047 | not counted | not counted | — |
| Breast Cancer | XGBoost | DiCE | 48 | 250.2 | 250.0 | 2,004 | 6 | — |
| Breast Cancer | SVM (RBF) | SHAP | 36 | 230.2 | 234.4 | 25,001 | 2 | — |
| Breast Cancer | SVM (RBF) | LIME (10) | 36 | 12.6 | 15.6 | 1,000 | 1 | — |
| Breast Cancer | SVM (RBF) | LIME (full) | 36 | 12.6 | 15.6 | 1,000 | 1 | — |
| Breast Cancer | SVM (RBF) | Anchors | 36 | 2,263 | 2,250 | 75,001 | 751 | — |
| Breast Cancer | SVM (RBF) | DiCE | 36 | 250.4 | 250.0 | 2,004 | 6 | — |
| Breast Cancer | MLP | SHAP | 42 | 32.8 | 31.2 | 25,001 | 2 | 165.01 |
| Breast Cancer | MLP | LIME (10) | 42 | 4.3 | 0.0 | 1,000 | 1 | 6.60 |
| Breast Cancer | MLP | LIME (full) | 42 | 4.2 | 0.0 | 1,000 | 1 | 6.60 |
| Breast Cancer | MLP | Anchors | 42 | 1,664 | 1,641 | 63,401 | 635 | 418.45 |
| Breast Cancer | MLP | DiCE | 42 | 233.2 | 234.4 | 2,004 | 6 | 13.23 |
| German Credit | Logistic regression | SHAP | 60 | 25.0 | 31.2 | 25,001 | 2 | 3.10 |
| German Credit | Logistic regression | LIME (10) | 60 | 5.2 | 0.0 | 1,000 | 1 | 0.12 |
| German Credit | Logistic regression | LIME (full) | 60 | 5.8 | 0.0 | 1,000 | 1 | 0.12 |
| German Credit | Logistic regression | Anchors | 60 | 848.2 | 851.6 | 19,302 | 194 | 2.39 |
| German Credit | Logistic regression | DiCE | 60 | 397.2 | 406.2 | 2,004 | 6 | 0.25 |
| German Credit | Random forest | SHAP | 60 | 13.3 | 15.6 | 0 | 0 | — |
| German Credit | Random forest | LIME (10) | 60 | 16.0 | 15.6 | 1,000 | 1 | — |
| German Credit | Random forest | LIME (full) | 60 | 16.8 | 15.6 | 1,000 | 1 | — |
| German Credit | Random forest | Anchors | 60 | 6,099 | 6,047 | 77,551 | 776 | — |
| German Credit | Random forest | DiCE | 60 | 424.9 | 421.9 | 2,004 | 6 | — |
| German Credit | XGBoost | SHAP | 60 | 1.7 | 0.0 | 0 | 0 | — |
| German Credit | XGBoost | LIME (10) | 60 | 8.3 | 15.6 | 1,000 | 1 | — |
| German Credit | XGBoost | LIME (full) | 60 | 8.9 | 15.6 | 1,000 | 1 | — |
| German Credit | XGBoost | Anchors | 60 | 1,663 | 1,625 | not counted | not counted | — |
| German Credit | XGBoost | DiCE | 60 | 422.0 | 421.9 | 2,004 | 6 | — |
| German Credit | SVM (RBF) | SHAP | 60 | 1,165 | 1,156 | 25,001 | 2 | — |
| German Credit | SVM (RBF) | LIME (10) | 60 | 52.4 | 46.9 | 1,000 | 1 | — |
| German Credit | SVM (RBF) | LIME (full) | 60 | 53.0 | 46.9 | 1,000 | 1 | — |
| German Credit | SVM (RBF) | Anchors | 60 | 1,873 | 1,867 | 18,701 | 188 | — |
| German Credit | SVM (RBF) | DiCE | 60 | 488.1 | 484.4 | 2,004 | 6 | — |
| German Credit | MLP | SHAP | 60 | 42.7 | 46.9 | 25,001 | 2 | 320.01 |
| German Credit | MLP | LIME (10) | 60 | 6.0 | 0.0 | 1,000 | 1 | 12.80 |
| German Credit | MLP | LIME (full) | 60 | 6.6 | 0.0 | 1,000 | 1 | 12.80 |
| German Credit | MLP | Anchors | 60 | 1,850 | 1,836 | 46,352 | 466 | 593.31 |
| German Credit | MLP | DiCE | 60 | 397.5 | 390.6 | 2,004 | 6 | 25.65 |
| Diabetes | Logistic regression | SHAP | 60 | 7.3 | 0.0 | 12,701 | 2 | 0.23 |
| Diabetes | Logistic regression | LIME (10) | 60 | 2.7 | 0.0 | 1,000 | 1 | 0.02 |
| Diabetes | Logistic regression | LIME (full) | 60 | 2.6 | 0.0 | 1,000 | 1 | 0.02 |
| Diabetes | Logistic regression | Anchors | 60 | 55.8 | 46.9 | 1,401 | 15 | 0.03 |
| Diabetes | Logistic regression | DiCE | 60 | 99.1 | 93.8 | 2,004 | 6 | 0.04 |
| Diabetes | Random forest | SHAP | 60 | 8.7 | 15.6 | 0 | 0 | — |
| Diabetes | Random forest | LIME (10) | 60 | 12.3 | 15.6 | 1,000 | 1 | — |
| Diabetes | Random forest | LIME (full) | 60 | 12.2 | 15.6 | 1,000 | 1 | — |
| Diabetes | Random forest | Anchors | 60 | 277.1 | 273.4 | 4,001 | 41 | — |
| Diabetes | Random forest | DiCE | 60 | 128.4 | 125.0 | 2,004 | 6 | — |
| Diabetes | XGBoost | SHAP | 60 | 1.6 | 0.0 | 0 | 0 | — |
| Diabetes | XGBoost | LIME (10) | 60 | 4.9 | 0.0 | 1,000 | 1 | — |
| Diabetes | XGBoost | LIME (full) | 60 | 4.9 | 0.0 | 1,000 | 1 | — |
| Diabetes | XGBoost | Anchors | 60 | 147.1 | 140.6 | not counted | not counted | — |
| Diabetes | XGBoost | DiCE | 60 | 105.1 | 109.4 | 2,004 | 6 | — |
| Diabetes | SVM (RBF) | SHAP | 60 | 316.9 | 312.5 | 12,701 | 2 | — |
| Diabetes | SVM (RBF) | LIME (10) | 60 | 27.6 | 31.2 | 1,000 | 1 | — |
| Diabetes | SVM (RBF) | LIME (full) | 60 | 27.5 | 31.2 | 1,000 | 1 | — |
| Diabetes | SVM (RBF) | Anchors | 60 | 120.9 | 117.2 | 2,001 | 21 | — |
| Diabetes | SVM (RBF) | DiCE | 60 | 147.9 | 156.2 | 2,004 | 6 | — |
| Diabetes | MLP | SHAP | 60 | 14.1 | 15.6 | 12,701 | 2 | 27.94 |
| Diabetes | MLP | LIME (10) | 60 | 2.9 | 0.0 | 1,000 | 1 | 2.20 |
| Diabetes | MLP | LIME (full) | 60 | 2.9 | 0.0 | 1,000 | 1 | 2.20 |
| Diabetes | MLP | Anchors | 60 | 59.4 | 62.5 | 1,451 | 16 | 3.19 |
| Diabetes | MLP | DiCE | 60 | 99.9 | 93.8 | 2,004 | 6 | 4.41 |
| Spambase | Logistic regression | SHAP | 60 | 23.2 | 15.6 | 25,001 | 2 | 2.90 |
| Spambase | Logistic regression | LIME (10) | 60 | 5.2 | 0.0 | 1,000 | 1 | 0.12 |
| Spambase | Logistic regression | LIME (full) | 60 | 5.6 | 0.0 | 1,000 | 1 | 0.12 |
| Spambase | Logistic regression | Anchors | 60 | 1,086 | 1,086 | 29,751 | 298 | 3.45 |
| Spambase | Logistic regression | DiCE | 60 | 398.5 | 406.2 | 2,004 | 6 | 0.23 |
| Spambase | Random forest | SHAP | 16* | 15.1 | 15.6 | 0 | 0 | — |
| Spambase | Random forest | LIME (10) | 17* | 14.4 | 15.6 | 1,000 | 1 | — |
| Spambase | Random forest | LIME (full) | 17* | 15.1 | 15.6 | 1,000 | 1 | — |
| Spambase | Random forest | Anchors | 16* | 4,114 | 4,070 | 54,051 | 542 | — |
| Spambase | Random forest | DiCE | 16* | 441.3 | 437.5 | 2,004 | 6 | — |

Anchors calls XGBoost through a prediction method the counter did not wrap, so its rows and calls on XGBoost were not counted; its time is measured as for every other explainer.


*[R] The random forest against XGBoost at matched number of trees and depth, with TreeSHAP and LIME cost against the total number of leaves. Written from the result rows when that study is complete.*

## S10. Configuration sweep

*[R] Grids of LIME kernel width and samples and of KernelSHAP budget and background; per-model Pareto fronts; share of degenerate explanations. Written from the result rows when that study is complete.*

## S11. Measurement controls

Exclusion of instances with an all-zero LIME vector (any of the explanation and its 15 perturbed copies), Adult, mixed-model estimate of SHAP − X:

| X | Endpoint | Instances | n | Estimate [95% CI] | p |
|---|---|---|---:|---:|---:|
| LIME (full) | Stability | all | 300 | 0.181 [−0.010, 0.372] | 0.063 |
| LIME (full) | Stability | without all-zero | 134 | 0.129 [−0.066, 0.323] | 0.196 |
| LIME (full) | Fidelity | all | 2,500 | 0.384 [0.225, 0.544] | <0.001 |
| LIME (full) | Fidelity | without all-zero | 2,326 | 0.384 [0.274, 0.494] | <0.001 |
| LIME (full) | Faithfulness gap | all | 2,500 | 0.131 [0.051, 0.212] | 0.001 |
| LIME (full) | Faithfulness gap | without all-zero | 2,326 | 0.132 [0.026, 0.239] | 0.014 |
| LIME (10) | Stability | all | 300 | 0.408 [0.247, 0.570] | <0.001 |
| LIME (10) | Stability | without all-zero | 155 | 0.387 [0.233, 0.541] | <0.001 |
| LIME (10) | Fidelity | all | 2,500 | 0.314 [0.153, 0.476] | <0.001 |
| LIME (10) | Fidelity | without all-zero | 2,347 | 0.315 [0.201, 0.429] | <0.001 |
| LIME (10) | Faithfulness gap | all | 2,500 | 0.091 [−0.034, 0.217] | 0.154 |
| LIME (10) | Faithfulness gap | without all-zero | 2,347 | 0.090 [0.033, 0.148] | 0.002 |

*[R] No-noise repeats; valid one-hot perturbation; rank and top-k stability; the four masking schemes on every model. Written from the result rows when that study is complete.*

## S12. Further datasets: per model

Mean (SD) over the three seeds, per dataset, model and explainer. Table 4 of the paper averages these over the five models.

| Dataset | Model | Explainer | Stability | Fidelity | Faithfulness gap | Sparsity |
|---|---|---|---:|---:|---:|---:|
| Breast Cancer | Logistic regression | SHAP | 0.88 (0.01) | 0.80 (0.01) | 0.16 (0.01) | 0.33 (0.00) |
| Breast Cancer | Logistic regression | LIME (10) | 0.89 (0.02) | 0.74 (0.03) | 0.08 (0.00) | 0.33 (0.00) |
| Breast Cancer | Logistic regression | LIME (full) | 0.99 (0.00) | 0.53 (0.02) | 0.05 (0.01) | 1.00 (0.00) |
| Breast Cancer | Logistic regression | Anchors | 0.47 (0.07) | 0.35 (0.03) | 0.08 (0.00) | 0.07 (0.00) |
| Breast Cancer | Logistic regression | DiCE | 0.27 (0.05) | 0.07 (0.02) | 0.04 (0.01) | 0.15 (0.01) |
| Breast Cancer | Random forest | SHAP | 0.84 (0.01) | 0.74 (0.01) | 0.26 (0.00) | 0.98 (0.00) |
| Breast Cancer | Random forest | LIME (10) | 0.88 (0.02) | 0.67 (0.01) | 0.24 (0.00) | 0.33 (0.00) |
| Breast Cancer | Random forest | LIME (full) | 0.99 (0.00) | 0.63 (0.00) | 0.23 (0.00) | 0.99 (0.00) |
| Breast Cancer | Random forest | Anchors | 0.25 (0.02) | 0.25 (0.03) | 0.12 (0.00) | 0.07 (0.00) |
| Breast Cancer | Random forest | DiCE | 0.24 (0.01) | 0.27 (0.02) | 0.12 (0.01) | 0.24 (0.02) |
| Breast Cancer | XGBoost | SHAP | 0.81 (0.01) | 0.59 (0.02) | 0.27 (0.02) | 0.89 (0.00) |
| Breast Cancer | XGBoost | LIME (10) | 0.87 (0.01) | 0.51 (0.02) | 0.22 (0.01) | 0.33 (0.00) |
| Breast Cancer | XGBoost | LIME (full) | 0.98 (0.00) | 0.46 (0.02) | 0.21 (0.01) | 0.99 (0.00) |
| Breast Cancer | XGBoost | Anchors | 0.40 (0.03) | 0.19 (0.03) | 0.08 (0.02) | 0.07 (0.00) |
| Breast Cancer | XGBoost | DiCE | 0.24 (0.02) | 0.25 (0.08) | 0.09 (0.01) | 0.17 (0.01) |
| Breast Cancer | SVM (RBF) | SHAP | 0.85 (0.02) | 0.68 (0.02) | 0.14 (0.01) | 0.33 (0.00) |
| Breast Cancer | SVM (RBF) | LIME (10) | 0.86 (0.03) | 0.67 (0.04) | 0.08 (0.01) | 0.33 (0.00) |
| Breast Cancer | SVM (RBF) | LIME (full) | 1.00 (0.00) | 0.47 (0.02) | 0.04 (0.00) | 0.99 (0.01) |
| Breast Cancer | SVM (RBF) | Anchors | 0.39 (0.06) | 0.26 (0.01) | 0.06 (0.01) | 0.07 (0.00) |
| Breast Cancer | SVM (RBF) | DiCE | 0.16 (0.04) | 0.04 (0.01) | 0.03 (0.01) | 0.07 (0.01) |
| Breast Cancer | MLP | SHAP | 0.83 (0.01) | 0.64 (0.02) | 0.21 (0.06) | 0.33 (0.00) |
| Breast Cancer | MLP | LIME (10) | 0.85 (0.02) | 0.56 (0.01) | 0.09 (0.03) | 0.33 (0.00) |
| Breast Cancer | MLP | LIME (full) | 0.99 (0.00) | 0.39 (0.01) | 0.06 (0.01) | 1.00 (0.00) |
| Breast Cancer | MLP | Anchors | 0.41 (0.05) | 0.23 (0.02) | 0.10 (0.03) | 0.07 (0.00) |
| Breast Cancer | MLP | DiCE | 0.32 (0.01) | 0.11 (0.02) | 0.06 (0.03) | 0.12 (0.01) |
| German Credit | Logistic regression | SHAP | 0.84 (0.00) | 0.89 (0.00) | 0.28 (0.01) | 0.16 (0.00) |
| German Credit | Logistic regression | LIME (10) | 0.84 (0.02) | 0.80 (0.01) | 0.19 (0.00) | 0.16 (0.00) |
| German Credit | Logistic regression | LIME (full) | 0.99 (0.00) | 0.69 (0.01) | 0.16 (0.01) | 1.00 (0.00) |
| German Credit | Logistic regression | Anchors | 0.74 (0.02) | 0.56 (0.01) | 0.23 (0.00) | 0.07 (0.00) |
| German Credit | Logistic regression | DiCE | 0.37 (0.04) | 0.14 (0.02) | 0.07 (0.00) | 0.04 (0.00) |
| German Credit | Random forest | SHAP | 0.99 (0.00) | 0.74 (0.01) | 0.17 (0.00) | 0.91 (0.00) |
| German Credit | Random forest | LIME (10) | 0.92 (0.01) | 0.41 (0.01) | 0.14 (0.01) | 0.16 (0.00) |
| German Credit | Random forest | LIME (full) | 0.93 (0.00) | 0.36 (0.01) | 0.14 (0.01) | 0.98 (0.00) |
| German Credit | Random forest | Anchors | 0.69 (0.04) | 0.31 (0.01) | 0.08 (0.00) | 0.18 (0.01) |
| German Credit | Random forest | DiCE | 0.31 (0.03) | 0.14 (0.02) | 0.06 (0.01) | 0.05 (0.00) |
| German Credit | XGBoost | SHAP | 0.64 (0.02) | 0.64 (0.01) | 0.29 (0.01) | 0.84 (0.00) |
| German Credit | XGBoost | LIME (10) | 0.90 (0.02) | 0.36 (0.01) | 0.19 (0.01) | 0.16 (0.00) |
| German Credit | XGBoost | LIME (full) | 0.88 (0.00) | 0.35 (0.01) | 0.18 (0.02) | 0.99 (0.00) |
| German Credit | XGBoost | Anchors | 0.62 (0.09) | 0.41 (0.03) | 0.25 (0.02) | 0.10 (0.00) |
| German Credit | XGBoost | DiCE | 0.22 (0.02) | 0.22 (0.01) | 0.15 (0.02) | 0.03 (0.00) |
| German Credit | SVM (RBF) | SHAP | 0.89 (0.01) | 0.81 (0.01) | 0.26 (0.01) | 0.16 (0.00) |
| German Credit | SVM (RBF) | LIME (10) | 0.90 (0.02) | 0.64 (0.00) | 0.17 (0.00) | 0.16 (0.00) |
| German Credit | SVM (RBF) | LIME (full) | 0.98 (0.00) | 0.57 (0.00) | 0.16 (0.00) | 1.00 (0.00) |
| German Credit | SVM (RBF) | Anchors | 0.67 (0.05) | 0.42 (0.01) | 0.17 (0.00) | 0.09 (0.00) |
| German Credit | SVM (RBF) | DiCE | 0.38 (0.08) | 0.23 (0.01) | 0.09 (0.00) | 0.03 (0.00) |
| German Credit | MLP | SHAP | 0.78 (0.01) | 0.79 (0.01) | 0.53 (0.03) | 0.16 (0.00) |
| German Credit | MLP | LIME (10) | 0.70 (0.01) | 0.40 (0.00) | 0.26 (0.02) | 0.16 (0.00) |
| German Credit | MLP | LIME (full) | 0.92 (0.00) | 0.24 (0.00) | 0.21 (0.01) | 1.00 (0.00) |
| German Credit | MLP | Anchors | 0.66 (0.04) | 0.44 (0.02) | 0.35 (0.02) | 0.11 (0.00) |
| German Credit | MLP | DiCE | 0.22 (0.05) | 0.16 (0.02) | 0.14 (0.01) | 0.03 (0.00) |
| Diabetes | Logistic regression | SHAP | 0.98 (0.00) | 0.93 (0.00) | 0.27 (0.00) | 1.00 (0.00) |
| Diabetes | Logistic regression | LIME (10) | 1.00 (0.00) | 0.68 (0.01) | 0.27 (0.00) | 1.00 (0.00) |
| Diabetes | Logistic regression | LIME (full) | 1.00 (0.00) | 0.68 (0.01) | 0.27 (0.00) | 1.00 (0.00) |
| Diabetes | Logistic regression | Anchors | 0.89 (0.04) | 0.54 (0.01) | 0.28 (0.00) | 0.29 (0.00) |
| Diabetes | Logistic regression | DiCE | 0.36 (0.03) | 0.36 (0.09) | 0.21 (0.01) | 0.19 (0.02) |
| Diabetes | Random forest | SHAP | 0.94 (0.01) | 0.71 (0.00) | 0.26 (0.00) | 0.99 (0.00) |
| Diabetes | Random forest | LIME (10) | 1.00 (0.00) | 0.38 (0.02) | 0.24 (0.00) | 1.00 (0.00) |
| Diabetes | Random forest | LIME (full) | 1.00 (0.00) | 0.38 (0.02) | 0.24 (0.00) | 1.00 (0.00) |
| Diabetes | Random forest | Anchors | 0.82 (0.04) | 0.28 (0.03) | 0.24 (0.00) | 0.49 (0.01) |
| Diabetes | Random forest | DiCE | 0.37 (0.04) | 0.30 (0.06) | 0.20 (0.01) | 0.20 (0.01) |
| Diabetes | XGBoost | SHAP | 0.86 (0.03) | 0.75 (0.01) | 0.38 (0.01) | 1.00 (0.00) |
| Diabetes | XGBoost | LIME (10) | 0.99 (0.00) | 0.45 (0.02) | 0.33 (0.01) | 1.00 (0.00) |
| Diabetes | XGBoost | LIME (full) | 0.99 (0.00) | 0.45 (0.02) | 0.33 (0.01) | 1.00 (0.00) |
| Diabetes | XGBoost | Anchors | 0.79 (0.01) | 0.29 (0.00) | 0.33 (0.00) | 0.53 (0.00) |
| Diabetes | XGBoost | DiCE | 0.32 (0.03) | 0.33 (0.03) | 0.31 (0.02) | 0.20 (0.00) |
| Diabetes | SVM (RBF) | SHAP | 0.98 (0.00) | 0.81 (0.02) | 0.27 (0.01) | 1.00 (0.00) |
| Diabetes | SVM (RBF) | LIME (10) | 1.00 (0.00) | 0.48 (0.04) | 0.26 (0.01) | 1.00 (0.00) |
| Diabetes | SVM (RBF) | LIME (full) | 1.00 (0.00) | 0.48 (0.04) | 0.26 (0.01) | 1.00 (0.00) |
| Diabetes | SVM (RBF) | Anchors | 0.78 (0.03) | 0.37 (0.01) | 0.27 (0.01) | 0.38 (0.01) |
| Diabetes | SVM (RBF) | DiCE | 0.28 (0.01) | 0.14 (0.06) | 0.17 (0.01) | 0.20 (0.01) |
| Diabetes | MLP | SHAP | 0.98 (0.00) | 0.78 (0.00) | 0.31 (0.01) | 1.00 (0.00) |
| Diabetes | MLP | LIME (10) | 1.00 (0.00) | 0.46 (0.01) | 0.30 (0.01) | 1.00 (0.00) |
| Diabetes | MLP | LIME (full) | 1.00 (0.00) | 0.46 (0.01) | 0.30 (0.01) | 1.00 (0.00) |
| Diabetes | MLP | Anchors | 0.81 (0.03) | 0.35 (0.04) | 0.32 (0.01) | 0.35 (0.00) |
| Diabetes | MLP | DiCE | 0.28 (0.02) | 0.21 (0.02) | 0.21 (0.01) | 0.19 (0.01) |
| Spambase | Logistic regression | SHAP | 0.78 (0.06) | 0.75 (0.01) | 0.36 (0.00) | 0.18 (0.00) |
| Spambase | Logistic regression | LIME (10) | 0.80 (0.02) | 0.59 (0.01) | 0.22 (0.01) | 0.17 (0.00) |
| Spambase | Logistic regression | LIME (full) | 0.98 (0.00) | 0.52 (0.02) | 0.21 (0.01) | 0.99 (0.01) |
| Spambase | Logistic regression | Anchors | 0.31 (0.07) | 0.35 (0.01) | 0.21 (0.01) | 0.06 (0.00) |
| Spambase | Logistic regression | DiCE | 0.06 (0.01) | 0.00 (0.02) | 0.09 (0.01) | 0.03 (0.00) |
| Spambase | Random forest | SHAP | 0.60 (0.02) | 0.51 (0.02) | 0.35 (0.02) | 0.90 (0.00) |
| Spambase | Random forest | LIME (10) | 0.83 (0.04) | 0.59 (0.00) | 0.24 (0.01) | 0.17 (0.00) |
| Spambase | Random forest | LIME (full) | 0.93 (0.04) | 0.61 (0.00) | 0.23 (0.01) | 0.97 (0.00) |
| Spambase | Random forest | Anchors | 0.29 (0.03) | 0.11 (0.02) | 0.21 (0.01) | 0.05 (0.00) |
| Spambase | Random forest | DiCE | 0.17 (0.03) | 0.31 (0.01) | 0.30 (0.00) | 0.06 (0.00) |
| Spambase | XGBoost | SHAP | 0.45 (0.03) | 0.53 (0.01) | 0.60 (0.01) | 0.80 (0.00) |
| Spambase | XGBoost | LIME (10) | 0.75 (0.05) | 0.47 (0.00) | 0.39 (0.02) | 0.17 (0.00) |
| Spambase | XGBoost | LIME (full) | 0.88 (0.04) | 0.46 (0.00) | 0.39 (0.02) | 0.97 (0.01) |
| Spambase | XGBoost | Anchors | 0.24 (0.01) | 0.10 (0.01) | 0.27 (0.02) | 0.05 (0.00) |
| Spambase | XGBoost | DiCE | 0.18 (0.01) | 0.26 (0.02) | 0.32 (0.01) | 0.04 (0.00) |
| Spambase | SVM (RBF) | SHAP | 0.90 (0.02) | 0.80 (0.01) | 0.36 (0.03) | 0.18 (0.00) |
| Spambase | SVM (RBF) | LIME (10) | 0.81 (0.01) | 0.55 (0.00) | 0.12 (0.01) | 0.17 (0.00) |
| Spambase | SVM (RBF) | LIME (full) | 0.99 (0.00) | 0.44 (0.00) | 0.11 (0.01) | 0.98 (0.00) |
| Spambase | SVM (RBF) | Anchors | 0.34 (0.04) | 0.39 (0.01) | 0.21 (0.01) | 0.06 (0.00) |
| Spambase | SVM (RBF) | DiCE | 0.10 (0.05) | 0.07 (0.00) | 0.07 (0.01) | 0.03 (0.00) |
| Spambase | MLP | SHAP | 0.72 (0.03) | 0.62 (0.03) | 0.62 (0.05) | 0.18 (0.00) |
| Spambase | MLP | LIME (10) | 0.71 (0.02) | 0.33 (0.02) | 0.28 (0.03) | 0.17 (0.00) |
| Spambase | MLP | LIME (full) | 0.95 (0.00) | 0.26 (0.03) | 0.28 (0.03) | 0.99 (0.01) |
| Spambase | MLP | Anchors | 0.32 (0.04) | 0.26 (0.01) | 0.32 (0.02) | 0.07 (0.00) |
| Spambase | MLP | DiCE | 0.05 (0.01) | 0.01 (0.02) | 0.13 (0.01) | 0.03 (0.00) |
| Phishing | Logistic regression | SHAP | 0.83 (0.02) | 0.87 (0.01) | 0.41 (0.03) | 0.15 (0.00) |
| Phishing | Logistic regression | LIME (10) | 0.87 (0.00) | 0.80 (0.00) | 0.25 (0.02) | 0.15 (0.00) |
| Phishing | Logistic regression | LIME (full) | 0.99 (0.00) | 0.78 (0.00) | 0.24 (0.01) | 1.00 (0.00) |
| Phishing | Logistic regression | Anchors | 0.94 (0.01) | 0.68 (0.01) | 0.36 (0.01) | 0.04 (0.00) |
| Phishing | Logistic regression | DiCE | 0.25 (0.05) | 0.29 (0.03) | 0.14 (0.01) | 0.05 (0.00) |
| Phishing | Random forest | SHAP | 1.00 (0.00) | 0.54 (0.01) | 0.35 (0.00) | 0.87 (0.00) |
| Phishing | Random forest | LIME (10) | 0.92 (0.00) | 0.30 (0.01) | 0.25 (0.01) | 0.15 (0.00) |
| Phishing | Random forest | LIME (full) | 0.93 (0.00) | 0.26 (0.01) | 0.23 (0.00) | 0.99 (0.00) |
| Phishing | Random forest | Anchors | 0.86 (0.04) | 0.38 (0.03) | 0.27 (0.00) | 0.06 (0.00) |
| Phishing | Random forest | DiCE | 0.28 (0.03) | 0.12 (0.02) | 0.12 (0.01) | 0.04 (0.00) |
| Phishing | XGBoost | SHAP | 0.41 (0.03) | 0.56 (0.01) | 0.62 (0.01) | 0.59 (0.00) |
| Phishing | XGBoost | LIME (10) | 0.90 (0.01) | 0.52 (0.01) | 0.49 (0.00) | 0.15 (0.00) |
| Phishing | XGBoost | LIME (full) | 0.90 (0.00) | 0.51 (0.01) | 0.49 (0.00) | 0.99 (0.00) |
| Phishing | XGBoost | Anchors | 0.89 (0.00) | 0.33 (0.02) | 0.31 (0.01) | 0.05 (0.00) |
| Phishing | XGBoost | DiCE | 0.20 (0.04) | 0.37 (0.06) | 0.47 (0.03) | 0.03 (0.00) |
| Phishing | SVM (RBF) | SHAP | 0.86 (0.02) | 0.87 (0.01) | 0.44 (0.01) | 0.15 (0.00) |
| Phishing | SVM (RBF) | LIME (10) | 0.90 (0.00) | 0.75 (0.01) | 0.26 (0.04) | 0.15 (0.00) |
| Phishing | SVM (RBF) | LIME (full) | 0.99 (0.00) | 0.72 (0.01) | 0.23 (0.03) | 1.00 (0.00) |
| Phishing | SVM (RBF) | Anchors | 0.96 (0.04) | 0.70 (0.02) | 0.36 (0.02) | 0.04 (0.00) |
| Phishing | SVM (RBF) | DiCE | 0.31 (0.04) | 0.36 (0.03) | 0.13 (0.02) | 0.07 (0.00) |
| Phishing | MLP | SHAP | 0.65 (0.05) | 0.65 (0.02) | 0.48 (0.01) | 0.15 (0.00) |
| Phishing | MLP | LIME (10) | 0.86 (0.01) | 0.47 (0.01) | 0.19 (0.01) | 0.15 (0.00) |
| Phishing | MLP | LIME (full) | 0.96 (0.00) | 0.45 (0.01) | 0.19 (0.01) | 1.00 (0.00) |
| Phishing | MLP | Anchors | 0.81 (0.04) | 0.46 (0.02) | 0.32 (0.03) | 0.08 (0.00) |
| Phishing | MLP | DiCE | 0.20 (0.04) | 0.17 (0.02) | 0.16 (0.02) | 0.04 (0.00) |
| Connect-4 | Logistic regression | SHAP | 0.73 (0.05) | 0.88 (0.00) | 0.28 (0.01) | 0.08 (0.00) |
| Connect-4 | Logistic regression | LIME (10) | 0.61 (0.04) | 0.68 (0.00) | 0.20 (0.00) | 0.08 (0.00) |
| Connect-4 | Logistic regression | LIME (full) | 0.98 (0.00) | 0.55 (0.01) | 0.14 (0.01) | 0.99 (0.01) |
| Connect-4 | Logistic regression | Anchors | 0.74 (0.03) | 0.62 (0.00) | 0.39 (0.01) | 0.04 (0.00) |
| Connect-4 | Logistic regression | DiCE | 0.06 (0.01) | 0.06 (0.01) | 0.05 (0.01) | 0.02 (0.00) |
| Connect-4 | Random forest | SHAP | 1.00 (0.00) | 0.80 (0.01) | 0.20 (0.01) | 0.67 (0.00) |
| Connect-4 | Random forest | LIME (10) | 0.72 (0.03) | 0.47 (0.01) | 0.16 (0.01) | 0.08 (0.00) |
| Connect-4 | Random forest | LIME (full) | 0.82 (0.01) | 0.32 (0.02) | 0.14 (0.01) | 0.98 (0.01) |
| Connect-4 | Random forest | Anchors | 0.68 (0.05) | 0.40 (0.01) | 0.15 (0.01) | 0.07 (0.01) |
| Connect-4 | Random forest | DiCE | 0.19 (0.05) | 0.10 (0.01) | 0.05 (0.00) | 0.02 (0.00) |
| Connect-4 | XGBoost | SHAP | 0.48 (0.04) | 0.77 (0.01) | 0.25 (0.03) | 0.64 (0.00) |
| Connect-4 | XGBoost | LIME (10) | 0.61 (0.02) | 0.32 (0.01) | 0.16 (0.01) | 0.08 (0.00) |
| Connect-4 | XGBoost | LIME (full) | 0.65 (0.03) | 0.23 (0.01) | 0.15 (0.02) | 0.97 (0.01) |
| Connect-4 | XGBoost | Anchors | 0.72 (0.02) | 0.41 (0.05) | 0.28 (0.05) | 0.06 (0.01) |
| Connect-4 | XGBoost | DiCE | 0.08 (0.02) | 0.18 (0.03) | 0.13 (0.03) | 0.02 (0.00) |
| Connect-4 | SVM (RBF) | SHAP | 0.79 (0.01) | 0.85 (0.00) | 0.40 (0.01) | 0.08 (0.00) |
| Connect-4 | SVM (RBF) | LIME (10) | 0.67 (0.01) | 0.64 (0.01) | 0.25 (0.01) | 0.08 (0.00) |
| Connect-4 | SVM (RBF) | LIME (full) | 0.96 (0.00) | 0.49 (0.01) | 0.18 (0.03) | 0.99 (0.00) |
| Connect-4 | SVM (RBF) | Anchors | 0.77 (0.05) | 0.57 (0.01) | 0.47 (0.03) | 0.05 (0.00) |
| Connect-4 | SVM (RBF) | DiCE | 0.13 (0.02) | 0.09 (0.01) | 0.08 (0.01) | 0.02 (0.00) |
| Connect-4 | MLP | SHAP | 0.48 (0.05) | 0.69 (0.03) | 0.71 (0.03) | 0.08 (0.00) |
| Connect-4 | MLP | LIME (10) | 0.45 (0.02) | 0.36 (0.01) | 0.34 (0.01) | 0.08 (0.00) |
| Connect-4 | MLP | LIME (full) | 0.83 (0.00) | 0.22 (0.01) | 0.27 (0.05) | 1.00 (0.00) |
| Connect-4 | MLP | Anchors | 0.67 (0.04) | 0.44 (0.02) | 0.53 (0.03) | 0.08 (0.00) |
| Connect-4 | MLP | DiCE | 0.05 (0.02) | 0.03 (0.01) | 0.08 (0.01) | 0.01 (0.00) |

## S13. How to regenerate every table

1. Install the frozen environment; prepare the datasets and check the model hashes of S6 (`paper_b_run.py prepare`, then `paper_b_run.py preflight`). The prepared data reproduce the data hashes of S6 exactly.
2. Quality pass: `paper_b_run.py launch` (resumable; one row per instance).
3. Cost pass: `paper_b_run.py launch-timing` on an idle host.
4. Analysis: `paper_b_analyze.py --root <results> --out <analysis>` writes every value of Tables 2–4 of the paper and of S7–S12 (primary_effects.csv, cells.csv, cost.csv, quality_checks.csv, cross_dataset.csv, friedman.csv).
5. This file: `build_supplement.py --analysis <analysis>` derives the instance counts, overlaps, distributions, Figure S1 and the exclusion check from the per-instance rows.
