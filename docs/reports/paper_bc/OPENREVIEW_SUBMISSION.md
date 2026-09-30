# OpenReview submission sheet — Paper B+C to TMLR

Prepared 2026-09-14 from the paper lane at `407ae32e6`; regenerated
2026-09-27 from the paper lane at `7df496a00`, and again 2026-09-30 from the
paper lane at `e57f49e04` after the pre-submission review fixes, as
described in the re-verification records below. Everything below is
copied from the manuscript's sources, not retyped: the abstract is the
generated fragment `pub/fragments/paper_bc_abstract_en.tex` with text-mode
LaTeX converted and inline math kept for OpenReview's MathJax. **If
`pub/claims.toml` changes before submission, regenerate this sheet.**

Submission venue: <https://openreview.net/group?id=TMLR>

> **Re-verified 2026-09-30 against the final manuscript** (record below),
> after the pre-submission review (F01–F19, except F10, closed by author
> decision), the abstract wording fix for the Adult dataset and the equation
> revision. Author confirmed 2026-09-28: the detailed revision is finished
> and the paper is not under review elsewhere. Any further edit to the
> manuscript, its supplementary or `pub/claims.toml` invalidates this
> record: run "After any revision" again.

## After any revision — regenerate before submitting

Any edit to `paper_bc_tmlr.tex`, `paper_bc_tmlr_supplementary.tex` or
`pub/claims.toml` invalidates the built PDFs, the artifact bundle and the
abstract reproduced in this sheet. Work in the paper lane, with `data/adult.csv`
present (it is gitignored, so copy it in from the main worktree if missing).

1. **Register first, edit second.** Any new or changed number goes into
   `pub/claim_registry.toml` before it reaches the manuscript (RCA-001
   invariant 1). A rescoped or retracted claim also triggers
   `docs/review/top-level-statement-sweep.md`.
2. **Rebuild both PDFs.**
   `./tools/tectonic-portable/tectonic.exe docs/reports/paper_bc/paper_bc_tmlr.tex`
   and the same for `paper_bc_tmlr_supplementary.tex`. Confirm zero undefined
   references and citations.
3. **Read page 1 of the built PDF**, not the source. On 2026-09-14 the abstract
   printed "SHAP's extttTreeExplainer" past a green verifier, a green readiness
   checklist and an anonymity pass (RCA-003).
4. **Re-run all three verifiers:** `verify_claims.py`, `verify_sync.py`,
   `verify_exp4_reconstruction.py` (needs Python 3.13).
5. **Re-scan for identity.** Both PDFs, text and metadata, and every file in the
   bundle. The only permitted hits are the third-person citation of the RIMI
   paper in the main PDF.
6. **Re-run the shared-result query** from `EIC_ENQUIRY_prior_publication.md`.
   It must return nothing: a result shared with the published Paper A is a TMLR
   policy conflict, not a style issue. **Then run
   `python scripts/pubs/scan_shared_literals.py --strict`**, which compares the
   printed numbers of both papers without using the registry, and must exit 0.
   The query alone missed the SHAP/LIME mean costs on 2026-09-27, because Paper
   A's site was never registered (review F02). A new match is either removed or
   triaged into `KNOWN_COINCIDENCES` with its reason. Also check the figures by
   eye: a plotted level is a result even without a data label.
7. **Rebuild the bundle** — `python scripts/pubs/build_artifact_bundle.py` —
   and confirm it contains `supplementary_tables.pdf`.
8. **Regenerate this sheet's abstract** from
   `pub/fragments/paper_bc_abstract_en.tex`; never retype it. Update the word
   and character counts, the page counts, and the commit stamp at the top.
9. **Report the result to the author in writing** before anything is uploaded.
   If the revision changed the title, abstract or keywords, the form fields
   below change with it.

### Re-verification record — 2026-09-30 (paper lane `e57f49e04`)

Since 2026-09-27: review fixes F01–F19 (except F10), the author name form,
"UCI Adult census-income dataset" in the abstract, and the equation revision
(numbered equations, every term defined, Bhatt et al. 2020 and Samek et al.
2017 added). Re-run the same day after §8 was corrected: the anonymous build
now lists bundle paths (every listed path checked present in the bundle)
instead of repository paths, and no longer says the corpus full texts are
released alongside while saying they are not shipped. The de-anonymised build
keeps the repository paths and the archived-release DOI; built once, read,
discarded.

