# Scientific Rigor Review: Paper E (SHAP–LIME instance-level agreement, Computación y Sistemas)

**Date**: 2026-10-04 | **Reviewer role**: Scientific Advisor | **Grade**: Major revision
**Mean score**: 3.3 | **Dimensions**: D1=3 D2=3.5 D3=3 D4=4.5 D5'=3.5 D6=2.5

**Scope reviewed**: `docs/reports/paper_e/paper_e.tex` (rendered; line numbers below refer to it), `paper_e_template.tex`, `tables/*.tex`, `references.bib`, `submission/paper_e_blind.pdf` (text and metadata), `ANALYSIS_PLAN.md`, `DATA_AUDIT.md`, `README.md`; `scripts/analyze_paper_e.py`, `docs/reports/paper_e/scripts/paper_e_posthoc.py`, `paper_e_sign_contribution.py`; `src/xai/lime_tabular.py`, `src/xai/shap_tabular.py`, `src/experiment/runner.py`, `src/experiment/metrics_engine.py`, `src/metrics/faithfulness.py`, `src/metrics/stability.py`, `src/evaluation/sampler.py`, `scripts/run_exp3_lime.py`, `configs/experiments/exp2_scaled/*`; the installed `lime` 0.2.0.1 source; all CSVs under `outputs/analysis/paper_e/analysis/` and `posthoc/`; the raw SHAP and LIME run files (read to recompute the sign analysis).
**Prior review**: none for Paper E. This is the first.
**Regression guards**: no Paper E file is under RCA-001/002/003 path guards. `python scripts/pubs/verify_claims.py`: "OK: 783 claims re-derived from artifacts, 996 manuscript sites checked, 48 retired-value guards clear, 13 cited artifacts present, 26 file(s) fully registered, 20 file(s) clear of unpublished results".
**Not read**: `docs/context/ACTIVE_CONTEXT.md` (2,381 lines) was not read in full.

**How to read the evidence labels.** *Re-derived* = I recomputed the number from the CSVs or raw runs. *Code* = I read the code or the `lime` package source. *Probe* = a small experiment I ran outside the repository (6 or 60 instances per model, Adult, seed 42, `n_50`); it indicates a problem and its rough size and is not an estimate fit to publish. *Inference* = my reasoning, not checked against data. *Web* = abstract or search-result level only; I did not read the full text of the cited papers.

## One-line summary

The numbers in the manuscript are all reproducible from the result files and the post hoc sign conversion is implemented correctly, but four interpretations are stronger than the evidence: there is no within-method reproducibility ceiling for the overlap (LIME does not reproduce its own top-5), the converted sign agreement is matched by a constant per-feature direction, the correctness contrast on Adult is confounded with training-set membership, and the "95% intervals" with three seeds are the range of three seed means.

## Strengths

- Every number I re-derived matches (list under "Verified, no finding").
- The unit of analysis is right: run means, seed as resampling unit, no p-values, pooled instance counts never used as n.
- The post hoc status of the sign analysis is stated in the abstract, the section title, the table caption, the registration subsection and the limitations.
- The sign script's alignment checks (labels, array hashes) are real and all 86 blocks pass; its slope-based recomputation reproduces the prespecified values.
- Limitations are unusually candid (training overlap, regenerated binaries, RF binary mismatch).

## Findings

### F01 [major] — D1 / D6. The overlap is compared with identity and with chance, but not with what LIME reproduces of itself

**Passages.** Abstract, l.75–76: "well above the overlap of random feature sets but far from identity". Discussion, l.591–597: "A user who reads a top-5 list would see a different list with the other method … so it is not an artefact of a particular sample of instances." l.599–603: "Agreement is a property of the model and the data."

