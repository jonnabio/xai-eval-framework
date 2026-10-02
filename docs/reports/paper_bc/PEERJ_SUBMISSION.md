# Paper B+C — PeerJ Computer Science submission sheet

**Status (2026-10-02):** preparing. TMLR desk-rejected submission 12779 without review. Plan:
`docs/planning/paper_bc_peerj_retarget_plan_2026-10-02.md`. Lane: `paper/bc-peerj-cs`, cut
from tag `tmlr-submission-12779`.

**Author decisions (2026-10-02):** D1 Research Article · D2 title spells out "Explainable AI"
· D4 Provenance kept, plus a Notes-to-Staff sentence · D5 AI disclosure in the form and the
Acknowledgments · D6 arXiv preprint approved · D7 gap analysis goes to Discussion.
**D3 (payment): OPEN, blocks filing.** See §9.

Each block below is text to paste into the PeerJ form or port into the manuscript. Items marked
**[AUTHOR]** need information only you have.

---

## 1. Article type and title

- Type: **Research Article**.
- Title (126 characters; limit 250):
  > From Fidelity to Semantics: A Taxonomy of Explainable AI Evaluation Metrics and a Paired
  > Empirical Comparison of LIME and SHAP

## 2. Author Cover Page (page 1 of the manuscript; must match the online form exactly)

```
From Fidelity to Semantics: A Taxonomy of Explainable AI Evaluation Metrics
and a Paired Empirical Comparison of LIME and SHAP

Jonathan Herrera-Vásquez¹

¹ [AUTHOR: department / programme], Universidad Americana de Europa (UNADE),
  Cancún, Quintana Roo, Mexico

Submission admin: Jonathan Herrera-Vásquez, jonnabio@gmail.com
```

Paper A's co-author (M. Herrero-Uceda) is **not** an author of Paper B+C, as in the TMLR filing.
**[AUTHOR]** confirm. PeerJ requires that every person meeting the ICMJE criteria is listed.

## 3. Structured abstract (≤ 500 words / 3,000 characters; bold run-in headings)

Same sentences and numbers as the filed abstract, split under PeerJ's headings. No result is
added, removed or changed. Source of truth stays `pub/claims.toml` (new key, RCA-003 rules).

> **Background.** Evaluation of post-hoc explanations in machine learning remains fragmented
> across incompatible metric families, yielding method comparisons that are sensitive to which
> endpoints are chosen.
>
> **Methods.** Drawing on a 44-paper structured scoping corpus assembled through a five-database
> search with a reported screening record, we build a four-axis taxonomy—by evaluation target,
> evidence source, quality property, and task context—that maps the measurement landscape. We
> then run a paired empirical benchmark comparing LIME and SHAP across 75 matched cells spanning
> five model families, five seeds, and three sampling sizes on the UCI Adult census-income
> dataset, with a cross-dataset extension on two further tabular datasets.
>
> **Results.** The taxonomy exposes three recurring gaps: proxy metrics dominate despite not
> capturing semantics; human-grounded constructs remain underspecified; and semantic evaluation
> is growing faster than its empirical validation base. Within the benchmark protocol, results
> are consistent and large in magnitude: SHAP leads on every fidelity- and stability-oriented
> endpoint (stability d_z = 3.00, fidelity d_z = 4.82, faithfulness gap d_z = 2.63), while LIME is
> sparser and faster for non-tree model families (median 53.3 ms vs. 694.6 ms for SHAP). Among
> tree ensembles the latency ordering depends on the model: SHAP's TreeExplainer was faster than
> LIME in every XGBoost cell but slower in every random-forest cell. The cross-dataset extension
> preserves the fidelity ordering—SHAP exceeds both Anchors and LIME in every dataset–model
> stratum—and shows that LIME's near-zero stability on the Adult data is not intrinsic to the
> method: it rises with the kernel width and is high on both lower-dimensional datasets.
>
> **Conclusions.** Together, the taxonomy and the benchmark motivate a
> model-architecture-conditioned deployment pattern for tabular classification: SHAP is
> preferred at both fidelity and latency for XGBoost, LIME retains a latency advantage for
> black-box architectures lacking a model-aware explainer, and for other tree ensembles latency
> should be measured before choosing. All experimental artifacts are publicly available.

