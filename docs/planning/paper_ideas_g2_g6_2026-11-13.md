# Paper ideas G2 to G6 (backlog)

**Status:** Ideas only, recorded 2026-11-13. None is started, and none has a lane.
**Origin:** Session of 2026-11-13. The author asked for candidates for a seventh paper
(Paper G). G1, agreement between faithfulness metrics, was chosen and is being developed
in `docs/reports/paper_g/`. The other five are kept here for later.
**Venue considered:** *Informática y Sistemas* (Universidad Técnica de Manabí, e-ISSN 2550-6730).
English only from Volume 11 (2027), 8 to 16 pages, no fees, double-blind review, APA 7,
.docx template, at most 10% similarity and at most 30% AI-generated text (Compilatio).

## Rules that apply to every idea

- **No reuse of results.** No idea may print a result already reported in Papers A to F.
  Each one needs its own run. The pipeline, loaders and metric code may be reused.
  Known overlap: the masking-sensitivity results (`exp6_masking_sensitivity`) and the
  LIME kernel-width sweep already appear in Paper B, so they are not available.
- **References.** Every reference has its DOI URL and is checked against the source.
  At least 80% date from 2024 or later.
- **Lane.** An idea that starts gets its own lane in `scripts/pubs/lanes.toml` (ADR-0021)
  and its own folder `docs/reports/paper_<x>/`.

## Complexity scale

1 = analysis of existing infrastructure only. 5 = new methods, new attack models or new
hardware, with a high risk of reviewer objections. The scale counts compute, new code,
methodological risk and the risk of overlap with A to F.

## Summary

| ID | Working title | Complexity | Main risk |
|---|---|---|---|
| G2 | How many samples are enough? Compute budget against explanation quality | 2/5 | Overlap with Paper B's configuration results |
| G3 | Same accuracy, different explanation: attribution stability under retraining | 3/5 | Many model fits |
| G4 | Is an explanation equally good for every group? Group-conditional explanation quality | 3/5 | Small subgroups, multiple comparisons |
| G5 | Do benchmark conclusions transfer to newer tabular models? | 4/5 | GPU, size limits of TabPFN |
| G6 | Can an evaluation protocol detect a manipulated explanation? | 5/5 | New attack code; risk to timeline and reviews |

---

## G2. Compute budget against explanation quality

**Question.** How does the quality of a KernelSHAP or LIME explanation change with the number
of samples and the size of the background set? Where does adding samples stop helping?

**Why it matters.** Practitioners pick `nsamples` and the background size by default or by
habit. A measured "elbow" per model family gives direct guidance, and the cost of reaching
it is reportable.

**Design sketch.**
- Tree models, where exact TreeSHAP gives a true reference for SHAP values.
- Sweep: KernelSHAP `nsamples` on a log scale; background size of 10, 50, 100 and 500;
  LIME `num_samples` on a log scale.
- Outcomes: error against exact TreeSHAP (rank correlation, top-k overlap, L1); stability
  across repeats; wall time.
- Analysis: piecewise or saturation fit of quality against log budget per dataset and model,
  with bootstrap intervals for the elbow.

**Data.** New sweeps on the datasets loaded by the Paper F loader (code only).
**Complexity 2/5.** Simple runs. Defining the boundary with Paper B (configuration sensitivity
of LIME) needs care. G2 must frame the question as budget against an exact reference,
not as kernel-width sensitivity.

---

## G3. Attribution stability under retraining

**Question.** When the same model class is retrained with different seeds or bootstrap
samples and reaches the same accuracy, how much do its explanations change?

**Why it matters.** An audit explains *one* fitted model. If equally accurate models give
different top features, an explanation describes the fit, not the task. This is the
"Rashomon" view applied to attributions.

**Design sketch.**
- For each dataset and model class: 20 to 30 retrainings that differ only in seed or
  bootstrap sample, kept if test AUC is within a tolerance of the reference.
- Same instances explained by every retraining, with SHAP and LIME.
- Outcomes: top-k Jaccard, rank correlation and sign agreement between retrainings. These
  are compared with the within-model stability (input perturbation) as a reference ceiling.
- Analysis: variance components (retraining against explainer sampling against instance).

**Complexity 3/5.** The method is standard. The cost is the number of model fits and
explanations; the experiment laptop can run it in shards.

---

## G4. Group-conditional explanation quality

**Question.** Do faithfulness and stability differ across sensitive subgroups (sex, age band,
race where available)? How much attribution goes to protected attributes or their proxies?

**Why it matters.** It links XAI evaluation to fairness auditing. If explanations are less
faithful for a minority group, the explanations used to audit the model are least reliable
exactly where the audit matters.

**Design sketch.**
- Datasets with documented sensitive attributes (Adult, COMPAS, German Credit, Default of
  credit card clients).
- Same explainers and metrics, computed per subgroup. Subgroup-stratified sampling so that
  small groups have enough instances.
- Analysis: paired differences between groups with bootstrap intervals; Holm correction
  over groups and metrics; minimum-detectable-effect stated in advance.

**Complexity 3/5.** Small subgroups and many comparisons. The sensitive-attribute definitions
need justification and ethical care in the text.

---

## G5. Transfer of benchmark conclusions to newer tabular models

**Question.** Do the explainer orders found for logistic regression, random forest, XGBoost
and MLP hold for newer tabular models (for example TabPFN, or recent tabular deep models)?

**Why it matters.** Benchmarks age quickly. A check of external validity across model
families tells readers whether older conclusions still apply.

**Design sketch.**
- Same protocol and metrics, with the new model family added.
- Model-agnostic explainers only (KernelSHAP, LIME), since TreeSHAP does not apply.
- Analysis: agreement of explainer orders between model families.

**Complexity 4/5.** Needs a GPU or long CPU runs. TabPFN has limits on rows and features,
so the dataset set may shrink. Licence and version of the model must be recorded.
Care is needed so the paper does not re-report Paper F's orders.

---

## G6. Detecting manipulated explanations

**Question.** Can the metrics of the evaluation protocol flag a model built to hide a biased
feature from perturbation-based explainers (scaffolding attacks)?

**Why it matters.** It turns the protocol into a defensive tool. Explanations are used in
audits, and an attacker who knows the explainer can fool it.

**Design sketch.**
- Build scaffolded models that behave in a biased way on real data and in an unbiased way
  on perturbed (out-of-distribution) samples.
- Run the protocol's metrics on honest and scaffolded models; measure detection
  (ROC AUC of each metric as a detector).
- Analysis: which metric, if any, separates honest from manipulated models, and at what
  cost.

**Complexity 5/5.** New attack code, an adversarial threat model to defend in the text, and
a high chance of reviewer objections about the realism of the attack. Highest novelty, and
the highest risk.

---

## Recommended order after G1

G3 (strongest result for its cost), then G4, then G2. G5 and G6 only if a GPU or a longer
time frame is available.