**Evidence.**
- *Probe.* I re-ran LIME with the repository wrapper and settings (1000 samples, kernel width 3, 10 features) twice with different random states on the first 60 stored instances of three Adult models (seed 42, `n_50`; the loaded models reproduced all 60 stored predictions). Top-5 Jaccard between the two LIME runs of the same instance and model: 0.73 (LR), 0.68 (XGB), 0.53 (MLP). Rerun versus the stored LIME top-5: 0.74, 0.70, 0.60. Stored LIME versus SHAP on the same 60 instances: 0.52, 0.43, 0.34.
- *Re-derived* from `instance_agreement.csv`: the stored LIME stability on Adult (cosine similarity over 15 noisy copies) has median 0.001–0.009 and maximum about 0.3 for every model family; on German Credit and Breast Cancer it is 0.79–0.96. SHAP stability on Adult is 0.23–0.98.
- *Code.* `lime_base.py`: with 10 requested features LIME selects them by `highest_weights` from a preliminary ridge fit, then refits; with 1000 samples in 108 dimensions the selection is noisy.

**What is wrong.** The upper reference for SHAP–LIME overlap is not 1 but the overlap of LIME with itself. On the probe, between a third and a half of the gap to identity is LIME's own sampling variability. The ordering of the model families in SHAP–LIME agreement (LR highest, MLP lowest) is the same as the ordering of LIME's self-agreement, so "agreement depends on the model family" may in part be "LIME's Monte Carlo noise depends on the model family". The sentence that the result is not an artefact of the sample of instances is true but does not address this. KernelSHAP variability (50 background rows) was not measured by me and is a second, unquantified part of the ceiling.

**Fix.** Add a ceiling analysis as a dated deviation: LIME–LIME (and KernelSHAP–KernelSHAP) top-5 overlap for the same instances with a different random state, at least on a subsample per model family, summarised with the same procedure. Report SHAP–LIME overlap next to it. Reword "far from identity" and the first two Discussion paragraphs so that method disagreement and within-method irreproducibility are separated. State in the limitations that 1000 LIME samples were used for 108 features and that the stored LIME stability on Adult is near zero (the plan forbids publishing pooled quality means; one sentence about the range is a deviation worth logging).

### F02 [major] — D1 / D3 / D5'. The converted sign agreement is reproduced by a constant direction per feature; the paper does not say so

**Passages.** Abstract, l.82–86: "After the slopes were converted into contributions, the two methods agreed on the sign of 0.945 to 0.990 of the shared top features. The two explainers therefore differ in which features they rank first, not in the direction they assign to them." l.437: "The direct test confirms this explanation." l.451–455; l.612–615; l.666–670.

**Evidence (all re-derived from the raw runs with reloaded feature values; my recomputation reproduces 0.374/0.990, 0.717/0.945, 0.511/0.960).**
1. *Baseline with no instance-level LIME information.* Replace the sign of each LIME slope by the majority sign of that feature's slope in the same run, then convert. Agreement with SHAP: Adult 0.962, German Credit 0.970, Breast Cancer 0.990 (mean of run means). That is equal to or higher than the reported 0.945, 0.960, 0.990. Using the majority sign over all runs of the dataset and model gives 0.966, 0.973, 0.990.
2. *Mechanical factor.* sign(c_j) = sign(w_j)·sign(x_j − m_j). For a model that is close to monotone in a feature, sign(SHAP_j) = direction_j·sign(x_j − reference_j). Both sides carry the same factor sign(x_j − m_j), which is data, not explanation. For one-hot columns it is fixed by the category: on Adult binary features the slope-based agreement is 0.927 when the category is active and 0.042 when it is not (German Credit 0.945 and 0.003); the conversion flips the second group. What is left to "agree" is one sign per feature.
3. *Predicted-class confound: checked, mostly not the explanation.* Top SHAP values and converted LIME values both tend to point toward the predicted class (pooled over shared features: Adult 0.81 and 0.84; German Credit 0.69 and 0.71; Breast Cancer 0.975 and 0.966). If the two were independent given the class, agreement would be 0.71, 0.58 and 0.94. Observed pooled agreement is 0.95, 0.96, 0.99, and it stays at 0.78 (Adult), 0.91 (German Credit), 0.99 (Breast Cancer, n = 70) on features where SHAP points against the predicted class. So on Adult and German Credit the result is well above this baseline. On Breast Cancer the baseline is already 0.94, so 0.99 carries little extra information there.
4. *Possible artefact, partly evidenced.* (Probe, 6 logistic-regression instances, with the true gradient computed analytically.) LIME samples around the training mean, not around the instance; the nearest perturbed sample is 9–10 standardised units away, the kernel weights of all 999 samples sum to 0.2–1.2 against weight 1 for the instance and ridge penalty 1. Slopes are shrunk 3–10 times relative to the true gradient, and for active rare categories (z of 3–5) the coefficient is pulled toward sign(z)·sign(f(x) − mean prediction): e.g. `workclass_Self-emp…` true 0.005, LIME 0.034. After conversion this component has the sign of f(x) − mean prediction, which is where SHAP's top features also point. The drop of agreement to 0.78 when SHAP points against the predicted class is consistent with this. I did not quantify how much of the 0.945 it accounts for.

