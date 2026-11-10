# Paper B revision 1: analysis report (cohort B2)

- Design hash: `a486391f05863b635747847e193e8f61d4f4abc37d97c17a783c77daf36f68d4`
- Rows: 2,676; cells: 15
- Complete cells only
- Seed overlap of instances (Jaccard, same dataset and model): mean nan, max nan

## Table 2: primary effects (Adult)

_(no data yet)_

## Friedman / Nemenyi (Adult, cell means; rank 1 = highest)

_(no data yet)_

## Table 4: other datasets (mean and SD over seeds of model-averaged means)

_(no data yet)_

## Quality checks

| dataset | explainer | rows | all_zero_share | fidelity_exact_zero_share | stability_rows | stability_zero_vectors_mean | stability_zero_vector_share |
|---|---|---|---|---|---|---|---|
| adult | kshap_ns1000_bg50 | 60 | 0 | 0 | 60 | 0 | 0 |
| adult | kshap_ns100_bg50 | 60 | 0 | 0 | 60 | 0 | 0 |
| adult | kshap_ns250_bg50 | 60 | 0 | 0 | 60 | 0 | 0 |
| adult | kshap_ns500_bg10 | 60 | 0 | 0 | 60 | 0 | 0 |
| adult | kshap_ns500_bg100 | 60 | 0 | 0 | 60 | 0 | 0 |
| adult | kshap_ns500_bg25 | 60 | 0 | 0 | 60 | 0 | 0 |
| adult | kshap_ns500_bg50 | 60 | 0 | 0 | 60 | 0 | 0 |
| adult | kshap_nsauto_bg50 | 60 | 0 | 0 | 60 | 0 | 0 |
| adult | lime_kw0p75_ns1000 | 60 | 1 | 1 | 60 | 15 | 1 |
| adult | lime_kw0p75_ns2000 | 60 | 1 | 1 | 60 | 15 | 1 |
| adult | lime_kw0p75_ns250 | 60 | 1 | 1 | 60 | 15 | 1 |
| adult | lime_kw0p75_ns500 | 60 | 1 | 1 | 60 | 15 | 1 |
| adult | lime_kw0p75_ns5000 | 60 | 1 | 1 | 60 | 15 | 1 |
| adult | lime_kw10p0_ns1000 | 60 | 0 | 0 | 60 | 0.06667 | 0.004444 |
| adult | lime_kw10p0_ns2000 | 60 | 0 | 0 | 60 | 0.08333 | 0.005556 |
| adult | lime_kw10p0_ns250 | 60 | 0 | 0 | 60 | 0.15 | 0.01 |
| adult | lime_kw10p0_ns500 | 60 | 0 | 0 | 60 | 0.1333 | 0.008889 |
| adult | lime_kw10p0_ns5000 | 60 | 0 | 0 | 60 | 0.05 | 0.003333 |
| adult | lime_kw15p0_ns1000 | 60 | 0 | 0 | 60 | 0 | 0 |
| adult | lime_kw15p0_ns2000 | 60 | 0 | 0 | 60 | 0 | 0 |
| adult | lime_kw15p0_ns250 | 60 | 0 | 0 | 60 | 0 | 0 |
| adult | lime_kw15p0_ns500 | 60 | 0 | 0 | 60 | 0 | 0 |
| adult | lime_kw15p0_ns5000 | 60 | 0 | 0 | 60 | 0 | 0 |
| adult | lime_kw1p5_ns1000 | 60 | 1 | 0.8 | 60 | 15 | 1 |
| adult | lime_kw1p5_ns2000 | 60 | 1 | 0.75 | 60 | 15 | 1 |
| adult | lime_kw1p5_ns250 | 60 | 1 | 0.8667 | 60 | 15 | 1 |
| adult | lime_kw1p5_ns500 | 60 | 1 | 0.7833 | 60 | 15 | 1 |
| adult | lime_kw1p5_ns5000 | 60 | 1 | 0.6667 | 60 | 15 | 1 |
| adult | lime_kw3p0_ns1000 | 60 | 0.1333 | 0.08333 | 60 | 15 | 1 |
| adult | lime_kw3p0_ns2000 | 60 | 0.1333 | 0.08333 | 60 | 15 | 1 |
| adult | lime_kw3p0_ns250 | 60 | 0.1333 | 0.08333 | 60 | 15 | 1 |
| adult | lime_kw3p0_ns500 | 60 | 0.1333 | 0.08333 | 60 | 15 | 1 |
| adult | lime_kw3p0_ns5000 | 60 | 0.1167 | 0.08333 | 60 | 15 | 1 |
| adult | lime_kw5p0_ns1000 | 60 | 0.03333 | 0 | 60 | 8.533 | 0.5689 |
| adult | lime_kw5p0_ns2000 | 60 | 0.03333 | 0 | 60 | 7.983 | 0.5322 |
| adult | lime_kw5p0_ns250 | 60 | 0.03333 | 0 | 60 | 10.07 | 0.6711 |
| adult | lime_kw5p0_ns500 | 60 | 0.03333 | 0 | 60 | 9.667 | 0.6444 |
| adult | lime_kw5p0_ns5000 | 60 | 0 | 0 | 60 | 7.4 | 0.4933 |
| adult | lime_kwdef_ns1000 | 60 | 0 | 0 | 60 | 1.133 | 0.07556 |
| adult | lime_kwdef_ns2000 | 60 | 0 | 0 | 60 | 0.75 | 0.05 |
| adult | lime_kwdef_ns250 | 60 | 0 | 0 | 60 | 1.317 | 0.08778 |
| adult | lime_kwdef_ns500 | 60 | 0 | 0 | 60 | 0.95 | 0.06333 |
| adult | lime_kwdef_ns5000 | 60 | 0 | 0 | 60 | 0.6167 | 0.04111 |
| adult | tshap_bg10 | 24 | 0 | 0 | 24 | 0 | 0 |
| adult | tshap_bg100 | 24 | 0 | 0 | 24 | 0 | 0 |
| adult | tshap_bg25 | 24 | 0 | 0 | 24 | 0 | 0 |
| adult | tshap_bg50 | 24 | 0 | 0 | 24 | 0 | 0 |