Measured 2026-10-02: 304 words, 2,170 characters (both under the limits). Re-measure on the rendered PDF.

Keywords: explainable AI, evaluation metrics, taxonomy, LIME, SHAP (unchanged).

## 4. Declarations (online form)

- **Funding statement:** "The author received no funding for this work."
- **Competing interests:** "The author declares that there are no competing interests."
- **Author contributions (CRediT/ICMJE):** "Jonathan Herrera-Vásquez conceived and designed
  the experiments, performed the experiments, analyzed the data, performed the computation work,
  prepared figures and/or tables, authored or reviewed drafts of the article, and approved the
  final draft."
- **Data availability:** "The code, experiment configurations, raw run outputs, statistical
  exports, review-corpus coding sheet and EXP4 judge outputs are available at Zenodo:
  [AUTHOR: version DOI from ZENODO_RELEASE.md] and GitHub:
  https://github.com/jonnabio/xai-eval-framework. An artifact bundle is provided as Supplemental
  Data S1. The UCI Adult, German Credit and Breast Cancer Wisconsin datasets are third-party
  and available from the UCI Machine Learning Repository."
- **Funding is removed from the Acknowledgments** (PeerJ: "Do not acknowledge funders here").

## 5. AI-use disclosures (PeerJ policy: Author Policies §4)

PeerJ separates two cases. Both apply to this paper.

**(a) AI as a component of the research (EXP4). Goes in Methods.** PeerJ requires the tool,
its version and the complete prompts. Port this into §Materials & Methods, EXP4:

> The three original-cohort judges were gpt-4o-mini (OpenAI), claude-3-haiku-20240307
> (Anthropic) and gemini-1.5-flash (Google); the replication panel was openai/gpt-5.4-mini,
> anthropic/claude-haiku-4.5 and google/gemini-3.8-flash, accessed through OpenRouter. All
> judges ran at temperature 0.0 (max_tokens 512 in the original cohort, 4000 in the
> replication). The complete system instruction, per-instance user prompt and rubric are given
> in Supplemental Article S1, Table S1. The replication's rendered prompts and raw responses are
> archived with the code (Data availability). The original cohort's three Jinja templates were
> not retained; the prompts in Table S1 were transcribed from the recovered instrument and are
> the authoritative record of it.

The model IDs and settings above are copied from `paper_bc_tmlr_supplementary.tex` l.134–142 and
are not new values.

**(b) AI used in preparing the manuscript. Goes in the Acknowledgments and the form.**
Scope as stated by the author (D5): grammar, spelling and text correction.

> Acknowledgments: "Generative AI tools (Anthropic Claude) were used to correct grammar,
> spelling and wording. The author reviewed all output and takes full responsibility for the
> content. No AI tool was used to generate data, figures or the reference list."

> Form, "AI use" field: same text.

**[AUTHOR — must resolve before filing, see §9.2]** Check that this scope is complete. PeerJ
treats undeclared or understated AI use as a serious breach.

## 6. Notes to Staff (confidential; not seen by reviewers)

> The empirical cohort analysed in this manuscript was released with an earlier article by the
> author, Herrera-Vásquez & Herrero-Uceda (2026), Revista de Investigación Multidisciplinaria
> Iberoamericana (RIMI), https://doi.org/10.69850/rimi.vi3.307. This manuscript reports no
> result reported in that article (see section "Provenance of the Empirical Cohort"); the
> overlap is the shared execution cohort only. A preprint of this manuscript is posted on arXiv:
> [AUTHOR: arXiv ID, if posted before filing].

Add a fee-assistance request here only if D3 is resolved that way (§9.1).

## 7. Paper A (RIMI) overlap: status 2026-10-02

PeerJ will not consider material already published in a peer-reviewed journal.

- `scan_shared_literals.py --strict`: **0 unexplained matches, 53 known coincidences** (each
  triaged with its reason in the script). Run on `paper/bc-peerj-cs` at the tag commit.
- §Provenance (`sec:prior_publication`) states that the per-method mean levels, the four-method
  omnibus and the cross-dataset SHAP levels are cited to RIMI and **not** restated.