**Is the conversion formula right?** Yes (*code*). `lime_tabular.py` l.257–258, 348: `StandardScaler(with_mean=False)` still stores `mean_`; the local model is fitted on `(data − mean_)/scale_`; no categorical features are declared, so every column, including one-hot columns, is treated this way. The script uses `x_train.mean(axis=0)` of the same partition given to LIME, and the sign does not need `s_j`.

**What is wrong.** The numbers are correct and the explanation of the low prespecified value (slope versus contribution) is correct. What does not follow is the reading that this is instance-level agreement between two explainers. An "explainer" that returns one fixed direction per feature scores the same. The result says: for features both methods rank in the top five, SHAP's sign equals a single global direction times the side of the mean in about 95% of cases, and LIME's slope has that global direction. That is a statement about near-monotone models and about LIME's slopes being globally constant (which the constancy measure already shows), not a test that could have failed in an informative way against a 0.5 null. "The direct test confirms" overstates it; so does "therefore … not in the direction they assign" in the abstract, which also drops the conditioning on shared features (2.7 of 5 on Adult and German Credit).

**Fix.** Report the majority-sign baseline and the conditional-independence baseline beside the converted agreement, in Table 2 or in the text. Replace "The direct test confirms this explanation" by a sentence that states what the conversion removes (the side-of-the-mean factor) and what remains (one direction per feature). In the abstract and conclusions, restrict the claim: "on the features both methods place in the top five, the two methods imply the same direction of effect in 0.945 to 0.990 of cases; a constant direction per feature reproduces this figure". Add the LIME sampling/regularisation behaviour to the limitations.

### F03 [major] — D6 / D5'. On Adult the correct-versus-misclassified contrast is a training-versus-held-out contrast for four of five seeds

**Passages.** l.193–196: "so part of the explained instances belong to the training data of the model". l.484–489: MLP "same direction in all five seeds", RF "0.045, 0.029 to 0.064, all five seeds". Limitations l.641–645.

**Evidence (re-derived by matching the feature row of every paired Adult instance against the seed-42 training matrix; seed 42 itself gives 0.1% matches, so false matches are negligible).**
- Share of paired explained instances that are training rows: 0.71, 0.71, 0.72, 0.69 for seeds 123, 456, 789, 999. "Part" is about 70%.
- Random forest, seeds other than 42: 83–84% of correctly classified instances are training rows; 0.3–1.0% of misclassified instances are. The forest has memorised its training data, so its errors are almost all held-out rows. MLP: 81–84% versus 64–72%.
- RF top-5 overlap is lower on training rows than on held-out rows in every such seed (0.370 vs 0.415; 0.357 vs 0.371; 0.326 vs 0.357; 0.397 vs 0.456), the same direction as the reported contrast.
- The clean seed 42 gives RF +0.029 and MLP −0.041, the smallest RF value and the smallest MLP magnitude of the five (`correctness_contrasts.csv`).