## Table 3: cost

| dataset | model | explainer | cpu_ms_median | wall_ms_median | rows_median | calls_median | n | flops_per_explanation |
|---|---|---|---|---|---|---|---|---|
| adult | logreg | kshap_ns1000_bg50 | 46.88 | 50.91 | 5e+04 | 2 | 12 | 1.09e+07 |
| adult | logreg | kshap_ns100_bg50 | 15.62 | 12.5 | 5001 | 2 | 12 | 1.09e+06 |
| adult | logreg | kshap_ns250_bg50 | 15.62 | 19.01 | 1.25e+04 | 2 | 12 | 2.725e+06 |
| adult | logreg | kshap_ns500_bg10 | 15.62 | 18.44 | 5001 | 2 | 12 | 1.09e+06 |
| adult | logreg | kshap_ns500_bg100 | 46.88 | 43.28 | 5e+04 | 2 | 12 | 1.09e+07 |
| adult | logreg | kshap_ns500_bg25 | 23.44 | 22.46 | 1.25e+04 | 2 | 12 | 2.725e+06 |
| adult | logreg | kshap_ns500_bg50 | 31.25 | 29.1 | 2.5e+04 | 2 | 12 | 5.45e+06 |
| adult | logreg | kshap_nsauto_bg50 | 109.4 | 103.4 | 1.076e+05 | 2 | 12 | 2.346e+07 |
| adult | logreg | lime_kw0p75_ns1000 | 15.62 | 9.348 | 1000 | 1 | 12 | 2.18e+05 |
| adult | logreg | lime_kw0p75_ns2000 | 15.62 | 19.58 | 2000 | 1 | 12 | 4.36e+05 |
| adult | logreg | lime_kw0p75_ns250 | 0 | 4.065 | 250 | 1 | 12 | 5.45e+04 |
| adult | logreg | lime_kw0p75_ns500 | 0 | 5.561 | 500 | 1 | 12 | 1.09e+05 |
| adult | logreg | lime_kw0p75_ns5000 | 46.88 | 47.29 | 5000 | 1 | 12 | 1.09e+06 |
| adult | logreg | lime_kw10p0_ns1000 | 15.62 | 9.304 | 1000 | 1 | 12 | 2.18e+05 |
| adult | logreg | lime_kw10p0_ns2000 | 15.62 | 19.64 | 2000 | 1 | 12 | 4.36e+05 |
| adult | logreg | lime_kw10p0_ns250 | 0 | 4.186 | 250 | 1 | 12 | 5.45e+04 |
| adult | logreg | lime_kw10p0_ns500 | 0 | 5.575 | 500 | 1 | 12 | 1.09e+05 |
| adult | logreg | lime_kw10p0_ns5000 | 46.88 | 47.27 | 5000 | 1 | 12 | 1.09e+06 |
| adult | logreg | lime_kw15p0_ns1000 | 15.62 | 9.263 | 1000 | 1 | 12 | 2.18e+05 |
| adult | logreg | lime_kw15p0_ns2000 | 15.62 | 19.55 | 2000 | 1 | 12 | 4.36e+05 |
| adult | logreg | lime_kw15p0_ns250 | 0 | 4.149 | 250 | 1 | 12 | 5.45e+04 |
| adult | logreg | lime_kw15p0_ns500 | 0 | 5.611 | 500 | 1 | 12 | 1.09e+05 |
| adult | logreg | lime_kw15p0_ns5000 | 46.88 | 47.33 | 5000 | 1 | 12 | 1.09e+06 |
| adult | logreg | lime_kw1p5_ns1000 | 15.62 | 9.413 | 1000 | 1 | 12 | 2.18e+05 |
| adult | logreg | lime_kw1p5_ns2000 | 15.62 | 19.79 | 2000 | 1 | 12 | 4.36e+05 |
| adult | logreg | lime_kw1p5_ns250 | 0 | 4.068 | 250 | 1 | 12 | 5.45e+04 |
| adult | logreg | lime_kw1p5_ns500 | 0 | 5.564 | 500 | 1 | 12 | 1.09e+05 |
| adult | logreg | lime_kw1p5_ns5000 | 46.88 | 48.16 | 5000 | 1 | 12 | 1.09e+06 |
| adult | logreg | lime_kw3p0_ns1000 | 15.62 | 9.55 | 1000 | 1 | 12 | 2.18e+05 |
| adult | logreg | lime_kw3p0_ns2000 | 15.62 | 19.6 | 2000 | 1 | 12 | 4.36e+05 |
| adult | logreg | lime_kw3p0_ns250 | 0 | 4.313 | 250 | 1 | 12 | 5.45e+04 |
| adult | logreg | lime_kw3p0_ns500 | 0 | 5.616 | 500 | 1 | 12 | 1.09e+05 |
| adult | logreg | lime_kw3p0_ns5000 | 46.88 | 47.35 | 5000 | 1 | 12 | 1.09e+06 |
| adult | logreg | lime_kw5p0_ns1000 | 15.62 | 9.336 | 1000 | 1 | 12 | 2.18e+05 |
| adult | logreg | lime_kw5p0_ns2000 | 15.62 | 19.78 | 2000 | 1 | 12 | 4.36e+05 |
| adult | logreg | lime_kw5p0_ns250 | 0 | 4.212 | 250 | 1 | 12 | 5.45e+04 |
| adult | logreg | lime_kw5p0_ns500 | 0 | 5.679 | 500 | 1 | 12 | 1.09e+05 |
| adult | logreg | lime_kw5p0_ns5000 | 46.88 | 47.71 | 5000 | 1 | 12 | 1.09e+06 |
| adult | logreg | lime_kwdef_ns1000 | 15.62 | 9.315 | 1000 | 1 | 12 | 2.18e+05 |
| adult | logreg | lime_kwdef_ns2000 | 15.62 | 19.63 | 2000 | 1 | 12 | 4.36e+05 |
| adult | logreg | lime_kwdef_ns250 | 0 | 4.306 | 250 | 1 | 12 | 5.45e+04 |
| adult | logreg | lime_kwdef_ns500 | 0 | 5.496 | 500 | 1 | 12 | 1.09e+05 |
| adult | logreg | lime_kwdef_ns5000 | 46.88 | 47.77 | 5000 | 1 | 12 | 1.09e+06 |
| adult | mlp | kshap_ns1000_bg50 | 93.75 | 89.31 | 5e+04 | 2 | 12 | 1.11e+09 |
| adult | mlp | kshap_ns100_bg50 | 15.62 | 16.74 | 5001 | 2 | 12 | 1.11e+08 |
| adult | mlp | kshap_ns250_bg50 | 31.25 | 30.16 | 1.25e+04 | 2 | 12 | 2.775e+08 |
| adult | mlp | kshap_ns500_bg10 | 15.62 | 22.55 | 5001 | 2 | 12 | 1.11e+08 |
| adult | mlp | kshap_ns500_bg100 | 78.12 | 82.87 | 5e+04 | 2 | 12 | 1.11e+09 |
| adult | mlp | kshap_ns500_bg25 | 31.25 | 33.82 | 1.25e+04 | 2 | 12 | 2.775e+08 |
| adult | mlp | kshap_ns500_bg50 | 46.88 | 50.94 | 2.5e+04 | 2 | 12 | 5.55e+08 |
| adult | mlp | kshap_nsauto_bg50 | 187.5 | 185 | 1.076e+05 | 2 | 12 | 2.389e+09 |
| adult | mlp | lime_kw0p75_ns1000 | 15.62 | 9.882 | 1000 | 1 | 12 | 2.22e+07 |
| adult | mlp | lime_kw0p75_ns2000 | 15.62 | 21.08 | 2000 | 1 | 12 | 4.44e+07 |
| adult | mlp | lime_kw0p75_ns250 | 0 | 4.321 | 250 | 1 | 12 | 5.55e+06 |
| adult | mlp | lime_kw0p75_ns500 | 0 | 6.081 | 500 | 1 | 12 | 1.11e+07 |
| adult | mlp | lime_kw0p75_ns5000 | 46.88 | 52.3 | 5000 | 1 | 12 | 1.11e+08 |
| adult | mlp | lime_kw10p0_ns1000 | 15.62 | 9.863 | 1000 | 1 | 12 | 2.22e+07 |
| adult | mlp | lime_kw10p0_ns2000 | 15.62 | 21.13 | 2000 | 1 | 12 | 4.44e+07 |
| adult | mlp | lime_kw10p0_ns250 | 0 | 4.507 | 250 | 1 | 12 | 5.55e+06 |
| adult | mlp | lime_kw10p0_ns500 | 0 | 5.905 | 500 | 1 | 12 | 1.11e+07 |
| adult | mlp | lime_kw10p0_ns5000 | 46.88 | 52.17 | 5000 | 1 | 12 | 1.11e+08 |
| adult | mlp | lime_kw15p0_ns1000 | 15.62 | 9.876 | 1000 | 1 | 12 | 2.22e+07 |
| adult | mlp | lime_kw15p0_ns2000 | 15.62 | 20.99 | 2000 | 1 | 12 | 4.44e+07 |
| adult | mlp | lime_kw15p0_ns250 | 0 | 4.434 | 250 | 1 | 12 | 5.55e+06 |
| adult | mlp | lime_kw15p0_ns500 | 0 | 5.804 | 500 | 1 | 12 | 1.11e+07 |
| adult | mlp | lime_kw15p0_ns5000 | 46.88 | 52.08 | 5000 | 1 | 12 | 1.11e+08 |
| adult | mlp | lime_kw1p5_ns1000 | 15.62 | 9.958 | 1000 | 1 | 12 | 2.22e+07 |
| adult | mlp | lime_kw1p5_ns2000 | 15.62 | 21.12 | 2000 | 1 | 12 | 4.44e+07 |
| adult | mlp | lime_kw1p5_ns250 | 0 | 4.473 | 250 | 1 | 12 | 5.55e+06 |
| adult | mlp | lime_kw1p5_ns500 | 0 | 5.955 | 500 | 1 | 12 | 1.11e+07 |
| adult | mlp | lime_kw1p5_ns5000 | 46.88 | 51.9 | 5000 | 1 | 12 | 1.11e+08 |
| adult | mlp | lime_kw3p0_ns1000 | 15.62 | 9.954 | 1000 | 1 | 12 | 2.22e+07 |
| adult | mlp | lime_kw3p0_ns2000 | 15.62 | 21.31 | 2000 | 1 | 12 | 4.44e+07 |
| adult | mlp | lime_kw3p0_ns250 | 0 | 4.391 | 250 | 1 | 12 | 5.55e+06 |
| adult | mlp | lime_kw3p0_ns500 | 0 | 5.966 | 500 | 1 | 12 | 1.11e+07 |
| adult | mlp | lime_kw3p0_ns5000 | 46.88 | 52.03 | 5000 | 1 | 12 | 1.11e+08 |
| adult | mlp | lime_kw5p0_ns1000 | 15.62 | 9.816 | 1000 | 1 | 12 | 2.22e+07 |
| adult | mlp | lime_kw5p0_ns2000 | 15.62 | 21.26 | 2000 | 1 | 12 | 4.44e+07 |
| adult | mlp | lime_kw5p0_ns250 | 0 | 4.327 | 250 | 1 | 12 | 5.55e+06 |
| adult | mlp | lime_kw5p0_ns500 | 0 | 5.958 | 500 | 1 | 12 | 1.11e+07 |
| adult | mlp | lime_kw5p0_ns5000 | 46.88 | 51.8 | 5000 | 1 | 12 | 1.11e+08 |
| adult | mlp | lime_kwdef_ns1000 | 15.62 | 9.842 | 1000 | 1 | 12 | 2.22e+07 |
| adult | mlp | lime_kwdef_ns2000 | 15.62 | 21.03 | 2000 | 1 | 12 | 4.44e+07 |
| adult | mlp | lime_kwdef_ns250 | 0 | 4.212 | 250 | 1 | 12 | 5.55e+06 |
| adult | mlp | lime_kwdef_ns500 | 0 | 5.964 | 500 | 1 | 12 | 1.11e+07 |
| adult | mlp | lime_kwdef_ns5000 | 46.88 | 51.35 | 5000 | 1 | 12 | 1.11e+08 |
| adult | rf | kshap_ns1000_bg50 | 359.4 | 360.3 | 5e+04 | 2 | 12 |  |
| adult | rf | kshap_ns100_bg50 | 46.88 | 51.37 | 5001 | 2 | 12 |  |
| adult | rf | kshap_ns250_bg50 | 109.4 | 109.7 | 1.25e+04 | 2 | 12 |  |
| adult | rf | kshap_ns500_bg10 | 62.5 | 56.06 | 5001 | 2 | 12 |  |
| adult | rf | kshap_ns500_bg100 | 343.8 | 352.3 | 5e+04 | 2 | 12 |  |
| adult | rf | kshap_ns500_bg25 | 109.4 | 112.7 | 1.25e+04 | 2 | 12 |  |
| adult | rf | kshap_ns500_bg50 | 187.5 | 189.2 | 2.5e+04 | 2 | 12 |  |
| adult | rf | kshap_nsauto_bg50 | 781.2 | 790.5 | 1.077e+05 | 2 | 12 |  |
| adult | rf | lime_kw0p75_ns1000 | 15.62 | 21.24 | 1000 | 1 | 12 |  |
| adult | rf | lime_kw0p75_ns2000 | 46.88 | 39.86 | 2000 | 1 | 12 |  |
| adult | rf | lime_kw0p75_ns250 | 15.62 | 11.23 | 250 | 1 | 12 |  |
| adult | rf | lime_kw0p75_ns500 | 15.62 | 14.6 | 500 | 1 | 12 |  |
| adult | rf | lime_kw0p75_ns5000 | 93.75 | 90.82 | 5000 | 1 | 12 |  |
| adult | rf | lime_kw10p0_ns1000 | 15.62 | 21.39 | 1000 | 1 | 12 |  |
| adult | rf | lime_kw10p0_ns2000 | 46.88 | 40.25 | 2000 | 1 | 12 |  |
| adult | rf | lime_kw10p0_ns250 | 15.62 | 10.98 | 250 | 1 | 12 |  |
| adult | rf | lime_kw10p0_ns500 | 15.62 | 14.44 | 500 | 1 | 12 |  |
| adult | rf | lime_kw10p0_ns5000 | 93.75 | 91.38 | 5000 | 1 | 12 |  |
| adult | rf | lime_kw15p0_ns1000 | 15.62 | 21.4 | 1000 | 1 | 12 |  |
| adult | rf | lime_kw15p0_ns2000 | 46.88 | 39.73 | 2000 | 1 | 12 |  |
| adult | rf | lime_kw15p0_ns250 | 15.62 | 11.15 | 250 | 1 | 12 |  |
| adult | rf | lime_kw15p0_ns500 | 15.62 | 14.46 | 500 | 1 | 12 |  |
| adult | rf | lime_kw15p0_ns5000 | 93.75 | 91.3 | 5000 | 1 | 12 |  |
| adult | rf | lime_kw1p5_ns1000 | 15.62 | 21.43 | 1000 | 1 | 12 |  |
| adult | rf | lime_kw1p5_ns2000 | 46.88 | 39.76 | 2000 | 1 | 12 |  |
| adult | rf | lime_kw1p5_ns250 | 15.62 | 11.02 | 250 | 1 | 12 |  |
| adult | rf | lime_kw1p5_ns500 | 15.62 | 14.59 | 500 | 1 | 12 |  |
| adult | rf | lime_kw1p5_ns5000 | 93.75 | 91.23 | 5000 | 1 | 12 |  |
| adult | rf | lime_kw3p0_ns1000 | 15.62 | 21.47 | 1000 | 1 | 12 |  |
| adult | rf | lime_kw3p0_ns2000 | 46.88 | 39.7 | 2000 | 1 | 12 |  |
| adult | rf | lime_kw3p0_ns250 | 15.62 | 10.92 | 250 | 1 | 12 |  |
| adult | rf | lime_kw3p0_ns500 | 15.62 | 14.46 | 500 | 1 | 12 |  |
| adult | rf | lime_kw3p0_ns5000 | 93.75 | 91.07 | 5000 | 1 | 12 |  |
| adult | rf | lime_kw5p0_ns1000 | 15.62 | 21.14 | 1000 | 1 | 12 |  |
| adult | rf | lime_kw5p0_ns2000 | 46.88 | 39.77 | 2000 | 1 | 12 |  |
| adult | rf | lime_kw5p0_ns250 | 15.62 | 10.91 | 250 | 1 | 12 |  |
| adult | rf | lime_kw5p0_ns500 | 15.62 | 14.56 | 500 | 1 | 12 |  |
| adult | rf | lime_kw5p0_ns5000 | 93.75 | 92.31 | 5000 | 1 | 12 |  |
| adult | rf | lime_kwdef_ns1000 | 15.62 | 21.31 | 1000 | 1 | 12 |  |
| adult | rf | lime_kwdef_ns2000 | 46.88 | 39.64 | 2000 | 1 | 12 |  |
| adult | rf | lime_kwdef_ns250 | 15.62 | 11.03 | 250 | 1 | 12 |  |
| adult | rf | lime_kwdef_ns500 | 15.62 | 14.73 | 500 | 1 | 12 |  |
| adult | rf | lime_kwdef_ns5000 | 93.75 | 92.19 | 5000 | 1 | 12 |  |
| adult | rf | tshap_bg10 | 7.812 | 8.703 | 0 | 0 | 12 |  |
| adult | rf | tshap_bg100 | 39.06 | 47.34 | 0 | 0 | 12 |  |
| adult | rf | tshap_bg25 | 15.62 | 14.75 | 0 | 0 | 12 |  |
| adult | rf | tshap_bg50 | 23.44 | 25.5 | 0 | 0 | 12 |  |
| adult | svm | kshap_ns1000_bg50 | 3.805e+04 | 3.825e+04 | 5e+04 | 2 | 12 |  |
| adult | svm | kshap_ns100_bg50 | 3820 | 3838 | 5001 | 2 | 12 |  |
| adult | svm | kshap_ns250_bg50 | 9516 | 9572 | 1.25e+04 | 2 | 12 |  |
| adult | svm | kshap_ns500_bg10 | 3812 | 3826 | 5001 | 2 | 12 |  |
| adult | svm | kshap_ns500_bg100 | 3.8e+04 | 3.826e+04 | 5e+04 | 2 | 12 |  |
| adult | svm | kshap_ns500_bg25 | 9531 | 9571 | 1.25e+04 | 2 | 12 |  |
| adult | svm | kshap_ns500_bg50 | 1.907e+04 | 1.923e+04 | 2.5e+04 | 2 | 12 |  |
| adult | svm | kshap_nsauto_bg50 | 8.197e+04 | 8.252e+04 | 1.076e+05 | 2 | 12 |  |
| adult | svm | lime_kw0p75_ns1000 | 765.6 | 767.1 | 1000 | 1 | 12 |  |
| adult | svm | lime_kw0p75_ns2000 | 1539 | 1548 | 2000 | 1 | 12 |  |
| adult | svm | lime_kw0p75_ns250 | 187.5 | 193.8 | 250 | 1 | 12 |  |
| adult | svm | lime_kw0p75_ns500 | 390.6 | 383.7 | 500 | 1 | 12 |  |
| adult | svm | lime_kw0p75_ns5000 | 3836 | 3859 | 5000 | 1 | 12 |  |
| adult | svm | lime_kw10p0_ns1000 | 765.6 | 769.7 | 1000 | 1 | 12 |  |
| adult | svm | lime_kw10p0_ns2000 | 1539 | 1551 | 2000 | 1 | 12 |  |
| adult | svm | lime_kw10p0_ns250 | 195.3 | 195.8 | 250 | 1 | 12 |  |
| adult | svm | lime_kw10p0_ns500 | 390.6 | 388 | 500 | 1 | 12 |  |
| adult | svm | lime_kw10p0_ns5000 | 3844 | 3862 | 5000 | 1 | 12 |  |
| adult | svm | lime_kw15p0_ns1000 | 765.6 | 774.5 | 1000 | 1 | 12 |  |
| adult | svm | lime_kw15p0_ns2000 | 1539 | 1553 | 2000 | 1 | 12 |  |
| adult | svm | lime_kw15p0_ns250 | 187.5 | 194.9 | 250 | 1 | 12 |  |
| adult | svm | lime_kw15p0_ns500 | 390.6 | 389 | 500 | 1 | 12 |  |
| adult | svm | lime_kw15p0_ns5000 | 3859 | 3887 | 5000 | 1 | 12 |  |
| adult | svm | lime_kw1p5_ns1000 | 765.6 | 767.9 | 1000 | 1 | 12 |  |
| adult | svm | lime_kw1p5_ns2000 | 1531 | 1540 | 2000 | 1 | 12 |  |
| adult | svm | lime_kw1p5_ns250 | 187.5 | 195.8 | 250 | 1 | 12 |  |
| adult | svm | lime_kw1p5_ns500 | 382.8 | 385.2 | 500 | 1 | 12 |  |
| adult | svm | lime_kw1p5_ns5000 | 3820 | 3846 | 5000 | 1 | 12 |  |
| adult | svm | lime_kw3p0_ns1000 | 765.6 | 773.7 | 1000 | 1 | 12 |  |
| adult | svm | lime_kw3p0_ns2000 | 1547 | 1545 | 2000 | 1 | 12 |  |
| adult | svm | lime_kw3p0_ns250 | 203.1 | 195.2 | 250 | 1 | 12 |  |
| adult | svm | lime_kw3p0_ns500 | 390.6 | 388.7 | 500 | 1 | 12 |  |
| adult | svm | lime_kw3p0_ns5000 | 3836 | 3866 | 5000 | 1 | 12 |  |
| adult | svm | lime_kw5p0_ns1000 | 765.6 | 771.1 | 1000 | 1 | 12 |  |
| adult | svm | lime_kw5p0_ns2000 | 1531 | 1539 | 2000 | 1 | 12 |  |
| adult | svm | lime_kw5p0_ns250 | 203.1 | 194.7 | 250 | 1 | 12 |  |
| adult | svm | lime_kw5p0_ns500 | 390.6 | 384.5 | 500 | 1 | 12 |  |
| adult | svm | lime_kw5p0_ns5000 | 3836 | 3854 | 5000 | 1 | 12 |  |
| adult | svm | lime_kwdef_ns1000 | 765.6 | 771.4 | 1000 | 1 | 12 |  |
| adult | svm | lime_kwdef_ns2000 | 1547 | 1551 | 2000 | 1 | 12 |  |
| adult | svm | lime_kwdef_ns250 | 187.5 | 196.7 | 250 | 1 | 12 |  |
| adult | svm | lime_kwdef_ns500 | 390.6 | 385.5 | 500 | 1 | 12 |  |
| adult | svm | lime_kwdef_ns5000 | 3844 | 3869 | 5000 | 1 | 12 |  |
| adult | xgb | kshap_ns1000_bg50 | 203.1 | 198.1 | 5e+04 | 2 | 12 |  |
| adult | xgb | kshap_ns100_bg50 | 31.25 | 28.41 | 5001 | 2 | 12 |  |
| adult | xgb | kshap_ns250_bg50 | 62.5 | 57.06 | 1.25e+04 | 2 | 12 |  |
| adult | xgb | kshap_ns500_bg10 | 31.25 | 34.5 | 5001 | 2 | 12 |  |
| adult | xgb | kshap_ns500_bg100 | 187.5 | 189.5 | 5e+04 | 2 | 12 |  |
| adult | xgb | kshap_ns500_bg25 | 62.5 | 61.06 | 1.25e+04 | 2 | 12 |  |
| adult | xgb | kshap_ns500_bg50 | 109.4 | 102.6 | 2.5e+04 | 2 | 12 |  |
| adult | xgb | kshap_nsauto_bg50 | 406.2 | 413.1 | 1.076e+05 | 2 | 12 |  |
| adult | xgb | lime_kw0p75_ns1000 | 15.62 | 12.84 | 1000 | 1 | 12 |  |
| adult | xgb | lime_kw0p75_ns2000 | 31.25 | 26.39 | 2000 | 1 | 12 |  |
| adult | xgb | lime_kw0p75_ns250 | 0 | 5.669 | 250 | 1 | 12 |  |
| adult | xgb | lime_kw0p75_ns500 | 0 | 7.898 | 500 | 1 | 12 |  |
| adult | xgb | lime_kw0p75_ns5000 | 62.5 | 63.98 | 5000 | 1 | 12 |  |
| adult | xgb | lime_kw10p0_ns1000 | 15.62 | 12.67 | 1000 | 1 | 12 |  |
| adult | xgb | lime_kw10p0_ns2000 | 31.25 | 26.27 | 2000 | 1 | 12 |  |
| adult | xgb | lime_kw10p0_ns250 | 0 | 5.704 | 250 | 1 | 12 |  |
| adult | xgb | lime_kw10p0_ns500 | 0 | 7.844 | 500 | 1 | 12 |  |
| adult | xgb | lime_kw10p0_ns5000 | 62.5 | 63.43 | 5000 | 1 | 12 |  |
| adult | xgb | lime_kw15p0_ns1000 | 15.62 | 12.68 | 1000 | 1 | 12 |  |
| adult | xgb | lime_kw15p0_ns2000 | 31.25 | 26.45 | 2000 | 1 | 12 |  |
| adult | xgb | lime_kw15p0_ns250 | 0 | 5.714 | 250 | 1 | 12 |  |
| adult | xgb | lime_kw15p0_ns500 | 15.62 | 7.906 | 500 | 1 | 12 |  |
| adult | xgb | lime_kw15p0_ns5000 | 62.5 | 62.55 | 5000 | 1 | 12 |  |
| adult | xgb | lime_kw1p5_ns1000 | 15.62 | 12.73 | 1000 | 1 | 12 |  |
| adult | xgb | lime_kw1p5_ns2000 | 31.25 | 26.55 | 2000 | 1 | 12 |  |
| adult | xgb | lime_kw1p5_ns250 | 0 | 5.725 | 250 | 1 | 12 |  |
| adult | xgb | lime_kw1p5_ns500 | 7.812 | 7.862 | 500 | 1 | 12 |  |
| adult | xgb | lime_kw1p5_ns5000 | 62.5 | 63.16 | 5000 | 1 | 12 |  |
| adult | xgb | lime_kw3p0_ns1000 | 15.62 | 12.75 | 1000 | 1 | 12 |  |
| adult | xgb | lime_kw3p0_ns2000 | 31.25 | 26.71 | 2000 | 1 | 12 |  |
| adult | xgb | lime_kw3p0_ns250 | 0 | 5.655 | 250 | 1 | 12 |  |
| adult | xgb | lime_kw3p0_ns500 | 15.62 | 8.045 | 500 | 1 | 12 |  |
| adult | xgb | lime_kw3p0_ns5000 | 62.5 | 62.82 | 5000 | 1 | 12 |  |
| adult | xgb | lime_kw5p0_ns1000 | 15.62 | 12.67 | 1000 | 1 | 12 |  |
| adult | xgb | lime_kw5p0_ns2000 | 31.25 | 26.82 | 2000 | 1 | 12 |  |
| adult | xgb | lime_kw5p0_ns250 | 0 | 5.796 | 250 | 1 | 12 |  |
| adult | xgb | lime_kw5p0_ns500 | 7.812 | 7.857 | 500 | 1 | 12 |  |
| adult | xgb | lime_kw5p0_ns5000 | 62.5 | 63.18 | 5000 | 1 | 12 |  |
| adult | xgb | lime_kwdef_ns1000 | 15.62 | 12.95 | 1000 | 1 | 12 |  |
| adult | xgb | lime_kwdef_ns2000 | 31.25 | 26.71 | 2000 | 1 | 12 |  |
| adult | xgb | lime_kwdef_ns250 | 0 | 5.679 | 250 | 1 | 12 |  |
| adult | xgb | lime_kwdef_ns500 | 15.62 | 7.857 | 500 | 1 | 12 |  |
| adult | xgb | lime_kwdef_ns5000 | 62.5 | 63.33 | 5000 | 1 | 12 |  |
| adult | xgb | tshap_bg10 | 0 | 0.3995 | 0 | 0 | 12 |  |
| adult | xgb | tshap_bg100 | 0 | 2.741 | 0 | 0 | 12 |  |
| adult | xgb | tshap_bg25 | 0 | 0.8 | 0 | 0 | 12 |  |
| adult | xgb | tshap_bg50 | 0 | 1.387 | 0 | 0 | 12 |  |