| Step | Result |
| ---- | ------ |
| 1. Register first | Registry 321 claims / 485 sites / 46 retired-value guards; 21 files fully registered |
| 2. Rebuild both PDFs | Tectonic 0.17.0: 27 + 5 pages, 0 undefined references or citations |
| 3. Page 1 of the built PDF | Read from the PDF: abstract and Eq. (1) render, no garbled macros |
| 4. Verifiers | `verify_claims`, `verify_sync`, `verify_exp4_reconstruction` (18 hash pins) green |
| 5. Identity scan | Main PDF: only the third-person RIMI citation (plus F. Herrera, an unrelated co-author of two cited surveys). Supplementary: none. Metadata clean. Bundle: 0 of 9,384 files |
| 6. Shared results | Registry query returns nothing; `scan_shared_literals.py --strict` exits 0 (0 unexplained, 53 known coincidences) |
| 7. Bundle | Rebuilt; contains `supplementary_tables.pdf`; 16.1 MB |
| 8. This sheet | Abstract regenerated from the fragment (306 words, 2,173 characters); page counts, stamp and this record updated |

### Re-verification record — 2026-09-27 (paper lane `7df496a00`)

The revision since 2026-09-14 changed the EXP3 sentence of the abstract
(`pub/claims.toml`), the Table S1–S6 heading dashes, and §EXP4 with
Supplementary S1 (ADR-0017: EXP4 replication cohort and corrected sample).

| Step | Result |
| ---- | ------ |
| 1. Register first | 39 new EXP4 claims plus paper sites registered before use; registry 257 claims / 389 sites |
| 2. Rebuild both PDFs | Tectonic 0.17.0: 26 + 5 pages, 0 undefined references or citations, no unrepresentable characters |
| 3. Page 1 of the built PDF | Read from the PDF: new EXP3 sentence renders, no garbled macros |
| 4. Verifiers | `verify_claims`, `verify_sync`, `verify_exp4_reconstruction` (hash pins) and both corpus checks green |
| 5. Identity scan | Both PDFs: only the third-person RIMI citation; PDF metadata clean. Bundle: 0 of 9,384 files contain an identity string |
| 6. Shared-result query | Returns nothing: no result shared with Paper A |
| 7. Bundle | Rebuilt; contains `supplementary_tables.pdf`; 16.1 MB |
| 8. This sheet | Abstract regenerated from the fragment (264 words, 1,955 characters); bundle size, stamp and this record updated. Page count unchanged (26; references start on page 23) |

## Status of the pre-submission confirmations

| Item | Status |
| ---- | ------ |
| OpenReview profile: affiliation, publication history (incl. RIMI) | done by author, 2026-09-14 |
| Conflict of interest: Dr Miguel Herrero-Uceda (thesis tutor; RIMI co-author) | done by author, 2026-09-14 |
| RIMI DOI `10.69850/rimi.vi3.307` | confirmed by author; resolves in Crossref to the RIMI article, issue 3, published 2026-09-01, ISSN 2992-7978 |
| RIMI journal name | Crossref registers "Revista de investigación multidisciplinaria, Iberoamericana", correctly spelled; the bibliography's title-cased form is right and needs no change |
| Zenodo snapshot `10.5281/zenodo.21538180` is this paper's | confirmed by author, 2026-09-14 (camera-ready only; not in the anonymous PDF) |
| Not under review at any other venue | confirmed by author, 2026-09-28 (tick the form checkbox when filing) |

## Form fields

**Title** (one line; the PDF breaks it over three):

```
From Fidelity to Semantics: A Taxonomy of XAI Evaluation Metrics and Paired Empirical Comparison of LIME versus SHAP
```

**Abstract** (306 words, 2,173 characters):

```
Evaluation of post-hoc explanations in machine learning remains fragmented across incompatible metric families, yielding method comparisons that are sensitive to which endpoints are chosen. We address this through two complementary contributions. First, drawing on a 44-paper structured scoping corpus assembled through a five-database search with a reported screening record, we build a four-axis taxonomy—by evaluation target, evidence source, quality property, and task context—that maps the measurement landscape and exposes three recurring gaps: proxy metrics dominate despite not capturing semantics; human-grounded constructs remain underspecified; and semantic evaluation is growing faster than its empirical validation base. Second, we fill the proxy-layer gap with a paired empirical benchmark comparing LIME and SHAP across 75 matched cells spanning five model families, five seeds, and three sampling sizes on the UCI Adult census-income dataset. Within this protocol, results are consistent and large in magnitude: SHAP leads on every fidelity- and stability-oriented endpoint (stability $d_z = 3.00$, fidelity $d_z = 4.82$, faithfulness gap $d_z = 2.63$), while LIME is sparser and faster for non-tree model families (median 53.3 ms vs. 694.6 ms for SHAP). Among tree ensembles the latency ordering depends on the model: SHAP's TreeExplainer was faster than LIME in every XGBoost cell but slower in every random-forest cell. A cross-dataset extension on two further tabular datasets preserves the fidelity ordering—SHAP exceeds both Anchors and LIME in every dataset–model stratum—and shows that LIME's near-zero stability on the Adult data is not intrinsic to the method: it rises with the kernel width and is high on both lower-dimensional datasets. Together, the taxonomy and the benchmark motivate a model-architecture-conditioned deployment pattern for tabular classification: SHAP is preferred at both fidelity and latency for XGBoost, LIME retains a latency advantage for black-box architectures lacking a model-aware explainer, and for other tree ensembles latency should be measured before choosing. All experimental artifacts are publicly available.
```