**What is wrong.** For RF the reported +0.045 mixes correctness with training membership, and "all five seeds" counts four confounded seeds as support. Only seed 42 is a clean estimate, and it has no interval. The limitation sentence checks only the overall overlap for seed 42, not the contrast. Also, on Adult the seed does not retrain the model, so "five seeds" are five test partitions of one fitted model per family.

**Fix.** State the share (about 70%). Report the RQ3 contrast for seed 42 separately, or restricted to held-out rows in all seeds (a logged deviation), and base the RF and MLP sentences on that. Keep the overall conclusion ("no consistent direction") only if it survives.

### F04 [major] — D6. With three seeds the "95% interval" is the range of three seed means; with one fitted model per family the Adult intervals do not cover model variation

**Passages.** l.301–306: "The 95% interval is a percentile bootstrap … so the intervals describe variation between seeds and are not precise." l.387–388: "the intervals of these two families do not overlap". l.390: "with an interval that includes zero". Table 1 and Table 3 captions.

**Evidence (re-derived by enumerating all resamples).** With three clusters there are 27 equally likely resamples; each single-seed resample has probability 1/27 = 3.7% > 2.5%, so the percentile limits are the smallest and the largest seed mean. Breast Cancer top-5: seed means 0.671, 0.679, 0.792; reported interval 0.671 to 0.792. German Credit: 0.343, 0.391, 0.426; reported 0.343 to 0.426. With five seeds (Adult) the limits are close to the range as well (seed means 0.369–0.413; interval 0.377–0.410). On Adult each family has one fitted model (*code*, `runner.py::setup`; stated at l.193), so the interval reflects test partition, instance sampling and explainer randomness only.

**What is wrong.** "Not precise" is honest but too weak: these are not intervals with anything near 95% coverage, and for German Credit and Breast Cancer they are a min–max of three numbers. "Do not overlap" and "includes zero" use them as tests. The claim that agreement "depended on the model family" (abstract l.77) rests on Adult on a single trained model per family; the data cannot separate the family from that one fit.

**Fix.** Either call them "range of seed means" for the three-seed datasets, or keep the bootstrap and say in Methods and in the captions that with three seeds the limits equal the extreme seed means. Remove "do not overlap" and "includes zero" as arguments, or replace by the per-seed values (LR above MLP in all five seeds: verified). Say "the five fitted models" rather than "model families" where Adult is the only evidence, and add this to the limitations.

### F05 [minor] — D4 / D5'. Method description of LIME omits how the ten features are chosen and how local the fit is

**Passages.** l.231–236; l.244–245: "For each instance, a run stores the ten features with the largest absolute value, in that order."

**Evidence.** *Code*: `LIMETabularWrapper` passes `num_features=10`, `feature_selection='auto'`; `lime_base.py` l.77–135 then uses `highest_weights`: a ridge fit (alpha 0.01) on all features, selection of the ten with the largest |coefficient × standardised instance value|, and a second ridge fit (alpha 1) on those ten. *Probe*: 8–10 of LIME's ten features coincide with the ten largest |gradient × z| of the logistic regression, 6–8 with the ten largest |gradient|. So LIME's ten features are chosen by contribution size and then ordered by slope size. `sample_around_instance=False`: perturbations are drawn around the training mean with the training standard deviation, one-hot columns included.

