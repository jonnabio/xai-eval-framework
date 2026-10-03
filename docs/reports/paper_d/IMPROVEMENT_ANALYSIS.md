# Paper D — improvement analysis of the first render (2026-10-03)

## Iteration 1 status (2026-10-03, second render)

**Result:** 12 Word pages (Word's own count); abstract 230 words, resumen 238; all verifiers green.

| Item | Status | What changed |
|---|---|---|
| S1 training overlap | ✅ done | Post-hoc (plan §9, deviation 3). 58% of instances were training data; fewer among errors. **Stability deficits hold** on held-out instances (all four explainers) and on seed 42 alone (SHAP, LIME, DiCE). **The raw faithfulness-gap deficits of SHAP and DiCE do not hold.** The margin-adjusted SHAP faithfulness deficit holds; those of LIME and Anchors do not. Abstract and conclusions narrowed to SHAP; new §3.4; held-out column in Table 3 |
| S2 random-forest model | ⏳ disclosed | Recovery attempt still open (P3). RCA entry for Papers A/B+C still to write |
| S3 SHAP fidelity | ✅ | Explained in §3.1 and the Fig. 1 caption |
| S4 Anchors stability | ✅ | Number of runs with a negative difference reported (49/57) |
| S5 RQ3 mechanism | ✅ done | Post-hoc (deviation 4): the gap follows the predicted class (TP−TN SHAP +0.597, all runs); errors fall between. Now stated as a finding, with the masking explanation kept as plausible |
| S6 RQ4 interaction | ✅ (text) | Described as visible in every margin bin; no interaction model added |
| S7 threshold scale | ✅ | Limitation sentence |
| S8 German Credit | ✅ | Reason checked; tree-only cannot explain it; stated that none is known |
| S9 related work | ❌ **author** | Needs 2–4 references on explanation quality vs model error/uncertainty, chosen and verified by the author |
| Length 14 → 12 | ✅ | Table 1 → text; sparsity rows and RQ4 fidelity rows removed; prose condensed |
| Fig. 2 small values / Fig. 3 legend and labels | ✅ | |
| Dataset DOIs | ✅ | In `note` fields |
| `scan_shared_literals` for Paper D | ✅ | `--paper-d` mode: 0 unexplained, 34 explained by registered provenance, 9 constants |
| Author items (ORCID, profession, Spanish read, "brecha de borrado", NEW refs) | ❌ **author** | |
| Open the .docx in Word once and re-save | ❌ **author** | |

The original analysis follows.

**Subject:** `submission/paper_d_blind.{pdf,docx}`, rendered from `paper_d_template.tex`. The
analysis follows `ANALYSIS_PLAN.md`, with deviations 1–2 in §9 of the plan.

**Current state:**
- **Length:** 14 pages in Word (counted by Word itself) and 13 in the PDF.
- **Size:** 4,505 words; 4 tables, 3 figures, 5 numbered equations.
- **Claims:** every number re-derives from `outputs/analysis/paper_d/`, with 200 Paper D claims registered.
- **Checks:** all verifiers green.

Priorities:
- **P1:** must fix before submission.
- **P2:** should fix; it strengthens the paper.
- **P3:** optional.

## 1. Compliance with the author guide (*Tecnología en Marcha*)

| Requirement | Status | Note |
|---|---|---|
| Word file, letter size, one column | ✅ | 612 × 792 pt, checked in Word |
| Times 12 pt, 1.5 line spacing | ✅ body / ⚠️ tables | Table cells are set at 10 pt, single-spaced, so the wide result tables fit the page. If the editor objects, the tables can return to 12 pt, at a cost of about 1.5 pages |
| 5–15 pages | ✅ 14 | Within the limit, but over the author's 12-page target (see §3) |
| Title, abstract and keywords in English and Spanish | ✅ | Abstract 224 words, resumen 233 (limit 250) |
| Structure: introduction, materials and methods, results, conclusions, references, acknowledgments | ✅ | A Discussion section is added; the guide allows it ("conclusions and/or recommendations") |
| Equations in Word's equation editor | ✅ | Native Word equations (OMML) produced by pandoc. Numbers in text and tables are plain text, so only real formulas are equation objects |
| Images in the document and as separate files at 300 ppi | ✅ | `submission/Figure1-3.tiff`, 300 ppi, LZW |
| IEEE references | ✅ | IEEEtran (PDF) and the IEEE CSL style (Word) |
| Author data: both surnames, profession, email, workplace, country, ORCID | ❌ **P1** | Only in the full version. `[AUTHOR: profession]` and `[AUTHOR: ORCID]` are still placeholders |
| Double-blind | ✅ | The blind build carries no names or URLs. The self-citation [10] is written in the third person. The Word file's metadata should be checked before sending (File → Info → Inspect Document) |
| AI-use disclosure | ✅ | In the Acknowledgments; the author keeps the questions, plan, design and interpretation |

## 2. Scientific issues

**S1 (P1): overlap between the evaluation sample and the training data.**
- **Problem:**
  - The models were trained on the seed-42 partition, but each run drew its instances from the partition of its own seed.
  - For seeds 123, 456, 789 and 999, some explained instances were therefore training instances.
  - Errors on training data are rarer and may be atypical.
  - The paper states this as a limitation; a reviewer will ask what effect it has.
- **Action:** a sensitivity analysis. Map each instance to its row in the original data, flag training-set membership, and repeat RQ1 with:
  - (a) seed-42 runs only;
  - (b) non-training instances only.
- **Labelling:** report it as a post-hoc sensitivity analysis and log it in plan §9. About half a day of work; the data allow it.

**S2 (P1, disclose; P3, recover): random-forest runs that cannot be reproduced.**
- **Problem:**
  - The stored `rf.joblib` (hash `5ebab4a9`, unchanged since January) reproduces only 75–82% of the predictions recorded by the January–February RF runs.
  - Neither the earlier preprocessor nor a freshly fitted one restores them.
  - RQ4 therefore uses 9 of 60 RF runs. This is disclosed as deviation 1.
- **Optional action (P3):** check whether a worker host kept another RF model (worker manifests, `experiments/exp1_adult/models/rf/`). Recovering it would restore RQ4 for RF.
- **Consequence for the benchmark:** this is also a provenance finding that affects Papers A and B+C. Their RF results were computed with a model that is no longer in the repository. It should be recorded in the project's RCA log.

**S3 (P2): SHAP fidelity.**
- **Problem:** the mean's 95% CI excludes zero, but the Holm-corrected Wilcoxon test is not significant (p = 0.057). The paper reports both, but a reader may see a contradiction.
- **Action:** add one sentence. The Wilcoxon test is on the median (+0.007), which is near zero; the mean is pulled up by a few runs, as Fig. 2 shows (SVM and RF).

**S4 (P2): Anchors stability.**
- **Problem:** the median Δ is 0.000, yet the result is significant (p < 0.001). Most runs have Anchors stability near zero for both groups, and the signal comes from a minority.
- **Action:** say so, or report the share of runs with Δ < 0 (49 of 57).

**S5 (P2): the RQ3 mechanism is a hypothesis.**
- **Problem:** the explanation for the faithfulness-gap asymmetry (masking to the mean pushes towards the negative class) is plausible but untested.
- **Action:** test it with data already in hand. Compare instances with the same predicted class but different correctness: TP against FP, and TN against FN. If the gap tracks the predicted class rather than correctness, the mechanism is confirmed.
- **Labelling:** exploratory, logged in plan §9. This would turn a speculation into a finding.

**S6 (P2): RQ4 interaction.**
- **Problem:** Fig. 3 suggests that for SHAP the gap between correct and misclassified instances *widens* with the margin. That is an interaction, which the additive model does not capture.
- **Action:** add a misclassified × margin term as an exploratory check, or describe the figure without over-claiming.

**S7 (P2): scale of the practical-relevance threshold.**
- **Problem:** |median Δ| ≥ 0.05 is absolute. LIME stability lives on a 0–0.02 scale on Adult, so the threshold can never be met for LIME.
- **Action:** say so in the limitations. Do not change the pre-registered rule.

**S8 (P2): external check.**
- **Problem:** SHAP stability is reversed on German Credit (higher on errors in 4 of 6 runs).
- **Action:** the discussion should offer a reason or state that none is known. Candidates are the different feature space (fewer one-hot features) and TreeExplainer only (RF and XGB). Avoid speculation not backed by the data.

**S9 (P2): related work.**
- **Problem:** the introduction cites explainers and metrics but no prior work on explanation quality *as a function of model error or uncertainty*. Reviewers in XAI will expect two to four such references.
- **Action:** the author selects and verifies them. AI-suggested references must not be added unchecked.
- **Unverified references:** the three new standard references (Kruskal–Wallis, Cameron–Miller, Platt) are marked `NEW` in `references.bib` and need the author's check.

## 3. Length: from 14 to 12 Word pages

| Cut | Saving (Word, approx.) | Cost |
|---|---|---|
| Move the four sparsity rows of Table 2 into one sentence (sparsity is secondary) | 0.3 p | none |
| Table 4: keep only "β with margin" plus a "% change" column; mention the raw β in the text | 0.4 p | little |
| Merge Table 1 into one sentence of §2.1 (four rows of counts) | 0.4 p | little |
| Tighten the Discussion (the first and third paragraphs repeat the Results) | 0.4 p | none |
| Shorten the Introduction's second paragraph | 0.2 p | none |
| Figure 2: two panels (stability, faithfulness gap); fidelity is described in the text | 0.3 p | some |

The first four cuts reach about 12 pages. S1 and S5 add about 0.3 pages if reported as one paragraph each.

## 4. Presentation

- **Fig. 2 (P2):** cells for LIME and Anchors stability print "−0.00". Show three decimals for small values, or note the scale in the caption.
- **Fig. 3 (P3):** the "Anchors" label touches the curve; the legend overlaps SHAP's low-margin points.
- **Fig. 1 (P3):** SHAP fidelity is drawn as not significant although its CI excludes zero. Explain this in the caption (see S3).
- **References (P2):** IEEEtran does not print DOIs for the `@misc` dataset entries [17], [20]. Add them in a `note` field.
- **Spanish (P1, author):**
  - **Terminology:** the resumen now says "brecha de borrado" for *faithfulness gap*, to avoid a clash with "fidelidad" (*fidelity*). Confirm the term.
  - **Native read:** the author should read the whole Spanish text.
- **Word file (P2):** open it once in Word, check that the equations are editable and that the table borders look right, then save. Word normalises the file.

## 5. Process

- **P1:** extend `scan_shared_literals.py` to Paper D, as plan §7 requires before submission.
  - Exclusivity and coverage are already enforced.
  - 23 chance numeric coincidences with Paper B+C values, plus the method constant 0.05, are recorded as exceptions scoped to `paper_d.tex`, each naming its Paper D source.
  - `verify_claims.py` gained file-scoped exceptions for this, so they do not weaken the CIFIE chapter's guard.
- **P2:** the analysis environment.
  - The project `.venv` cannot load SciPy, because Windows Application Control blocks its DLL.
  - The analysis ran in a scratch environment: Python 3.13, SciPy, scikit-learn 1.7.1 and XGBoost.
  - Record this in `README.md`, or fix the `.venv`.
- **P2:** register `paper_d_template.tex` → `paper_d.tex` in the build documentation: the `.tex` file is generated and must not be edited.

## Recommended order (to the 13 October submission)

| Date | Work |
|---|---|
| 4 Oct | S1 sensitivity; S5 mechanism check (log both in plan §9) |
| 5 Oct | S3, S4, S6–S8 text; length cuts in §3 |
| 6–7 Oct | Related work (S9; the author verifies the references); figure fixes |
| 8 Oct | Re-render; Word check (12 pages); `scan_shared_literals` for Paper D |
| 9–11 Oct | Scientific-rigor review |
| 12 Oct | Author items: ORCID, profession, Spanish read, reference approval |
| 13 Oct | Submit |