After pasting, check the form preview: the three $d_z$ values should render
as math. If they show literal dollar signs, replace each `$d_z = X$` with
`d_z = X`.

**Keywords:** explainable AI, evaluation metrics, taxonomy, LIME, SHAP

**Authors:** Jonathan Herrera-Vásquez, sole author, via the OpenReview profile.
TMLR admits no change to the author list after submission.

**PDF:** `docs/reports/paper_bc/paper_bc_tmlr.pdf`. 27 pages, anonymous.

**Supplementary material:** `docs/reports/paper_bc/paper_bc_artifacts.zip`.
16.1 MB, 9,384 files, including `supplementary_tables.pdf` (Tables S1–S6) and
the EXP4 replication's raw judge responses. TMLR allows up to 100 MB of
supplementary material, as PDF or ZIP.
Gitignored, so rebuild it right before uploading:
`python scripts/pubs/build_artifact_bundle.py`.

**Submission length, if asked:** long. The main text runs to page 23 and the
references start on page 24.

**Human subjects / IRB:** no human-subjects research. The study uses the
public, de-identified UCI Adult, Breast Cancer Wisconsin and German Credit
datasets. The review corpus is published literature. EXP4 uses LLMs as
judges, with no human participants. The manuscript's validity table states
"No participant study; EXP4 is an LLM reliability probe only".

**Funding:** none; self-funded. Matches the camera-ready acknowledgment.

**Competing interests:** none. Matches the camera-ready acknowledgment.

## Suggested Action Editors

Taken from the TMLR Action Editor list (<https://jmlr.org/tmlr/editorial-board.html>,
read 2026-09-14), using the research areas each editor lists. None of them is
cited in the manuscript, and none shares an affiliation with the author.

| Priority | Action Editor | Affiliation | Listed areas (verbatim) | Why |
| -------- | ------------- | ----------- | ----------------------- | --- |
| 1 | Dennis Wei | IBM | "Explainability attribution, fairness, trustworthy, interpretability" | Closest match: feature attribution plus its evaluation, which is both halves of the paper |
| 2 | Satoshi Hara | The University of Electro-Communications | "Interpretability, anomaly detection, feature selection" | Interpretability of tabular models and feature importance |
| 3 | Amir-Hossein Karimi | University of Waterloo | "Causal inference, interpretable machine learning, explainable ai" | XAI methods; relevant to the DiCE/recourse material |
| 4 | Mengnan Du | The Chinese University of Hong Kong, Shenzhen | "Trustworthy ai, explainability, fairness" | Explainability and trustworthy AI |
| 5 | Olawale Elijah Salaudeen | Microsoft | "Causality, transfer learning, benchmarking, distribution shifts, machine learning, deep learning, validity" | The measurement-validity and benchmarking angle, not XAI directly; an alternate if the form allows more |

Other plausible alternates: Lijie Hu (MBZUAI, "Interpretability and
explainability…") and Di Wang (KAUST, "Interpretability, fairness, learning
theory, differential privacy").

## Immediately after submitting

1. Note the submission number and forum URL.
2. Email the editor note (`EIC_ENQUIRY_prior_publication.md`) to
   **tmlr-editors@jmlr.org**, with the submission number in the subject line.
   Send it by email rather than as a forum comment: it is signed and names the
   earlier article's authors, and a forum comment visible to reviewers would
   break anonymity.
3. Record the forum ID in `docs/context/ACTIVE_CONTEXT.md` and close Next
   Steps item 00.

## Camera-ready only (not now)

- Set `\openreview`, `\month` and `\year`, and switch to `\usepackage[accepted]{tmlr}`.
- The acknowledgment still reads "This draft was prepared from repository
  artifacts dated May 2026". That sentence is out of date, but it only appears
  in the de-anonymised build. Revise it before the camera-ready.
