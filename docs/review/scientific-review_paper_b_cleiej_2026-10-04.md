# Scientific review: Paper B (CLEI Electronic Journal draft)

**Date**: 2026-10-04 | **Role**: Scientific Editor | **Requested by**: the author

**Manuscript**: `docs/reports/paper_b/paper_b_cleiej.tex`, "LIME versus SHAP under Matched
Conditions: A Paired Comparison on Tabular Models", 13 pages.

**Verdict**: submit after the author has read the corrected text. One major defect was found
and corrected in this session: the draft said the earlier article left the SHAP-LIME contrast
unresolved, and the published article contains a paired SHAP-LIME test. With that corrected,
the paper's own contribution is narrower than the title suggests and rests on the two
conditional results.

**Independence**: this review is not independent. The same session wrote the draft. A review
by a separate session or person is still advisable.

**Compared against**: the published RIMI article (PDF downloaded from the journal on
2026-10-04, 15 pages) and its source `docs/reports/paper_a/paper_a_prototype_jmlr.tex`;
`docs/reports/paper_d/paper_d.tex`; `docs/reports/paper_e/paper_e.tex`.

## 1. Novelty against Paper A (published, RIMI): HIGH risk, now disclosed

### F01 [major, fixed] - the paired SHAP-LIME test is already published for a subset

- **Evidence**: the published article has a research question "RQ2 (targeted pairwise
  contrast): on matched cells, does SHAP differ from LIME on quality-cost trade-offs?" and a
  section "Targeted Pairwise Comparison (SHAP vs LIME on Shared Families)" with a table of
  paired Wilcoxon tests on **45 matched configurations** (logistic regression, random forest,
  XGBoost): per-method means and p-values for the five metrics, all significant, SHAP higher
  on fidelity, stability and faithfulness gap, LIME cheaper and sparser. Its methods section
  announces a "75-cell sensitivity set" and reports no result for it. The published table has
  no effect sizes and no confidence intervals.
- **What the draft said**: "left the contrast between SHAP and LIME unresolved"; "effect sizes
  that an omnibus test cannot supply"; "The paired design turns the omnibus result, which
  could not separate the two methods on fidelity, into a difference". A referee who opens
  reference [10] would find the paired test and read these sentences as concealment.
- **Origin**: the wording came from the 32-page edition. The registry check and the literal
  scan did not catch it because no number is shared: the 45-cell values differ from the
  75-cell values. The earlier assessment of 2026-10-04 called the benchmark "incremental" and
  did not identify this either.
- **Fix applied**: the introduction, contribution 1, Section 3.1, Section 4.1 (renamed
  "Context: Earlier Results on This Cohort"), Section 5.1 and the provenance paragraph now
  state that the earlier article reports the paired test on a 45-cell subset, that the present
  analysis extends it to the 75 cells of five model families and adds intervals and effect
  sizes, and that the two are not independent. The abstract says "extends an earlier paired
  test".

### What is new in Paper B, after F01

| Result | In the published article? |
|---|---|
| Paired SHAP-LIME test, direction and significance | **Yes**, on 45 of the 75 cells |
| The same test on 75 cells, with SVM and MLP | No (announced, not reported) |
| Confidence intervals and effect sizes of the paired differences | No |
| Cost by model group; SHAP faster for XGBoost, slower for random forest | No |
| Cost percentiles, heavy tail of KernelSHAP | No |
| LIME fidelity and stability on Breast Cancer and German Credit | No (the article says a companion work has it) |
| LIME kernel-width probe | No |
| SHAP-Anchors gaps and Anchors levels on the two datasets | No (the article reports SHAP levels only) |
| Masking-scheme sensitivity | No |

The first contribution is an extension. The paper's case for publication is the remaining
rows, above all the two conditional results.

### F02 [suggestion, author decision] - the title promises the part that is least new

"A Paired Comparison" names what the earlier article partly did. A title that names the
conditional findings would describe the contribution better, for example "When Does SHAP
Outperform LIME? Model- and Configuration-Dependent Results on Tabular Benchmarks". Not
changed.

## 2. Novelty against Paper D (under review): LOW risk

Paper D compares, within each explainer, the explanations of correctly classified and
misclassified instances. It makes no SHAP-against-LIME contrast and reports no paired
difference, cost result or kernel-width result. It notes that LIME's stability on Adult is
near zero under the fixed settings, as a limitation. No shared result; the registry
exclusivity check passes. Paper B's provenance paragraph mentions it.

## 3. Novelty against Paper E (under review): LOW to MODERATE risk

