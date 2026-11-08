| dataset | model | explainer | t/explanation (s) | full job (h) | x seeds (h) | peak (GB) | pilot failed rows |
|---|---|---|---:|---:|---:|---:|---:|
| adult | svm | shap | 108.779 | 14.00 | 70.02 | 0.37 | 0 |
| connect4 | svm | shap | 171.973 | 19.11 | 57.32 | 0.42 | 0 |
| adult | svm | anchors | 17.571 | 5.66 | 28.30 | 1.46 | 0 |
| connect4 | svm | anchors | 60.538 | 9.11 | 27.34 | 1.47 | 0 |
| adult | mlp | anchors | 8.224 | 2.87 | 14.37 | 2.84 | 0 |
| connect4 | rf | anchors | 14.620 | 4.38 | 13.13 | 3.03 | 0 |
| connect4 | mlp | anchors | 12.081 | 3.82 | 11.47 | 2.86 | 0 |
| phishing | svm | shap | 20.186 | 2.42 | 7.25 | 0.33 | 0 |
| adult | rf | anchors | 5.772 | 1.36 | 6.82 | 1.46 | 0 |
| breast_cancer | rf | dice | 0.508 | 2.19 | 6.57 | 0.26 | 0 |
| connect4 | xgb | anchors | 4.230 | 1.83 | 5.49 | 2.60 | 0 |
| spambase | svm | shap | 12.471 | 1.80 | 5.39 | 0.29 | 0 |
| german_credit | rf | anchors | 7.826 | 1.69 | 5.08 | 1.25 | 0 |
| spambase | rf | dice | 2.458 | 1.66 | 4.98 | 0.27 | 0 |
| phishing | svm | anchors | 9.902 | 1.48 | 4.43 | 1.25 | 0 |
| adult | xgb | anchors | 4.264 | 0.71 | 3.57 | 2.51 | 0 |
| connect4 | logreg | anchors | 3.271 | 1.05 | 3.16 | 1.96 | 0 |
| diabetes | mlp | dice | 0.166 | 1.05 | 3.14 | 0.26 | 0 |
| connect4 | svm | dice | 5.828 | 0.96 | 2.87 | 0.37 | 0 |
| breast_cancer | rf | anchors | 7.571 | 0.84 | 2.52 | 0.70 | 0 |
| diabetes | svm | dice | 0.208 | 0.81 | 2.42 | 0.26 | 0 |
| phishing | rf | anchors | 7.062 | 0.78 | 2.35 | 1.43 | 0 |
| german_credit | svm | shap | 6.409 | 0.76 | 2.27 | 0.29 | 0 |
| adult | svm | dice | 3.606 | 0.43 | 2.15 | 0.37 | 0 |
| spambase | rf | anchors | 6.372 | 0.71 | 2.12 | 0.59 | 0 |

(top 25 of 175 job types by total hours)

Quality pass: 348.7 CPU-hours; on 4 workers about 87.2 h of wall time (lower bound).
Longest single job: connect4/svm/shap 19.1 h.
Timing pass (sequential, quiet host): about 35.9 h plus gate waits.
