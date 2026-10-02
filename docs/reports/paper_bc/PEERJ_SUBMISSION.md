# Paper B+C — PeerJ Computer Science submission sheet

**Status (2026-10-02):** manuscript ported. TMLR desk-rejected submission 12779 without review.
Plan: `docs/planning/paper_bc_peerj_retarget_plan_2026-10-02.md`. Lane: `paper/bc-peerj-cs`,
cut from tag `tmlr-submission-12779`.

**PeerJ files:** `paper_bc_peerjcs.tex` / `.pdf` (26 pp, line numbers on) and
`paper_bc_peerjcs_supplemental_S1.tex` / `.pdf` (6 pp), on `wlpeerj.cls` v1.2 (the rticles
copy of the Overleaf class). Build: `make peerj`, or Tectonic on each file. Under XeTeX the
build maps Times/Helvetica to TeX Gyre; under pdflatex (PeerJ, Overleaf) the class's own fonts
load. Results, tables and figures are moved verbatim from the TMLR source, and every number site
is registered twice (TMLR and PeerJ) in `pub/claim_registry.toml`.

**Author decisions (2026-10-02):** D1 Research Article · D2 title spells out "Explainable AI"
· D4 Provenance kept, plus a Notes-to-Staff sentence · D5 human-directed AI-assistant
disclosure (§5b) · D6 arXiv preprint approved · D7 gap analysis goes to Discussion ·
Department of Computer Science.
**Pending before filing:** Zenodo release (author, today: `ZENODO_RELEASE.md`). The PDF prints
"[ZENODO VERSION DOI PENDING]" until `\zenodoversiondoi` is set. **D3 payment** (§9.1).

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

¹ Department of Computer Science, Universidad Americana de Europa (UNADE),
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

Ported into §3.3 of `paper_bc_peerjcs.tex`.

**(b) AI used as an assistant. Goes in the Acknowledgments and the form (D5, 2026-10-02).**
Framing set by the author: the human researcher guides the work and does the planning, the
decisions and the experimental design; AI is an assistant. The scope lists every use visible in
the public repository history (language editing, programming support, number checking), so the
disclosure matches what an editor would find.

> Acknowledgments (in the manuscript): "The author designed and directed this research.
> Generative AI tools (Anthropic Claude, used through Claude Code) served as assistants under
> the author's direction for language editing (grammar, spelling and wording), programming
> support for the evaluation framework, and checking the manuscript's numbers against the
> committed artifacts. The research questions, study design, experimental protocol, choice of
> methods and metrics, interpretation of the results and all conclusions are the author's. The
> author reviewed every AI-assisted change, accepted or rejected it, and takes full
> responsibility for the content. No AI tool generated research data, figures or the reference
> list. Large language models were also objects of study in EXP4, as described in
> Section 3.3."

> Form, "AI use" field: "Generative AI (Anthropic Claude via Claude Code) was used as an
> assistant under the author's direction for language editing, programming support and
> checking reported numbers against the study's artifacts. All research questions, design,
> methods, analysis decisions, interpretation and conclusions are the author's; the author
> reviewed and approved every AI-assisted change. No data, figures or references were generated
> by AI. Separately, three LLM judges are the object of study in the EXP4 reliability
> experiment; their models, versions, settings and complete prompts are given in Section 3.3
> and Supplemental Article S1, Table S1."

**[AUTHOR] confirm one fact:** "No AI tool generated the reference list" means every
reference was found by you or taken from the sources you read. AI assistance in *checking*
references against Crossref/DOI records is covered by "checking". If any reference entry was
first proposed by the AI, say so instead. PeerJ prohibits AI-generated reference lists.

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

- The PeerJ main text, Supplemental Article S1 and the PeerJ abstract fragment are now in the
  scanner's `PAPER_BC` list. `scan_shared_literals.py --strict` on the PeerJ edition: **0
  unexplained matches** (108 known coincidences = the 53 triaged TMLR ones, found again in the
  PeerJ copies).
- `verify_claims.py`: 321 claims, 581 sites (96 new PeerJ twins), all green. The PeerJ files
  are under `[coverage]`, so any unregistered result-shaped number fails the build.
- §Provenance (`sec:prior_publication`, now Discussion 5.5.1) states that the per-method mean
  levels, the four-method omnibus and the cross-dataset SHAP levels are cited to RIMI and
  **not** restated.
- New text added in the port carries no results. The software versions are skipped by a new
  scanner rule: a dotted triple such as 1.7.1 is never a result. Declaring "1.7" structural
  would have masked real results everywhere.

**Conclusion: the PeerJ edition reports no Paper A result.** No content had to be removed.

## 8. Other elements to port

- **Computing infrastructure: ported (§3.2.8), extracted from the experiments.** What the
  artifacts record:
  - Software: `environment.yml` (Python 3.11) and `requirements-frozen.txt` (scikit-learn
    1.7.1, XGBoost 3.1.2, SHAP 0.50.0, LIME 0.2.0.1, NumPy 2.2.6, pandas 2.3.3, SciPy 1.16.3).
    No GPU setting in any config.
  - Hosts: worker manifests and claims name `JON_ASUS` / `jon_asus` and `jonaasusrog`
    (Windows), `linux_dell` (Linux), a WSL environment (EXP3 runbook), and macOS
    (`docs/postmortems/macos_process_bomb.md`).
  - **Not recorded anywhere:** CPU model, core count, RAM. Not recorded either is the host of
    most EXP2 runs. Only work-queue runs (Mar–Apr 2026: 4 MLP-SHAP and 4 SVM-SHAP files
    committed from other identities or the `jon_asus` worker) carry one. The paragraph
    therefore says so instead of inventing specifications.
  - **Consequence disclosed** in §5.5 ("Execution hosts and the cost endpoint"): wall-clock
    cost includes between-host variance, and the two members of a paired cell may have run on
    different hosts. The quality endpoints are unaffected. This limitation was not stated in the
    TMLR version. **[AUTHOR]** If you can still recall or check each machine's CPU and RAM,
    adding them strengthens the paragraph. The run-to-host mapping cannot be recovered.
- **Dataset citations: ported.** Adult: Becker & Kohavi (1996), doi:10.24432/C5XW20. German
  Credit (Statlog): Hofmann (1994), doi:10.24432/C5NC77. Breast Cancer Wisconsin (Diagnostic):
  Wolberg et al. (1993), doi:10.24432/C5DW2B. All three DOIs resolved through doi.org on
  2026-10-02; author lists follow UCI's recommended citations.
- **Supplement: ported** as "Supplemental Article S1" (PDF), with tables keeping S1–S6 labels.
  Cited as "Table S1". Artifact bundle = "Supplemental Data S1".
- **Figures: open.** The figures are still embedded. PeerJ also asks for separate upload files
  (`Figure1.pdf`…) without in-image titles. Export them from the committed generators at the
  gate.

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

### 9.2 AI-disclosure scope (D5): resolved 2026-10-02

Resolved by the human-directed assistant wording in §5b. It covers language editing,
programming support and number checking, which matches the repository history. One fact to
confirm remains (the reference list, §5b).

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