Paper E measures whether SHAP and LIME select the same features for the same instance. Its
endpoints (top-k overlap, sign agreement, self-agreement) do not appear in Paper B, and
Paper B's endpoints are used in E only as covariates. Two points of contact:

- Both papers say that LIME's output on Adult depends on the kernel width (E: a rerun at the
  default width changes the selected features; B: a wider kernel raises stability). The
  measurements differ, the message is close. Each paper should cite the other once one is
  published.
- Paper E's submitted text names the 32-page paper as a companion. If E is revised, the
  statement must name Paper B.

No shared result; the exclusivity check passes.

**Overall**: four manuscripts now draw on the same executions (A, B, D, E). Each asks a
different question, and Paper B says so. An editor may still see a series of thin papers.
The provenance paragraph and the note to the editor are the mitigation; they must stay.

## 4. Other findings

### F03 [minor, fixed] - the lead finding on kernel width rests on one model and one seed

Table 6 is a four-row probe (random forest, seed 42, N=100). The abstract said LIME's
stability "rises with the kernel width" without scope. Now: "in a single-model probe"; and
Section 4.6 states what the probe does and does not show.

### F04 [minor, fixed] - an untested mechanism was stated as a fact

"The cost of TreeExplainer grows with the number and depth of the trees" was given as the
reason for the XGBoost / random-forest reversal. The paper does not report the size of the
ensembles, and the repository's records for the random forest disagree (one metadata file
says 50 trees of depth 15, another 100 trees). The sentence is now a candidate explanation,
not tested.

### F05 [minor, fixed] - hypothesis H2 had the wrong direction

$P$ is the active-feature ratio, lower is sparser, so "LIME is sparser" is
$P_{LIME} < P_{SHAP}$. The draft, like the 32-page edition, had $>$.

### F06 [minor, fixed] - unsupported opening claim in the abstract

"guidance ... rests mostly on unpaired comparisons" had no support. Now "controlled paired
comparisons of the two remain scarce", the claim the introduction makes.

### F07 [minor, open] - the cross-dataset SHAP-LIME gaps have no table

The gaps (+0.23, +0.24, +0.07, +0.07) are in the text only, because the SHAP levels belong
to the earlier article. Table 4 and Figure 3 show SHAP against Anchors, which is peripheral
to a SHAP-LIME paper, and Figure 3 repeats the four values of Table 4. Option: drop Figure 3
and add a SHAP-LIME gap column to Table 5. It needs four registered values; not done.

### F08 [minor, open] - stability under Gaussian noise on one-hot features

The stability metric adds Gaussian noise to every transformed feature, including the one-hot
columns, which then take non-binary values. This may contribute to LIME's near-zero stability
on Adult and is consistent with the high values on the two datasets with few or no
categorical features. The paper names the encoding as a candidate cause; it could say this
more directly. No experiment separates the two.

### F09 [note] - disclosure of AI assistance

The author removed the AI-use statement from the acknowledgments. The journal's pages state
no policy on it. The author's decision.

### F10 [note] - what was checked and holds

- Every number is registered and re-derives (`verify_claims.py`); the cost-by-model table was
  recomputed from `paired_cells_shap_lime_all_models.csv`.
- No literal overlap with the published article (`scan_shared_literals.py --strict`, which
  now reads Paper B).
- Abstract 199 words; 13 pages; 38 references in citation order, 33 with a DOI or URL.

## 5. Before submission

1. Author reads the corrected PDF, in particular the introduction and Section 4.1.
2. Author decides F02 (title) and F07 (figure and table).
3. The note to the editor must mention the 45-cell test of the earlier article
   (`docs/reports/paper_b/CLEIEJ_SUBMISSION.md`, section 3, updated).
4. A review by someone who did not write the draft.

## 6. Follow-up (2026-10-04, same day): open findings applied at the author's request

| Finding | Action |
|---|---|
| F02 title | New title: "When Does SHAP Outperform LIME? Model- and Configuration-Dependent Results from a Paired Tabular Benchmark" |
| F07 cross-dataset presentation | Figure 3 (SHAP against Anchors, a repeat of Table 4) removed. Table 5 has a new column with the paired SHAP-LIME fidelity gap (+0.07, +0.07, +0.23, +0.24), values already registered |
| F08 stability protocol | Section 4.6 now says that the Gaussian noise is added to every transformed feature, including the one-hot columns (checked in `src/metrics/stability.py`), that Breast Cancer has no categorical feature, and that no experiment separates the encoding from the perturbation scheme |
| Step 4, independent review | Still open; it cannot be done by this session |

A double-blind build was added at the author's request (`paper_b_cleiej_blind.tex`, 12 pages).
The full build has 13 pages and 2 figures.