**What is wrong.** The stored LIME list is not "the ten features with the largest absolute value" of a full coefficient vector. The top-10 set is contribution-selected (like SHAP's), the top-5 within it is slope-ordered. This matters for the reading of J5 versus J10 and of the rank measure, and the reader cannot know it. "Local slope" is also generous given the sampling (F02, item 4).

**Fix.** Describe the selection step and the sampling distribution in Section 3.2; state that all columns were treated as continuous.

### F06 [minor] — D6 / D1. Zero is not the "no association" value of the rank measure as constructed

**Passages.** l.353: "The order of the features agreed less than their identity." l.388–390; l.593: "the order of the features was almost unrelated for two model families".

**Evidence.** *Code*: τ_b is computed on the union of two top-10 lists with rank 11 for absent features. A feature in one list only is ranked ≤ 10 in one and 11 in the other, which creates discordant pairs by construction; the measure mixes set overlap with order. *Re-derived*: τ_b restricted to the features present in both lists (no imputation) is 0.19 (Adult), 0.24 (German Credit), 0.61 (Breast Cancer), against 0.126, 0.122, 0.517 reported.

**What is wrong.** The measure is prespecified and correctly computed. The interpretation is not: a Jaccard value and this τ are not on a common scale, so "agreed less than their identity" has no basis, and τ ≈ 0 does not mean unrelated order.

**Fix.** Say what the measure contains, drop the comparison with overlap and "almost unrelated", and optionally add the shared-only τ as a labelled sensitivity analysis.

### F07 [minor] — D1. "A slope and a contribution also differ in magnitude, which is one source of the low rank concordance" is asserted, and the available check does not support it

**Passage.** l.619–622.

**Evidence (re-derived).** Re-ranking LIME's ten stored features by |c_j| and recomputing: top-5 overlap 0.416 (Adult), 0.393 (German Credit), 0.633 (Breast Cancer) against 0.393, 0.387, 0.714; τ 0.149, 0.116, 0.443 against 0.126, 0.122, 0.517. Small gains on Adult, none on German Credit, a loss on Breast Cancer. Limit: only ten LIME features are stored, and they were already selected by contribution (F05).

**What is wrong.** The sentence states a cause that was not tested. The good news is the converse: the RQ1 estimates are not an artefact of ranking slopes against contributions, within the stored lists.

**Fix.** Report this sensitivity analysis (deviation) and replace the sentence by its result.

### F08 [minor] — D3 / D1. Wording stronger than the estimates

- Abstract l.77–78 and Conclusions l.661: agreement "did not depend on the number of explained instances". The data show 0.395, 0.394, 0.390 (re-derived). Write "did not vary visibly".
- l.398–400: "Explaining more instances makes the estimate of agreement more precise" was not shown; delete or show it.
- Abstract l.79–80: "Disagreement was larger where the fidelity of the LIME explanation was lower", without qualification. Breast Cancer XGB is +0.01. Under contribution re-ranking (re-derived) the Adult correlations hold (−0.39, −0.45, −0.20, −0.34, −0.38) but German Credit RF falls from −0.26 to −0.10. Qualify: "on Adult and, more weakly, German Credit".
- l.631–633: "Part of the disagreement may thus come from instances that LIME explains less well". The fidelity measure rewards attributions whose size tracks |effect of replacing the feature by its mean|, which is contribution-like; a slope vector is penalised by construction. The sentence at l.535–537 half-says this. State it plainly and drop "explains less well".
- l.626–627: "Disagreement between explainers is therefore not a usable signal of a wrong prediction" is a predictive claim; no predictive analysis was run and F03 applies. Write "we found no consistent association".
- l.603–604: "as for logistic regression, the approximations coincide more" is offered as mechanism; F01 gives a competing one.

### F09 [minor] — D5'. SVM coverage is understated and class-dependent

**Passages.** l.285–287; l.647–648: "KernelSHAP failed for part of the SVM instances, so that family has fewer pairs."

**Evidence (re-derived from `pairing_diagnostics.csv`, `row_exclusion_diagnostics.csv`).** SVM has 2,064 pairs of about 7,000 LIME instances (29%). Only 235 SHAP rows are error records; the remaining shortfall (4,936 unpaired LIME records, all SVM) is rows absent from the SHAP files, i.e. incomplete runs. Paired SVM instances are 765 predicted class 0 and 1,299 class 1; class-0 sign values exist in 6 of 14 runs and 4 of 5 seeds. The SVM "All" slope sign agreement (0.829, the highest) reflects that class mix. Table 3 shows 3/4 seeds for SVM without comment.

**Fix.** Give the coverage (29%), say the SHAP runs are incomplete rather than failed per instance, say whether completion could depend on the instance, and footnote the SVM rows of Tables 1–3.

### F10 [minor] — D5'. Pre-registration: wording and unreported plan items

- **"Registered".** Abstract l.71, l.324–328, Data Availability. *Verified with git*: plan commit `7726bb0a9` 2026-10-03 11:32; analysis script 12:27; result artefacts 16:01; post hoc 21:40 and 2026-10-04 08:04; the plan commit is on `origin`. The order holds. But this is a commit in the author's own repository, on the same day, with author-controlled timestamps, on a cohort the author had already analysed in two other papers. "Registered" suggests a registry. Use "pre-specified and committed to the public repository before…", and give the commit hash in the full version.
- **Plan §4/§5 items not in the manuscript**: medians of run means (computed, not reported); the sign-agreement denominator and coverage (plan: "Always report"): mean shared non-zero top-5 features is 2.69, 2.66, 4.05 and coverage is 1.0 (re-derived), only the 516 undefined pairs are given; intervals for the prespecified sign agreement (0.687–0.747, 0.481–0.528, 0.357–0.385) are in RESULTS.md but not in the text or Table 2; seed-level variability for RQ4 appears only in Fig. 4.
- **Post hoc label missing in places**: the chance reference (plan §9 item 3 says it is labelled post hoc wherever it appears) is presented in Methods l.275–279 and used in the abstract without the label; contribution (iv) in the Introduction l.143–146 and the Conclusions l.664–670 state the sign result without "post hoc". l.329 says "One analysis is post hoc"; the plan logs five (class split, constancy, chance reference, conversion, margins).
- **Plan §7**: the paper must disclose that the cohort also supports Paper B+C. The manuscript mentions one earlier publication and one companion manuscript (Paper D). If B+C is submitted or under review with the same runs, name it as a second companion.
- **Plan §1 premise**: "Both provide signed additive feature contributions" was false for this LIME configuration. The deviation log covers it; one sentence in Section 3.7 saying the plan's premise was wrong would be more direct than "it was broken down".

### F11 [minor] — D1. Citation–claim fit

- **Roy et al.**, l.157–159: "reported disagreement between LIME and SHAP for defect prediction models, on the features and on their sign". *Web* (abstract and secondary summaries): the paper uses feature, rank and sign agreement and reports that rank disagreements are the most frequent, more than sign disagreements. The sentence should say that, and the paper should be cited in Section 4.3/5 as earlier evidence that sign disagreement is the smaller problem. Full text not read.
- **Garreau and von Luxburg**, l.164–166 and l.609–611: cited for "a LIME coefficient without discretisation is a slope". *Web/inference*: their analysis is of tabular LIME in its default form, which discretises along quantile boxes; the proportional-to-gradient result is for that setting. Check Section 2 of the paper; if so, the citation supports "LIME coefficients track the gradient of a linear model", not the non-discretised case.
- **Alvarez-Melis and Jaakkola**, l.316–318: cited for the stability measure. Their measure is a local Lipschitz estimate; the cosine similarity over noisy copies is the repository's own. Write "in the spirit of". State the noise standard deviation (0.1 on the encoded scale, one-hot columns included; *code*).
- **Bhatt et al.**, l.313–316: their faithfulness correlates attribution sums with output changes over feature subsets; the stored metric is a single-feature, absolute-value variant (*code*, `faithfulness.py`). Write "a variant of".
- **Krishna, Neely, Han, Slack**: characterisations agree with the abstracts (*web*).
- **"to our knowledge"**, l.174–175: narrow ("with a clustered design") and defensible. Two searches found no earlier paper that reports the slope-versus-contribution sign issue for LIME without discretisation; several state in general terms that LIME weights and SHAP values are different quantities. I cannot establish absence.

### F12 [minor] — D4. The seed-42 reassurance holds for the overlap only

**Passage.** l.643–645: "the overall estimate for seed 42 … lies within the range of the other four seeds."
**Evidence (re-derived).** Top-5: 0.412 against 0.369–0.413 (inside, at the upper edge). Kendall: 0.160 against 0.083–0.154 (outside).
**Fix.** Name the measure, or give both.

### F13 [suggestion] — Journal fit and blind review

- CyS guidelines (*web*, fetched today): original results; "not available on line or under review simultaneously elsewhere"; PDF from LaTeX or Word; 10-pt Arial, single spacing; URLs in references; blind review. No page limit, abstract limit or fee is stated. The format conditions are met.
- **Risk**: the manuscript PDFs, title and results are in a public GitHub repository (`docs/reports/paper_e/submission/`), and Data Availability says so. A reviewer who searches the title finds the author, and an editor may read "not available on line" strictly. Decide before submitting: keep the PDFs out of the public branch until acceptance, or declare it in the cover letter.
- The blind PDF has no author in text or metadata (checked: `pdfinfo`, text search for name, affiliation, e-mail, repository, DOI of the earlier paper). The CreationDate carries a time zone; harmless.
- "A companion manuscript under review" is fine for blind review; the cover letter should identify it to the editor.

## Verified, no finding

- *Re-derived* from `instance_agreement.csv`: 31,411 pairs, 86 runs (74/6/6), 29,667/1,060/684; top-5 0.393/0.387/0.714; top-10 0.507/0.480/0.669; Kendall 0.126/0.122/0.517; sign 0.717/0.511/0.374; all per-model values of Table 1; intensity margins 0.395/0.394/0.390; sign by predicted class 0.977/0.036, 0.875/0.506; 0 undefined τ, 516 undefined sign; 87 blocks, 76 identical, 4,936 unpaired, 278 error rows.
- *Re-derived* from the raw runs with reloaded data: contribution-based sign agreement 0.945/0.960/0.990 and its by-class values; no feature at the training mean.
- Tables 2–5 agree with `sign_contribution_summary.csv`, `correctness_group_summary.csv`, `quality_association_summary.csv`, `secondary_group_summary.csv`; chance values 0.026/0.047/0.099; constancy 0.993/0.621, 0.912/0.679, 0.850/0.757.
- Abstract, text, tables and conclusions carry the same values. "Fewer than three shared features" (2.69, 2.66) and "above four" (4.05) hold.
- *Code*: `paper_e_sign_contribution.py` uses the same shared non-zero top-5 definition as `primary_agreement`; instance = `X_test[instance_id]` from the loader the runs used; mean = training mean of the partition given to LIME; feature-name-to-column map from the loader's names; conversion formula correct for `lime` 0.2.0.1 with `discretize_continuous=False`.
- *Code/config*: KernelSHAP for LR, SVM, MLP and TreeSHAP (interventional, probability) for RF, XGB; 50 background rows; LIME 1000 samples, kernel width 3, 10 features, no discretisation; top-10 stored by absolute value; quadrant sampling; fidelity and stability definitions; 15 perturbations; bootstrap 2000 resamples, seeds resampled, runs of a seed kept together; RQ3 minimum of ten per group.
- The LIME-fidelity association on Adult survives re-ranking LIME by contribution (F08).
- The converted sign agreement is not explained by both methods pointing to the predicted class on Adult and German Credit (F02, item 3), and it is at the level of LIME's own sign reproducibility between reruns (0.93–0.97 on common top-10 features, *probe*).
- Git order: plan before analysis code before results; post hoc entries dated after the results.

## Could not verify

- Full texts of Roy et al., Garreau and von Luxburg, Bhatt et al. (abstract/secondary level only).
- KernelSHAP rerun variability (not run: cost).
- LIME self-agreement beyond 3 models × 60 instances × seed 42, and for the two smaller datasets (model binaries not tracked).
- Whether the plan commit was public before the analysis ran (it is on `origin` now).
- Zenodo release/archive macros in the full version (not checked).

## Reference audit (reference-audit skill)

| Check | Result |
|---|---|
| Entries in `references.bib` | 25 |
| Cited keys without entry (orphans) | 0 |
| Entries never cited | 0 in the full build; `herrera2026framework` is cited only inside `\iffull`, so the blind list has 24 (rendered list checked: 24 items, no `??`) |
| Duplicates (DOI, title, near-identical keys) | 0 |
| Entries with DOI | 17; with URL only 5 (Krishna, Neely, Garreau, Alvarez-Melis, Doshi-Velez); neither: Lundberg and Lee 2017, Efron and Tibshirani 1993 |

| Key | Problem | Proposed fix |
|---|---|---|
| `krishna2024disagreement` | Published in TMLR but linked to the arXiv record; no volume/URL of the published version | Link the OpenReview/TMLR page |
| `lundberg2017unified` | No URL or DOI; the journal asks for URLs where available | Add the proceedings URL |
| `efron1993introduction` | Not checked against a record (stated in the .bib header); no DOI | Add DOI 10.1201/9780429246593 after checking it |
| `han2022which` | DOI 10.52202/068431-0380 is the Curran reprint DOI; not resolved by me | Confirm it resolves to this paper, or use the proceedings URL |
| `wolberg1993breast` | Author list "Street, Nick and Street, W." looks like the same person twice; UCI lists Wolberg, Mangasarian, Street, Street | Check the UCI citation; year 1993 vs UCI's 1995 donation date |
| `roy2022why`, `garreau2020explaining`, `alvarezmelis2018robustness`, `bhatt2020evaluating` | Citation–claim fit, see F11 | Reword the citing sentences |
| `herrera2026framework` | Journal field carries the issue ("…(RIMI), No.~3"), a workaround for `cys.bst`; full version only | Acceptable; check the rendered entry in `paper_e_full.pdf` |

Metadata was not re-queried against Crossref in this review (the .bib header records a check on 2026-10-03/04); rows above are from reading the entries and the rendered list.

## Dimension rationale

- **D1 = 3.** Numbers are sound; three interpretations (F01, F02, F08) say more than the evidence.
- **D2 = 3.5.** Descriptive questions without stated refutation criteria; the "direct test" could hardly have failed (F02).
- **D3 = 3.** One fitted model per family on Adult (F04); "not in the direction" drops its conditioning (F02).
- **D4 = 4.5.** Internally consistent; one partial statement (F12).
- **D5' = 3.5.** Post hoc status well disclosed for the main result; gaps in F05, F09, F10; training overlap understated (F03).
- **D6 = 2.5.** No reproducibility ceiling (F01), confounded contrast (F03), intervals that are ranges (F04), rank measure read on the wrong scale (F06).

## Readiness assessment

Not ready to submit. F01–F04 can each be raised by a competent reviewer from the manuscript alone or with one small experiment. F02 and F04 are fixable in prose plus one table column. F01 needs a small new run (LIME and KernelSHAP reruns). F03 needs a re-cut of existing data. None requires new cohorts.

## Questions for the author

1. Why were the Adult one-hot columns not declared as categorical to LIME, and was sampling around the training mean intended?
2. Are the SVM SHAP runs truncated by time-outs? If so, in what order were instances processed?
3. Is Paper B+C under review with the same runs at the time of submission?
4. Was the plan commit pushed before 12:27 on 2026-10-03?
5. Would you accept reporting the majority-sign baseline next to the converted agreement, given that it equals or exceeds it?