- Gate: re-run both the scan and `verify_claims.py` (registry-side prior-publication check) on
  the PeerJ `.tex` once it exists. The scanner's `PAPER_BC` list must include the new file
  (plan task P2.4), or the PeerJ text goes unscanned.

No adjustment is needed beyond keeping both gates in the PeerJ build. If a new sentence in
the port (infrastructure, dataset citations) introduces a number, it is registered first.

## 8. Other elements to port

- **Computing infrastructure (AI Application checklist).** Draft:
  > Experiments were run in Python 3.x with scikit-learn 1.7.1, xgboost 3.1.2, shap 0.50.0,
  > lime 0.2.0.1, numpy 2.2.6, pandas 2.3.3 and scipy 1.16.3 (pinned in
  > `requirements-frozen.txt`), on [AUTHOR: OS, CPU model, cores, RAM]. EXP3 ran on Windows and
  > Linux hosts [AUTHOR: specifics]. No GPU was used [AUTHOR: confirm].
  **[AUTHOR]** The run metadata records timestamps and durations but no hardware, so this
  cannot be taken from artifacts. Also confirm the EXP2 runs (Feb 2026) used this frozen file
  (dated 2026-01-07). The EXP3 SHAP re-run (July 2026) used a newer environment: the A03
  finding attributed the BC/XGB shift to a library change. State both environments or say
  "versions as pinned at each run".
- **Dataset citations.** Adult: Becker & Kohavi (1996), doi:10.24432/C5XW20. German Credit
  (Statlog): Hofmann (1994), doi:10.24432/C5NC77. Breast Cancer Wisconsin (Diagnostic):
  Wolberg et al. (1993), doi:10.24432/C5DW2B. All three DOIs were resolved through doi.org on
  2026-10-02 (titles and years match). These go in the references; they are not AI-generated reference entries.
- **Supplement:** "Supplemental Article S1" (PDF), with tables keeping S1–S5 labels. Cited as
  "Table S1". Artifact bundle = "Supplemental Data S1".
- **Figures:** `Figure1.pdf`… exported from committed generators, without in-image titles.

## 9. Open blockers

### 9.1 Payment (D3) — blocks filing, not preparation

PeerJ charges only **after acceptance**. Submission and review are free. If the fee is not paid,
the accepted paper is not published. Current prices (check https://peerj.com/pricing before
deciding):
- APC (per article): about **US$2,155**.
- Individual Lifetime Membership (single author, so only one is needed): about **US$755**
  (Basic, one paper per 12 months) to US$970.
- Waivers: automatic only for World Bank **low-income** countries. Mexico is upper-middle, so
  it does not qualify. Institutional plans: check whether UNADE has one at
  peerj.com/institutions. A discretionary request can be made in Notes to Staff, but do not
  count on it.

### 9.2 AI-disclosure scope (D5)

The repository's history shows generative AI assisting with code, analysis scripts and
manuscript drafting, not only grammar and spelling (commits co-authored by Claude). PeerJ
requires disclosing **any** use and prohibits AI-generated reference lists. A disclosure
limited to grammar risks a breach finding if an editor looks at the public repository. Choose
the wording that matches what actually happened.

## 10. arXiv preprint (D6)

1. Build the de-anonymised PDF (PeerJ build, line numbers **off**, or the TMLR `[preprint]`
   build). Use **one** version consistently.
2. arXiv category: primary **cs.LG**, cross-list **cs.AI**. Licence: **CC BY 4.0**, which is
   compatible with PeerJ's CC BY publication.
3. Upload the LaTeX source (arXiv compiles it). Include `wlpeerj.cls` if using the PeerJ build.
4. Comments field: "Submitted to PeerJ Computer Science." Add the journal DOI after acceptance.
5. arXiv requires endorsement for first-time submitters in cs.LG. **[AUTHOR]** check your
   account status first.
6. Paste the arXiv ID into the Notes to Staff (§6).

## 11. Upload set (filled in at the gate)

Review PDF (line numbers, cover page first) · `.tex` · references · `wlpeerj.cls` ·
`Figure1..N.pdf` · `Table1..N.tex` · Supplemental Article S1 (PDF) · Supplemental Data S1
(bundle zip, 3.8 MB). Each file under 30 MB, total under 50 MB.
