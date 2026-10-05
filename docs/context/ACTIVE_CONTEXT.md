# Active Context: XAI Evaluation Framework

## Publication status - 2026-10-04

| Paper | Venue | Status | Submission / publication record |
|---|---|---|---|
| **A** | *Revista de Investigación Multidisciplinaria Iberoamericana* (RIMI) | Published | 2026; DOI [10.69850/rimi.vi3.307](https://doi.org/10.69850/rimi.vi3.307) |
| **B** | *CLEI Electronic Journal* (CLEIej) | Submitted; under review | Submitted 2026-10-04; submission 1196 |
| **C** | *Tecnología en Marcha*, AI special issue | Revised draft on `main`, 15 Word pages; **not submitted** (deadline 2026-10-15) | Zenodo 0.10.0, [10.5281/zenodo.23149419](https://doi.org/10.5281/zenodo.23149419); release `paper-c-tm-2026-10-04` |
| **D** | *Tecnología en Marcha*, AI special issue | Submitted | Emailed 2026-10-03; acknowledgement pending in the latest record |
| **E** | *Computación y Sistemas* (CIC-IPN) | Submitted; under review | Submitted 2026-10-04; submission 6783 |
| **F** | No venue selected | Analytical framework in progress | Pre-analysis plan and methodological appraisal exist; no empirical results or submission |

**Paper B+C history:** The combined 32-page manuscript was submitted to TMLR on
2026-09-30 (submission 12779) and desk-rejected on 2026-10-02, then submitted to
*Inteligencia Artificial* (IBERAMIA) on 2026-10-01 (date reported by the author) and
desk-rejected on 2026-10-04. It is no longer under review. On 2026-10-04 the author
decided to split it: Paper B is the paired SHAP-LIME study now submitted separately to
CLEIej, and Paper C is being developed separately around LLM-judge reliability and the
taxonomy. The combined manuscript is not counted as a current paper submission.

## Session Handoff - 2026-10-04 (session end: Paper C drafted, reviewed, revised, archived, on main)

This is the latest Paper C entry. The Paper C entries below keep the detail of each step.

- **Completed**:
  - **Lane and folder:** lane `paper-c` (branches `paper/c-*`, owns `docs/reports/paper_c/**`)
    added to `scripts/pubs/lanes.toml` with tests (pull request #20). The April 2026 survey
    prototype was removed; the Paper C inputs were copied out of `docs/reports/paper_bc/`,
    which is frozen. ADR-0022 amended.
  - **Plan:** `docs/reports/paper_c/PLAN.md`, sections 1 to 15, approved by the author. Venue
    fixed: *Tecnología en Marcha*, AI special issue, deadline 2026-10-15, English, single
    author.
  - **Manuscript:** "Do LLM Judges Agree on the Quality of Explanations? A Two-Panel
    Reliability Study" (title chosen by the author). Source `paper_c_template.tex`; numbers
    are filled from result files by `scripts/build_paper_c.py`. Blind and full versions, PDF
    and Word, both **15 pages in Word (the limit)**; abstract 246 words, resumen 249; 5
    tables, 1 figure, 25 references.
  - **Rigor review** (Scientific Advisor): `docs/review/scientific-rigor-review_paper_c_2026-10-04.md`,
    major revision, findings F01 to F14. All were answered in the revision except F11
    (literature) and F12 (registry); the table is in `docs/reports/paper_c/README.md`.
  - **New analyses:** `scripts/paper_c_reliability.py` (agreement inside each explainer, one
    call, panel mean, ICC(2,1) and ICC(3,1), F-based intervals, raw agreement, use of the
    printed metrics) and `scripts/paper_c_posthoc.py`.
  - **Clean condition** (new cohort, RCA-002): 192 cases, 3 judges, one call, no metrics,
    outcome or label in the prompt; 576 calls, all valid; in
    `docs/reports/paper_c/clean_condition/`.
  - **Human subset prepared, not run:** 56 cases (seed 20261004), two rating sheets that show
    the clean record. No sheet has been sent.
  - **Author decisions:** draft read; the two added references are fine; AI declaration has
    the author's own text; built PDF and Word files stay local; Anchors and DiCE are not
    re-rendered.
  - **On `main`:** pull requests #20, #21 and #22 merged, plus this handoff. GitHub release
    `paper-c-tm-2026-10-04`; **Zenodo 0.10.0, `10.5281/zenodo.23149419`**; the full version
    cites both.
- **Current State**:
  - Paper C is a complete revised draft on `main`. **It is not submitted.**
  - `docs/reports/paper_c/submission/` (local, git-ignored) holds `paper_c_blind.{pdf,docx}`,
    `paper_c_full.{pdf,docx}` and `Figure1.tiff`, built after the DOI was set.
  - The numbers of the draft come from result files but are **not in
    `pub/claim_registry.toml`**; `pub/claims.toml` still has a placeholder Paper C abstract
    and `verify_sync.py` does not check `paper_c.tex`.
  - `docs/reports/paper_bc/` is frozen. Papers B, D and E are submitted and were not touched.
  - The lane lock `paper-c` is released.
- **Next Steps**:
  1. Draft the note to the editor: Paper D is in the same issue, and earlier reliability
     tables are public in the 32-page edition and the thesis.
  2. Claim registry for `paper_c.tex`, on a `pubs/*` branch and by pull request: `[coverage]`,
     `docs/reports/paper_c/` on the protected side of `[exclusivity]`, a `paper_c` resolver
     in `scripts/pubs/claim_sources.py`, the real abstract in `pub/claims.toml`,
     `verify_sync.py`. Several values are already registered for the thesis and the 32-page
     edition, so they gain sites on existing claims; expect chance collisions with Papers D
     and E that need exceptions.
  3. A rigor review by a session or person that did not write the draft.
  4. Targeted literature search on LLM-judge reliability (review F11); the paper cites four
     works on it. Any added text needs an equal cut.
  5. Author: send the email to `revistatm@tec.ac.cr` with the blind and full Word files, the
     figure and a telephone number.
- **Blockers/Issues**:
  - **Pending decision (author):** whether the human subset is part of this submission. The
    recommendation is no; the draft says it has none. If yes, the sheets must go out at once
    and the section needs an equal cut.
  - The paper is at the page limit: nothing can be added without removing as much.
  - The revision was made by the session that wrote the review, so it has had no independent
    review.
  - The second-reviewer adjudication of the corpus (28 disagreements, `corpus_audit/`) is
    open; the paper uses the corpus in one sentence only.
  - Two uncommitted edits from another session were left as found: the journal account
    request note at the top of this file and `docs/reports/paper_d/README.md` (lane
    `paper-d`).
- **Notes**:
  - Start with `python scripts/pubs/check_lane.py claim --owner <name>` on branch
    `paper/c-llm-judges`. Lane files and shared files go in separate commits; shared files
    reach `main` by pull request.
  - Build order and commands: `docs/reports/paper_c/README.md`, section Build. Run
    `paper_c_reliability.py` before `paper_c_summary.py`. Use `.venv\Scripts\python.exe`
    for the analyses and for `pytest`.
  - Edit `paper_c_template.tex`, never `paper_c.tex`. Count pages in Word itself.
  - Do not change the title or the AI declaration without the author's approval.
  - A change to code or results needs a new Zenodo version; a text change does not.
  - A new judge run is a new cohort in its own directory (RCA-002).
  - `pub/fragments/build_meta.env` changes on every fragment build; restore it before a
    commit.
  - Local `main` is checked out in `../xai-eval-framework-main-status`; compare against
    `origin/main`.

## Session update - 2026-10-04 (Paper C: author's read, release 0.10.0)

The session-end handoff above is the latest; the Paper C handoff below keeps the detail.

- **Author decisions:** the draft was read; the two added references are fine; the human
  raters see the clean record (sheets rebuilt, none had been sent); built PDF and Word files
  stay local; the AI declaration has the author's own text and is not changed without
  approval; merge and release approved.
- **Pull request #21 merged** (`main` at `d97dbe188`): the Paper C folder, the rigor review
  and the handoffs.
- **Zenodo version 0.10.0: `10.5281/zenodo.23149419`**, from GitHub release
  `paper-c-tm-2026-10-04`. The full version of the paper cites it; both placeholders are
  gone. The draft is still 15 pages in Word.
- **Still open:** claim registry for `paper_c.tex`; a review by a session that did not write
  the draft; the search on LLM-judge reliability (review F11); the note to the editor;
  whether the human subset is in this submission (recommendation: no).

## Session Handoff - 2026-10-04 (Paper C revised after the rigor review; clean condition run)

This is the Paper C handoff of the revision. The two Paper C entries below keep the earlier detail.

- **Completed**
  - **Author decisions on the review:** SHAP and LIME are the main analysis; the clean
    condition is approved; the within-explainer analysis is accepted as a dated addition; the
    venue does not change (`docs/reports/paper_c/PLAN.md`, section 15).
  - **Clean condition run:** 192 cases, 3 judges, one call, no metrics, outcome or label in
    the prompt; 576 calls, all valid. A new cohort in its own directory,
    `docs/reports/paper_c/clean_condition/` (prompts, raw responses, parsed scores), written
    by `scripts/run_clean_condition.py`. Nothing under `experiments/` or `outputs/` changed.
  - **New analyses** (`scripts/paper_c_reliability.py`, fixed in the plan before they ran):
    agreement inside each explainer, one call, panel mean, two-way models, F-based intervals,
    raw agreement, rationales naming a metric, correctness contrast, clean against primary.
  - **Manuscript rewritten** around the review: title unchanged ("Do LLM Judges Agree on the
    Quality of Explanations? A Two-Panel Reliability Study"); 5 tables, 1 figure, 25
    references; abstract 246 and resumen 249 words. Response to each finding in
    `docs/reports/paper_c/README.md`.
- **Current State**
  - **The draft is at 15 pages in Word, the journal's limit.** Any addition needs an equal cut.
  - Results: over all cases no dimension reaches 0.75 (0.601 and 0.731); up to 67% of the
    variance is between explainers; inside SHAP no dimension exceeds 0.19 (0.20 without
    metrics), inside LIME five dimensions are between 0.63 and 0.75; without metrics the
    fidelity relation vanishes for SHAP and DiCE, Claude Haiku 4.5 scores higher, and
    agreement on audit usefulness falls from 0.66 to 0.42.
  - Not reviewed again; the author has not read it. **Not in the claim registry** (unchanged).
  - Verified: `verify_claims.py` 985 claims / 1297 sites; `verify_sync.py`;
    `verify_exp4_reconstruction.py` 18 pins. Lane lock released.
- **Next Steps**
  1. Start with `python scripts/pubs/check_lane.py claim --owner <session name>`.
  2. Author: read `docs/reports/paper_c/submission/paper_c_blind.pdf`; decide whether the
     raters see the clean record; send the rating sheets; adjudication; check the two
     references marked NEW; a targeted search on LLM-judge reliability (review F11).
  3. Registry work through `main`; a review by a session that did not write the draft;
     Zenodo version; `\papercrelease` and `\papercarchive`.
- **Blockers/Issues**
  - Deadline 2026-10-15. The human subset, if it arrives, does not fit without cuts.
  - Anchors and DiCE were judged as lists of feature weights; the paper says so and does not
    repair it.
  - The clean condition has one call per judge; the primary has three.
- **Notes**
  - The judge client reads `configs/secrets/api_keys.env`; the run used the project's key.
  - Gemini 3.8 Flash was the slow judge (about 20 seconds per call); run the shards in
    parallel: `--judge <id> --shard i/4`, then `--parse-only`.
  - A look at partial clean data overstated the effect; only the full data are reported
    (PLAN.md 15.4).
  - `paper_c_reliability.py` must run before `paper_c_summary.py`: the figure reads its output.

## Session Handoff - 2026-10-04 (Paper C: plan approved, prompt findings, first draft built)

This is the latest Paper C handoff; it supersedes the one directly below, which keeps the
detail of the lane setup.

- **Completed**
  - Pull request #20 merged (`paper-c` lane, ADR-0022 amendment, sync checks unwired from the
    April prototype). Branch `paper/c-llm-judges` has taken `origin/main`.
  - **Author decisions:** plan approved, adjusted as the work goes; English; 56-case human
    sample; raters are not the corpus reviewer; single author; AI-use statement as Paper D;
    no question to the editor for now (`docs/reports/paper_c/PLAN.md`, section 13).
  - **Two findings about the EXP4 prompts** (PLAN.md, section 14):
    - all 192 prompts of `hidden_label_primary` print the field `quadrant` (TP, FN, TN, FP),
      which with the prediction gives the true label: no condition of cohort 2 withholds it;
    - all 576 prompts print the technical metrics of the explanation.
  - **Human subset prepared:** `human_subset/sample_cases.csv` (7 cases per dataset-by-explainer
    cell, seed 20261004) and one self-contained rating sheet per rater, with instructions.
    Not sent; sending is the author's step.
  - **Post hoc analysis run as fixed in the plan:** within each explainer the overall-quality
    score rises with the fidelity value shown in the prompt (Spearman 0.35 to 0.59, all four
    significant after Holm over 20 tests); results in `docs/reports/paper_c/results/`.
  - **First draft built:** `paper_c_template.tex` (source), generated `paper_c.tex`,
    `scripts/build_paper_c.py` (render, PDF, Word, blind and full). Title, set by the
    author: "Do LLM Judges Agree on the Quality of Explanations? A Two-Panel Reliability
    Study"; it is not changed without the author's approval. 12 pages measured in Word, abstract 244 and resumen 248 words, 4 tables,
    1 figure, 25 references. Identity scan of the blind files clean except the citation of
    the RIMI article, as in Paper D.
  - **Rigor review of the draft** (Scientific Advisor, same session, not independent):
    `docs/review/scientific-rigor-review_paper_c_2026-10-04.md`. Grade: major revision, mean
    3.1; 5 major and 7 minor findings. The study can stand alone, but not as drafted:
    - F01: the pooled ICC mostly measures agreement on the explainer. Inside SHAP the ICC of
      overall quality is -0.19 and of completeness 0.06; only LIME keeps 0.63 to 0.75;
    - F02: Anchors and DiCE were shown to the judges as lists of feature weights, not as a
      rule and a counterfactual (108 of 192 cases);
    - F03: the primary estimate averages three replicates (one call: 0.675 for completeness)
      and the panel mean, ICC(1,k), exceeds 0.75 on four dimensions;
    - F04: the rationales cite the printed metrics in 80% (Claude), 40% (GPT) and 15%
      (Gemini) of the responses.
    The values of the review are probes, not results; they must be planned, dated and run in
    the lane before they are printed.
- **Current State**
  - The draft is the fallback version: no human-rated subset, no counts on the audited corpus
    axes. **It is not ready to submit** (review above) and the author has not read it.
  - **The draft's numbers are not in `pub/claim_registry.toml`.** They are generated from
    result files by the build. `paper_c.tex` is not under `[coverage]` or `[exclusivity]`, and
    `verify_sync.py` does not check it. `pub/claims.toml` still holds the placeholder abstract.
  - Verified: `verify_claims.py` 985 claims / 1297 sites; `verify_sync.py`. Built files are in
    `docs/reports/paper_c/submission/`, local only (`.gitignore` in the folder).
  - The lane lock was released at the end of the session.
- **Next Steps**
  1. Start with `python scripts/pubs/check_lane.py claim --owner <session name>`.
  2. Author: read `docs/reports/paper_c/submission/paper_c_blind.pdf`; decide on the clean
     prompt condition (PLAN.md 14.4); send the rating sheets; start adjudication with the
     second reviewer; check the two references marked NEW.
  3. Registry work (shared files, pull request to `main`): coverage, exclusivity, a `paper_c`
     resolver in `claim_sources.py`, `verify_sync.py`, the real abstract in `pub/claims.toml`.
  4. Human-subset analysis script, written before the ratings arrive (PLAN.md section 6).
  5. Independent rigor review; Zenodo version; `\papercrelease` and `\papercarchive`.
- **Blockers/Issues**
  - Deadline 2026-10-15. Cut-offs: adjudication 2026-10-08, ratings 2026-10-10.
  - The quadrant finding also concerns the thesis chapter 5 and the 32-page edition, which
    call the condition label-hidden; the thesis lane must check its text.
  - Local `main` is checked out in a second folder (`../xai-eval-framework-main-status`) with
    a commit that `origin/main` does not have (`df9daf3bb`); it is not level with origin.
  - `docs/reports/paper_d/README.md` and the status block at the top of this file carry
    uncommitted edits made outside this session (journal account request). This session did
    not commit them.
- **Notes**
  - `paper_c_posthoc.py` takes about ten minutes (bootstrap); run it in the background.
  - A shell heredoc dropped LaTeX backslashes again; write patch scripts with the editor tool.
  - `build_paper_c.py` follows `scripts/pubs/build_paper_d.py`; Word page count was measured
    through Word's COM interface from PowerShell.

## Session Handoff - 2026-10-04 (Paper C: own lane and folder, prototype removed, plan proposed)

This handoff records the Paper C setup; the publication status summary above is current.

- **Completed**
  - **Author decisions:** Paper C is the LLM-judge reliability study with the taxonomy as
    framing; it is worked in `docs/reports/paper_c/` only, under a new lane; the April survey
    prototype is removed; the Paper C inputs are copied out of `docs/reports/paper_bc/`, which
    is frozen; venue *Tecnología en Marcha*, special issue on AI (deadline **2026-10-15**, the
    issue Paper D was sent to). Recorded as an amendment to ADR-0022.
  - **Pull request #20** (`pubs/paper-c-lane`), CI green, **not merged**: lane `paper-c`
    (`paper/c-*`, owns `docs/reports/paper_c/**`) in `lanes.toml` with two test lines; the
    ADR amendment; `verify_sync.py` no longer checks a Paper C manuscript; the 24-study claim
    and `[review_corpus.paper_c]` removed from the registry; the CI check of the old corpus
    removed; a placeholder Paper C abstract in `pub/claims.toml`.
  - **Branch `paper/c-llm-judges`** (cut from `pubs/paper-c-lane`): prototype removed (11
    files); `paper_c_review_corpus.csv` (44 papers) and `corpus_audit/` copied in;
    `README.md` and `PLAN.md` written.
- **Current State**
  - The plan is **proposed, not approved**. No manuscript and no new analysis exist.
  - Verified: `verify_claims.py` 985 claims / 1297 sites; `verify_sync.py`;
    `scan_shared_literals.py --strict` 0 unexplained; `verify_exp4_reconstruction.py` 18
    pins; 9 lane tests.
  - The main folder is on `paper/c-llm-judges`, pushed. The lane lock was released.
- **Next Steps**
  1. Author: merge pull request #20 (the assistant's merge was refused by the permission
     check). Then `git fetch origin main:main` and `git merge main` on `paper/c-llm-judges`.
  2. Start with `python scripts/pubs/check_lane.py claim --owner <session name>`.
  3. Author: answer the seven decisions in `docs/reports/paper_c/PLAN.md`, section 13.
  4. After approval: draw the 56-case sample and build the rating sheet (plan section 6);
     start adjudication (section 5); build script and manuscript (section 8).
  5. Unchanged: Papers B, D and E wait for their journals; the thesis sentence about the
     earlier article; Task 3 / RCA-001 Phase 2; `git worktree prune`.
- **Blockers/Issues**
  - Eleven days to the deadline, with adjudication and human ratings depending on other
    people; the plan sets cut-offs of 2026-10-08 and 2026-10-10 with fallbacks.
  - The existing annotation viewer and guidelines were made for EXP1 (three dimensions, 20
    Adult cases); the seven-dimension EXP4 rubric needs a new rating sheet.
  - The journal limit is 15 Word pages at 12 pt and 1.5 spacing, about 5,000 words.
  - Paper D is in the same special issue; the 32-page edition with the reliability tables is
    public.
- **Notes**
  - `scripts/pubs/claim_sources.py` still maps `review_corpus_rows:paper_c` to
    `docs/reports/paper_c/paper_c_review_corpus.csv`, which now holds the 44-paper corpus.
  - The chapter manuscript (`07_diseno_empirico.md`) names `pub/fragments/paper_c_abstract_en.tex`
    as an initial source; that fragment is now a placeholder.
  - `python -m pytest` needs the project `.venv`; `pub/fragments/build_meta.env` changes on
    every fragment build and is restored before committing.
## Session Handoff - 2026-10-04 (Paper B SUBMITTED to CLEI Electronic Journal, ID 1196)

This is the latest handoff. It closes Next Steps 2 and 3 of the Paper B handoff directly
below, which keeps the detail of the draft.

- **Completed**
  - **Paper B was submitted by the author on 2026-10-04** through the journal's online
    system; the journal acknowledged it by email (Esteban Clua) as **submission 1196**
    (https://www.clei.org/cleiej/index.php/cleiej/authorDashboard/submission/1196). Record in
    `docs/reports/paper_b/CLEIEJ_SUBMISSION.md`, "Submission record".
  - File sent: `docs/reports/paper_b/paper_b_cleiej.pdf`, **12 pages**, source at commit
    `c72a17e88`, with the comments for the editor of section 3 of the sheet.
  - Changes from the author's revision before submitting:
    - Figure 2 re-rendered without the horizontal grid lines
      (`scripts/generate_paper_b_figures.py`);
    - the "Provenance of the cohort" paragraph of Section 5.3 removed (author: the relation to
      the earlier executions is already stated). The full PDF went from 13 to 12 pages.
  - Author decisions: title confirmed; the keywords item is dropped; the sentence about the
    two earlier rejections is not in the comments for the editor (kept as an optional
    sentence in the sheet).
- **Current State**
  - Paper B is under review at CLEIej. Both PDFs have 12 pages, the journal's minimum.
  - Last verification (after the final build): `verify_claims.py` 986 claims / 1298 sites /
    60 retired-value guards; `verify_sync.py`; `scan_shared_literals.py --strict` 0
    unexplained; blind check clean.
  - Pull request #19 (this session's commits and this handoff) merged to `main`. The main
    folder is on `paper/b-cleiej`, level with `main`, clean. The `paper-b` lane lock was
    released at the end of the session.
  - The assumptions in the submission record (the comments sent were the text of section 3
    without the optional sentence; the file uploaded was the 12-page build) were stated to
    the author and not contradicted.
- **Next Steps**
  1. Start with `python scripts/pubs/check_lane.py claim --owner <session name>`; stop if it
     fails.
  2. Paper B: wait for the journal. When the decision arrives, record it in the sheet and
     plan the response.
  3. Paper C: its own plan and lane; adjudication with the second reviewer; a stratified
     sample of 50 to 60 EXP4 cases for two human raters; a dated plan before any post hoc
     analysis of judge scores against technical metrics.
  4. Check the thesis chapters and the 32-page edition for the sentence that the earlier
     article left the SHAP-LIME contrast unresolved; it is wrong.
  5. Unchanged: Paper E and Paper D wait for their journals; return the main folder to
     `thesis/rca-001-phase-2` for Task 3 / RCA-001 Phase 2; `git worktree prune`.
- **Blockers/Issues**
  - The two manuscripts under review elsewhere (Papers D and E) are disclosed to the editor
    in the submission comments only; the manuscript no longer mentions them. A referee does
    not see the comments.
  - Both PDFs are at the 12-page minimum: a cut in a revision needs an equal addition.
  - The Zenodo 0.9.0 archive carries the earlier title, Figure 3, the old Figure 2 and the
    removed paragraph. The comments for the editor say the archive has an earlier title.
  - Unchanged: the novelty risk (four manuscripts on the same executions); the repository's
    records of the random-forest size disagree.
- **Notes**
  - Do not rebuild the Paper B PDFs or change its text unless a revision is requested. A
    revision that changes code or results needs a new Zenodo version.
  - Figure 1 still has faint vertical grid lines; the author asked only about Figure 2.
  - `generate_paper_b_figures.py` needs the project `.venv`
    (`.\.venv\Scripts\python.exe`). It rewrites both figures; an unchanged figure differs
    only in its PDF timestamp, so restore it with `git checkout --` before committing.
  - A shell heredoc dropped the backslashes of a LaTeX string again in this session; use the
    editor tool for `.tex` edits.
  - Commit order that the hook accepted: `scripts/` (shared), then `docs/reports/paper_b/`,
    then `ACTIVE_CONTEXT.md`, each in its own commit.

## Session Handoff - 2026-10-04 (session end: Paper B+C split; Paper B drafted, reviewed, archived, on main)

This is the latest handoff and the full state at the end of the session. It supersedes the
three Paper B entries of the same day directly below it, which keep the detail.

- **Completed**
  - **Rejection recorded.** *Inteligencia Artificial* (IBERAMIA) rejected the 32-page Paper
    B+C at the initial editorial assessment (reported 2026-10-04; submitted 2026-10-01
    according to the author; no ID, no review, no named defect):
    `docs/reports/paper_bc/IBERAMIA_REJECTION_RECORD.md`. Tag `iberamia-submission-2026-10`.
  - **Assessment** (Scientific Advisor):
    `docs/review/paper-c-resurrection-assessment_2026-10-04.md`. Paper C is viable only as the
    LLM-judge reliability study with the taxonomy as framing.
  - **Author decisions (ADR-0022):** split the paper; Paper B first, then Paper C; about 13
    pages (the author's own target); Paper B goes to the **CLEI Electronic Journal**; Paper B
    has its own folder and lane; the second-reviewer disagreements must be adjudicated; two
    human raters are available for Paper C.
  - **Paper B written:** `docs/reports/paper_b/paper_b_cleiej.tex`, in the journal class
    `cleiej.cls`. Plan: `docs/planning/paper_b_13pp_reduction_plan_2026-10-04.md`. Sheet:
    `docs/reports/paper_b/CLEIEJ_SUBMISSION.md`. No registered value changed; 78 registry
    sites added; the file is under `[coverage]`, the Paper A overlap scan and the
    retired-value guards; `[exclusivity]` forbids both `paper_bc/` and `paper_b/`.
  - **Folder and lane:** the April prototype in `docs/reports/paper_b/` was removed (in the
    history, last at `cd4af0e94`); lane `paper-b`, branches `paper/b-*`, in `lanes.toml`. The
    fragment id `paper_b` holds the CLEIej abstract.
  - **Review** (Scientific Editor, same session, not independent):
    `docs/review/scientific-review_paper_b_cleiej_2026-10-04.md`. Major finding, fixed: the
    published RIMI article already reports a paired SHAP-LIME Wilcoxon test on 45 cells and
    announces the 75-cell set without reporting it; Paper B now says it extends that test.
    Also fixed: H2 direction, scope of the kernel-width probe, the TreeExplainer cost
    mechanism as a candidate explanation, the abstract opening, the title, Table 5 (SHAP-LIME
    gap column; Figure 3 removed), the stability-protocol caveat.
  - **Journal checklist** checked; 13 references gained a verified DOI or URL (33 of 38).
    Acknowledgments thank Miguel Herrero Uceda only (author's text; the AI-use statement was
    removed by the author).
  - **Double-blind build** added at the author's request: `paper_b_cleiej_blind.tex`.
  - **Zenodo version 0.9.0: `10.5281/zenodo.23147228`**, from GitHub release
    `paper-b-cleiej-2026-10-04` (tag on `main` `a2ea80080`); the paper cites it.
  - Pull requests #15, #16, #17 and the one carrying this handoff merged to `main`; CI green.
  - Paper C preparation: `docs/reports/paper_bc/second_reviewer_adjudication_sheet.csv` (28
    disagreements in 12 records, decision columns empty).
- **Current State**
  - **Paper B is ready for the author's read, not yet submitted.** Title: "When Does SHAP
    Outperform LIME? Model- and Configuration-Dependent Results from a Paired Tabular
    Benchmark". Full PDF `paper_b_cleiej.pdf`: 13 pages, 2 figures, 9 tables, 38 references,
    abstract 199 words (limit 200). Blind PDF `paper_b_cleiej_blind.pdf`: 12 pages, the
    journal's minimum.
  - Last verification: `verify_claims.py` 986 claims / 1298 sites / 60 retired-value guards;
    `verify_sync.py`; `scan_shared_literals.py --strict` 0 unexplained;
    `verify_exp4_reconstruction.py` 18 pins; 9 lane tests.
  - `docs/reports/paper_bc/` holds the unedited 32-page edition (still under `[coverage]`),
    the rejection records, the corpus and the adjudication sheet: the Paper C material.
  - The main folder is on `paper/b-cleiej`, level with `main`, clean. No lane lock is held.
- **Next Steps**
  1. Start with `python scripts/pubs/check_lane.py claim --owner <session name>`; stop if it
     fails.
  2. Author: read `docs/reports/paper_b/paper_b_cleiej.pdf` (introduction and Section 4.1
     first), confirm the new title, decide the note to the editor (`CLEIEJ_SUBMISSION.md`,
     section 3), and submit the full PDF at https://www.clei.org/cleiej. Record the
     submission in the sheet and here.
  3. Advisable before submitting: a review by a session or person that did not write the
     draft.
  4. Paper C, after Paper B is submitted: its own plan and lane; adjudication with the second
     reviewer; a stratified sample of 50 to 60 EXP4 cases for two human raters; a dated plan
     before any post hoc analysis of judge scores against technical metrics.
  5. Check the thesis chapters and the 32-page edition for the sentence that the earlier
     article left the SHAP-LIME contrast unresolved; it is wrong.
  6. Unchanged: Paper E and Paper D wait for their journals; return the main folder to
     `thesis/rca-001-phase-2` (`git switch`, then `git merge main`) for Task 3 / RCA-001
     Phase 2; `git worktree prune` for the removed side folders.
- **Blockers/Issues**
  - Novelty: four manuscripts (A, B, D, E) use the same executions. Paper B discloses its
    relation to each; an editor may still see it as incremental.
  - The Paper B review was not independent.
  - The Zenodo 0.9.0 archive and the GitHub release carry the earlier title and Figure 3. A
    text change needs no new version; a change to code or results does.
  - The blind PDF is at the 12-page minimum: any cut takes it below.
  - The journal says keywords should come from its list of topics; the list was not found.
  - Paper E's submitted text names the 32-page paper as a companion; correct it only if E is
    revised.
  - The repository's records of the random-forest size disagree (50 trees of depth 15 in one
    metadata file, 100 trees in another); the paper states no size.
- **Notes**
  - CLEIej: no fees, single-blind, at least 12 pages, abstract of at most 200 words, table
    captions above and without a final period, IEEE numbered references in citation order.
  - Build: `tools/tectonic-portable/tectonic docs/reports/paper_b/paper_b_cleiej.tex` and the
    same for `paper_b_cleiej_blind.tex`. Figures:
    `python scripts/generate_paper_b_figures.py --output-dir docs/reports/paper_b/figures`.
  - Blind check after every edit: the `pdftotext ... | grep` line in `CLEIEJ_SUBMISSION.md`,
    section 6; expected output nothing.
  - A file under `docs/reports/paper_bc/` or `docs/reports/paper_b/` is never added to the
    `[exclusivity]` file list; those folders are its protected side.
  - In this shell `sed` and heredocs drop backslashes, and a heredoc with apostrophes can
    fail to parse: use the editor tool or a script file for LaTeX, TOML and long text.
  - Release route that worked again: pull request, `gh pr merge --merge`, tag `origin/main`,
    push the tag, `gh release create <tag> --verify-tag`; Zenodo archived it in about two
    minutes.

## Session update - 2026-10-04 (Paper B: review fixes applied, new title, double-blind build)

This entry is the latest. It closes the two open author decisions of the entry below.

- **Title is now** "When Does SHAP Outperform LIME? Model- and Configuration-Dependent Results
  from a Paired Tabular Benchmark" (review F02). The Zenodo 0.9.0 archive carries the earlier
  title; a text change needs no new version.
- **F07:** Figure 3 removed; Table 5 has the paired SHAP-LIME fidelity gap column (registered
  values). **F08:** Section 4.6 states that the stability noise also perturbs the one-hot
  columns and that the encoding and the perturbation scheme are not separated.
- **Double-blind build** added at the author's request:
  `docs/reports/paper_b/paper_b_cleiej_blind.tex` and `.pdf` (12 pages; same source, switched
  by `\blindreview`). Identity scan clean. CLEIej reviews single-blind, so the file to
  submit there is `paper_b_cleiej.pdf` (13 pages, 2 figures, 7 data tables plus 2 text tables).
- Verified after the last build: `verify_claims.py` 986 claims / 1298 sites; `verify_sync.py`;
  `scan_shared_literals.py --strict` 0 unexplained.
- **Next:** the author reads the PDF and submits; an independent review is still advisable.

## Session update - 2026-10-04 (Paper B reviewed, on main, Zenodo 0.9.0)

This entry is the latest. It closes Next Steps 2 and 4 of the handoff directly below, and
corrects its paths: Paper B is in `docs/reports/paper_b/`.

- **Review** by the Scientific Editor role:
  `docs/review/scientific-review_paper_b_cleiej_2026-10-04.md`. It was done by the drafting
  session and is not independent.
  - **Major finding, fixed:** the published RIMI article already reports a paired SHAP-LIME
    Wilcoxon test on 45 matched cells (logistic regression, random forest, XGBoost) and
    announces a 75-cell set without reporting it. The draft, like the 32-page edition, said
    the earlier article left the contrast unresolved. The introduction, Sections 3.1, 4.1,
    5.1, the provenance paragraph and the abstract now say that Paper B extends that test.
  - Novelty risk: high against Paper A (now disclosed in the text), low against Paper D, low
    to moderate against Paper E. What is new in Paper B is the cost reversal between XGBoost
    and random forest, the dependence of LIME stability on kernel width and dataset, the
    cross-dataset LIME results, the masking probe, and intervals and effect sizes on 75 cells.
  - Also fixed: direction of H2, scope of the kernel-width probe, the TreeExplainer cost
    mechanism stated as a candidate explanation. Open, author decisions: the title (F02) and
    Figure 3 / a SHAP-LIME gap column (F07).
- **Before submission checklist** of the journal checked; 13 references gained a verified DOI
  or URL (33 of 38 have one). Acknowledgments now thank Miguel Herrero Uceda only (author's
  text); the AI-use statement was removed by the author.
- **`main`:** pull request #15 merged (`a2ea80080`), CI green.
- **Zenodo version 0.9.0: `10.5281/zenodo.23147228`**, from GitHub release
  `paper-b-cleiej-2026-10-04`. The paper cites it.
- **Verified after the last build:** 13 pages, abstract 199 words; `verify_claims.py` 986
  claims / 1298 sites; `verify_sync.py`; `scan_shared_literals.py --strict` 0 unexplained.
- **Next:** the author reads `docs/reports/paper_b/paper_b_cleiej.pdf` (introduction and
  Section 4.1 first), decides the title and the note to the editor
  (`docs/reports/paper_b/CLEIEJ_SUBMISSION.md`, section 3), and submits. A review by someone
  who did not write the draft is still advisable. Then Paper C.
- **For Paper C and the thesis:** the 32-page edition carries the same sentences about the
  earlier article leaving the contrast unresolved; check the thesis chapters for the same
  wording before they are deposited.

## Session Handoff - 2026-10-04 (Paper B+C rejected by IBERAMIA; split; Paper B 13-page draft for CLEIej)

This is the latest handoff. The Paper E handoff of the same day follows it and is unchanged.

- **Completed**
  - *Inteligencia Artificial* (IBERAMIA) rejected Paper B+C at the initial editorial
    assessment (reported 2026-10-04; submitted 2026-10-01 according to the author; no ID, no
    reviews, no named defect). Record: `docs/reports/paper_bc/IBERAMIA_REJECTION_RECORD.md`.
    The 32-page edition is tagged `iberamia-submission-2026-10`.
  - Scientific Advisor assessment:
    `docs/review/paper-c-resurrection-assessment_2026-10-04.md`. Paper C is viable only as
    the LLM-judge reliability study with the taxonomy as framing; not as a survey alone.
  - **Author decisions (ADR-0022):** reduce to about 13 pages (the author's own target);
    split the paper; **Paper B first, then Paper C**; Paper B goes to the **CLEI Electronic
    Journal**; title "LIME versus SHAP under Matched Conditions: A Paired Comparison on
    Tabular Models" for now; the second-reviewer disagreements must be adjudicated; two
    human raters are available for Paper C.
  - Plan approved and steps 1 to 6 executed:
    `docs/planning/paper_b_13pp_reduction_plan_2026-10-04.md`.
  - **Paper B first draft:** `docs/reports/paper_b/paper_b_cleiej.tex` and `.pdf`, 13 pages
    in the journal class (`cleiej.cls`), abstract 191 words (limit 200), 38 references in
    citation order, 9 tables, 3 figures, no appendix. Submission sheet:
    `docs/reports/paper_b/CLEIEJ_SUBMISSION.md`.
  - Registry: 78 sites added for the new file, which is under `[coverage]`; no value changed.
    The fragment id `paper_b` in `pub/claims.toml` now holds the CLEIej abstract.
  - **Paper B has its own folder and lane** (author, same day): `docs/reports/paper_b/`, lane
    `paper-b`, branches `paper/b-*`, with its own figures. The April prototype that was in
    that folder was removed (still in the history, last at `cd4af0e94`). Nothing of Paper B
    remains in `docs/reports/paper_bc/`. The Paper A overlap scan and the retired-value
    guards now read the Paper B files; `[exclusivity]` forbids both folders.
  - Paper C preparation: `docs/reports/paper_bc/second_reviewer_adjudication_sheet.csv`
    (28 disagreements in 12 records, decision columns empty).
- **Current State**
  - Main folder on `paper/b-cleiej` (it contains `paper/bc-refocus-13pp`), pushed, not
    merged to `main`. Lane `paper-b` is claimed by `claude-paper-b`.
  - Verified after the last build: `verify_claims.py` 986 claims / 1298 sites / 28 files fully
    registered; `verify_sync.py`; `scan_shared_literals.py --strict` 0 unexplained;
    `verify_exp4_reconstruction.py` 18 pins; 9 lane tests.
  - **Paper B is not ready to submit.** It has had no independent review and the author has
    not read it.
  - The 32-page files (`paper_bc_iberamia.*`) are unedited and still under `[coverage]`; they
    are the source for Paper C.
- **Next Steps**
  1. Start with `python scripts/pubs/check_lane.py claim --owner <session name>`.
  2. New session, Scientific Advisor: review `paper_b_cleiej.pdf` for focus, novelty against
     Papers A, D and E, and claim support. Findings to `docs/review/`.
  3. Author: read `docs/reports/paper_b/paper_b_cleiej.pdf`; decide the note to the editor
     (`CLEIEJ_SUBMISSION.md`, section 3).
  4. After the review: fixes, a new Zenodo version, update `\zenodoversiondoi`, pull request
     to `main`, then the author submits.
  5. Paper C, afterwards: adjudication with the second reviewer, sample of 50 to 60 cases for
     two human raters, its own plan, and a Paper C lane in `lanes.toml`.
  6. Unchanged: Paper E and Paper D wait for their journals; Task 3 / RCA-001 Phase 2.
- **Blockers/Issues**
  - Novelty risk (assessment F02): Paper B shares its runs with Papers A, D and E.
  - The Zenodo DOI printed in the draft (version 0.4.0) archives the 32-page edition.
  - Paper E's submitted text names the 32-page paper as a companion manuscript.
  - Float order: Table 5 lands after Section 4.6 in the PDF; cosmetic.
- **Notes**
  - `[exclusivity]` protects other documents from printing results of files under
    `docs/reports/paper_bc/`; a file in that folder is never added to its list.
  - CLEIej: at least 12 pages, abstract of at most 200 words, captions without a final
    period, IEEE numbered references in citation order, single-blind, no fees.
  - In this shell, `sed` and heredocs drop backslashes; use the editor tool or a script file
    for LaTeX edits.

## Session Handoff - 2026-10-04 (Paper E: second review, revision, Zenodo 0.8.0, SUBMITTED)

This is the latest handoff. It summarises the whole session and supersedes the four
Paper E entries of the same day directly below it, which keep the detail.

- **Completed**
  - **Second rigor review** of the revised Paper E (Scientific Advisor, read-only):
    `docs/review/scientific-rigor-review_paper_e_2026-10-04_r2.md`, major revision, 2
    major and 6 minor findings, 2 suggestions.
  - **Revision answering it** (response table in `docs/reports/paper_e/README.md`):
    - permutation reference for the overlap (`paper_e_review2_analyses.py`): SHAP of an
      instance against LIME of another instance of the same run gives 0.203 / 0.287 /
      0.648; instance-specific part 0.191 / 0.100 / 0.066 (Adult / German Credit / Breast
      Cancer);
    - self-agreement experiment rerun in full (`paper_e_ceiling.py`): saved top-10 lists,
      skipped candidates counted (32, Adult random forest only), SHAP-LIME between the new
      runs, LIME at the default kernel width, a permutation reference for each pair;
    - LIME configuration disclosed: kernel width 3 against the package default, kernel
      weights (median 0.26 / 2.3 / 83.6), range of the stored LIME stability;
    - text fixes, captions, README and plan updated; Table 1 and Table 2 extended.
  - **Author decisions:** no technical reason for the kernel width of 3 (stated in the
    manuscript); default-width rerun accepted; title shortened to "Do Explainers Agree on
    Which Features Matter? Instance-Level Agreement between SHAP and LIME"; Zenodo release
    and merges approved; no action on the public repository and archive.
  - **Zenodo version 0.8.0: `10.5281/zenodo.23142429`**, from GitHub release
    `paper-e-cys-2026-10-04-r2` (tag on `main` `8bed86320`); cited in the full PDF.
  - **Paper E SUBMITTED by the author on 2026-10-04** to *Computación y Sistemas*,
    **submission 6783** (https://cys.cic.ipn.mx/index.php/CyS/author/submission/6783):
    the blind PDF, a note to the editor, no supplementary file.
  - Pull requests #12 (review and revision), #13 (Zenodo 0.8.0) and #14 (submission
    record and this handoff) merged to `main`.
- **Current State**
  - Paper E is under review. `docs/reports/paper_e/submission/paper_e_blind.pdf` (local
    only, 15 pages) is the file sent; its source is `main` at `193f1660e`.
  - Last verification (after the final build): `verify_claims.py` 986 claims / 1220 sites;
    `verify_sync.py`; `scan_shared_literals.py --strict` 0 unexplained;
    `verify_exp4_reconstruction.py` 18 pins; 24 lane and Paper E tests; CI passed on the
    pull requests.
  - The main folder is on `paper/e-feature-agreement`, level with `main`, clean. No lane
    lock is held.
- **Next Steps**
  1. Start with `python scripts/pubs/check_lane.py claim --owner <session name>`; stop if
     it fails.
  2. Paper E: wait for the journal. When the decision arrives, record it in the Paper E
     README and plan the response to the referees.
  3. Return the main folder to `thesis/rca-001-phase-2` (`git switch`, then
     `git merge main`); the other lanes take `main`.
  4. Unchanged: Paper D acknowledgement; Paper B+C submission to *Inteligencia
     Artificial*; Task 3 / RCA-001 Phase 2 on the thesis lane; `git worktree remove
     ../xai-paper-e` if the folder still exists.
- **Blockers/Issues**
  - Earlier Paper E drafts remain publicly reachable (repository history, GitHub
    releases, Zenodo 0.6.0 to 0.8.0). The journal's guidelines ask that a submission is not
    available online; the note to the editor states it. The editor may raise it.
  - The paper is at the 15-page limit set by the author: any addition in a revision needs
    an equal cut.
  - The text after the second revision was read by the author and not reviewed a third
    time.
  - Known and disclosed: the Adult random-forest binary reproduces 75% to 81% of the
    predictions recorded in the runs.
- **Notes**
  - Do not rebuild `submission/` or change the Paper E analysis unless a revision is
    requested. A revision that changes code or results needs a new Zenodo version and new
    values for the two macros in `paper_e_layout.tex`.
  - `paper_e_ceiling.py` needs the EXP3 binaries: `python scripts/train_exp3_models.py
    --model-root <dir> --data-cache-dir data` (about one minute), then
    `--exp3-model-root <dir>`; `--summarise-only` recomputes its CSV files from
    `ceiling_lists.json`. Run the Paper E scripts with the project `.venv`, which has
    SciPy, scikit-learn, shap and lime; the system Python does not.
  - A shell heredoc loses backslashes and can fail on quotes: write patch scripts to a
    file, or use the editor tool for LaTeX.
  - The build prints the line range of an overfull box in `paper_e.tex`.
  - Release route that worked: tag `origin/main`, push the tag, `gh release create
    <tag> --verify-tag`; Zenodo archived it in about one minute.
  - A session that ends without `check_lane.py release` leaves the lane locked for the
    next one.

## Session update - 2026-10-04 (Paper E SUBMITTED to Computación y Sistemas, ID 6783)

This entry is the latest.

- **Paper E was submitted by the author on 2026-10-04** through the journal's online
  system; the journal acknowledged it by email as **submission 6783**
  (https://cys.cic.ipn.mx/index.php/CyS/author/submission/6783).
- File sent: `docs/reports/paper_e/submission/paper_e_blind.pdf` (15 pages, source at
  `main` `193f1660e`), with a note to the editor and no supplementary file. Record in
  `docs/reports/paper_e/README.md`, "Submission record".
- Venue requirements re-read on the journal site the same day: Artificial Intelligence is
  in scope, publication has no cost for authors, three referees, blind review, authors
  transfer copyright on publication.
- The author decided to take no action on the public repository and archive; the note to
  the editor states that earlier drafts are reachable there.
- **Do not rebuild `submission/` or change the Paper E analysis unless a revision is
  requested.** A revision that changes code or results needs a new Zenodo version.
- **Next:** wait for the journal's decision. Then return the main folder to
  `thesis/rca-001-phase-2`; the other lanes take `main`. Unchanged: Paper D
  acknowledgement, Paper B+C submission, Task 3 / RCA-001 Phase 2.

## Session update - 2026-10-04 (Paper E: title, Zenodo 0.8.0, merged to main)

This entry is the latest. It closes Next Steps 1 and 2 and the merge in step 3 of the
handoff directly below.

- **Author decisions:** the blind PDF was read; the title is now "Do Explainers Agree on
  Which Features Matter? Instance-Level Agreement between SHAP and LIME" ("on Three
  Tabular Datasets" removed). The author approved the Zenodo release and the merge.
- **`main`:** pull request #12 merged (`8bed86320`); it holds the second review, the
  revision and the new title.
- **Zenodo version 0.8.0: `10.5281/zenodo.23142429`**, from GitHub release
  `paper-e-cys-2026-10-04-r2` (tag on `8bed86320`). The full PDF cites it
  (`paper_e_layout.tex`).
- **Verified after the last build:** both PDFs 15 pages; `verify_claims.py` 986 claims /
  1220 sites; `verify_sync.py`; CI (fragments, lanes, exp4-reconstruction) passed on the
  pull request.
- **Next, author:** register at the journal site and submit
  `docs/reports/paper_e/submission/paper_e_blind.pdf`; in the cover letter say that
  earlier drafts were in a public repository and in Zenodo 0.6.0, and name the two
  companion manuscripts. Record the submission in the Paper E README.
- **Still open, unchanged:** return the main folder to `thesis/rca-001-phase-2` when
  Paper E work ends; the other lanes take `main`; Paper D acknowledgement; Paper B+C
  submission; Task 3 / RCA-001 Phase 2.

## Session Handoff - 2026-10-04 (Paper E revised after the second rigor review)

This is the latest handoff. It closes the "second rigor review" entry directly below.

- **Completed**
  - Author's answers to the second review: no technical reason for the LIME kernel width
    of 3; the run log of the self-agreement experiment is not available; the default-width
    LIME rerun is accepted; the author asked for a recommendation on the title (kept, with
    the permutation reference in the abstract).
  - All findings of `docs/review/scientific-rigor-review_paper_e_2026-10-04_r2.md` are
    addressed; the response to each is in `docs/reports/paper_e/README.md`, "Response to
    the second rigor review".
  - New post hoc analyses, dated in `ANALYSIS_PLAN.md` section 9 before they were run:
    - permutation reference (`paper_e_review2_analyses.py`): SHAP of an instance against
      LIME of another instance of the same run overlaps by 0.203 / 0.287 / 0.648; the
      instance-specific part is 0.191 / 0.100 / 0.066 (Adult / German Credit / Breast
      Cancer), positive in all 86 runs;
    - kernel weights: the 999 perturbed samples of a LIME explanation receive a median
      total weight of 0.26 / 2.3 / 83.6, against 1 for the instance;
    - range of the stored LIME stability: model medians 0.001 to 0.009 on Adult (a dated
      deviation from plan section 4);
    - self-agreement experiment rerun in full (`paper_e_ceiling.py`): top-10 lists saved,
      skipped candidates counted (32 for the Adult random forest, none elsewhere),
      SHAP-LIME between the new runs (Adult 0.383, stored 0.393), LIME at the default
      kernel width (shares 0.370 of its top-5 with LIME at width 3 on Adult; less specific
      to the instance: 0.589 between different instances, against 0.195). Every earlier
      estimate was reproduced exactly.
  - Manuscript: Table 1 has the permutation column, Table 2 the new-run SHAP-LIME values
    and the permutation reference of each pair; abstract, methods, results, discussion,
    limitations and conclusions revised; captions say "spread of the seed means".
- **Current State**
  - Both PDFs have 15 pages, the limit; there is no room left. `verify_claims.py`: 986
    claims / 1220 sites, pass. `verify_sync.py`, `scan_shared_literals.py --strict`,
    `verify_exp4_reconstruction.py` and the 24 lane and Paper E tests pass.
  - The revised text has not been reviewed a third time.
  - **Zenodo 0.7.0 does not contain the new analysis code and result files.** The full PDF
    still cites 0.7.0.
- **Next Steps**
  1. Author: read `docs/reports/paper_e/submission/paper_e_blind.pdf` (local only).
  2. Author approves a new GitHub release; then set `\papererelease` and `\paperearchive`
     in `paper_e_layout.tex` and rebuild. The assistant did not publish a release.
  3. Author: merge this branch to `main` (pull request), register at the journal and
     submit; cover letter as noted in the Paper E README.
- **Blockers/Issues**
  - Page limit: any further addition needs an equal cut.
  - `paper_e_ceiling.py` needs the EXP3 model binaries, regenerated with
    `scripts/train_exp3_models.py --model-root <dir> --data-cache-dir data` (about one
    minute); the whole experiment runs in about three minutes without the SVM.
- **Notes**
  - A bash heredoc that contains Python source with quotes can fail to parse in this
    shell; write patch scripts to a file.
  - The build now prints where an overfull box is (line range in `paper_e.tex`).
  - A held-out column did not fit Table 4 (single column); the values are in the text.

## Session Handoff - 2026-10-04 (Paper E, second rigor review)

This is the latest handoff. It follows the Paper E entry of the same day below.

- **Completed**
  - Second rigor review of the revised Paper E manuscript by the Scientific Advisor role,
    read-only: `docs/review/scientific-rigor-review_paper_e_2026-10-04_r2.md`. Grade: major
    revision, mean 3.6; 2 major, 6 minor findings, 2 suggestions. Of the 13 findings of the
    first review, 10 are fixed and 3 partly fixed.
  - Every manuscript number that was recomputed matches. `verify_claims.py`: 917 claims /
    1136 sites, pass.
- **Current State**
  - No manuscript, registry or result file was changed. Paper E is not ready to submit.
  - **F01 (major):** pairing the SHAP list of one instance with the LIME list of another
    instance of the same run gives a top-5 overlap of 0.202 / 0.286 / 0.652 (Adult / German
    Credit / Breast Cancer) against 0.393 / 0.387 / 0.714 for the same instance. Most of
    the Breast Cancer agreement is a global ranking; the chance reference is too low and
    the dataset conclusion does not hold as written.
  - **F02 (major):** LIME ran with kernel width 3 (package default 0.75·√p: 7.8 / 5.9 /
    4.1). On Adult the 999 perturbed samples have a total kernel weight of about 0.26
    against 1 for the instance; the stored LIME stability on Adult has median 0.001 to
    0.009. The manuscript reports neither.
  - Minor: the random-forest row of Table 2 mixes the present binary with stored
    explanations of another forest (the binary reproduces 0.75 to 0.81 of the stored
    predictions); one sentence of the stability paragraph reports the fidelity column;
    README and plan still carry statements the manuscript withdrew.
- **Next Steps**
  1. Author: read the review and answer its four questions (kernel width; title and
     framing; run log of the self-agreement experiment; default-width sensitivity run).
  2. Scientific Editor: add the permutation reference as a dated deviation in
     `ANALYSIS_PLAN.md`, then the text changes of F01 to F08. New result files need a new
     Zenodo version before submission.
  3. Unchanged from the entry below: journal registration and submission, cover letter.
- **Blockers/Issues**
  - The self-agreement script stores measures, not the top-10 lists, so the permutation
    reference cannot be computed for Table 2 without a rerun.
- **Notes**
  - The project `.venv` loads SciPy, scikit-learn, shap and lime again; the system Python
    does not have them.
  - The first claim of this session failed: the lane was locked by `claude-paper-e`. The
    claim succeeded after the author said to try again. Release the lock at the end of
    every session.

## Session Handoff - 2026-10-04 (session end: Paper E revised, archived, on main; with the author)

This is the latest handoff and the full state at the end of the session of 2026-10-03/04.
It supersedes the two Paper E entries of 2026-10-03 below.

- **Completed**
  - **Method description checked against the code.** Three corrections: the stored
    "fidelity" is a masking correlation (`FaithfulnessMetric`), not a surrogate R2;
    TreeSHAP ran on the probability scale; the Adult models were trained once on the
    seed-42 partition, so about 71% of the explained instances of the other four seeds are
    training rows.
  - **Independent rigor review** by the Scientific Advisor role (separate agent, read-only):
    `docs/review/scientific-rigor-review_paper_e_2026-10-04.md`, grade major revision, 4
    major and 9 minor findings. All addressed the same day; the response to each is in
    `docs/reports/paper_e/README.md`.
  - **New post hoc analyses** (all dated in `ANALYSIS_PLAN.md` section 9), outputs in
    `outputs/analysis/paper_e/posthoc/`:
    - direct sign test (`paper_e_sign_contribution.py`): after LIME slopes are converted
      into contributions, sign agreement is 0.945 / 0.960 / 0.990;
    - majority-sign baseline (`paper_e_review_analyses.py`): a fixed direction per feature
      reaches the same level (0.951 / 0.978 / 0.990), so the paper claims a shared global
      direction per feature, not instance-level agreement;
    - self-agreement (`paper_e_ceiling.py`, 760 instances): LIME vs LIME 0.690 / 0.642 /
      0.836, SHAP vs SHAP 0.782 / 0.708 / 0.939, against SHAP vs LIME 0.393 / 0.382 /
      0.724 on the same subsample. The SVM was left out (KernelSHAP: 23 minutes for six
      instances);
    - correctness contrast on held-out Adult rows: MLP -0.042, RF +0.049, same sign in all
      five seeds;
    - rank sensitivity (re-ranking by contribution; Kendall on shared features) and
      pairing coverage (SVM 29.5%).
  - **Author decisions (2026-10-04):** clickable blue links (`hyperref`); journal footer
    with received/accepted placeholders; Krishna et al. linked to arXiv; DOIs for Han et
    al., the RIMI article and the PMLR page for Garreau; Bhatt et al. (2020) approved (25
    references); **the manuscript PDFs are local only** (`submission/*.pdf` git-ignored);
    Paper B+C named as a second companion manuscript.
  - Claim registry: Paper E block regenerated by every build; six table files and
    `paper_e.tex` under coverage and exclusivity.
  - Earlier in the session (2026-10-03, detail in the entries below): Paper E moved to the
    main folder (ADR-0021 amended, `lanes.toml`); venue *Computación y Sistemas* and its
    LaTeX class; first draft; `paper_e` resolver in `scripts/pubs/claim_sources.py`; single
    author, no AI-use declaration, at most 15 pages.
  - Medians of the run means for the primary measure added to Section 4.1 (one sentence).
  - Pull requests #5 to #9 merged into `main`, CI green on #6 to #9. Zenodo 0.6.0 and
    0.7.0 published.
- **Current State**
  - Manuscript: 14 pages (limit 15, enforced by the build), 6 tables, 4 figures, 25
    references. `verify_claims.py`: 917 claims / 1136 sites / 27 files fully registered /
    21 files clear of unpublished results. `verify_sync.py`, `scan_shared_literals.py
    --strict` and the 17 lane and Paper E tests pass.
  - The revised text has not been reviewed a second time; the author does the scientific
    read next.
  - Main folder on `paper/e-feature-agreement`, clean, level with `main` and origin. The
    two PDFs exist only on this machine, in `docs/reports/paper_e/submission/` (ignored by
    git; a branch switch does not remove them; `build_paper_e.py` regenerates them).
  - The lane lock held by `claude-paper-e` was released at the end of the session.
  - Zenodo: **version 0.7.0, `10.5281/zenodo.23139911`**, from release
    `paper-e-cys-2026-10-04` (commit `3923d1b68`); the full PDF cites it. Pull request #8
    merged; `main` holds the revision and no manuscript PDF. Version 0.6.0 (`10.5281/zenodo.23130949`) predates the revision and contains
    the earlier PDFs; it cannot be withdrawn.
- **Next Steps**
  0. Start with `python scripts/pubs/check_lane.py claim --owner <session name>`; stop if
     it fails.
  1. Author: scientific read of `docs/reports/paper_e/submission/paper_e_blind.pdf`. Apply
     the author's edits in `paper_e_template.tex` only, then rebuild. A change to the
     analysis needs a new Zenodo version; a text change does not.
  2. Author: register at the journal site and submit; say in the cover letter that earlier
     drafts were in a public repository and name the two companion manuscripts. Record the
     submission in the Paper E README.
  3. Optional: run the SVM in the self-agreement experiment (about two hours); a second
     rigor review of the revised text.
  4. Unchanged: confirm the removed side folders and run `git worktree prune` (see
     Blockers); return the main folder to
     `thesis/rca-001-phase-2` when Paper E work ends; the other lanes take `main`; Paper D
     acknowledgement; Paper B+C submission; Task 3 / RCA-001 Phase 2.
- **Blockers/Issues**
  - **Found at session end, not done by this session:** the folders `../xai-paper-e`,
    `../xai-paper-f` and `../xai-chapter`, and the bundle file
    `../xai-eval-framework-backup-2026-10-03.bundle`, are no longer on disk. Git still
    lists the three as working trees ("prunable"). Their branches exist locally and on
    origin (`paper/f-external-validity` at `f2f04cc44`; `chapter/cifie-sync-2026-09`
    locally at `0740d93ed`, one commit behind origin `4575e22b1`), so committed work is
    intact; any uncommitted file in those folders is lost. The author confirms whether the
    removal was intended, then runs `git worktree prune`. Only `../xai-exp4` remains
    beside the main folder.
  - The Adult random-forest binary does not reproduce the stored runs exactly (known); in
    the self-agreement experiment a new SHAP run agrees less with the stored one (0.640)
    than with another new run (0.887). Disclosed in the plan.
  - `paper_e_ceiling.py` and `paper_e_sign_contribution.py` need scikit-learn, shap, lime,
    the datasets under `data/` and the model binaries; the EXP3 binaries must be
    regenerated with `scripts/train_exp3_models.py`.
- **Notes**
  - Paper E commands, from the main folder:
    `python docs/reports/paper_e/scripts/build_paper_e.py` (figures, tables, `paper_e.tex`,
    registry block, both PDFs; stops above 15 pages or on an undefined citation), then
    `python scripts/pubs/verify_claims.py`. The post hoc scripts
    (`paper_e_posthoc.py`, `paper_e_sign_contribution.py`, `paper_e_review_analyses.py`,
    `paper_e_ceiling.py`) are run only when the runs or the analysis change.
  - Commit order the hook requires: the registry block and other shared files
    (`pub/`, `.gitignore`, `.zenodo.json`, `CITATION.cff`, `docs/review/`), then the Paper
    E files, then `ACTIVE_CONTEXT.md`, each in its own commit; `main` only through a pull
    request (`gh pr create`, `gh pr merge --merge` worked in this session).
  - Zenodo archives a GitHub release within a few minutes; the DOI goes in
    `paper_e_layout.tex` (the `\paperearchive` macro) and the Paper E README.
  - A `%` comment inside a BibTeX entry silently drops the entry; keep comments outside.
  - `cys.bst` prints a DOI as `\url{10...}`; the template redefines `\url` inside the
    reference list and full addresses in the `.bib` file use `\fullurl`.
  - With three seeds, a percentile bootstrap over seeds returns the smallest and largest
    seed mean. Describe such intervals as the spread of seed means.
  - Shell heredocs passed to Python lose backslashes in LaTeX strings; write the edit
    script to a file, or use the Edit tool.

## Session update - 2026-10-03 (Paper E registered, archived, on main)

This entry is the latest and supersedes the open items of the Paper E handoff below.

- **Author decisions:** single author (the director declined); the 24 references
  approved; no AI-use declaration; **at most 15 pages** (the draft has 11; the build
  stops above 15).
- **Claim registry:** Paper E is under `[coverage]` and `[exclusivity]`. New `paper_e`
  resolver in `scripts/pubs/claim_sources.py`; the Paper E build writes a generated block
  of 280 claims. `verify_claims.py`: 759 claims / 971 sites / 26 files fully registered /
  20 files clear of unpublished results.
- **`main`:** pull requests #5 (Paper D record) and #6 (Paper E) are merged; CI passed.
- **Zenodo version 0.6.0: `10.5281/zenodo.23130949`**, from GitHub release
  `paper-e-cys-2026-10-03` (commit `fe3604406`). The full PDF cites it.
- **Next:** the author reads the draft, registers at the journal site and submits
  `docs/reports/paper_e/submission/paper_e_blind.pdf`; record the submission in the
  Paper E README. Still open: `git worktree remove ../xai-paper-e`; return the main
  folder to `thesis/rca-001-phase-2` when Paper E work ends; the other lanes take `main`.

## Session Handoff - 2026-10-03 (Paper E first draft for Computación y Sistemas)

This is the latest handoff. The Paper D submission handoff of the same day follows it.

- **Completed**
  - **Paper E is worked in the main folder**, `docs/reports/paper_e/`, on branch
    `paper/e-feature-agreement` (author decision; ADR-0021 amended, `lanes.toml` and its
    test updated). The session had first followed the registry and worked in
    `../xai-paper-e`; the author corrected this and the files were moved here the same
    session. `../xai-paper-e` holds nothing (detached at `f2f04cc44`).
  - Venue chosen by the author: *Computación y Sistemas* (CIC-IPN), in English. The
    journal's LaTeX template (`cys.cls`, `cys.bst`) and Word template are in the Paper E
    folder.
  - First full draft: `paper_e_template.tex` (source), generated `paper_e.tex`, five
    generated tables, four figures (PDF), 24 references checked against Crossref/arXiv,
    and `submission/paper_e_blind.pdf` and `paper_e_full.pdf` (11 pages each).
  - Post hoc finding, recorded in `ANALYSIS_PLAN.md` section 9: the prespecified sign
    agreement follows the predicted class (Breast Cancer 0.977 for class 0, 0.036 for
    class 1), because LIME was run without discretisation and stores slopes while SHAP
    stores contributions. Script `docs/reports/paper_e/scripts/paper_e_posthoc.py`,
    outputs in `outputs/analysis/paper_e/posthoc/`.
- **Current State**
  - Main folder on `paper/e-feature-agreement`, pushed. Verified after the build:
    `verify_claims.py` (479 claims / 645 sites), `verify_sync.py`,
    `scan_shared_literals.py --strict` (0 unexplained), 17 lane and Paper E tests.
  - Every number in the Paper E manuscript is generated from the CSV files by
    `scripts/build_paper_e.py`; the build fails on an unresolved placeholder. Paper E is
    **not** yet in `pub/claim_registry.toml`.
  - Pull request #5 (Paper D submission record and its handoff) is still open; `main`
    and this branch do not have those three commits.
- **Next Steps**
  1. Author: read the Paper E draft; decide authorship, the references and the AI-use
     declaration (open items in `docs/reports/paper_e/README.md`).
  2. Author: merge pull request #5; then this branch takes `main`.
  3. Register Paper E in `[coverage]` and `[exclusivity]` of the claim registry (shared
     commit through `main`), then tag a release and archive it on Zenodo before
     submission.
  4. Author: `git worktree remove ../xai-paper-e`.
  5. Unchanged: Paper D acknowledgement, Paper B+C submission, Task 3 / RCA-001 Phase 2,
     the chapter lane sync, the backup branches.
- **Blockers/Issues**
  - The Paper A reference (RIMI) has no volume in the bibliography record; the journal
    style prints an empty field.
  - CyS states no page limit and no fee on its guidelines page; confirm on the site.
- **Notes**
  - **A paper the author asks to work on is worked in the main folder** unless the author
    names another folder. If `lanes.toml` disagrees, change it first.
  - In a LaTeX tabular, a rule placed after an input command fails; each generated table
    file carries its own closing rule.
  - Tectonic is XeTeX: `cys.cls` loads `helvet`, which has no effect there, so the
    template sets TeX Gyre Heros through `fontspec`.
## Session Handoff - 2026-10-03 (Paper D submitted; lane guard; Zenodo 0.5.0)

It closes the three "Session update - 2026-10-03" entries
directly below it (Paper D reproducibility; Paper D in the main folder; ADR-0021), which
give the detail.

- **Completed**
  - **Paper D was submitted** by the author on 2026-10-03, by email to
    revistatm@tec.ac.cr (*Tecnología en Marcha*, special issue on Artificial
    Intelligence): the blind and full Word files and three TIFF figures.
  - Paper D moved to the main folder, `docs/reports/paper_d/`, on branch
    `paper/d-tecnologia-en-marcha` (author decision; ADR-0021 amended). The folder
    `../xai-paper-d` and the branch `paper-d/tecnologia-en-marcha` are gone.
  - Lane guard built: `scripts/pubs/check_lane.py`, `scripts/pubs/lanes.toml`,
    `.githooks/pre-commit`, CI job `lanes` in `pubs-sync.yml`, 9 tests in
    `tests/pubs/test_check_lane.py`, and a rule in `.aceconfig`.
  - Paper D reproducibility: clean-clone test passed; `requirements.txt` and a
    "Reproduce the results" section added to the Paper D README; the data availability
    statement rewritten in both versions.
  - Zenodo version 0.5.0 published as `10.5281/zenodo.23130014` from GitHub release
    `paper-d-submission-2026-10-03`; the paper cites it.
  - Author items closed: profession ("PhD candidate"), the three added references
    approved, the Spanish text (reviewed in an earlier session), the Word files checked.
  - `main` synced twice: a fast-forward approved by the author, then pull request #4
    (merge commit `f2f04cc44`). CI passed on both.
- **Current State**
  - The main folder is on `paper/d-tecnologia-en-marcha`, clean. The branch is three
    commits ahead of `main`: `f8e88a6d7` (Spanish and Word check closed), `f093779c7`
    (README submission record) and this handoff. They are pushed to the branch and
    waiting in an open pull request to `main`.
  - `main`, thesis, EXP4 cohort 2, Paper E and Paper F are level at `f2f04cc44`, locally
    and on origin. The chapter lane is not: origin has `4575e22b1`, which the local
    `../xai-chapter` folder has not pulled, and it has not taken `main`.
  - The files sent to the journal are `docs/reports/paper_d/submission/` at commit
    `f8e88a6d7`.
  - Verified after the last build: `verify_claims.py` (479 claims / 645 sites / 48
    retired-value guards), `verify_sync.py`, the strict Paper D shared-literal scan
    (0 unexplained). `verify_exp4_reconstruction.py` (18 pins) passed earlier in the
    session and in CI.
  - The lane lock held by `claude-paper-d` was released at the end of the session.
- **Next Steps**
  1. Author: merge the open pull request from `paper/d-tecnologia-en-marcha` to `main`.
     Then, in the main folder: `git switch thesis/rca-001-phase-2`, `git merge main`.
  2. Start every session with
     `python scripts/pubs/check_lane.py claim --owner <session name>`; stop if it fails.
     Add this line to the session start prompt.
  3. Chapter lane, in `../xai-chapter`: `git pull`, then `git merge main`, before any
     edit. The lane guard refuses the claim until this is done.
  4. Paper D: wait for the journal's acknowledgement and record it in the Paper D
     README. Do not rebuild `submission/` unless a revision is requested.
  5. Paper B+C: the author submits to *Inteligencia Artificial*; record the ID here.
  6. Resume Task 3 / RCA-001 Phase 2 on the thesis lane: coverage sweep starting with
     `thesis/apendices.qmd`, then macro generation and the CI build job.
  7. Paper E: the author reviews the exploratory results and chooses a venue.
  8. Author, when satisfied: delete the ten `backup/2026-10-03/*` branches on origin and
     the bundle file `xai-eval-framework-backup-2026-10-03.bundle` beside the main folder.
- **Blockers/Issues**
  - RF provenance, unchanged: `rf.joblib` reproduces only 75-82% of the predictions
    recorded by the Jan-Feb 2026 random-forest runs. Paper D discloses it and restricts
    RQ4 to reproducible runs; Papers A and B+C still need the RCA entry.
  - The project `.venv` cannot load SciPy. The Paper D analysis runs in a separate
    environment built from `docs/reports/paper_d/requirements.txt`.
  - The assistant cannot push to `main` or delete branches without the author's
    approval in the session; a pull request that the author approves works.
  - The journal's general instructions page names its website as the submission route
    and asks for telephone numbers. The author followed the special-issue instructions
    (email). If the journal asks for a resubmission through the website, an account is
    requested from revistatm@itcr.ac.cr.
  - Lane guard limits: a session that never runs `claim` can still edit files; the hook
    is local and `--no-verify` bypasses it; CI sees only what reaches `main`.
- **Notes**
  - A change to Paper D's analysis code or results needs a new Zenodo version and new
    values for the `paperdrelease` and `paperdarchive` macros in `paper_d_template.tex`.
    A text change alone does not.
  - Zenodo archives a GitHub release by itself within a few minutes (integration is on).
    Check with
    `https://zenodo.org/api/records?q=conceptrecid:19297723&all_versions=true&sort=mostrecent`.
  - A fresh clone on Windows needs `git config core.longpaths true` or the checkout is
    incomplete.
  - Commit a lane's own paths and shared paths separately; the hook refuses a mixed
    commit. `ACTIVE_CONTEXT.md` goes in a commit of its own.
  - The main folder hosts the thesis, Paper B+C and Paper D lanes, one at a time. Switch
    branch only with a clean tree.

## Session update - 2026-10-03 (Paper D reproducibility and archive)

- **Data availability statement rewritten** in `paper_d_template.tex` (full and blind
  versions). It names the public datasets, what the repository holds, the release and
  its archive, and points to the regeneration instructions.
- **Zenodo version 0.5.0 published: `10.5281/zenodo.23130014`**, from GitHub release
  `paper-d-submission-2026-10-03` (commit `021d85ead`, on the Paper D branch, not yet on
  `main`). 917 MB, open access, MIT. The paper cites it. Record kept in
  `docs/reports/paper_d/README.md`, "Release and archive".
- **Clean-clone test passed.** In a fresh clone and a fresh Python 3.13 environment,
  `paper_d_analysis.py` regenerated all 13 result files: 159 of 11,976 cells differ, by
  at most 8e-11 relative; `paper_d.tex` and the registry block came out unchanged and
  `verify_claims.py` passed. Two gaps found and fixed in the instructions: `certifi` was
  missing from the documented packages (now `docs/reports/paper_d/requirements.txt`),
  and a Windows clone needs `core.longpaths true`.
- **Length:** the full PDF went from 11 to 12 pages; the blind PDF, which is the file
  sent for review, stays at 11. The author checks the Word page count when re-saving.
- Verified after the final build: `verify_claims.py` (479 claims / 645 sites),
  `verify_sync.py`, the strict Paper D shared-literal scan (0 unexplained).
- **Still open, author:** push this branch to `main`
  (`git push origin paper/d-tecnologia-en-marcha:main`), delete the old branch
  `paper-d/tecnologia-en-marcha`, and the Paper D items before 2026-10-13 (profession
  placeholder, Spanish read, three `NEW` references, re-save the .docx in Word, send).
- The main folder is still on `paper/d-tecnologia-en-marcha`, claimed by
  `claude-paper-d` in the lane guard.

## Session update - 2026-10-03 (Paper D in the main folder; lane guard)

This entry supersedes the Paper D row of the table in the ADR-0021 entry below.

- **Paper D is worked in the main folder**, at `docs/reports/paper_d/`, on branch
  `paper/d-tecnologia-en-marcha` (author decision; ADR-0021 amended). The folder
  `../xai-paper-d` was removed after a file comparison showed no difference from the
  main folder. The old branch `paper-d/tecnologia-en-marcha` is fully contained in
  `main`; the author still has to delete it locally and on origin.
- **The main folder hosts three lanes, one at a time:** thesis, Paper B+C and Paper D.
  It is on `paper/d-tecnologia-en-marcha` now. Return it to `thesis/rca-001-phase-2`
  when the Paper D session ends.
- **Lane guard added** (`scripts/pubs/check_lane.py`, `scripts/pubs/lanes.toml`,
  `.githooks/pre-commit`, CI job `lanes`). Before this, the ADR-0021 rules had no
  mechanism behind them. Now:
  - every session starts with `python scripts/pubs/check_lane.py claim --owner <name>`
    and ends with `release --owner <name>`; a claim fails if another session holds
    the folder, the branch is not a lane, the folder is wrong, or `main` was not taken;
  - the pre-commit hook refuses a commit with no live lock, a commit touching another
    lane's paths, and a commit mixing lane paths with shared paths;
  - CI repeats the path rules for commits reaching `main`.
  The hook needs `git config core.hooksPath .githooks`, which is set for this
  repository and all its folders; a folder gets the hook file when it takes `main`.
- **Limits:** a session that never runs `claim` is not stopped from editing files, only
  from committing when no lock is live. `--no-verify` bypasses the hook and must not be
  used. Add the claim step to the session start prompt.
- **Not done: `main` is not synced.** The assistant's push to `main` was refused by the
  permission system. `main` is three shared commits behind this branch; the author runs
  `git push origin paper/d-tecnologia-en-marcha:main`, then every lane takes `main`.
- Verified: the 9 guard tests pass; five refusals were reproduced by hand (no lock,
  second claim, another lane's path, mixed commit, wrong owner); `verify_claims.py`
  (479 claims / 645 sites) and `verify_sync.py` pass.

## Session update - 2026-10-03 (one working tree per paper, ADR-0021)

At the author's direction, each paper in progress now has its own folder and branch
(`docs/adr/0021-one-working-tree-per-paper.md`). This supersedes two lines in the
handoff below: `../xai-paper-f` is the Paper F lane, not a leftover, and Next Steps
item 1 (remove it) no longer applies.

| Paper | Folder | Branch |
|---|---|---|
| Thesis | `xai-eval-framework` | `thesis/rca-001-phase-2` |
| CIFIE chapter | `../xai-chapter` | `chapter/cifie-sync-2026-09` |
| EXP4 cohort 2 | `../xai-exp4` | `results/exp4-cohort2` |
| Paper D | `../xai-paper-d` | `paper-d/tecnologia-en-marcha` |
| Paper E | `../xai-paper-e` | `paper/e-feature-agreement` |
| Paper F | `../xai-paper-f` | `paper/f-external-validity` |

- All six branches and `main` were at the same commit when the folders were created.
  The three paper folders are seeded with `.ace/`; `../xai-paper-d` also has the
  Tectonic compiler.
- Rules (ADR-0021): a lane edits only its own paths; a shared change is its own
  commit and goes through `main` in the same session; finished paper work is merged
  into `main` and the main folder updated the same session; lanes never merge into
  each other; one agent session per folder.
- Paper B+C stays in the main folder on short-lived `paper/bc-<topic>` branches
  (ADR-0019).
- Still to delete, by the author: the ten `backup/2026-10-03/*` branches on origin
  and the bundle file `..\xai-eval-framework-backup-2026-10-03.bundle`.

## Session Handoff - 2026-10-03 (repository consolidation and cleanup)

This is the latest handoff. The "Session update - 2026-10-03 (repository
consolidation)" entry just below gives the detail of the `main` rebuild.

- **Completed**
  - Loaded the project rules, roles, context and regression guards, and found two
    mismatches: Paper E work committed with no context entry, and an uncommitted
    `docs/reports/paper_d/paper_d.tex` (line endings only; restored by the author).
  - Backed up every local branch tip to origin as `backup/2026-10-03/*` (ten refs)
    and wrote a full bundle to
    `C:\Users\jonna\Github\xai-eval-framework-backup-2026-10-03.bundle` (575 MB).
  - Rebuilt `main` from `origin/main` without the merge-and-revert pair. It now holds
    the Paper E tooling, results and handoff; Paper D; three chapter commits; and
    the Paper F documents. Pushed as `72f70a83b`.
  - Saved three untracked Paper F documents (`docs/reports/paper_f/`) that existed
    only on disk; they are on `main`.
  - Archived the first Paper E branch as tag
    `archive/paper-e-feature-agreement-2026-10-03` after confirming it holds no file
    that `main` lacks.
  - Fast-forwarded the thesis, chapter, exp4 and Paper D lanes to `main` and pushed
    them. Put the main folder back on `thesis/rca-001-phase-2`.
  - Removed four redundant working trees, five local branches and two branches on
    origin (`paper/e-feature-agreement`, `paper/f-external-validity`).
- **Current State**
  - `main`, `thesis/rca-001-phase-2`, `chapter/cifie-sync-2026-09`,
    `results/exp4-cohort2` and `paper-d/tecnologia-en-marcha` held the same commit,
    locally and on origin, when this entry was written. The main folder had no
    uncommitted files and no stashes.
  - Working trees: the main folder (thesis lane), `../xai-chapter`, `../xai-exp4`,
    and a leftover `../xai-paper-f`.
  - Verified on the rebuilt `main`: `verify_claims.py` (479 claims / 645 sites / 48
    retired-value guards), `verify_sync.py`, `verify_exp4_reconstruction.py`
    (18 pins), both shared-literal scans (0 unexplained) and the 16 Paper E tests.
  - Paper D: complete; its PDF and Word files are in
    `docs/reports/paper_d/submission/`, not beside `paper_d.tex`.
  - Paper E: results in `outputs/analysis/paper_e/`, no manuscript. Paper F: plan
    only. Neither is in `pub/claim_registry.toml`.
- **Next Steps**
  1. Remove the last leftover: `git worktree remove ..\xai-paper-f`, then
     `git branch -D paper/f-external-validity` (its commit is in `main`).
  2. Paper D, author items before sending about 2026-10-13 (deadline 2026-10-15):
     profession placeholder, Spanish read, the three `NEW` references, re-save the
     .docx in Word, send to revistatm@tec.ac.cr.
  3. Paper B+C: the author submits to *Inteligencia Artificial*; record the
     submission ID here.
  4. Paper E: the author reviews the exploratory results, approves the references
     and chooses a venue before any manuscript is drafted.
  5. Resume Task 3 / RCA-001 Phase 2 on the thesis lane (coverage sweep, then macro
     generation and the CI build job).
  6. When the author is satisfied, delete the `backup/2026-10-03/*` branches on
     origin, the archive tag if unwanted, and the bundle file.
- **Blockers/Issues**
  - RF provenance, unchanged: the stored `rf.joblib` reproduces only 75-82% of the
    predictions recorded by the Jan-Feb 2026 random-forest runs. It affects Papers A
    and B+C and still needs an RCA entry.
  - The project `.venv` cannot load SciPy and lacks `seaborn` and `scikit_posthocs`,
    so `tests/analysis/test_stats.py` and `test_visualization.py` fail to import.
    The Paper E tests run when their four files are named directly.
  - Paper F was started by another session; whether it goes ahead, and when, is the
    author's decision.
  - `C:\Users\jonna\Github\xai-benchmark` sits beside the working trees. It is not
    part of this repository and was not inspected.
- **Notes**
  - Run one agent session at a time on this repository. Two sessions moving the same
    branches produced the merge-and-revert on `main`.
  - A revert of a merge leaves the merged commits in history, so merging that branch
    again brings no files. Rebuild from the last good commit or revert the revert.
  - In this environment the assistant could not run: merges into or pushes of
    `main`, `git checkout --` on modified files, `git worktree remove`,
    `git branch -D`, or deletion of branches on origin. The author ran those by
    hand. Pushes of other branches, backups and tags worked.
  - `paper_d.tex` is generated by `scripts/pubs/render_paper_d.py` from
    `paper_d_template.tex`; a modified `paper_d.tex` with an empty
    `git diff --ignore-cr-at-eol` is line-ending churn, not a change.
  - The Paper E handoff further down still says "No pushes were made" and describes
    the old `main`; both are superseded by the entry below this one.

## Session update - 2026-10-03 (repository consolidation)

`main` was rebuilt from `origin/main` so that it holds every lane's work and no
merge-and-revert pair. This entry supersedes the "Branch state" paragraph of the
Paper E handoff below, the line "Paper E stays documented-only until after Paper D
is submitted", and "Lane `paper-d/tecnologia-en-marcha`, not merged to `main`" in
Session Metadata.

- **Why:** local `main` held a merge of the first Paper E branch (which also carried
  Paper D) followed by its revert. With that history, a later merge of Paper D into
  `main` would have brought no files.
- **What `main` now contains, in order:** the clean Paper E tooling
  (`paper/e-feature-agreement-clean`), the Paper E results and handoff, Paper D
  (`paper-d/tecnologia-en-marcha` plus the main-checkout record), three chapter
  commits from `chapter/cifie-sync-2026-09`, and the Paper F documents
  (`paper/f-external-validity`). Before the Paper D merge its files were identical to
  the previous local `main`.
- **Nothing was discarded.** Every branch tip from before the rebuild is on origin
  under `backup/2026-10-03/*`. The first Paper E branch is kept as tag
  `archive/paper-e-feature-agreement-2026-10-03`; a file comparison showed it holds
  no file that `main` lacks.
- **Paper F ("External validity of XAI benchmark conclusions"), initiated at the
  author's direction.** It treats the benchmark as the instrument and cross-dataset
  generalizability as the object of study: 48 conditions (4 datasets × 3 model
  families × 4 explainers). `docs/reports/paper_f/` holds `README.md` (charter and
  pipeline), `ANALYSIS_PLAN.md` (H1 dataset main effect, H2 explainer × dataset
  interaction, H3 rank generalizability, H4 quality-cost Pareto stability) and
  `METHODOLOGICAL_ANALYSIS.md`. Documents only: no dataset is fixed and no experiment
  has been run.
- **Paper status:** D is complete and awaits the author's items before 2026-10-13;
  E has results in `outputs/analysis/paper_e/` and no manuscript; F is a plan.
  None of E or F is in `pub/claim_registry.toml`.
- **Verified on this `main`:** `verify_claims.py` (479 claims / 645 sites / 48
  retired-value guards), `verify_sync.py`, `verify_exp4_reconstruction.py` (18 pins),
  `scan_shared_literals.py --strict` (0 unexplained) and its `--paper-d` mode
  (0 unexplained) pass; the 16 Paper E tests pass.
- **Working rule that failed here:** two agent sessions changed the same branches at
  the same time. Run one session at a time on this repository.

## Session update - 2026-10-03 (Paper D location correction)

The author requires Paper D in the main project checkout, alongside the other
papers: `docs/reports/paper_d/`. The Paper D branch and its publication dependencies
were integrated into the current checkout, preserving the in-progress Paper E
changes. All Paper D analysis artifacts and build scripts are present. Blind/full
PDF and Word builds, claim verification, synchronization, EXP4 pins and strict
Paper D overlap verification pass here. The extra `../xai-paper-d` worktree is
removed; its location in the earlier style-revision entry is historical.

## Session update - 2026-10-03 (Paper D impersonal style)

At the author's request, the Scientific Editor reviewed all Paper D prose and
replaced authorial first person in English and Spanish with study/analysis subjects
and impersonal constructions. Source: `paper_d_template.tex`; generated manuscript
and blind/full PDF and Word files rebuilt. Claims, numbers and citations unchanged.
Claim, sync, EXP4-pin and strict Paper D overlap checks pass. Word text confirms
the revised English and Spanish wording. Worktree: `../xai-paper-d`, branch
`paper-d/tecnologia-en-marcha`. Standing Task 3 objective remains unchanged.

## Session Metadata
- **Last Updated:** 2026-10-03
- **Mode (2026-10-03, final):** HANDOFF - **Paper D SUBMITTED** to *Tecnología en
  Marcha*; Zenodo 0.5.0 `10.5281/zenodo.23130014`; lane guard in place. **Active
  objective: Task 3 / RCA-001 Phase 2 on the thesis lane.** See "Session Handoff -
  2026-10-03 (Paper D submitted; lane guard; Zenodo 0.5.0)" at the top of this file.
- **Mode (2026-10-03, latest):** HANDOFF - **repository consolidation task COMPLETE**
  (rebuilt `main`, one working tree per paper under ADR-0021, all seven branches level
  and pushed). **Active objective: Task 3 / RCA-001 Phase 2 on the thesis lane.** See
  "Session Handoff - 2026-10-03 (repository consolidation and cleanup)" and the
  ADR-0021 session update at the top of this file.
- **Mode (2026-10-03):** HANDOFF - **Paper D task COMPLETE** (manuscript ready for the
  author's final read; Tecnología en Marcha, due 2026-10-15). Lane
  `paper-d/tecnologia-en-marcha`, not merged to `main`. **Active objective returns to
  Task 3 / RCA-001 Phase 2 on the thesis lane.** See "Session Handoff - 2026-10-03
  (Paper D first render and iteration 1)".
- **Mode (2026-10-02, later):** PUBLICATION - **Venue is now *Inteligencia
  Artificial* (IBERAMIA)**: the author cannot pay PeerJ's fee (ADR-0020). Paper
  refactored in place to `paper_bc_iberamia.tex` (double-blind, Spanish
  Resumen, Appendix A). Ready to submit. See the last Session Handoff.
- **Mode (2026-10-02):** PUBLICATION - **TMLR desk-rejected Paper B+C (12779)
  without review; the paper is retargeted to PeerJ Computer Science.** The TMLR
  artifacts are removed (kept at tag `tmlr-submission-12779`); the PeerJ edition
  (`paper_bc_peerjcs.tex` + Supplemental Article S1) is the only Paper B+C and
  is merged to `main` and this lane. **Zenodo v0.4.0 published:
  `10.5281/zenodo.23111684`**, cited in the paper. The separate paper working tree
  `xai-paper-bc` and both `paper/bc-*` branches are retired (ADR-0019): all
  Paper B+C material is in `docs/reports/paper_bc/` of the main folder. Not
  filed: the payment decision is pending. See
  "Session Handoff - 2026-10-02".
- **Mode (2026-09-30):** PUBLICATION - **Paper B+C filed with TMLR as submission
  12779** (filed version: paper lane `75b93a7f4`). Before filing: abstract names
  the "UCI Adult census-income dataset"; equations numbered with every term
  defined and sources cited (Bhatt 2020, Samek 2017 added); §8 lists bundle paths
  in the anonymous build; Step 8 gate passed (record in
  `OPENREVIEW_SUBMISSION.md`). Editor note (`EIC_ENQUIRY_prior_publication.md`)
  shortened and filled in for 12779; the author sends it by email to
  tmlr-editors@jmlr.org, never as a forum comment. Forum:
  https://openreview.net/forum?id=VkmWJZclmH (forum ID `VkmWJZclmH`). Editor
  note sent by email (author confirmed 2026-09-30). **Next Steps item 00
  (file Paper B+C) is CLOSED.** The paper lane stays open, frozen, for the
  review-response revision; filed version is tag `tmlr-submission-12779`.
- **Mode (2026-09-29):** HANDOFF - the CIFIE science-first drafting pass,
  literature enrichment, empirical-figure provenance, and formatted Word build
  were committed on `chapter/cifie-sync-2026-09` and merged to `main`. The
  active objective remains Task 3 / RCA-001 Phase 2 on the thesis lane. See
  "Session Handoff - 2026-09-29 (CIFIE drafting and Word delivery)".
- **Mode (2026-09-28, third session):** HANDOFF - the CIFIE science-first
  assessment, evidence staging, and production scaffold are complete on
  `chapter/cifie-sync-2026-09`. The active objective returns to Task 3 / RCA-001
  Phase 2 on the thesis lane. The next CIFIE unit is queued, not active. See
  "Session Handoff - 2026-09-28 (third session)".
- **Mode (2026-09-28, second session):** PUBLICATION - Paper B+C remediation Steps 1-7
  done on the paper lane: every review finding fixed except F10 (author: won't-fix), Paper B+C
  under `[coverage]`, merged to main and all lanes, CI green. **Step 8 (submission gate) is
  next and filing waits for it.** See "Session Handoff - 2026-09-28 (second session)".
- **Mode (2026-09-28):** PEER_REVIEW / PLANNING - pre-submission review of Paper B+C for TMLR.
  Rigor review, reference audit and coverage triage done; remediation plan written; F16/F17
  fixed. **Not ready to file** (6 major findings). See the 2026-09-28 Session Handoff.
- **Active Role:** Scientific Editor / Developer / Architect
- **Mode (2026-09-27):** INCIDENT - new laptop. EXP4 bytecode found lost (never
  committed); pubs-sync CI found never green. Fixed the untracked-dataset and
  build_meta causes; EXP4 job stays red pending an author decision. Paper B+C
  abstract EXP3 sentence restated. See the 2026-09-27 Session Handoff.
- **Mode (2026-09-15):** HANDOFF - submission-preparation task CLOSED. The Paper B+C
  package is complete and re-verified, and the author is now revising the manuscript
  in detail before filing. Active objective returns to Task 3 / RCA-001 Phase 2 on the
  thesis lane. **The package must be regenerated and re-reviewed after that revision;
  it must not be submitted as it stands.** See the 2026-09-15 Session Handoff.
- **Mode (2026-09-14):** PUBLICATION / INCIDENT - OpenReview account activated;
  pre-submission check of Paper B+C found and fixed two defects (RCA-003) and
  prepared the submission sheet. Not yet submitted. See the 2026-09-14 Session
  Handoff.
- **Mode (2026-09-08):** STATUS - no changes. Paper B+C is submission-ready and
  blocked on OpenReview account approval. See the 2026-09-08 Session Handoff.
- **Mode (2026-09-06):** ARCHITECTURE / PUBLICATION - adopted ADR-0013 and a second
  worktree so Paper B+C could proceed beside the thesis; swept Ch.3; took Paper B+C
  to TMLR-submittable. See the 2026-09-06 Session Handoff below.
- **Mode (2026-08-30):** PUBLICATION / EXECUTION - repository restructuring plus a thesis
  front-matter and presentation pass. Nine commits on the new branch `thesis/rca-001-phase-2`,
  pushed. **Branch hygiene first:** the working tree was found checked out on `main`, which still
  held a 2026-07-04 snapshot; all thesis work lived on `publication/cifie-xai-fom7-book-chapter`,
  a branch cut for the book chapter that had become the trunk for everything since May (78
  commits). It was merged into `main` - 12 conflicts, 10 of them CRLF-only and 2 superseded
  (`ACTIVE_CONTEXT.md`, `implementation_plan.md`, both recording the manuscript-editing skill
  rename the branch already carries) - with the tree taken wholesale from the branch so the merge
  landed byte-identical. Old branch deleted locally; **its remote ref still exists** and needs
  `git push origin --delete publication/cifie-xai-fom7-book-chapter`. Work then continued on
  `thesis/rca-001-phase-2`, cut from `main`.
  **Thesis changes, all verified in the rendered DOCX rather than by exit code:**
  (1) citations removed from all six specific objectives - an objective is a commitment, not a
  claim, and every key removed is cited elsewhere (hedstrom2023 x28 down to wachter2017 x1, so no
  bibliography orphan); (2) Dedicatoria and Agradecimientos added as front matter, one page each;
  (3) a cover page ahead of the TOC, content in `thesis/cover.txt`, inserted by
  `insert_cover_page` because Quarto metadata cannot express it (no slot above the title);
  (4) **the official title adopted** - Arquitectura Agnostica para la Interpretabilidad de
  Modelos de Inteligencia Artificial de Caja Negra - across `_quarto.yml`, `index.qmd`,
  `pub/claims.toml` (SSOT, fragments regenerated) and `README.md`, which had carried a third
  variant; (5) the duplicate title heading after the TOC dropped; (6) `lang: es` set and 20
  self-labelled crossrefs switched to `-@`, eliminating 80 English prefixes and 15 doubled
  labels of the form 'La Tabla Table 2.1'; (7) 20 leaked section slugs converted to real
  crossrefs, which exposed a dangling `sec-metricas` reference that had been invisible while it
  rendered as literal text; (8) heading numbering (1, 1.1, 1.1.1) generated by `number_headings`,
  reverting the literal chapter labels of `88933c7f6`.
  **Two of my own assumptions were overturned by evidence and are recorded as such:** the literal
  chapter labels (right only while numbering looked impractical), and my advice to drop
  `number-sections: true` - it is load-bearing, it is what makes Quarto compute the crossref
  numbers at all. No numeric result, table value or citation changed anywhere in this pass;
  `verify_claims.py` (142 claims / 225 sites), `verify_sync.py` and
  `verify_exp4_reconstruction.py` green throughout.
- **Mode:** PUBLICATION — synchronized the thesis, Paper A, and merged Paper B+C around validation-boundary wording and EXP3 status. Created `docs/reports/sync/thesis_paper_sync_matrix.md`; updated the implementation plan with sync task 6; aligned Chapter 3/6 EXP3 wording to the Paper B+C + artifact source of truth (SHAP-Anchors fidelity replication plus LIME-only extension, but no full paired SHAP-LIME cross-dataset stability test); aligned Paper A boundary language while preserving its narrower SHAP-only EXP3 claim scope; aligned Paper B+C validity-claim language and corrected the LIME extension export path.
- **Mode (2026-08-22, second pass):** PUBLICATION — full tri-document alignment + recency audit
  (Paper A, Paper B+C, thesis Ch.1-6), every shared numeric claim re-derived from committed
  artifacts. Report at `docs/review/tri-document-alignment-review_2026-08-22.md`: 12 findings
  (A01-A05 major, A06-A10 minor, A11-A12 suggestions). All EXP2 confirmatory statistics verified
  and consistent across all three documents. **A01 (headline, and it inverts the earlier sync
  assumption):** Paper A says the EXP3 Anchors cross-dataset check "could not be executed" and
  books 12 cells as a permanent `alibi`/`dice-ml` limitation, but those 12 runs completed
  2026-04-26 and sit on the unmerged `results/exp3-windows-breast-cancer` and
  `results/exp3-linux-german-credit` branches; their recomputed fidelity means (0.2648 / 0.2079 /
  0.3510 / 0.4507) match Paper B+C's `tab:exp3_fidelity` exactly, and SHAP > Anchors holds 12/12.
  Paper A, not the thesis, is the stale document on EXP3. A02: the earlier same-day Paper A edit
  fixed only one of three places and mislabels the companion as a "LIME-only" extension. A03: the
  two papers report different values for EXP3 SHAP Breast Cancer/XGB (0.6165 committed July re-run
  vs 0.607 April side-branch snapshot). A04: thesis F01 (Ch.5 vs Ch.4 numbers) still unfixed. A05:
  thesis Ch.4 per-method profile uses pre-recovery-overlay costs (SHAP 24,804 ms vs artifact
  11,708 ms; LIME 226 vs 3,660.7; DiCE 2,056 vs 28,208.8). A08: thesis never received the Paper B+C
  EXP4 n=147/192 disclosure fix. A09: thesis cites the superseded `10.5281/zenodo.19297724`.
  Recency: both PDFs and the thesis `.docx` predate the current sources. No manuscript was edited —
  the substantive fixes need author decisions (branch merge, canonical EXP3 SHAP snapshot,
  provenance of Ch.5's 0.514/0.412). Sync matrix updated with the corrected EXP3 row, three new
  rows, and five new checklist items.
- **Mode (2026-08-22, third pass):** PUBLICATION — remediation. Landed the four-week backlog in
  three commits (`d1c9ba1d1` Paper B+C F01/F02 + EXP3 path; `00cdc8f3e` thesis/Paper A EXP3 wording
  + sync matrix; `b09b92a1d` both review reports + context), then applied six artifact-verified
  fixes in `3eeed3b04`: A02 partial (Paper A "LIME-only" mischaracterisation), A06 (thesis Anchors
  coverage 56→57 / 74.7%→76.0%), A07 (EXP3 minimum gap German Credit RF→XGB, in both Paper B+C and
  thesis Ch.6), A08 (EXP4 n=147/192 disclosure ported into thesis Ch.5), A10 (Paper B+C Friedman
  p-values labelled Holm-adjusted), A13 (new: dangling `@tbl-exp4-dimensiones` crossref in Ch.3,
  found by the rebuild, repointed to `@tbl-exp4-icc`). No statistic or table value changed.
  Rebuilt all four outputs — three PDFs via `tools/tectonic-portable`, thesis DOCX via
  `thesis/render.ps1` — all clean. Toolchain notes: MiKTeX `pdflatex` cannot build Paper A
  (microtype font-expansion error at the bibliography), use Tectonic; `render.ps1` calls a
  nonexistent `quarto clean` and prints a harmless error every run.
  **Still blocked on author decisions:** A01 (merge `results/exp3-*` branches, then rewrite Paper A
  §sec:exp3 + Conclusion), A03 (canonical EXP3 SHAP snapshot: July 0.6165 vs April 0.6065),
  A04 (thesis Ch.5 0.514/0.412 provenance), A05 (thesis Ch.4 cost profile), A09 (thesis Zenodo DOI).
- **Mode (2026-08-23):** PUBLICATION — remediation round 2, on author decisions. (1) Merged the EXP3
  Anchors cohort: imported the 12 run dirs (1,768 files) from `results/exp3-windows-breast-cancer`
  surgically via `git checkout <branch> -- <anchors paths>` (a full merge would have dragged in
  stale docs and junk paths `.venvScriptspython.exe` / `[14`); SHAP > Anchors re-verified 12/12,
  gap range +0.2601 GC/XGB to +0.5137 BC/RF. Paper A §sec:exp3 + Conclusion + artifact availability
  rewritten — A01/A02 closed. **Root cause of A01 found:** `scripts/run_exp3_shap_configs.py`'s
  docstring says Anchors "remain blocked by numpy<2.0 vs Python 3.13", true of the *July*
  environment; Paper A generalized it to "never executed". (2) A03 closed with July as canonical:
  Paper B+C BC/XGB 0.607→0.617, gap +0.06→+0.07. **Why BC/XGB differed:** all 12 SHAP configs were
  re-run 2026-07-23/24; only BC/XGB's quality metrics moved (sparsity 0.3333→0.8822 — 10/30 vs
  ~26.5/30 features above the 1e-4 threshold). Models were retrained 2026-05-10 with identical
  config *and identical test metrics*, and the runner is a thin wrapper over the same
  ExperimentRunner + YAML, so the cause is a SHAP/XGBoost library change across the April→July
  environment migration, not model or code. (3) A05 closed: Ch.4's profile *and* transversal
  subsections regenerated from `exp2_run_level_metrics.csv` with aggregation stated; the transversal
  section had been mixing per-model means with single-cell Appendix C sensitivity values (SVM
  0.928/159,059 is the k=50 row of `@tbl-appendix-shap-sensitivity`, not the 15-run mean 0.882/54,231).
  N-effect SHAP means also refreshed. (4) A09 closed: thesis repointed to `10.5281/zenodo.21538180`
  / commit `553f65d71`. (5) A12 closed incidentally. All four outputs rebuilt clean.
  (6) A04 closed on author approval: Ch.5's illustrative figures corrected to
  Anchors 0.388 / DiCE 0.172 / DiCE parsimony 0.017 / SHAP stability 0.732, and the "óptimo en
  parsimonia y eficiencia" claim reworded since DiCE's 28,209 ms cost is second-worst. Provenance
  settled first: the numbers entered in `f639935d0` (2026-05-10) at a commit where
  `outputs/analysis/` did not yet exist, and match no artifact at any commit — draft figures, not a
  different aggregation. Rest of Ch.5 swept: no other benchmark numbers.
  **All 13 audit findings (A01-A13) are now closed.** Remaining open items in the publication set
  are pre-existing and author-accepted: Paper B+C F03 (supplementary tables not independently
  re-derived) and F04 (EXP4 scripts + raw judge data unrecoverable); A11 (Paper A leads with the
  45-cell d_z, the others with the 75-cell) is an open suggestion with no action requested.
- **Mode (2026-08-24):** INCIDENT → EXECUTION — RCA-001 Phase 1, the permanent fix for the defect
  class behind the whole audit. Diagnosis: FOM-7 gate 7 (claim traceability) was editorial policy
  with no mechanism, in a workflow where the same quantity is authored independently in three
  documents. The SSOT machinery already existed (`pub/claims.toml` → `pub/fragments/` →
  `pubs-sync.yml`) but covered only abstracts/keywords, hand-typed its own numbers, and excluded
  Paper B+C entirely. Built: `pub/claim_registry.toml` (44 numbers, each with resolver + every
  manuscript carrying it), `scripts/pubs/claim_sources.py` (resolvers over `outputs/analysis/` and
  the EXP3 tree; separates block-level from run-level aggregation — the origin of A05),
  `scripts/pubs/verify_claims.py` (4 checks: value vs artifact, per-site occurrence count, retired
  values, cited-artifact existence), `docs/rca/RCA-001-manuscript-artifact-drift.md`. Wired Paper
  B+C into the fragment pipeline (rebuilt byte-equivalent), added the verifier to `pubs-sync.yml`
  CI and to `.aceconfig` `pre_commit`, and registered the **first entry in
  `regression-guards.yaml`** (9 guarded files, 6 invariants, 2 tests, 4 review triggers).
  Negative-tested, not just passing: the first manuscript-site check failed to catch an edited
  Paper A table cell because the value recurs in prose, so per-site occurrence counts were added.
  **New finding A14 (major, OPEN):** building the verifier revealed Paper B+C claims a 48-paper
  coded corpus throughout, while the only committed corpus artifact
  (`docs/reports/paper_c/paper_c_review_corpus.csv`) has 24 rows and no 48-row corpus exists at any
  commit. Deliberately not registered in the registry (would encode an unbacked number or force CI
  red); needs the author to commit the corpus or correct the manuscript.
  Note: `.aceconfig` is excluded via `.git/info/exclude`, so its new hook line is local-only.
  Phase 2 remains: generate numbers into LaTeX macros / Quarto inline values, and a CI build gate
  failing on undefined references.
- **Mode (2026-08-24 to 26):** INCIDENT/EXECUTION — RCA-001 Phase 1 plus A14 closure.
  Built the claim-traceability enforcement that makes FOM-7 gate 7 executable
  (`pub/claim_registry.toml`, `scripts/pubs/claim_sources.py`, `verify_claims.py`,
  `check_review_corpus.py`, `check_corpus_pdfs.py`, `fetch_corpus_pdfs.py`,
  `seed_corpus_from_audit.py`), wired Paper B+C into the fragment pipeline, added all
  checks to `pubs-sync.yml` CI, and registered the first `regression-guards.yaml` entry.
  **A14 closed 2026-08-26:** Paper B+C's review corpus is reconstructed and released as
  `docs/reports/paper_bc/paper_bc_review_corpus.csv` — 44 rows, of which 16 carry the
  original first-reviewer coding recovered from `second_reviewer_audit_results.csv` and
  28 were identified from the citation record and re-coded from full text. All 44 full
  texts are held under `corpus_pdfs/` (25 auto-retrieved, 17 copied from
  `thesis/papers/`, 2 supplied by the author), each verified by PDF header, size floor
  and page-one title match. ~4 papers coded but never cited are unrecoverable, so the
  corpus is 44 not 48, and twelve manuscript edits moved Paper B+C's printed figures
  onto the corpus: cluster distribution 15/10/7/6/4/2, evidence coverage
  21 proxy / 15 expert-taxonomy / 13 benchmark / 12 end-user / 4 LLM-judge, PRISMA
  included 44, audit fraction 36%, plus a new **Corpus provenance** paragraph in
  §Validity disclosing the reconstruction. `[review_corpus.paper_bc]` now pins the
  distribution and CI verifies it. **All 15 audit findings (A01-A15) are closed.**
  Outstanding by author decision: F03 (supplementary tables not re-derived), F04 (EXP4
  scripts/raw judge data unrecoverable), A11 (Paper A leads with 45-cell d_z).
  Author verification wanted on the 28 reconstructed coding rows before submission.
- **Mode (2026-08-28):** PUBLICATION / RCA — closed the two findings carried as
  accepted-as-is at the end of RCA-001, then finished the recovery they opened.
  **F04 was not unrecoverable.** The EXP4 sources were gone from the tree and from
  history, but their bytecode survived in `__pycache__`. All 16 files are now
  reconstructed and committed: 7 modules (`exp4_reliability_metrics`, `exp4_prompts`,
  `exp4_schema`, `exp4_parser`, `exp4_runner`, `exp4_cases`, `exp4_analysis`), 4 CLI
  scripts, 5 test modules. `scripts/pubs/verify_exp4_reconstruction.py` proves the
  modules compile to the same instruction stream as the original `.pyc`; the scripts
  (3.12 bytecode) get a structural check; the tests are verified by running (7 pass,
  4 skip). The recovery found **the published ICC is ICC(1,1), one-way random
  effects — not the ICC(2,1) all three documents described**. It is the conservative
  direction and the negative result stands (max 0.601, CI upper 0.695 vs the 0.75
  threshold); relabelled across Paper B+C and thesis Ch.3/Ch.5/Ch.6/appendix. It also
  answers the 2026-07-28 rigor review's open question 2 as fact: `icc_2_1` calls
  `pivot_table().dropna()` (n=147), `alpha_ordinal` does not and masks with
  `np.isnan` (n=192). **F03 found two wrong supplementary tables.** Table S6's
  drop-correlation column was wrong in 3 of 4 rows and printed a monotone sequence the
  artifact does not show (marginal replacement is highest, not lowest); the prose
  generalised the attenuation claim to both endpoints and now holds it to the top-k
  gap. Table S3's four occupation/workclass associations reproduced under no
  convention — those columns are unobserved on the same 2,809 records — and are now
  computed over pairwise-complete cases with the rule stated in the caption. Running
  the recovered tests surfaced a third defect: the EXP4 Jinja templates were never
  committed, and the `explanation_eval.j2` cited as the EXP4 rubric in Paper B+C, the
  supplementary and the thesis appendix is an unrelated three-dimension EXP1 template;
  all three citations corrected. 16 supplementary claims, 2 retired-value guards and
  2 cited artifacts added to the registry with stdlib-only resolvers. RCA-002 opened
  and closed for source recovery; RCA-001's "not covered" section corrected. Commits
  `1b4157116` and `357a03201`.
- **Mode (2026-08-28, second pass):** PEER_REVIEW — Scientific Advisor ran
  `scientific-rigor-review` against the full thesis (index through apendices). Report at
  `docs/review/scientific-rigor-review_thesis_2026-08-28.md` (Grade: **Accept**, mean 3.9/5;
  D1=3.5 D2=4.5 D3=3.5 D4=3.5 D5'=4.5 D6=4.0). Read-only: no manuscript file was edited.
  Confirmed fixed from the 2026-08-11 review: F01 (Ch.5 vs Ch.4 numbers), F02 (Ch.6 item 4 vs
  `sec-exp3-nota`), F03 (parsimony direction). Crossrefs verified clean (69 labels, 0 dangling)
  and the confirmatory core re-derived exactly from `exp2_run_level_metrics.csv`.
  13 findings, 3 major:
  **F01** — the thesis's self-nominated highest-impact claim ("LIME's instability is
  structural") is contradicted by two of its own results: Appendix C's `kernel_width` table
  (kw=10.0 → stability **0.664** vs 0.000 at the reference kw=3.0) and EXP3 (LIME stability
  0.748–0.927 on BC/GC at the reference kw). Ch.6 §sec-limitaciones states "no dependiente de
  la configuración del kernel" while §sec-futuro item 3, one page later, calls kw=10.0 the
  "alternativa más estable"; §sec-sintesis generalises to "cualquier sistema". §sec-exp3-nota
  states the correct narrow conclusion and it is not propagated.
  **F02** — the prescriptive per-instance cost ranges in Ch.4 Contextos A–D and Ch.6 are not
  derivable from any artifact: DiCE "770–4,500 ms" vs run-level mean **28,209** (and vs Ch.4's
  and Ch.5's own text); LIME "3–9 ms" vs per-model means 51.6–122.3; TreeSHAP "1–322 ms" vs RF
  533–7,836. Same defect class as A05, which was fixed in Ch.4's profile/transversal sections
  but never reached the Contexto paragraphs or Ch.6's criteria.
  **F03** — Appendix C's two LIME tables report four different values for the *identical*
  reference cell (RF/s42/N=100/kw=3.0/num_samples=1000): fidelity 0.461 vs 0.518, stability
  0.014 vs 0.000, cost 226 vs 30 ms. Only the kw table is artifact-backed; the `num_samples`
  probe is the open RCA-002 leftover.
  Minor: F04 (SHAP F>=0.80 / S>=0.70 asserted as guarantees, but fail in 2/5 model families
  each — including the tree models the same sentence recommends: xgb stability 0.575, rf
  fidelity 0.729), F05 (CV<3% reproducibility headline is the RF/N=100 subgroup; benchmark-wide
  is 12.0–12.8%), F06 ("Brecha 3" referenced 4x, never defined anywhere in the thesis —
  the conceptual analogue of A13), F07 (Fronteras row for LIME instability omits the
  dataset/feature-space boundary and requests future work Appendix C already completed),
  F08 (Appendix C Anchors-tau table: coverage column is design-wide x/75 but the caption
  scopes it to "RF, semilla 42"), F09 (Ch.4 Anchors profile labels run-level means 0.388/0.052
  as "sobre los bloques"; block-level is 0.3886/0.0429).
  Suggestions: F10–F12 carried unchanged from 2026-08-11 (chi2~15.2 underived; Anchors MNAR
  bias direction undisclosed; "prescriptivos" register). **F13 is a Task 3 input:**
  `verify_claims.py` is green (61 claims / 111 sites) yet F02/F03/F08/F09 all passed through
  it, because those numbers were never *registered*. Phase 1 guarantees "a registered number
  matches its artifact"; the failure mode actually found is "a load-bearing number was never
  registered". Recommend a registration-completeness sweep plus an unregistered-numeric-literal
  check before Phase 2's macro generation.
  Readiness: defensible as-is — no finding touches H1–H3, P1, P2, the statistical plan or
  FOM-7 itself — but F01/F02/F04/F06 are half a day of prose edits and sit in exactly the
  passages an examiner will probe. F01/F02/F04 concern quantities shared with Paper A and
  Paper B+C, so any fix must go through the sync matrix (RCA-001 invariant 3), and all
  implicated files are guarded (Ch.3–6 + apendices by RCA-001, Ch.5 also by RCA-002).
- **Prior session (2026-08-11):** ran `scientific-rigor-review` against the full PhD thesis (`thesis/index.qmd` through `apendices.qmd`, all 6 chapters + appendices); report at `docs/review/scientific-rigor-review_thesis_2026-08-11.md` (Grade: Accept, mean 4.3/5). Six findings: F01/F02 major (Ch.5 restates Ch.4's Anchors/DiCE fidelity+parsimony numbers incorrectly — needs a numeric fix before defense; Ch.6 "future work" item 4 contradicts the completed-work note `sec-exp3-nota` a few paragraphs earlier), F03-F06 minor/suggestions (parsimony-direction wording slip in Ch.4, undreived 50%-power-reduction sensitivity claim in Ch.3, unflagged Anchors non-convergence selection-bias direction, "prescriptivo" framing in Ch.6 in tension with the thesis's own conditional-language discipline).
- **Prior session (2026-07-30):** ran `scientific-rigor-review` against `docs/reports/paper_bc/paper_bc_jmlr.pdf`; report at `docs/reports/paper_bc/scientific-rigor-review_paper_bc_jmlr_2026-07-28.md` (Grade: Accept, mean 4.0/5). F01 (major, Friedman/Nemenyi block-count mislabeling) and F02 (minor, EXP4 ICC/Krippendorff n=147-vs-192 disclosure) were fixed with captioning-only edits to `paper_bc_jmlr.tex`; recompiled clean both times, no statistics changed. F03 (suggestion, supplementary tables not independently re-verified) remains open, lower priority. F04 (EXP4 analysis scripts + raw judge-response data both missing from the repo, never committed) was investigated in depth on 2026-07-30 — confirmed not fixable without re-running EXP4 from scratch; author decided to leave it as-is rather than fabricate a restoration. CIFIE PUBLICATION work below is unaffected by either review.

## Session Handoff - 2026-08-30

Authoritative summary of the 2026-08-30 session. 15 commits on
`thesis/rca-001-phase-2` (`ef4ec67f1`..`778151f9a`) plus the merge commit
`72a2a9665` on `main`. Working tree clean, everything pushed.

- **Completed**
  - **Branch restructuring.** The tree was found checked out on `main`, still a
    2026-07-04 snapshot, while all real work sat on
    `publication/cifie-xai-fom7-book-chapter` - a branch named for the book chapter
    that had been the trunk since May (78 commits). Merged into `main` byte-identical
    (12 conflicts: 10 CRLF-only, 2 superseded), cut `thesis/rca-001-phase-2` from it,
    deleted the old branch locally and on origin.
  - **Objectives.** Citations removed from all six specific objectives in Chapter 1.
    No bibliography orphan created: every key stays cited elsewhere.
  - **Front matter.** Dedicatoria and Agradecimientos added; cover page (programme,
    title, author, director, place) placed ahead of the TOC from `thesis/cover.txt`;
    the duplicate title heading after the TOC removed.
  - **Official title adopted** across `_quarto.yml`, `index.qmd`, `pub/claims.toml`
    (SSOT) and `README.md`, which had carried a third variant. Fragments regenerated.
  - **Crossreferences.** `lang: es` set; 20 self-labelled crossrefs switched to `-@`
    (80 English prefixes and 15 doubled labels eliminated); 20 leaked `sec-...` slugs
    converted to real crossrefs, which exposed and fixed a dangling `sec-metricas`.
  - **Numbering.** Hierarchical heading numbers generated post-render, with level 1
    reading "Capitulo N."; front matter, Referencias and the self-lettered Apendices
    excluded. Reverted `88933c7f6`, which had hardcoded the labels in the sources.
  - **Tables and figures.** All 82 tables centred; the 38 data tables given solid
    black borders and bold header rows; the 44 captions and 7 figures centred; the
    37 caption wrappers and 7 figure wrappers left unbordered.
  - **Two latent DOCX defects fixed.** All 44 caption paragraphs carried two `w:pPr`
    elements (malformed; Word honoured the injected one and dropped the caption
    style) - now merged into one schema-ordered element. Tables had no borders at
    all, because they reference a table style the template never defines.
  - **Context hygiene.** ACTIVE_CONTEXT updated twice; a wrong earlier finding about
    the corpus PDFs corrected rather than deleted.

- **Current State**
  - `thesis/rca-001-phase-2` at `778151f9a`, pushed; `main` at `72a2a9665`, pushed.
    Working tree clean. Origin holds exactly these two branches.
  - `scripts/enforce_docx_thesis_format.py` is now the thesis presentation layer:
    `merge_paragraph_properties`, `insert_cover_page`, `insert_break_after_toc`,
    `number_headings` + `collect_unnumbered_titles`, `format_tables` +
    `set_table_borders` + `bolden_header_row` + `is_layout_wrapper`, and
    `centre_captions_and_figures`. All driven from version-controlled sources, never
    the binary template.
  - Thesis sources: all seven `.qmd` files touched, plus `_quarto.yml`, `index.qmd`,
    new `thesis/cover.txt`. No numeric result, table value or citation changed in any
    commit this session.
  - Rendered DOCX committed and current: p1 cover, p2 TOC, p3 Dedicatoria,
    p4 Agradecimientos, p5 Resumen; Capitulo 1-6 numbered, sub-sections 1.1/1.1.1.
  - All three verifiers green: `verify_claims.py` (142 claims / 225 sites / 26
    retired-value guards / 10 cited artifacts), `verify_sync.py`,
    `verify_exp4_reconstruction.py`.

- **Next Steps**
  1. **Done 2026-08-30 by the author, but it is not durable.** The TOC was refreshed
     in Word and saved, and that saved file is what is committed: 127 TOC entries
     (13/53/61 at levels 1-3) against the empty field Quarto emits. **The tracked
     DOCX is therefore a post-Word-save artifact, not raw `render.ps1` output.** Any
     future render overwrites it and empties the TOC again, so the refresh must be
     repeated after every render, as the last step before the file is shared.
     Word also normalised the style ids on save (`Ttulo1` -> `Heading1`, `Compact`/
     `Textoindependiente` -> `BodyText`, and the caption style likewise). All direct
     formatting survived intact - verified after the save: 82/82 tables centred,
     38/38 bordered and bold-headed, 0/7 figure wrappers bordered, 7/7 figures
     centred, 0 duplicate `w:pPr`, Capitulo 1-6 headings present. The post-render
     script is unaffected because it only ever runs on a fresh render.
  2. **Resume the standing objective, Task 3 / RCA-001 Phase 2** - emit registry
     values as LaTeX macros and Quarto inline values, and add a CI job building all
     four outputs, failing on undefined references and crossref warnings.
  3. **Coverage sweep, one file at a time**, before Phase 2's macro generation. Only
     Chapter 4 is in `[coverage]`; Ch.3, Ch.5, Ch.6, `apendices`, Paper A, Paper B+C
     and the supplementary are unswept. Triage each with
     `python scripts/pubs/verify_claims.py --coverage-report`.
  4. **Author-verify the 28 reconstructed review-corpus coding rows** before
     submission.

- **Blockers/Issues**
  - **Word file lock.** `render.ps1` deletes the old DOCX first, so it fails while the
    document is open in Word. Close it before rendering. To validate without closing:
    `quarto render --to docx --output-dir _output_test`, then patch that copy - but
    note the post-render hook globs `_output*`, so it will also try the locked one.
  - **CIFIE chapter still blocked** on final template, word limit and citation
    rendering requirements (pre-existing, unchanged).
  - **Corpus PDFs exist only on this machine.** Correctly gitignored, but two were
    supplied by the author under institutional access and are not re-fetchable.
    Back them up outside git before deposit.
  - **Open by author decision, unchanged:** Paper B+C F03 (supplementary tables not
    independently re-derived) and A11 (Paper A leads with the 45-cell d_z).
  - **Cosmetic, unresolved:** `render.ps1` calls a nonexistent `quarto clean` and
    prints a harmless error every run.

- **Notes**
  - **A green render proves nothing about layout.** Four defects this session
    survived a successful `render.ps1`: two silently-failed CRLF edits, a page break
    Quarto reordered, headings numbered nowhere, and a frame drawn around every
    figure. Verify by unzipping the DOCX and reading `word/document.xml`.
  - **Count tables with a tree walk, not a regex.** `<w:tbl>.*?</w:tbl>` cannot see
    nesting and reported 45 where there are 82. The document is 38 data tables +
    37 caption wrappers + 7 figure wrappers; pandoc wraps captioned content in
    single-cell tables, which must never take a border.
  - **`scripts/enforce_docx_thesis_format.py` is CRLF.** Multi-line edits written
    with a bare newline match nothing, fail silently, and leave a file that still
    parses and runs. Assert on every replacement.
  - **Quarto promotes a chapter file's first level-1 heading** to the chapter title
    when the file declares no `title`, hoisting it above everything else in that
    file - so a page break written at the top of `index.qmd` lands after it. Insert
    such breaks post-render.
  - **The committed DOCX is Word-saved, not render output.** Re-rendering resets the
    TOC to an empty field and reverts Word's style-id normalisation; that is expected.
    Sequence for a shareable document: edit sources -> `thesis/render.ps1` -> open in
    Word -> refresh the TOC -> save -> commit. Verifying a fresh render against the
    committed file will show large diffs for this reason alone.
  - Useful commands: `thesis/render.ps1` (full render + post-render patches);
    `python scripts/pubs/verify_claims.py`; `verify_sync.py`;
    `verify_exp4_reconstruction.py` (needs Python 3.13);
    `python scripts/pubs/generate_fragments.py` after editing `pub/claims.toml`.
  - The fragment generator rewrites files with LF; if only line endings change,
    `git checkout -- pub/fragments/` to drop the churn.

## Session Handoff - 2026-09-02

Continues the 2026-08-30 session below, which remains accurate for the branch
restructuring and the first presentation pass. 5 further commits,
`ceb87964f`..`18f183a4e`. Working tree clean, everything pushed.

- **Completed**
  - **Dedication-style front matter.** Dedicatoria and Agradecimientos are set in
    right-aligned italics under centred, upright headings, generated post-render by
    `format_dedication_sections`. Scope is bounded by the next heading of any level:
    the only right-aligned paragraphs in the document are those six body lines plus
    the two empty page-break paragraphs inside the sections, and Resumen immediately
    after is still justified and upright.
  - **Resumen and Abstract rewritten, and mirrored.** A Scientific Editor review
    scored the old Resumen 2.83/5 (Weak Reject) as a standalone summary against the
    thesis's own 4.3/5 Accept - the gap being that the abstract had not kept up with
    the corrected body. Four majors fixed: (F01) it asserted LIME instability as
    "estructuralmente inestables", the universal framing Chapter 6 explicitly
    retracts, and the English abstract repeated it - both now carry the scoped claim;
    (F02) OE6 and its negative inter-judge result were absent entirely and now have
    their own paragraph; (F03) the cross-dataset replication was unmentioned;
    (F04) the abstract carried no quantitative result at all. Three minors also
    closed: "SHAP domina" softened to the mean-with-exceptions form Ch.4 supports,
    the taxonomy now reports its three construct gaps, and the ES/EN framing mismatch
    resolved. Resumen 245 -> 404 words, Abstract 341, three paragraphs each.
  - **Registry discipline held.** Only already-registered figures were used, so no new
    resolver was needed - "12/12" and the 0.75 ICC threshold were deliberately
    avoided because neither is registered. Five claims gained 15 sites (225 -> 240).
    Negative-tested: replacing the ICC 0.321 fails `verify_claims.py`, and localises
    to the ES fragment while `claims.toml` still holds the value in the English text.
  - **The Word-saved DOCX with a refreshed TOC** was committed rather than discarded
    (`ceb87964f`), then necessarily replaced by later renders.

- **Current State**
  - `thesis/rca-001-phase-2` at `18f183a4e`, pushed; `main` at `72a2a9665`. Clean tree.
  - `scripts/enforce_docx_thesis_format.py` gained `format_dedication_sections` and
    `DEDICATION_SECTIONS`, joining the existing post-render set.
  - The Resumen and Abstract live in `pub/claims.toml` and flow to
    `pub/fragments/thesis_resumen_es.qmd` and `thesis_abstract_en.qmd`; both were
    regenerated from the SSOT, never hand-edited.
  - Rendered DOCX current and committed. Verified in it: retracted wording 0
    occurrences, the new figures present, 82/82 tables centred, 38/38 data tables
    bordered and bold-headed, 0/7 figure wrappers bordered, 0 duplicate `w:pPr`,
    Capitulo 1-6 intact, raw slugs 0, unresolved crossrefs 0.
  - All three verifiers green: 142 claims, 240 manuscript sites.

- **Next Steps**
  1. **Refresh the TOC in Word** (author, manual, recurring after every render).
  2. **Confirm the faculty abstract word limit.** The Resumen is 404 words, up from
     245. If capped, the closing sentence of paragraph 3 and the taxonomy clause in
     paragraph 1 are the cleanest cuts - neither carries a registered figure, so
     trimming them needs no registry work.
  3. **Have the author read the revised Resumen.** The re-score after the edit would
     be a self-assessment of my own text and is worth less than the first review.
  4. **Resume Task 3 / RCA-001 Phase 2**, the standing objective, with the coverage
     sweep first (only Chapter 4 is in `[coverage]`).
  5. **Run the top-level statement sweep** whenever a claim is rescoped in the body,
     and once more before deposit: `docs/review/top-level-statement-sweep.md`.

- **Blockers/Issues**
  - **The Word file lock recurred four times this session.** `render.ps1` deletes the
    old DOCX first and fails while the document is open; a stale `~WRL*.tmp` in
    `_output` is the tell. Workaround that avoids the hook's `_output*` glob:
    `quarto render --to docx --output-dir _scratch`, then patch that copy by hand.
  - Everything listed under the 2026-08-30 handoff's Blockers is unchanged: the CIFIE
    template, the corpus PDFs held only on this machine, Paper B+C F03, A11, and the
    harmless `quarto clean` error.

- **Notes**
  - **An abstract is a manuscript site like any other.** The August rigor review
    scoped the LIME claim across Ch.4-6 and Paper B+C and registered a retired value
    for it, but nothing swept `pub/claims.toml`, so the retracted wording survived for
    five weeks in the most-read text of the thesis. When a claim is rescoped, sweep
    the abstracts in the same pass.
  - **Prefer figures that are already registered when editing an abstract.** Reaching
    for an unregistered number ("12/12", the 0.75 ICC threshold) turns a prose edit
    into a resolver-writing exercise or forces an `[[unbacked]]` entry.
  - Everything in the 2026-08-30 Notes still applies, in particular that a green
    render proves nothing about layout.

## Session Handoff - 2026-09-04

Task 3 / RCA-001 Phase 2 is under way: the coverage sweep. **Session closed
2026-09-05.** 5 commits, `b17573245`..`c9d504da6` (the fifth being this handoff
itself). Working tree clean, nothing unpushed, no commits after `c9d504da6`.
Verified at close: `verify_claims.py` 166 claims / 270 sites / 26 retired-value
guards / 10 cited artifacts / 3 files fully registered; `verify_sync.py` and
`verify_exp4_reconstruction.py` green; `main` at `72a2a9665`, branch at
`c9d504da6`, and origin holds only those two branches.

- **Completed**
  - **Objetivo general revised** after a Scientific Editor review scored it 3.00/5.
    `validar` overreached what Ch.6 concedes and became `evaluar empíricamente`; the
    three components now sit in apposition, which defines "multinivel" at its first
    use, since the term was load-bearing and enumerated nowhere; a closing clause on
    delimiting validity scope gives OE6 somewhere to belong.
  - **Top-level statement sweep created** (`docs/review/top-level-statement-sweep.md`)
    and wired into RCA-001 as a sixth review trigger. It maps the 14 statements read
    as promises to the sections that can falsify them, because `verify_claims.py`
    checks numbers and these are prose.
  - **Coverage sweep: Chapters 6 and 5 registered and enforced.** `[coverage]` went
    from one file to three (Ch.4, Ch.6, Ch.5). Registry 142 -> 166 claims,
    225 -> 270 sites.
  - **Two defects found in Ch.6, both by asking an artifact rather than reading:**
    (1) the masking-bias passage cited Cramér's V = 0.34 for education/occupation,
    the value RCA-002 corrected to 0.196 in the supplementary on 2026-08-28 and never
    propagated -- wrong by 74% for five weeks; (2) "+0.07 en BC frente a +0.27 en
    Adult" are both RF cells, not dataset-wide figures (the benchmark-wide Adult gap
    is 0.2479), so the scope is now stated -- RCA-001 invariant 6, the F09 class.
    One editorial tightening: `$d_z > 2.8$`, an author-chosen floor, became
    `$d_z \geq 3.00$`, which is exact and already registered.
  - **Chapter 5 came back clean.** All fourteen EXP4 cells re-derived exactly on the
    first attempt; nothing in that table changed.
  - **A composing resolver was the blocker and is now built.** Six Ch.6 literals were
    differences or complements of registered values, so `[[unbacked]]` would have been
    untrue. `claim_sources.py` gained `diff:<exprA>|<exprB>` and `exp2_missing_pct`.

- **Current State**
  - `thesis/rca-001-phase-2` at `ca309ac6b`, pushed; `main` at `72a2a9665`. Clean tree.
  - `[coverage]` enforces `capitulo-4-resultados`, `capitulo-6-conclusiones`,
    `capitulo-5-taxonomia`. 166 claims, 270 sites, 26 retired-value guards.
  - All three verifiers green. DOCX rebuilt and current.

- **Next Steps**
  1. **Refresh the TOC in Word** (author, manual, recurring after every render).
  2. **Continue the coverage sweep, one file at a time.** Remaining: `capitulo-3`,
     `capitulo-2`, `capitulo-1`, `apendices`, Paper A, Paper B+C, the supplementary.
     Take `capitulo-3` next: it carries the design tables and the FOM-7 gate
     definitions. Workflow: add the file to `[coverage]`, run
     `python scripts/pubs/verify_claims.py --coverage-report` (exits 0), triage,
     register or declare structural, then leave enforcement on.
  3. **Then RCA-001 Phase 2 proper:** emit registry values as LaTeX macros and Quarto
     inline values, and add a CI job building all four outputs, failing on undefined
     references and crossref warnings.
  4. **Run the top-level statement sweep** before deposit and after any rescoping.

- **Blockers/Issues**
  - **The Word file lock** recurs constantly; close the document before rendering. To
    validate without closing: `quarto render --to docx --output-dir _scratch`, then
    patch that copy by hand (`_scratch` avoids the post-render hook's `_output*` glob).
  - Everything under the 2026-09-02 and 2026-08-30 handoffs is unchanged: the CIFIE
    template, the corpus PDFs held only on this machine, Paper B+C F03, A11, and the
    harmless `quarto clean` error.

- **Notes**
  - **The sweep is finding real defects at a steady rate:** two files, four findings
    (F14/F15 in Ch.4; the stale V and the unstated RF scope in Ch.6). Ch.5 clean. Treat
    the remaining files as likely to contain one or two each, not as a formality.
  - **Before calling a mismatch a defect, try every aggregation.** The Adult gap looked
    wrong at 0.2479 vs 0.27 until the per-model RF figure (0.2716) matched; the finding
    was undisclosed scope, not a wrong number. This is what F15 taught.
  - **`[[unbacked]]` is for values that cannot be re-derived, not for values that need
    arithmetic.** Prefer a resolver.
  - **Editing `pub/claim_registry.toml` programmatically:** it is CRLF, and joining a
    block with NL and then calling `.replace("\n", NL)` double-converts, producing
    CR-CR-LF that breaks the TOML parser. Always assert
    `open(p,'rb').read().count(b'\r\r\n') == 0` and re-parse before committing.
  - The EXP4 dimension key in the artifact is `concision`, not `conciseness`.

## Session Handoff - 2026-09-06

Two workstreams ran in parallel for the first time: the thesis coverage sweep and
Paper B+C's venue preparation. 78 commits on `main` (`72a2a9665`..`357f62af8`).
All three lanes level, working trees clean, everything pushed. Verified at close:
`verify_claims.py` 209 claims / 300 sites / 26 retired-value guards / 10 cited
artifacts / 4 files fully registered; `verify_sync.py` and
`verify_exp4_reconstruction.py` green.

### Completed

- **ADR-0013, the publication branching model.** The trunk was 29 commits behind
  the only active lane, so any second lane would have started on a stale claim
  substrate. Principle adopted: *manuscript bodies are branch-private, the claim
  substrate is trunk-owned, a lane may be ahead of `main` but never behind*. It
  follows from RCA-001 invariant 3, which forbids registering a shared quantity
  twice and so forbids forking `pub/claim_registry.toml`. Lanes, the shared-file
  list and five merge rules are in `docs/adr/0013-publication-branching-model.md`
  and mirrored into Active Constraints. Plan tasks 7 and 8 added.
- **Second worktree** at `C:\Users\jonna\Github\xai-paper-bc` on
  `paper/bc-venue-definition`, so the thesis DOCX can stay open in Word while
  Paper B+C builds.
- **Ch.3 coverage sweep (thesis).** Fourth file enforced. Registry 166 -> 209
  claims, 270 -> 313 sites; nine resolvers added (`exp1_model_metric`,
  `exp1_split`, `exp1_repro_cv_max`, `exp2_artifacts_present`,
  `exp2_coverage_pct`, `exp2_method_coverage_pct`, `exp2_block_replication`,
  plus the composers `linear:<a>|<b>|<expr>` and `chi2_sf3:<expr>`). Two defects:
  **F16**, four section and table numbers typed rather than generated - all
  correct, which is why nothing had caught them - now `@sec-`/`@tbl-` crossrefs
  with three new anchors (`sec-muestreo`, `sec-fom7`, `sec-cobertura`); **F17**,
  two EXP1 CV bounds stated one ulp below the value they bound.
- **Three cited artifacts were untracked.** `verify_claims.py` was green on this
  machine and red on any fresh checkout, proved by running it in the new
  worktree: 41 failures. `.gitignore` excluded `outputs/`, and git cannot
  re-include a file under an excluded directory, so every `!outputs/analysis/...`
  negation was inert. `exp4_llm_evaluation/`, `lime_kernel_width_sensitivity.csv`
  and `exp3_lime_results.csv` had never entered the repository. Fixed with
  `outputs/*`; RCA-001 gained the invariant that a cited artifact must be
  *tracked*, not merely present.
- **Paper B+C venue: TMLR.** Chosen over IJIMAI, which caps papers at 12 pages
  against this manuscript's 26 and would have forced un-merging Papers B and C.
  Converted to the official `tmlr.sty`, renamed `paper_bc_jmlr*` ->
  `paper_bc_tmlr*` (78 references repointed across ten live pointers; dated
  review reports deliberately keep the old name), anonymised through the package
  option with `\ifdeanon` / `\ifdeanonymised` guards driven by the same
  `\if@accepted`.
- **Paper A published and cited.** RIMI (3), 2026, doi:10.69850/rimi.vi3.307.
  Cited in the Introduction and at the head of the empirical section.
- **B1, prior publication - closed.** TMLR forbids reuse of text, figures *or
  results* with archivally published work; the carve-out covers only
  non-archival venues. Thirteen registered results appeared in both papers.
  All thirteen removed: the four-method Friedman omnibus and the block-means /
  Nemenyi tables replaced by a cited paragraph; the paired table's per-method
  mean columns replaced by the mean difference with a 95% CI it never carried;
  the EXP3 SHAP column replaced by the SHAP-Anchors gap; three prose uses of
  LIME's stability level reworded to "near zero". **Text and figures never
  overlapped** - 2 shared sentences out of 405, both bibliography titles, and
  Paper A has no figures.
- **A retired value was shipping inside a figure.** `fig_exp3_fidelity.pdf`
  labelled its Breast Cancer / XGB bar `0.607`, the April snapshot retired
  2026-08-23 as `A03.exp3.bc_xgb.april`. It survived five weeks because
  `verify_claims.py` reads manuscript text and cannot see inside an embedded
  figure, and no committed script produced that figure. Wrote
  `scripts/generate_exp3_gap_figure.py`; `fig_exp3_gap.pdf` plots Anchors levels
  with the gap stacked above, so each bar still reaches the SHAP level without
  labelling it. RCA-001/002 gained the matching invariant.
- **B2, authorship - closed.** Dr Herrero-Uceda was added, then removed at his
  request ("he says I made all the work"); sole author is Jonathan
  Herrera-Vasquez, acknowledgment singular. OpenReview profile created under a
  UNADE email. He remains an author of the RIMI paper, which is cited.
- **B3, artifacts - closed.** `scripts/pubs/build_artifact_bundle.py` produces
  `docs/reports/paper_bc/paper_bc_artifacts.zip`, 3.8 MB / 3,568 files
  (gitignored; regenerate rather than store). Scrubbed **577 absolute paths
  containing the author username** from three exports - in the bundle copies
  only, never in the repository artifacts, which are the evidence the registry
  resolves against.
- **Abstract typography.** `pub/claims.toml` had `vs.\` at a line end; TOML reads
  a trailing backslash as a line continuation and ate the space, so the abstract
  read "53.3 ms vs.694.6 ms". Only instance in the file.
- **Broader Impact Statement** added, and the prior-publication subsection
  unguarded and retitled *Provenance of the Empirical Cohort* now that no result
  is shared.

### Current State

- `main` `357f62af8`; both lanes level with it, 0 substrate files differing.
- **Thesis:** `[coverage]` enforces four files (Ch.3, 4, 5, 6). Six remain:
  `capitulo-1`, `capitulo-2`, `introduccion`, `apendices`, Paper A, Paper B+C.
- **Paper B+C: submittable on the evidence available.** 26 pp + 5 pp
  supplementary, zero unresolved references or citations, `tmlr.sty`
  byte-identical to upstream, anonymous title block with no name, email or
  affiliation, zero results shared with the published Paper A.

### Next Steps

1. **Author actions before submitting Paper B+C** (nothing in the manuscript
   blocks): send the editor note
   `docs/reports/paper_bc/EIC_ENQUIRY_prior_publication.md`; build the bundle
   with `python scripts/pubs/build_artifact_bundle.py` and attach
   `paper_bc_artifacts.zip` as supplementary; confirm the RIMI journal spelling
   and DOI, that the work is under review nowhere else, and that
   `10.5281/zenodo.21538180` is the right snapshot for this paper. After
   submission, set `\openreview`, `\month` and `\year` for the camera-ready.
2. **Decide `data/adult.csv`.** Ten `verify_claims.py` failures on any clean
   checkout, all from the `supp.s3.*` claims reaching into the 5.3 MB raw
   dataset, which `/data/` ignores. Recommended: derive
   `outputs/analysis/supp_s3_associations.csv` using the existing resolver code
   so values are identical by construction, and repoint those ten claims; the
   alternative is vendoring the dataset. Not done because it changes how
   RCA-002-guarded statistics resolve.
3. **Continue the coverage sweep.** Take `apendices` next: it carries the same
   typed section/table numbers F16 fixed in Ch.3, and the Anchors-tau and
   Appendix C probe values.
4. **Plan task 8** - `scripts/pubs/check_substrate_current.py` in CI, plus
   `pubs-sync.yml` triggers for `thesis/**`, `paper/**`, `pubs/**`.
5. **RCA-001 Phase 2 proper** - registry values into Quarto inline values, and a
   CI job building all four outputs.

### Blockers/Issues

- **CI is almost certainly red** and has been: `verify_claims.py` fails on a
  fresh checkout for `data/adult.csv` (item 2 above). Could not confirm - `gh`
  is not installed on this machine.
- `pubs-sync.yml` runs only on `pull_request` and push to `main`, so a local
  merge on a lane gets no CI at all.
- **TMLR's judgement on the shared cohort** is the one thing outside our
  control. No result is shared, but both papers rest on the same executions;
  the editor note discloses it.
- Author verification of the 28 reconstructed review-corpus coding rows, and an
  off-machine backup of the 44 corpus PDFs, both still open from earlier
  sessions.
- Word TOC refresh after every thesis render - manual, unavoidable.

### Notes

- **Worktrees need seeding.** `.ace/` (except the four tracked
  `standards/*.md`), `.aceconfig`, `tools/tectonic-portable/` and
  `outputs/` are gitignored, so a new worktree lacks them. Seed with
  `cp -r .ace/. <worktree>/.ace/` - contents, not the directory, or it nests.
  Copy `tectonic.exe` explicitly: **Git Bash resolves `tectonic` to
  `tectonic.exe` on Windows** and silently overwrote one with the other.
- **Do not write Python with backslashes through a Bash heredoc.** The harness
  collapses `\\` to `\`, which silently corrupts LaTeX anchors and regexes.
  Write the script to a file first, then run it. This cost several retries.
- **PowerShell `Set-Content -Encoding utf8` adds a BOM.** It did, to
  `paper_bc_tmlr.tex`; stripped afterwards. Prefer Python for round-trips.
- **The post-render hook rewrites `thesis/_output/` even when Quarto is given
  `--output-dir _scratch`**, contrary to the older note. Restore `_output` from
  git after a scratch validation render.
- **Two worktrees means two copies of every file.** Twice this session a stale
  PDF was read from the thesis lane while the work sat on the paper lane. Merge
  to `main` as soon as a unit is green.
- **The registry can detect prior-publication conflicts.** A claim whose
  `appears_in` names both a published document and a live submission is a
  candidate; the query is in the editor note. Re-run it whenever any registered
  manuscript is published - RCA-001 has the trigger.
- Paper B+C build: `python scripts/pubs/build_artifact_bundle.py` for the ZIP;
  Tectonic for the PDFs; `docs/reports/paper_bc/BUILD.md` documents the three
  anonymity modes and the pre-submission checklist.

## Session Handoff - 2026-09-08

**Status update only. No code, manuscript or registry change.** Repository
identical to the 2026-09-06 close: `main` `eeec4852b`, both lanes level, working
trees clean, nothing unpushed, all three verifiers green (209 claims / 300 sites
/ 26 retired-value guards / 10 cited artifacts / 4 files fully registered).

### Completed

- Nothing was built or changed. This entry exists to record where the Paper B+C
  submission actually stands, so a resuming session does not mistake "ready" for
  "submitted".

### Current State

- **Paper B+C is submission-ready and not submitted.** All three blockers from
  the readiness review (B1 prior publication, B2 authorship, B3 artifacts) are
  closed; the manuscript, supplementary, artifact bundle and editor note are
  complete and committed.
- **Submission is blocked on OpenReview account approval.** The profile was
  created under a UNADE email on 2026-09-06 and is still awaiting moderator
  activation. TMLR submissions go only through OpenReview, so nothing can be
  filed until it clears.
- **The editor note is written and will be sent with the submission, not
  before.** Author's decision, recorded as such: the earlier recommendation was
  to send it in advance. The note already supports this route - it names the
  OpenReview submission comment field as an alternative to the Editors-in-Chief
  address - so no change to
  `docs/reports/paper_bc/EIC_ENQUIRY_prior_publication.md` is needed. The risk
  accepted is that if the editors object to the shared cohort, that objection
  now arrives after filing rather than before.

### Next Steps

1. **Wait for OpenReview activation**, then submit. In order: build the bundle
   (`python scripts/pubs/build_artifact_bundle.py`), upload
   `paper_bc_tmlr.pdf` with `paper_bc_artifacts.zip` as supplementary, and post
   the editor note in the submission's comment field at the same time.
2. **After submission**, set `\openreview` to the forum URL, and `\month` /
   `\year`, for the camera-ready build only. See
   `docs/reports/paper_bc/BUILD.md`.
3. **Three confirmations still pending** and unchanged since 2026-09-06 - see
   Blockers below.
4. Thesis workstream continues as before: sweep `apendices` next.

### Blockers/Issues

- **OpenReview account not yet approved.** Hard blocker on submission; outside
  our control, no workaround.
- **Three author confirmations outstanding**, all carried from 2026-09-06 and
  none yet done: the RIMI journal-title spelling and DOI against the published
  article (the journal's own site prints "multidisiplinaria", apparently a typo,
  while the manuscript bibliography uses the corrected spelling); that the work
  is under review at no other venue; and that
  `10.5281/zenodo.21538180` is the correct snapshot DOI for this paper rather
  than for the thesis, since it was adopted there first.
- Everything under the 2026-09-06 Blockers section is unchanged: the
  `data/adult.csv` decision and the CI it is probably failing, the
  `pubs-sync.yml` trigger gap, the 28 reconstructed corpus rows, the corpus-PDF
  backup, and the Word TOC refresh.

### Notes

- **Ready is not submitted.** The readiness checklist
  (`docs/review/tmlr_readiness_checklist_2026-09-06.md`) reads "submittable",
  which is a statement about the manuscript, not about the filing. Do not close
  Next Steps item 00 until an OpenReview forum ID exists.
- Nothing else from the 2026-09-06 Notes has changed; the worktree seeding,
  heredoc-backslash, PowerShell BOM and figure-blind-spot notes all still apply.

## Session Handoff - 2026-09-14

**OpenReview account active; Paper B+C is ready to file and NOT yet submitted.**
The pre-submission check found two defects that every earlier check had passed.
Both are fixed. The author's confirmations are all in except one.

### Completed

- **Author actions confirmed (2026-09-14):** OpenReview profile complete
  (affiliation, publication history including RIMI); Dr Herrero-Uceda declared
  as a conflict of interest (thesis tutor); RIMI DOI confirmed, and Crossref
  resolves it to the article (issue 3, 2026-09-01, ISSN 2992-7978) with the
  journal name correctly spelled, so the bibliography needs no change; Zenodo
  snapshot `10.5281/zenodo.21538180` confirmed as this paper's.
- **Defect 1, the abstract printed "SHAP's extttTreeExplainer" (RCA-003).**
  `pub/claims.toml` held `\texttt` with a single backslash, which TOML reads as
  a TAB. It was present since 2026-08-24, and it is the second instance of the
  class: `3d6ba90ba` fixed `vs.\` one line above and did not look further.
  `verify_sync.py` now fails, in CI, on any odd-length backslash run inside a
  `"""` string in `claims.toml` and on any control character in a fragment.
  Negative-tested against the old source. Guard RCA-003 added.
- **Defect 2, the supplementary tables were not in the upload.** OpenReview
  takes one supplementary file; the ZIP lacked `paper_bc_tmlr_supplementary.pdf`.
  `build_artifact_bundle.py` now ships it as `supplementary_tables.pdf`, and
  refuses to build when an input is missing.
- **Submission sheet** `docs/reports/paper_bc/OPENREVIEW_SUBMISSION.md` (paper
  lane): one-line title, the abstract converted by script from the fragment
  (246 words, inline math kept for MathJax), keywords, upload paths,
  human-subjects/funding/competing-interest answers matching the manuscript,
  and five suggested Action Editors from the TMLR board's listed areas: Dennis
  Wei, Satoshi Hara, Amir-Hossein Karimi, Mengnan Du, Olawale Elijah Salaudeen.
  None is cited in the manuscript.
- **Editor note revised** for email to `tmlr-editors@jmlr.org` right after
  submission, quoting the submission number. It is signed, so it must not go
  in as a forum comment. It now also discloses the tutor relationship. BUILD.md
  updated to match.
- Verified: anonymity scan of both PDFs (text and metadata) and all 3,569 bundle
  files, where the only name hits are the third-person RIMI citation; PDF 26 pp,
  0 undefined refs; shared-result query 0 of 209; verifiers green.

### Current State

- `main` `2e1bb6a33` (+ this handoff). Paper lane `16ae73404`: main plus the
  rebuilt PDF and the submission documents. Thesis lane `be6f79e68`: main merged.
  All pushed.
- The paper worktree now holds an untracked copy of `data/adult.csv`, which it
  needs for `verify_claims.py` and the bundle build. It is gitignored.

### Next Steps

1. **Author: confirm the work is under review at no other venue** (form
   checkbox), then submit using `OPENREVIEW_SUBMISSION.md`. Rebuild the bundle
   just before uploading.
2. **Right after submitting:** email the editor note with the number and forum
   URL filled in.
3. Record the forum ID here and close Next Steps item 00.
4. Camera-ready only: the acknowledgment's "This draft was prepared from
   repository artifacts dated May 2026" is stale. It is hidden in the anonymous
   build.

### Notes

- **A generator's output is a manuscript site.** Source, verifier and
  readiness checklist were all green while page 1 of the PDF was wrong. Read the
  rendered text of anything that passes through `generate_fragments.py`.
- **`git worktree add` under the session scratchpad fails** with "Filename too
  long" (`thesis/papers/`, `outputs/git_safety_backups/`). The substrate merge
  was a fast-forwardable no-conflict case, so it was done with `git commit-tree`
  + `git update-ref`, with no checkout. For a real merge, use a short path.

## Session Handoff - 2026-09-15

**Submission-preparation task closed. Paper B+C is NOT submitted, and must not be
submitted from its current package.** The author is revising the manuscript in
detail; any revision invalidates parts of the package that were built from it.
Active objective moves back to Task 3 / RCA-001 Phase 2 on the thesis lane.

### Where the paper stands

- Everything needed to file exists and was verified on 2026-09-14: anonymous PDF
  (26 pp, 0 undefined references), artifact bundle (3.9 MB, 3,569 files,
  including `supplementary_tables.pdf`), editor note, and the submission sheet
  `docs/reports/paper_bc/OPENREVIEW_SUBMISSION.md`.
- Author confirmations in hand: OpenReview profile complete, Herrero-Uceda
  declared as a conflict, RIMI DOI verified against Crossref, Zenodo snapshot
  confirmed.
- **Two things outstanding, both author-side:** confirm the work is under review
  at no other venue (form checkbox), and finish the detailed revision.
- Lanes at close: `main` `ec1433b33`, paper lane `14bf66b6f`, thesis lane
  `5c4705d03`, all pushed, both worktrees clean.

### The submission gate (do not skip)

A revision to `paper_bc_tmlr.tex`, its supplementary, or `pub/claims.toml`
invalidates the built PDF, the bundle, and the abstract copied into the
submission sheet. Before filing, run the re-verification checklist in
`docs/reports/paper_bc/OPENREVIEW_SUBMISSION.md` ("After any revision") and
report the result to the author. **Never confirm the package is ready on the
strength of the 2026-09-14 verification.** In short: rebuild both PDFs and the
bundle, re-run all three verifiers, re-scan both PDFs and the bundle for author
identity, re-run the shared-result query against Paper A, regenerate the
sheet's abstract from the fragment, and re-read page 1 of the built PDF.

The last item is not ceremony: on 2026-09-14 the abstract printed
"SHAP's extttTreeExplainer" through a green verifier, a green readiness
checklist and an anonymity pass (RCA-003).

### Next steps, in order

1. **Author:** finish the detailed revision of Paper B+C.
2. **Then, before any submission:** run the re-verification checklist and hand
   the author a written result. Register any new or changed number in
   `pub/claim_registry.toml` first - a revision that introduces an unregistered
   figure fails RCA-001 invariant 1, and prose edits that rescope a claim
   trigger the top-level statement sweep.
3. **Author:** confirm no concurrent submission, then file using the sheet.
4. **Immediately after filing:** email the editor note to tmlr-editors@jmlr.org
   with the submission number and forum URL filled in. Not as a forum comment -
   the note is signed.
5. **After filing:** record the forum ID here and close Next Steps item 00.
6. **Thesis lane, meanwhile:** Task 3 / RCA-001 Phase 2 - continue the coverage
   sweep with `apendices`, then `capitulo-1`, `capitulo-2`, `introduccion`,
   Paper A and the supplementary, then the macro generation and the CI build
   job.

### Note on sweeping Paper B+C

`docs/reports/paper_bc/paper_bc_tmlr.tex` is one of the ten files still outside
`[coverage]`. Do not add it while the author is revising it: adding a file to
`[coverage]` is a trunk event that turns CI red on every lane until triaged, and
it would collide with in-flight manuscript edits. Sweep it after the revision
settles, before filing.

## Session Handoff - 2026-09-27

**New laptop. The EXP4 bytecode is lost, and pubs-sync CI had never been green.**

### Completed

- Paper B+C abstract: the EXP3 sentence now states the fidelity ordering held in
  every dataset--model stratum and reports the LIME-stability moderation finding,
  instead of "partial support ... does not establish cross-modal generality". No
  number changed; page 1 of the built PDF read and correct.
- Supplementary Table S1-S6 headings: the Unicode em dash could not be set in the
  heading font and was silently dropped from the PDF; now LaTeX `---`.
- `data/adult.csv` is tracked (`/data/` -> `/data/*` plus a negation), regenerated
  from OpenML 1590 via `src/data_loading/adult.py`; every Table S3 claim
  re-derives from it.
- `pubs-sync.yml`: `build_meta.env` excluded from the freshness diff (it holds a
  machine path and mtime, so that step could never pass).

### Blockers/Issues

- **EXP4 `.pyc` files are gone.** They were never committed on any branch and
  existed only on the old laptop. The reconstructed sources verified against them
  on 2026-08-28 (RCA-002) are all that remain; that verification cannot be
  repeated. **Resolved by author decision (2026-09-27): hash pins.**
  `scripts/pubs/exp4_source_pins.json` pins all 16 files as of `357a03201`;
  `verify_exp4_reconstruction.py` checks them (and still runs the bytecode
  comparison if the `.pyc` files ever return). RCA-002 guard invariants updated.
- **Author decision (2026-09-27): re-run the three EXP4 LLM judges** to obtain raw
  data. This is a NEW cohort, not a reproduction: the templates are lost, so the
  prompts must be rebuilt from Supplementary Table S1, and the output goes to its
  own directory beside, never over, the committed aggregates. **COMPLETE
  2026-09-27: 5,184/5,184 calls (US$20.24)**, same 192 cases, judges
  gpt-5.4-mini / claude-haiku-4.5 / gemini-3.8-flash via OpenRouter; 11
  provider errors retried (kept in `failed_attempts/`); 5,180 parse. Raw data
  and analysis committed; findings in `experiments/exp4_cohort2/RESULTS.md`.
  Headline: hidden_label ICC still < 0.75 on every dimension but CIs cross it
  on two; rubric_alt puts completeness at 0.753; default pooling puts two
  dimensions above 0.75. Manuscript impact is an author decision (OPEN).
- **EXP4 cannot be recomputed from raw data** (author asked 2026-09-27). A full
  forensic search - all Git history and refs, unreachable objects, GitHub
  releases and artifacts, this laptop - found no raw judge responses, templates
  or bytecode. The committed aggregate CSVs (`f6591d680`) are intact and still
  back every published EXP4 number; nothing was recomputed or changed. Record:
  `docs/review/exp4-forensic-search_2026-09-27.md`; RCA-002 has an addendum.
- **pubs-sync was red on every run checked (40, back to at least 2026-09-07)**:
  the claims step failed on the untracked `data/adult.csv`, the EXP4 job on the
  untracked bytecode. "Green under all three verifiers" held only on the old
  laptop. The first cause is fixed here; the second is the bytecode above.
- `.aceconfig` and `.ace/` (except `standards/`) were local-only and did not
  survive the move. **Restored 2026-09-27:** upstream framework v2.7.0 from
  `github.com/jonnabio/ace-framework`, plus the recorded project
  customizations:
  - the Scientific Advisor role and `PEER_REVIEW` routing;
  - the manuscript-editing, scientific-rigor-review and reference-audit
    skills, rebuilt from their descriptions and the surviving reports;
  - the trigger keywords;
  - a verification gate and pre-commit hook running the three verifiers.

  The project-specific files are now tracked (ADR-0013 amendment). The skill
  texts are reconstructions, not the lost originals.

### Notes

- Worktrees on this laptop: thesis lane in the main checkout, paper lane at
  `../xai-paper-bc`; `core.longpaths` is on. Python 3.13 is at
  `%LOCALAPPDATA%\Programs\Python\Python313`; Tectonic 0.17.0 portable in the
  paper worktree's `tools/tectonic-portable/`.
- `core.autocrlf=true` here: regenerating fragments marks all of them modified
  though only line endings differ. `git diff --ignore-cr-at-eol` shows the real
  change.

## Session Handoff - 2026-09-28

**Paper B+C pre-submission review for TMLR. Review done, plan written, filing blocked
on remediation.** All work is on the paper lane (`paper/bc-venue-definition`,
worktree `../xai-paper-bc`), head `3929936e3`, pushed.

### Completed

- **Author confirmations (2026-09-28):** the detailed revision is finished; the paper is
  not under review at any other venue; the 28 reconstructed corpus rows were verified by
  the author earlier (Next Steps 0a closed, `d1299e3e2`). Recorded in
  `OPENREVIEW_SUBMISSION.md` (`6c92be577`).
- **Review plan:** `docs/planning/paper_bc_tmlr_review_plan_2026-09-28.md` (`a3258e80e`).
- **Phase 1 rigor review:** `docs/review/scientific-rigor-review_paper_bc_tmlr_2026-09-28.md`
  (`df6a86b1b`). Grade: Major revision, mean 3.4. The 2026-07-28 findings F01/F02 were
  confirmed fixed. The major findings:
  - **F01:** "TreeExplainer reverses latency for tree models" (abstract, Tier 1) is false for
    RF, which was SHAP-slower in 15/15 cells; only XGBoost is faster.
  - **F02:** Paper A's published SHAP/LIME mean costs (11,708.3/3,660.7) are restated, and
    Figure 1 plots the per-method levels. The shared-result query missed both because
    `appears_in` lacked the Paper A site.
  - **F03:** the abstract and the body contradict each other on LIME instability
    ("one-hot encoding" vs "structural").
  - **F04:** the screening table counts 4 lost papers as full-text exclusions, and the search
    log is not released.
  - **F05:** Table S5 is unbacked, disagrees with S2, and is undisclosed.
  - **F06:** the "optimally aligned" axiomatic claim is unsupported.

  There are also minors F07-F12 and suggestions F13-F15.
- **Remediation plan:** `docs/planning/paper_bc_tmlr_remediation_plan_2026-09-28.md`
  (`65089a2b4`, decisions `22f8f26c8`, Step 0 outcome `12d2b8660`). Steps 0-8, ~10-11 h.
- **Author decisions:**
  - Q1: redraw the EXP3 figure as gaps only.
  - Q2: the search log is treated as lost; the caption says the counts are not released.
  - Q4: Tier 1 is conditioned on XGBoost, with "measure first" for other ensembles.
  - **Q3/F10: won't-fix. Do not disclose or mention the EXP4 prompt question anywhere.**
- **Step 0 done (`b2ee05ce7`):**
  - Reference audit, `docs/review/reference-audit_paper_bc_tmlr_2026-09-28.md`: 60 entries;
    8 unused; 3 metadata errors (fok year, wilming volume, zheng2023 DOI); 2 preprints with
    published versions; 3 unverified; 1 mojibake label.
  - Coverage triage, `docs/review/coverage-triage_paper_bc_tmlr_2026-09-28.md`: 73
    unregistered literals, of which 44 re-derive, 22 are structural, 4 are unbacked (S5)
    and 2 are wrong (F07). It also produced two new minor findings, F16 and F17.
- **F16 and F17 fixed (`3929936e3`):**
  - The EXP6 sample is now "five RF runs at N=50, one per seed", with a note that five pairs
    cannot reach α=0.05.
  - The cost ratio is now "median per-cell ratio 5.3×".

  No number changed. The verifiers are green, and both PDFs were rebuilt with 0 undefined
  references.

### Current State

- The Paper B+C manuscript differs from the 2026-09-27 gate record, so the built package
  (bundle, sheet abstract) is **invalid until Step 8**.
- The verifiers are green (257 claims / 429 sites), but Paper B+C is still outside `[coverage]`.
- All four worktrees were clean and pushed at close. The chapter worktree was 1 commit behind
  origin.

### Next Steps

1. **Fresh Scientific Editor session, remediation Step 1:** register the remediation values,
   the 44 re-deriving literals, the structural declarations and the S5 `[[unbacked]]`
   entries. Add the Paper A site to `exp2.run.shap.cost.mean` and its LIME counterpart.
   Two new resolvers are needed: the paired t-CI, and the composed EXP3 SHAP-LIME gap.
2. **Steps 2-3 (critical path):** F01/F03/F09 through `pub/claims.toml`, then the page-1
   PDF read. F02: delete the means sentence; redraw Figure 1 as paired differences; make
   the EXP3 figure gaps-only; add `scripts/pubs/scan_shared_literals.py` to the gate.
3. **Steps 4-7:** F04, F05, F06; the minors; the references (R01-R10); then Paper B+C
   into `[coverage]` (a trunk event).
4. **Step 8 (QA, fresh session):** the whole "After any revision" checklist, then a
   written report to the author. Filing waits for it.

### Blockers/Issues

- **Filing is blocked** until at least F01, F02 and the Step 8 re-verification are done.
- **F02 exposed a gap in RCA-001:** the prior-publication check depends on complete
  `appears_in` registration. Record this in RCA-001 when the scan script lands.
- Possible thesis-lane follow-up: if the thesis still says "structural" LIME instability, or
  repeats the tree-latency generalisation, open a thesis item (sync matrix).

### Notes

- The paper `.tex` files use CRLF line endings: Python `str.replace` on `
` fails, so use
  the Edit tool.
- Coverage triage without touching the registry: copy `pub/claim_registry.toml` to the
  scratchpad, add the files to `[coverage]`, then run
  `verify_claims.py --registry <copy> --coverage-report`.
- Crossref lookup script pattern: see the reference audit's method section. Title queries
  often return unrelated works; treat those as unverified, not as mismatches.
- Build: `tools/tectonic-portable/tectonic.exe <file>.tex`, run from
  `docs/reports/paper_bc/` in the paper worktree.

## Session Handoff - 2026-09-28 (second session)

**Paper B+C remediation Steps 1-7 complete. Only Step 8, the submission gate, stands
between the paper and filing.** Plan and per-step record:
`docs/planning/paper_bc_tmlr_remediation_plan_2026-09-28.md` (paper lane).

### Completed

- **Step 1** (`4267145ac`): registered every value the fixes print, before any prose edit.
  - Registry 257 -> 320 claims, 429 -> 491 sites.
  - 8 new resolvers in `scripts/pubs/claim_sources.py`: paired-cell stats, paired t-CI, stratum
    dispersion, second-reviewer audit, cohort 2 score floor.
  - Registration surfaced **F18** (the CV table was labelled a stratum median but prints the
    RF/N=100 cell) and **F19** (the German Credit gap ranges were wrong).
- **Step 2** (`91766b04d`):
  - **F01:** the tree-latency claim is scoped to XGBoost; RF was SHAP-slower in 15/15 cells.
  - **F03:** one scoped account of LIME instability everywhere.
  - **F09:** "SHAP leads on every fidelity- and stability-oriented endpoint".
  - The abstract went through `claims.toml`, and page 1 was read from the PDF.
- **Step 3** (`85c65557a`, `b37fae1ff`), **F02:**
  - The Paper A mean costs are removed and retired.
  - Figure 1 is redrawn as paired differences with CIs, and the EXP3 figure shows gaps only.
  - New `scripts/pubs/scan_shared_literals.py` finds overlap with Paper A without the registry.
    It is report-only in CI and `--strict` in the gate, and is listed under RCA-001.
  - The editor note now says fifteen results were removed.
- **Step 4** (`c5457ab9c`):
  - **F04:** the screening table shows 47/48/4/44, and the record is stated as not released.
  - **F05:** the Table S5 provenance is disclosed.
  - **F06:** the axiom paragraph is rewritten as an untested mechanism.
- **Step 5** (`8caf2b29e`): F07, F08, F11, F12, F18 and F19 fixed.
- **Step 6** (`f6c244dd1`): F13-F15; bibliography reduced from 60 to 52 entries, all cited, with
  metadata fixes verified against Crossref.
- **Step 7** (`0e1510a16`): Paper B+C and its supplementary added to `[coverage]`.
  - Merged to main by fast-forward, then into the thesis lane (`3a5ec41ee`) and the chapter
    lane (`ec70f7da2`).
  - CI pubs-sync is green on main.
- **PDFs rebuilt at close** (`8b118ddf7`): 26 + 5 pages, 0 undefined references, text identical
  to the Step 6 build.
- **Config:** `configs/secrets/api_keys.env.example` (key-free template) committed
  (`69808653d`). The real `api_keys.env` stays gitignored.

### Current State

- Verifiers green: 320 claims / 491 sites / 35 retired guards / 21 files fully registered.
  The shared-literal scan reports 0 unexplained matches.
- The 2026-09-27 gate record in `OPENREVIEW_SUBMISSION.md` is **invalid**: the manuscript, the
  abstract, the figures and the bibliography have all changed since.
- All lanes were merged and pushed at close.

### Next Steps

1. **Step 8, in a fresh QA session:** run the whole "After any revision" checklist in
   `OPENREVIEW_SUBMISSION.md`.
   - Check both PDFs and page 1.
   - Build the de-anonymised variant once, for the availability sentence.
   - Run the three verifiers, then `scan_shared_literals.py --strict`.
   - Run the identity scan on both PDFs and the bundle.
   - Rebuild the bundle.
   - Regenerate the sheet's abstract, counts and stamp.
   - Mark each finding F01-F19 against its commit, and append a post-fix status to the review.
   - Give the author a written report.
2. **Author:** file on OpenReview, then email the editor note to tmlr-editors@jmlr.org.
3. **Thesis lane (not blocking filing):** the same defect class as F01/F03.
   - Ch.4 l.193: "no es marginal, sino estructural".
   - Ch.6 P1 row: "incoherencia estructural".
   - Ch.4 l.620: TreeSHAP efficient "para modelos basados en árboles"; scope it to XGBoost as
     Ch.6 l.134-136 does.

### Blockers/Issues

- None blocking. F10 is closed as won't-fix by author decision: never disclose or mention
  the EXP4 prompt question.
- A pre-existing 2 pt overfull box at the end of `tab:hybrid_deployment` is cosmetic, and was
  left unchanged.

### Notes

- **Retired texts** must be added in the commit that removes them, not earlier: a retired
  string still present in the manuscript fails the verifier.
- **Negative-test every new check by planting inside the body.** The shared-literal scan
  ignores everything after `\begin{thebibliography}`, so a planted value appended at the end of
  the file proves nothing.
- `generate_fragments.py` rewrites every fragment. Commit only `paper_bc_abstract_en.tex`
  and `build_meta.env`, and discard the rest after `git diff --ignore-cr-at-eol` shows they
  are empty.
- Plotting needs `pandas`/`matplotlib`, which are now installed in Python 3.13. The figure
  generators are `scripts/generate_paper_b_figures.py` and
  `scripts/generate_exp3_gap_figure.py`.

## Session Handoff - 2026-09-28 (third session)

**The CIFIE science-first assessment and chapter-architecture task is complete.
The active objective is now Task 3 / RCA-001 Phase 2.**

### Completed

- Closed the former CIFIE requirements blockers by author direction: there is no
  publisher template and no hard word-count limit; the chapter will use a highly
  scientific but readable register, APA 7 citations and references, and a final Word
  document visually aligned with the thesis standards.
- Created the general assessment, science-first revision plan, and detailed chapter
  scaffold under
  `publications/book_chapters/2026_cifie_xai_fom7/planning/`.
- Adopted the working title *De la explicación a la evidencia: fundamentos,
  aplicaciones y evaluación auditable de la inteligencia artificial explicable*,
  with FOM-7 retained as the bounded methodological contribution in the subtitle and
  empirical case.
- Rebuilt `manuscript/chapter_outline.md` and
  `manuscript/00_hoja_diseno_editorial.md` around the general XAI overview, five
  application domains, seven scientific-gap categories, FOM-7, and the protected
  Adult/tabular case. The existing eleven-file build contract is preserved.
- Staged 17 verified candidate sources, including systematic reviews, official
  frameworks, primary human studies, and counterevidence. They remain outside the
  production bibliography until cited in revised prose. Updated the evidence map,
  source inventory, citation audit, and chapter README accordingly.
- At the chapter checkpoint, protected verification passed: 257 claims re-derived,
  429 manuscript sites checked, 26 retired-value guards clear, 15 files clear of
  unpublished Paper B+C results, paper/thesis fragments synchronized, and all 18
  EXP4 source hashes matched. The larger repository totals subsequently advanced
  during Paper B+C remediation and remain governed by the same checks.
- A Word render was deliberately not produced at this checkpoint because the new
  title and architecture would still be paired with the legacy chapter body. Render
  and page-level visual QA resume after the first integrated prose unit.

### Transition

- **Active next task:** Task 3 / RCA-001 Phase 2 on
  `thesis/rca-001-phase-2`: generate registry-backed LaTeX macros and Quarto inline
  values, then add CI builds that fail on undefined references and cross-reference
  warnings.
- **Queued CIFIE continuation:** rewrite sections 02 and 03 from the approved evidence
  architecture, transfer only cited candidates into the APA 7 production
  bibliographies, then create the application section 04.
- All standing constraints remain in force, including ADR-0013 lane separation,
  ADR-0018 CIFIE exclusivity, the protected-claim verifiers, and the Paper B+C
  pre-submission rebuild and re-review gate.

## Current Objective
**Two workstreams, one per lane (ADR-0013).**

**`paper/bc-venue-definition` — Paper B+C, TMLR: PAUSED for author revision
(2026-09-15).** The submission package is complete and was verified on
2026-09-14, but the author is revising the manuscript in detail. The package
must be regenerated and re-reviewed against the revised manuscript before
filing — see the submission gate in the 2026-09-15 handoff. Do not submit
before that re-verification, and do not submit before sending the editor note.

**ACTIVE — `thesis/rca-001-phase-2` — Task 3, RCA-001 Phase 2: make each
published number exist in exactly one place.**
This is again the active objective after completion of the 2026-09-28 CIFIE
assessment and scaffold task, and again after completion of the 2026-10-03
repository consolidation task. It is worked in the main folder on
`thesis/rca-001-phase-2`. First unit: continue the coverage sweep with
`thesis/apendices.qmd` (then `capitulo-1`, `capitulo-2`, `introduccion` and
Paper A), before the macro generation and the CI build job.
Generate the `pub/claim_registry.toml` values into LaTeX macros and Quarto inline
values so the manuscripts consume them rather than restating them, and build all four
outputs in CI, failing on undefined references and crossref warnings. Phase 1 verifies
that a manuscript number still matches its artifact; Phase 2 removes the opportunity
for it to diverge at all, and closes the one gap Phase 1 cannot cover — render-time
defects like A13, which was found only by rebuilding.

Standing workstream (unchanged): maintain the CIFIE/FOM-7 book chapter and its ACE
manuscript-editing support tooling.

**Third lane, 2026-09-27: `chapter/cifie-sync-2026-09`** (ADR-0013 `chapter/cifie-*`).
The chapter is synced to the verified results: retired values and pre-audit profiles replaced, and the
tutor corrections applied. It is kept free of Paper B+C results by ADR-0018, enforced in CI
(`[exclusivity]`), and put under `[coverage]`. The build is `scripts/build_cifie_chapter.py`.
Tables 1-4 were converted to final APA form and the uncited Altukhi (2025) was
dropped (2026-09-27). The science-first assessment, evidence staging, and production
scaffold were completed 2026-09-28. The next chapter unit is queued after Task 3:
rewrite sections 02 and 03, then create the application section 04. The thesis is
still cited as unpublished (noted).

See `docs/review/cifie-chapter-sync_2026-09-27.md`.

## Current State

### Working
- **Paper B+C is ready to submit to TMLR (2026-09-06).** 26 pp plus a 5 pp
  supplementary, official `tmlr.sty` unmodified, anonymous under double-blind,
  zero results shared with the published RIMI paper, Broader Impact Statement
  present, artifacts released as a 3.8 MB anonymised bundle from which all 48
  of its registered claims re-derive. Submission artifacts:
  `docs/reports/paper_bc/paper_bc_tmlr.tex` / `.pdf`,
  `paper_bc_tmlr_supplementary.tex` / `.pdf`,
  `paper_bc_artifacts.zip` (gitignored; rebuild with
  `scripts/pubs/build_artifact_bundle.py`),
  `EIC_ENQUIRY_prior_publication.md`, `BUILD.md`, and the readiness record
  `docs/review/tmlr_readiness_checklist_2026-09-06.md`.
- **Task 1 (closed 2026-08-26):** Paper B+C's review corpus released as a 44-row coded
  CSV, CI-verified against the manuscript's printed distribution; reconstruction
  disclosed in §Validity. Author verification still wanted on the 28 reconstructed
  coding rows before submission.
- **Task 2 (closed 2026-08-28):** F03 and F04 resolved. All 16 EXP4 source files
  recovered from bytecode and verified; ICC relabelled ICC(1,1); Supplementary Tables
  S3 and S6 corrected; EXP4 rubric citation corrected in three documents. See RCA-002.
- Manuscript-claim enforcement now covers the supplementary document as well as the
  main text: 61 claims, 111 manuscript sites, 16 retired-value guards, 10 cited
  artifacts, plus both review corpora and the EXP4 reconstruction, all in CI.
- Thesis/Paper synchronization pass completed for validation-boundary language and EXP3 scope. The sync matrix is available at `docs/reports/sync/thesis_paper_sync_matrix.md`.
- New `Scientific Advisor` role added to `.ace/roles/roles.md` (idea/hypothesis critique, manuscript rigor review, reference audit), sitting between Data Scientist/AI Expert (research) and Scientific Editor (publication) in the Research Workflow.
- New project-local skill `.ace/skills/scientific-rigor-review/SKILL.md`: adapts the ai-research pack's ARA-directory `rigor-reviewer` (6-dimension epistemic review) to plain manuscript/thesis-chapter prose. Produces severity-ranked reports to `docs/review/scientific-rigor-review_*.md`. Read-only on the manuscript.
- New project-local skill `.ace/skills/reference-audit/SKILL.md`: bibliography dedup, orphaned/unused citation detection, APA7 consistency checks, and re-verification via `paper-lookup`. Produces reports to `docs/review/reference-audit_*.md`. Report-only by default; does not edit `.bib`/reference files without explicit instruction.
- `.aceconfig` updated: added `PEER_REVIEW: Scientific Advisor` to `role_routing`, and trigger keywords `idea review`, `hypothesis review`, `peer review`, `science correctness`, `methodology review` → scientific-rigor-review; `references`, `bibliography`, `duplicate citations`, `citation dedup` → reference-audit.
- `.ace/packs/scientific/.aceconfig-ext` updated: added `scientific rigor` / `reference audit` triggers and `Scientific Advisor` to `roles_augmented`.
- Project-local reusable manuscript editing skill available at `.ace/skills/manuscript-editing/SKILL.md`.
- `.aceconfig` now maps `cifie`, `book chapter`, `manuscript editing`, `publication editing`, `academic manuscript`, `citation editing`, and `literature enrichment` to the reusable skill.
- The skill supports Spanish academic prose revision, APA 7 consistency, evidence traceability, open-access literature enrichment, FOM-7 terminology preservation, and submission-readiness checks.
- Sections 09 and 10 have been strengthened with verified open-access XAI evaluation sources supporting multidimensional evaluation, functionally grounded benchmarks, and human/application-grounded limits.
- `10_limitaciones_trabajo_futuro.md` has been revised into a stronger academic Spanish section aligned with FOM-7 evidence boundaries, with expanded in-text citations for metric dependence, method configuration sensitivity, human validation limits, recourse constraints, coverage gaps, and future-work priorities.
- `02_introduccion.md` has been revised into a stronger academic Spanish introduction that frames FOM-7 as a response to the evidentiary gap in XAI evaluation, with expanded APA-style in-text citations for opacity, post-hoc methods, metric fragmentation, functional evaluation, toolkits, and auditable evidence.
- `02_introduccion.md` received a follow-up polish aligning its evidentiary language with section 03: explanation as evidence must not confuse narrative persuasiveness with technical validity, and FOM-7 preserves the relationship among artefact, construct, test, result, and claim.
- `03_fundamentos_xai.md` has been revised through a literature-enrichment loop into a stronger foundations section. It now distinguishes artifact type, interpretability, explainability, transparency, local/global scope, plausibility, fidelity, stability, robustness, metric proxies, and the functionally-grounded scope of FOM-7.
- `@miller2019` was added to the CIFIE references to support the social/contrastive dimension of explanation while keeping the manuscript clear that audience plausibility is not technical fidelity.
- **Thesis front matter, presentation and table/figure formatting (closed 2026-08-30;
  see Session Handoff above for the full record):** cover page, Dedicatoria,
  Agradecimientos, official title, Spanish crossref labels, resolved section references and
  hierarchical heading numbering. The rendered DOCX now reads: p1 cover, p2 TOC, p3 Dedicatoria,
  p4 Agradecimientos, p5 Resumen. Integrity in the render: raw slugs 0, unresolved crossrefs 0,
  doubled labels 0, English crossref prefixes 0.
- `scripts/enforce_docx_thesis_format.py` is the thesis presentation layer, all of it driven
  from version-controlled sources rather than the binary template:
  `merge_paragraph_properties`, `insert_cover_page` (+ `thesis/cover.txt`),
  `insert_break_after_toc`, `number_headings` (+ `collect_unnumbered_titles`, which reads the
  `{.unnumbered}` markers from the .qmd sources because the rendered DOCX gives numbered and
  unnumbered headings identical style and pPr), `format_tables` (+ `set_table_borders`,
  `bolden_header_row`, `is_layout_wrapper`) and `centre_captions_and_figures`.
- **Resumen and Abstract rewritten (closed 2026-09-02):** four major and three minor
  editorial findings closed, including a claim the body had retracted five weeks
  earlier; both are mirrored and regenerated from `pub/claims.toml`. See the
  2026-09-02 Session Handoff.
- **Dedication-style front matter (closed 2026-09-02):** Dedicatoria and
  Agradecimientos in right-aligned italics under centred upright headings, generated
  post-render.
- **Top-level statement sweep (added 2026-09-02):**
  `docs/review/top-level-statement-sweep.md` maps the 14 statements read as promises
  — objetivo general, OE1-6, H1-H3, P1, P2, Resumen, Abstract, `tbl-estudios` — to the
  body sections whose correction would falsify them, with the checks that catch the
  mechanical half and a sweep log. Wired into RCA-001 as a review trigger.
- **RCA-001 Phase 2 coverage sweep, in progress (2026-09-04):** three of ten files
  enforced (Ch.4, Ch.6, Ch.5); 166 claims / 270 sites; `diff` and `exp2_missing_pct`
  resolvers added. Two defects found in Ch.6, none in Ch.5. See the 2026-09-04
  Session Handoff.
- **Repository consolidation (closed 2026-10-03):** `main` rebuilt from `origin/main`
  without the merge-and-revert pair and now holding Papers D, E and F, the chapter
  commits and all handoffs. `main`, `thesis/rca-001-phase-2`,
  `chapter/cifie-sync-2026-09`, `results/exp4-cohort2`,
  `paper-d/tecnologia-en-marcha`, `paper/e-feature-agreement` and
  `paper/f-external-validity` were level and pushed at close, each folder with no
  uncommitted files. Verifiers green on that commit: 479 claims / 645 sites / 48
  retired-value guards; sync; 18 EXP4 pins.
- **One working tree per paper (ADR-0021, 2026-10-03):** `../xai-paper-d`,
  `../xai-paper-e` and `../xai-paper-f` join the main folder (thesis),
  `../xai-chapter` and `../xai-exp4`. Paper B+C stays in the main folder (ADR-0019).
- **Papers D, E, F (2026-10-03):** D complete, files in
  `docs/reports/paper_d/submission/`, awaiting the author's items; E has results in
  `outputs/analysis/paper_e/` and no manuscript; F has a plan only.

### In Progress
- **Task 3 — RCA-001 Phase 2** (see Current Objective): registry values into LaTeX
  macros and Quarto inline values; all four outputs built in CI.
- CIFIE/FOM-7 book chapter publication editing remains a standing workstream; its
  science-first assessment and scaffold are complete, and the next prose unit is
  queued after Task 3.
- Thesis/Paper final scientific-editor consistency checks

### Blocked
- **Resolved 2026-09-28:** the former CIFIE requirements blocker is closed. There is
  no publisher template or hard word-count limit; use APA 7 and a thesis-aligned Word
  render.

## Next Steps
00. [x] **CLOSED 2026-09-30: Paper B+C filed with TMLR as submission 12779 (forum `VkmWJZclmH`); editor note emailed. See "Session Handoff - 2026-09-30". The text below is historical.** **Paper B+C is NOT submitted and is PAUSED for author revision
   (2026-09-15).** OpenReview account active since 2026-09-14 and the package is
   built, but it was verified against the pre-revision manuscript. **Before filing,
   run the "After any revision" checklist in
   `docs/reports/paper_bc/OPENREVIEW_SUBMISSION.md` and report the result to the
   author.** Remaining author confirmation: no concurrent submission. Editor note
   goes by email to tmlr-editors@jmlr.org right after filing, never as a forum
   comment (see the 2026-09-14 and 2026-09-15 handoffs). When the account clears: build the
   bundle with
   `python scripts/pubs/build_artifact_bundle.py` and attach
   `docs/reports/paper_bc/paper_bc_artifacts.zip` as supplementary material,
   and post `EIC_ENQUIRY_prior_publication.md` in the submission's comment
   field at the same time (author's decision: sent with the submission, not
   ahead of it). Still to confirm: the RIMI DOI and journal-title spelling,
   no concurrent submission, and that the Zenodo snapshot is this paper's.
   Full detail and the anonymity build modes: the 2026-09-06 Session Handoff
   and `docs/reports/paper_bc/BUILD.md`.
0. [ ] **Task 3 / RCA-001 Phase 2:** emit registry values as LaTeX macros + Quarto
   inline values; add a CI job building Paper A, Paper B+C, the supplementary and the
   thesis, failing on undefined references and crossref warnings.
0a. [x] Author-verify the 28 reconstructed review-corpus coding rows before submission. **Done by the author before 2026-09-28** (confirmed in session 2026-09-28). Also confirmed 2026-09-28: Paper B+C revision finished; no concurrent submission. Pre-submission review plan: `docs/planning/paper_bc_tmlr_review_plan_2026-09-28.md` (paper lane).
0b. [ ] RCA-002 leftovers: re-run and archive the Table S5 `num_samples` probe (its
   script `src/scripts/run_sensitivity_analysis.py` is committed); decide final
   disclosure wording for the lost raw judge data and the three EXP4 Jinja templates.
0c. [x] **Thesis rigor review 2026-08-28 remediation — COMPLETE 2026-08-28.** All 13
   findings closed in 11 commits (e7d1f01f4..35eccb62b), plus F14/F15 found and fixed by
   the new coverage check. Plan:
   `docs/planning/thesis_rigor_remediation_plan_2026-08-28.md` (Architect, 2026-08-28).
   Blast radius verified: **F02 and F04 are thesis-only** (Paper A carries only the registered
   aggregate costs); only F01 crosses documents, into one Paper B+C paragraph (~l.1297);
   Paper A §636 and Supplementary Table S2 are already correctly scoped.
   Author decisions taken 2026-08-28: **D1 = Option A** (defend the narrow,
   configuration-/feature-space-scoped LIME instability claim; EXP3's 0.75-0.93 and Appendix C's
   kw=10.0 -> 0.664 become a second reported finding rather than contradictions);
   **D2 = re-run the Table S5 num_samples probe, 1h timebox**, falling back to historical
   disclosure (closes the RCA-002 leftover either way); **D3 = keep "prescriptivos"** plus a
   scope sentence, promoted to T2.9 now that T2.4 removes the threshold tension.
   Plan is registry-first by design: Phase 1 registers 20 per-model cost cells + 10 SHAP quality
   cells + 4 retired-value guards BEFORE any prose edit, because F02/F03/F08/F09 all passed a
   green verifier for want of registration, not for want of accuracy.
   Critical path Phases 1-3 ~9h; Phase 5 (F13 unregistered-literal check) folds into Task 3.
   Detail of the finding list below / in the review:
0d. [ ] (superseded detail) original per-finding priority order (see
   `docs/review/scientific-rigor-review_thesis_2026-08-28.md`). Priority order:
   F01 (scope the LIME "structural instability" claim in Ch.6 §sec-limitaciones,
   §sec-sintesis and Ch.5's opening — it currently contradicts Appendix C and EXP3),
   F02 (re-derive the four prescriptive cost ranges; rewrite the DiCE recommendation),
   F04 (make the SHAP F>=0.80 / S>=0.70 thresholds conditional on model family),
   F06 (define the Brechas or drop the numbering), then F05/F07/F09 (sentence-level).
   If time allows: F03, F08, F10, F11, F12. All targets are RCA-001-guarded; run
   `verify_claims.py` + `verify_sync.py` and register new numbers rather than typing them.
1. [x] Resolve the 2026-08-11 thesis-review findings F01/F02/F03 in Ch.4/Ch.5/Ch.6 —
   verified fixed by the 2026-08-28 re-review.
2. [ ] Re-run targeted consistency check for EXP3 mentions after any future Paper A or Paper B+C edits.
3. [ ] Verify final rendered PDFs after publication manuscripts stabilize.
4. [ ] Use `manuscript-editing` with the CIFIE/FOM-7 profile for future CIFIE section revision passes.
5. [ ] Continue APA/citation and compression checks once final CIFIE requirements are confirmed.
6. [ ] Validate final submission artifacts after manuscript stabilization.
7. [ ] Run `Scientific Advisor` (`scientific-rigor-review` + `reference-audit`) against the CIFIE chapter and/or Paper A/B+C once each is near-final, before final submission.
8. [x] **Done 2026-08-30.** Stale remote branch `publication/cifie-xai-fom7-book-chapter`
   deleted on origin. It was fully merged into `main`, so nothing became unreachable.
9. [ ] Refresh the Table of Contents in Word - `render.ps1` prints this reminder every run and it
   is the one step the pipeline cannot do itself.
10. [x] **No action needed - the item was wrong.** The corpus PDFs are already formally
    ignored: `.gitignore:78` carries `docs/reports/paper_bc/corpus_pdfs/*.pdf`, added in
    `1a9c0a6af`. The claim that they were un-ignored came from grepping `.gitignore` while the
    tree was still on the pre-merge `main`, whose copy predates that rule. The decision was
    taken deliberately and stands: ~142 MB of third-party publications, 17 of them duplicates of
    `thesis/papers/`, are not redistributed through the repository. What is tracked is the
    evidence the manuscript rests on - `paper_bc_review_corpus.csv`, `corpus_pdfs/README.md` and
    `RETRIEVAL_LOG.md`, the last recording a source URL and verification per paper so the set is
    reproducible via `scripts/pubs/fetch_corpus_pdfs.py`. `check_corpus_pdfs.py` is not in CI and
    tolerates the directory being absent.
    **Residual risk, unchanged:** the retrieved files themselves live only on this machine, and
    two were supplied by the author under institutional access rather than fetched. Worth a
    backup outside git before deposit.

- **Mode (2026-08-28, third pass):** EXECUTION — Developer applied the rigor-review
  remediation, Phases 1-3 of the approved plan, in 8 atomic commits:
  F01 (e7d1f01f4), F02 (ed54a97ec), F04+F12 (9baf99921), F03 (fdee4e9bf),
  F08+F09 (6046171ac), F05+F07 (d398bcb8f), F06 (46fab539f), Paper B+C F01 +
  sync matrix (dd589660c). **No statistic changed in any commit.**
  Registry grew 61 -> 83 claims and 111 -> 157 manuscript sites: 13 per-model cost
  claims, 8 per-model SHAP quality claims, supp.s2.kw10.fidelity, plus 5 new
  retired-value guards (F01.lime.kernel_independence and F02.{dice,lime,treeshap,
  anchors}.cost_range). The F02 guard was negative-tested: reinserting "770-4,500"
  fails verify_claims.py with exit 1.
  **F03 took the D2 fallback.** The re-run was not attempted because the surviving
  script `src/scripts/run_sensitivity_analysis.py` sweeps {500,1000,2000,5000,10000}
  over the EXP1 base config, not the appendix's three levels at RF/seed42/N=100 —
  running it would produce a new measurement, not a reproduction of Table S5 (the
  same reasoning RCA-002 applied to re-running the EXP4 judges). Table S5 is now
  disclosed as a historical exploratory probe, with the two probes' disagreement
  stated explicitly and both held to their directional conclusion. This closes the
  RCA-002 leftover by disclosure. **Do not re-run that script expecting Table S5.**
  Blast radius confirmed during execution: F02 and F04 were thesis-only; Paper A
  needed no edit at all (its §636 was already correctly scoped); the Paper B+C
  supplementary was already correct — only its main-text summary of Table S2 had
  dropped the kw=10.0 row while citing the table.
  Verification: verify_claims.py, verify_sync.py and verify_exp4_reconstruction.py
  all green; crossrefs 70 labels / 0 dangling; all four outputs rebuilt clean
  (3 PDFs via tectonic-portable, thesis DOCX via render.ps1) with no undefined
  references; the four retired cost ranges absent from all sources.
  Still open: F10 (chi2~15.2 underived) and F11 (Anchors MNAR bias direction) as
  accepted suggestions, and F13 -> Task 3.

- **Mode (2026-08-28, fourth pass):** EXECUTION — Phases 4 and 5 of the remediation plan.
  **All 13 review findings now closed** (F10 `df49569b0`, F11 same commit, F13 `35eccb62b`).
  F10's figure turned out to be arithmetically exact but mislabelled: 30.44/2 = 15.22 and
  P(chi2_3 > 15.22) = 0.0016 is *halving the statistic*, not a 50% power reduction. The
  passage now shows the operation and adds the noncentrality reading (16.72, p = 0.0008) so
  the conclusion holds under either. F11 bounded the Anchors MNAR bias empirically with the
  tau=0.90 row: coverage 76->96% and fidelity 0.386->0.421, so the bias is real, moderate,
  and does not move Anchors off third/fourth.
  **F13 built the check that closes the defect class.** `verify_claims.py` gained a fourth
  check, `_check_coverage`: for files listed under `[coverage]` in the registry, every
  result-shaped numeric literal must be registered, retired, `[[unbacked]]`, or declared
  structural. `[[unbacked]]` is the escape hatch and the point — "we cannot re-derive this"
  becomes a reviewable entry with a reason instead of a silent gap. `--coverage-report`
  triages a new file without failing. Negative-tested: an invented "4,321.9" in Ch.4 fails
  with exit 1.
  **The Ch.4 sweep found two more defects that four prior audits read past.**
  **F14:** the P1 table is attributed to the wrong artifact — `tbl-claim-traceability` and
  Appendix D both cited `exp1_adult/reproducibility/reproducibility_report.csv`, a different
  cohort (n_runs=9, rf/xgb only, RF/SHAP fidelity 0.737 vs the table's 0.732). All twelve
  values re-derive exactly from the EXP2 run-level table, RF/N=100, five seeds, sample SD.
  Numbers right, provenance pointer wrong — in the table that demonstrates FOM-7 gate 7.
  **F15:** the pooled fidelity CV was wrong and the comparison inverted. LIME's 12.0% is
  right (11.96%); SHAP is 11.43%, not 12.8%, and no aggregation tested reproduces 12.8. SHAP
  is the *more* reproducible of the two, not the less. Both corrected and registered.
  Registry 84 -> 138 claims, 159 -> 219 sites, via 9 new resolvers (exp2_subset_{mean,sd,cv},
  exp2_n_mean, exp2_pooled_cv, exp2_sd, exp2_block_sd, friedman_rank,
  wilcoxon_{meandiff,sd}). RCA-001 gained two invariants and a review trigger.
  **Coverage is Ch.4 only.** Ch.3, Ch.5, Ch.6, apendices, Paper A, Paper B+C and the
  supplementary are NOT swept — add them to `[coverage]` one at a time, triage with
  `--coverage-report`, before RCA-001 Phase 2's macro generation. F14/F15 are the argument
  for doing it: one swept file yielded two defects in a document already under two guards.
  All four outputs rebuilt clean; all three verifiers green; crossrefs 70 labels / 0 dangling.

- **Mode (2026-08-29):** PUBLICATION — Scientific Editor retired the thesis's letter-based
  study labels. The trigger was OE5 on p. 14 (`capitulo-1-marco-teorico.qmd`), which promised a
  taxonomy that would integrate "los Estudios A y B" — letters the reader does not meet until
  Chapter 3. Three defects behind it: forward references with no antecedent; three competing
  naming systems for the same objects (letter / Paper A-B / EXP1-EXP2, all three colliding in
  Chapter 3's opening sentence); and a scheme that no longer closed, because the LLM inter-judge
  study behind OE6 was formulated after the taxonomy and never got a letter.
  **Canonical names now:** Estudio Omnibus Multimétrico (was A, OE2), Estudio Pareado LIME–SHAP
  (was B, OE3), Estudio Taxonómico (was C, OE5), Estudio de Fiabilidad Inter-juez (was unlettered,
  OE6). OE1 and OE4 are declared transversal to the two empirical studies rather than assigned to
  one. Definition site is the new `{#tbl-estudios}` table in Chapter 1, placed between the specific
  objectives and the hypotheses — before any study name is used in an argument.
  36 sites migrated across `introduccion`, `capitulo-1`, `capitulo-3`, `capitulo-4`, `capitulo-5`.
  **Anchors deliberately frozen:** `#sec-estudio-a`, `#sec-estudio-b`, `#sec-exp4-fiabilidad` keep
  their identifiers though their headings were renamed — they are crossref infrastructure, and
  churning them breaks `@sec-` references for no reader-visible gain.
  **Second, author-directed change:** the thesis now cites no paper. "Paper A"/"Paper B" removed
  from Chapter 3's opening (a pre-existing reference) and from the glossary note. A thesis is a
  self-contained deposit document, and the "Paper B" it named no longer exists under that name —
  it is the merged Paper B+C. This also closes the Paper B vs Paper B+C discrepancy flagged in
  `thesis_paper_sync_matrix.md` by removing the reference rather than correcting it.
  **Out of scope, deliberately:** `outputs/analysis/paper_a_exp2_stats/` paths in `apendices`,
  `capitulo-3` and `capitulo-4` stay. They are artifact locations under the RCA-001 invariant
  "every artifact path a manuscript cites exists in the working tree", and are consumed by Paper A
  and Paper B+C too; renaming is an artifact migration (directory + generating scripts +
  `claim_registry.toml` resolvers), not a prose edit.
  No numeric value, table datum or citation changed; `verify_claims.py` (142 claims, 225 sites,
  26 retired-value guards) and `verify_sync.py` green before and after. Diff line counts are
  inflated by re-wrapping paragraphs to the files' ~78-column prose width. Prior review reports
  that use the old letters are dated records and were **not** rewritten.
  Decision recorded in `docs/adr/0012-thesis-study-nomenclature.md`. Outputs not rebuilt — the
  thesis `.docx` still carries the old labels until the next `thesis/render.ps1` run.
  **Resolved later the same day (OE5/OE6 wording, a content change, not a naming one).** The open
  item was that OE5 claimed only an integrative role while OE6 declared itself derived from the
  taxonomy's Brecha 3, leaving OE6 without a legitimate antecedent. The forward reference first
  considered — OE5 saying "y base de la que se deriva el objetivo 6" — was **rejected**: an
  objective is stated ex ante and must not describe an ex post outcome, which is the very vice
  OE6 admits about itself. Fixed instead from both ends:
  (1) **OE5 gains an ex-ante deliverable** — "y que haga explícitas las brechas de constructo del
  campo". Gap-identification is formulable in advance, is what Chapter 5 already delivers
  (§`sec-taxonomia-brechas`, three gaps) and is already how Ch.1's "Tipo de investigación"
  describes the taxonomic component. OE6 now executes something OE5 promised.
  (2) **OE6 compressed from four sentences to two.** Its epistemic-status defence was stated four
  times over (OE6 itself, the "Estatuto epistémico diferenciado de P2" paragraph, Ch.5 §`sec-exp4-fiabilidad`, the Ch.6 objectives table); in a list where OE1–OE5 are single sentences,
  the four-sentence outlier flagged OE6 as the weak objective before the reader had cause to think
  so. The redundant sentence ("a diferencia de los objetivos 1–5, se formuló una vez construida esa
  taxonomía") is dropped; Brecha-3 traceability, the exploratory/non-confirmatory scope marker and
  both citations are kept, with the status argument left to P2 where the claim is actually made.
  **No scope declaration was retired — only de-duplicated.** Ch.6's OE5 row updated to match
  ("y explicitar brechas de constructo", pointing at the three gaps and Brecha 3 as OE6's origin);
  its OE6 row is left as "Completado (resultado negativo)", which is right: the objective was to
  *quantify*, and a low ICC is the objective met, not failed.

## Active Constraints
- **Paper B+C is not submitted, and no submission proceeds on an unverified package.**
  Any edit to `docs/reports/paper_bc/paper_bc_tmlr.tex`, its supplementary or
  `pub/claims.toml` invalidates the built PDFs, the artifact bundle and the abstract
  copied into `OPENREVIEW_SUBMISSION.md`. Rebuild and re-verify all of them, and hand
  the author a written result, before the manuscript is filed (added 2026-09-15 at the
  author's instruction; the gate exists because a defect on page 1 of the abstract
  survived a green verifier and a readiness checklist on 2026-09-14, RCA-003).
- **Branching is governed by ADR-0013.** Manuscript bodies are branch-private; the claim
  substrate is trunk-owned. A work branch's `pub/`, `scripts/pubs/` and `docs/rca/` may be
  ahead of `main`, never behind it. Lanes: `thesis/*`, `paper/bc-*`, `paper/a-*`,
  `chapter/cifie-*`, `pubs/*` (substrate only), `rca/*`, `results/*`. `main` is never worked
  on directly and must be green under all three verifiers after every merge.
- No commit mixes shared-substrate files (`pub/claim_registry.toml`, `pub/claims.toml`,
  `pub/fragments/`, `scripts/pubs/**`, `docs/rca/**`, the sync matrix, `pubs-sync.yml`,
  `ACTIVE_CONTEXT.md`) with manuscript-body files. Substrate commits reach `main` in the
  session they are made; both lanes then pull `main`. Lanes never merge into each other,
  and `results/*` merges into `main` only.
- Adding any file to `[coverage]` in `pub/claim_registry.toml` is a trunk event: it turns CI
  red on every lane, so it is triaged to `--coverage-report` exit 0 on a `pubs/*` branch and
  merged before any lane consumes it.
- `.git/info/exclude` excludes `/.ace/` and `/.aceconfig`, but the project-specific ACE files
  are tracked (force-added 2026-09-27, ADR-0013 amendment) and reach every worktree:
  - `.aceconfig`;
  - `.ace/standards/*.md`;
  - `.ace/roles/roles.md`;
  - the three project skills;
  - `.ace/packs/scientific/.aceconfig-ext`.

  The upstream framework (other skills, packs, prompts, scripts, workflows, schemas) does not
  reach a worktree. Seed it with `cp -r .ace/. <worktree>/.ace/` (contents, not the directory),
  or reinstall from `github.com/jonnabio/ace-framework` without overwriting tracked files.
  `.aceconfig` `pre_commit` hooks remain local: anything that must hold across lanes belongs in
  `.github/workflows/pubs-sync.yml`.
- `pub/fragments/` conflicts are never resolved by hand: take either side and re-run
  `scripts/pubs/generate_fragments.py`.
- .ace/standards/coding.md
- .ace/standards/security.md
- Keep thesis and paper artifacts read-only unless explicitly instructed otherwise.
- Keep the CIFIE chapter as a distinct publication output under `publications/book_chapters/2026_cifie_xai_fom7/`.
- Thesis study nomenclature is fixed by ADR-0012: functional names (Estudio Omnibus Multimétrico / Estudio Pareado LIME–SHAP / Estudio Taxonómico / Estudio de Fiabilidad Inter-juez), never letters; the thesis names no paper; section anchors `#sec-estudio-a`, `#sec-estudio-b`, `#sec-exp4-fiabilidad` are frozen.
- The official thesis title is Arquitectura Agnostica para la Interpretabilidad de Modelos de
  Inteligencia Artificial de Caja Negra (adopted 2026-08-30). It is authored in
  `pub/claims.toml` and flows to `pub/fragments/thesis_title.txt`; `_quarto.yml`, `index.qmd` and
  `README.md` must agree. Dated review reports keep the superseded title as historical record.
- Cover-page content lives in `thesis/cover.txt`, never hardcoded in the formatting script.
- `number-sections: true` in `thesis/_quarto.yml` is load-bearing: it makes Quarto compute the
  `@sec-` crossref numbers. Do not remove it because headings look unnumbered in the DOCX - the
  numbers are applied post-render by `number_headings`.
- Chapter and section numbers must never be typed literally into headings; they are generated.
- Thesis prose is Spanish; interaction, reports and commit messages are English.
- The Resumen and Abstract are authored in `pub/claims.toml` and regenerated into
  `pub/fragments/`; never hand-edit the fragments, and keep the two languages mirrored
  paragraph for paragraph. Any figure either one cites must be registered in
  `pub/claim_registry.toml` first, with the fragment listed as a site.
- Dedicatoria and Agradecimientos formatting is generated post-render via
  `DEDICATION_SECTIONS`; do not hand-format those sections in the `.qmd` sources.
- Single-cell tables are pandoc layout wrappers, around both captioned tables and
  figures, and must never take a border - bordering them is what framed every figure.
- A number that needs arithmetic over registered values is not `[[unbacked]]`: compose
  it with the `diff:<exprA>|<exprB>` resolver kind. `[[unbacked]]` is reserved for
  values that genuinely cannot be re-derived.
- Wherever a gap, range or mean could be read at more than one aggregation level, the
  level must be stated in the sentence (RCA-001 invariant 6).

## Session Notes
- Synchronized thesis, Paper A, and Paper B+C around the June 13 validation-boundary assessment: functionally grounded comparative evidence is retained as the supported contribution; synthetic/transparent-model ground-truth tests, dependency-aware perturbation, and human-centered validation remain future validity-strengthening work.
- Updated `thesis/capitulo-3-diseno-experimental.qmd` and `thesis/capitulo-6-conclusiones.qmd` so EXP3 no longer contradicts the later LIME extension: EXP3 supports SHAP-Anchors fidelity replication and a LIME-only extension, but not a full paired SHAP-LIME cross-dataset stability claim.
- Updated `docs/reports/paper_a/paper_a_prototype_jmlr.tex` and `docs/reports/paper_a/paper_a_validity_and_reporting_caveats.md` to keep Paper A scoped to its SHAP-only EXP3 check while acknowledging the broader LIME-only extension outside Paper A's confirmatory claim.
- Updated `docs/reports/paper_bc/paper_bc_jmlr.tex` to align the validity-claim ladder and correct the LIME extension export path to `outputs/analysis/exp3_lime_results.csv`.
- Created and later generalized the CIFIE skill into the reusable `manuscript-editing` ACE skill with CIFIE/FOM-7 profile support.
- Updated `.aceconfig` trigger mappings for CIFIE manuscript editing tasks.
- Strengthened the skill with an explicit open-access literature enrichment workflow that uses the `literature` / `paper-lookup` skill for Semantic Scholar, Crossref/OpenAlex, and OA verification before citations are added.
- Ran an OA literature enrichment pass: Semantic Scholar returned HTTP 429 for broad searches but verified selected identifier lookups; OpenAlex and Crossref verified accepted DOI metadata and OA status for Nauta et al. (2023), Canha et al. (2025), Pawlicki et al. (2024), Bhattacharya and Verbert (2024), and Doshi-Velez and Kim (2017).
- Updated section 09/10 manuscript citations, `references.bib`, `references_apa7.md`, `citation_audit.md`, and `sources/evidence_map.md` with accepted source details.
- Revised `10_limitaciones_trabajo_futuro.md` for academic prose, APA 7 in-text citation support, and FOM-7 alignment; no thesis or paper artifacts were edited.
- Revised `02_introduccion.md` for academic prose, APA 7 in-text citation support, and FOM-7 alignment; no thesis or paper artifacts were edited.
- Updated `docs/planning/implementation_plan.md` for the skill creation task.
- On branch `publication/cifie-xai-fom7-book-chapter`, added implementation-plan task 5 for revising section 03 through a literature-enrichment loop.
- Queried Semantic Scholar first for selected XAI foundations sources; the shared pool returned successful DOI lookups for Murdoch et al. (2019), Marcinkevičs and Vogt (2023), and Miller (2019), and HTTP 429 for some other DOI/topic queries.
- Cross-checked accepted foundations sources through OpenAlex and Crossref. OpenAlex verified OA status for Murdoch et al. (PNAS PDF), Marcinkevičs and Vogt (Wiley PDF), Nauta et al. (ACM PDF), Schwalbe and Finzel (Springer PDF), Rudin et al. (Project Euclid PDF), and Miller (arXiv PDF).
- Added `@miller2019` to `references/references.bib` and `references/references_apa7.md`; updated `references/citation_audit.md` and `sources/evidence_map.md` for the section 03 literature loop.
- Revised `03_fundamentos_xai.md` for academic Spanish prose, citation support, and FOM-7 alignment; no `thesis/` or `pub/` artifacts were edited.
- Added `Scientific Advisor` role and `scientific-rigor-review`/`reference-audit` skills to extend ACE with peer-review-style science-correctness and bibliography-hygiene capability, on user request. No thesis/paper/CIFIE content was reviewed or edited in this session — this was a framework-extension task only.
- 2026-08-28: "unrecoverable" is a claim about evidence and deserves the same
  verification as any other. RCA-001 wrote off the EXP4 scripts without checking
  `__pycache__`; all seven modules, four CLI scripts and five test modules were in
  fact recoverable, and recovering them exposed a mislabelled statistic (ICC(1,1)
  reported as ICC(2,1)) and a mis-cited measurement instrument that no amount of
  re-reading the manuscripts would have found.
- 2026-08-28: the EXP4 bytecode in `src/evaluation/__pycache__/` and
  `scripts/__pycache__/` is now the only surviving copy of the original source and is
  guarded by RCA-002. Do not delete it.
- 2026-08-29: Retired the thesis's Estudio A/B/C letters for functional names and removed every Paper A / Paper B reference from thesis prose, on user request. Definition site is `{#tbl-estudios}` in Chapter 1; section anchors kept. See `docs/adr/0012-thesis-study-nomenclature.md`. Regression check: grep the thesis sources for a bare study letter (only the tbl-estudios note should match) and for "Paper A"/"Paper B"/"Paper C" (nothing should match).
- 2026-08-30: a green render proves nothing about layout. Three separate defects this session
  passed a successful `render.ps1`: two silently-failed CRLF edits to a Python script, a page
  break Quarto reordered, and headings numbered nowhere. Every claim about the output in this
  session was checked by unzipping the DOCX and reading `word/document.xml`.
- 2026-08-30: Quarto promotes a chapter file's first level-1 heading to the chapter title when
  the file declares no `title`, hoisting it above everything else in that file - so a page break
  written at the top of `index.qmd` lands after that heading. Insert such breaks post-render.
- 2026-08-30: `scripts/enforce_docx_thesis_format.py` is CRLF. Multi-line edits written with a
  bare newline match nothing, fail silently, and still leave a file that parses and runs.

## Session Handoff - 2026-09-29 (CIFIE drafting and Word delivery)

The current CIFIE drafting unit is complete and merged. The active objective
returns to **Task 3 / RCA-001 Phase 2** on `thesis/rca-001-phase-2`; no existing
constraint or overarching goal is superseded.

- Enriched `02_introduccion.md` and `03_fundamentos_xai.md` into a more readable,
  science-first account of XAI, its importance, conceptual distinctions, evidence
  requirements, application horizons, and field gaps.
- Expanded the supporting literature, APA 7 bibliography, citation audit,
  evidence map, source inventory, and science-first planning/scaffold documents.
- Added `scripts/generate_cifie_chapter_figures.py` and regenerated the chapter's
  critical-difference diagram from qualified EXP2 artifacts; updated figure
  provenance and empirical captions accordingly.
- Extended `scripts/build_cifie_chapter.py` to remove reader-facing
  `Fuente inicial` notes, apply black text, 1.5 line spacing and justified prose,
  format multi-page tables, preserve APA hanging indents, and embed grayscale
  figures for black-ink output.
- Delivered and visually verified the 68-page Word artifact at
  `publications/book_chapters/2026_cifie_xai_fom7/drafts/v3_editorial_review/cifie_xai_fom7_2026-09-29_formatted.docx`.
- Verification at handoff: 320 claims / 491 manuscript sites / 35 retired-value
  guards / 13 cited artifacts; sync green; 18 EXP4 source pins green; shared
  literals 0 unexplained / 53 known; both chapter scripts compile and the figure
  generator runs successfully.
- Next CIFIE action: independent Scientific Advisor review for rigor, references,
  readability, flow, and DOCX presentation before the next drafting unit.

## Session Handoff - 2026-09-30 (Paper B+C filed with TMLR)

**Paper B+C is submitted: TMLR submission 12779,
https://openreview.net/forum?id=VkmWJZclmH.** The filed version is tag
`tmlr-submission-12779` (paper lane `75b93a7f4`). The active objective returns
to **Task 3 / RCA-001 Phase 2** on `thesis/rca-001-phase-2`.

- **Completed**
  - Author name: Herrera-Vásquez (hyphen and accent) in every paper, reference,
    submission document and repository metadata file; the thesis keeps
    "Herrera Vásquez" (`9ed98f299`). Papers A, B, B+C and C PDFs rebuilt.
  - Abstract (`pub/claims.toml`): "the Adult tabular benchmark" became "the UCI
    Adult census-income dataset", and "on Adult" became "on the Adult data"
    (`57811d139`).
  - Equations (`05016a963`): five display equations numbered and
    cross-referenced; the duplicate LIME objective removed from the
    introduction; every term defined (U, G, L, pi_x, phi_0, M, perturbation noise,
    masked instances); definitions checked against `src/metrics/faithfulness.py`,
    `stability.py` and `src/experiment/runner.py` (masking = training-set mean;
    f = positive-class probability; fidelity = Pearson correlation over
    single-feature masks). Citations added: Bhatt et al. 2020 (fidelity),
    Samek et al. 2017 and Hooker et al. 2019 (gap), Alvarez-Melis and Jaakkola
    2018 (stability); both new entries verified in Crossref. 27 pages.
  - Step 8 submission gate (`1ca107200`): both PDFs rebuilt (27 + 5 pages), all
    verifiers and the strict shared-literal scan green, identity scan clean,
    bundle rebuilt, de-anonymised variant built once and discarded, sheet
    regenerated (306-word abstract), post-fix status of F01-F19 appended to the
    rigor review.
  - §8 availability section (`75b93a7f4`): the anonymous build now lists the
    bundle's own paths (each checked present) instead of repository paths, and
    no longer contradicts itself on the corpus full texts; the de-anonymised
    build keeps repository paths and the Zenodo DOI. Bundle rebuilt and
    re-scanned.
  - Filed by the author on OpenReview; editor note shortened, filled in for
    12779 and sent by email to tmlr-editors@jmlr.org (`b83b35731`). Forum ID
    recorded; Next Steps item 00 closed (`90ed6e5b9`).
- **Current State**
  - All four lanes clean, pushed, and containing `main` (`90ed6e5b9` or later).
  - Paper lane `paper/bc-venue-definition` is kept open and **frozen** for the
    review-response revision. Do not edit Paper B+C on any lane before reviews.
  - Verification at handoff: 321 claims / 485 sites / 46 retired-value guards;
    sync green; 18 EXP4 source pins green; shared literals 0 unexplained / 53
    known.
- **Next Steps**
  1. Resume Task 3 / RCA-001 Phase 2 on the thesis lane.
  2. Watch OpenReview for the Action Editor assignment, any desk-reject or
     formatting notice, then reviews. If the editors reply to the note, draft
     the response with the author.
  3. Optional, thesis lane: scope three passages as the paper now does - Ch.4
     l.193 "no es marginal, sino estructural"; Ch.6 P1 row "incoherencia
     estructural"; Ch.4 l.620 TreeSHAP efficiency scoped to XGBoost.
  4. CIFIE: the Scientific Advisor review queued in the 2026-09-29 handoff.
- **Blockers/Issues**
  - None blocking. The camera-ready build with `[accepted]` compiles; the
    acknowledgment's "prepared from repository artifacts dated May 2026" is out
    of date and must be revised if accepted, along with `\openreview`, `\month`
    and `\year`.
  - Review F10 is closed as won't-fix by author decision; never raise it.
- **Notes**
  - Any change to Paper B+C is now a revision in response to review: branch from
    tag `tmlr-submission-12779` on the paper lane, then run the whole "After any
    revision" checklist in `OPENREVIEW_SUBMISSION.md`.
  - Keep double-blind: nothing public linking the author to forum `VkmWJZclmH`
    while under review.
  - The artifact bundle is gitignored; rebuild with
    `python scripts/pubs/build_artifact_bundle.py` (needs `data/adult.csv`).
  - GNU sed treats `\u` in a replacement as "uppercase next char": edit LaTeX
    with the Edit tool or Python, not sed.
  - Build the de-anonymised variant by copying the `.tex` with
    `\usepackage[accepted]{tmlr}` to a temporary file; never commit it.

## Session Handoff - 2026-10-02 (TMLR rejection; PeerJ CS edition)

**TMLR rejected submission 12779 without review.** The notice gave no reasons
beyond "unlikely to meet one or both of TMLR criterion" and reviewer bandwidth.
Record: `docs/reports/paper_bc/TMLR_REJECTION_RECORD.md`. TMLR is deprecated as
a venue. Everything in this file that says "filed with TMLR", "paper lane
frozen" or "keep double-blind" is historical.

- **Completed**
  - Venue chosen by the author: PeerJ Computer Science (soundness-only review).
    Plan: `docs/planning/paper_bc_peerj_retarget_plan_2026-10-02.md`.
  - PeerJ edition built from the filed source: `paper_bc_peerjcs.tex` (26 pp,
    `wlpeerj.cls` v1.2, line numbers on) and
    `paper_bc_peerjcs_supplemental_S1.tex` (6 pp). Results, tables and figures
    moved verbatim; sections re-ordered to PeerJ's standard (gap analysis in
    Discussion); structured abstract (304 words / 2,170 characters).
  - New text required by PeerJ, none carrying a result: computing
    infrastructure, EXP4 judge model IDs in Methods, UCI dataset DOIs,
    human-directed AI-assistant disclosure in the Acknowledgments, Department of
    Computer Science affiliation.
  - New disclosed limitation: wall-clock cost was measured on several hosts
    (macOS, Windows, Linux) whose CPU and RAM were never recorded, and paired
    cells may have run on different hosts. Quality endpoints are unaffected.
  - TMLR artifacts removed from `docs/reports/paper_bc/`; registry, coverage,
    guards, `verify_sync`, `scan_shared_literals`, bundle script and Makefile
    point at the PeerJ files. `[papers.paper_bc]` in `pub/claims.toml` holds the
    structured abstract.
  - `verify_claims.py` skips dotted version triples (e.g. 1.7.1).
  - `.zenodo.json` / `CITATION.cff` set to v0.4.0 (record 21538180 already uses
    0.3.0); `CITATION.cff` cites the concept DOI `10.5281/zenodo.19297723`;
    affiliation spelling fixed.
- **Current State**
  - This lane is merged with `main`. Verification: 321 claims / 485 sites / 46
    retired-value guards; sync green; 18 EXP4 pins green; shared literals 0
    unexplained / 55 known. Both PDFs build in the main folder (26 + 6 pages,
    no undefined reference).
  - **Cleanup (ADR-0019).** The `xai-paper-bc` working tree is removed and the
    branches `paper/bc-venue-definition` and `paper/bc-peerj-cs` are merged into
    `main` and deleted, locally and on origin. Fully merged `pubs/*` branches
    and `results/adult-dataset` are deleted too. Twelve tracked latexmk build
    files at the repository root are removed and ignored from now on. Remaining
    working trees: `xai-eval-framework` (thesis lane), `xai-chapter`, `xai-exp4`.
  - The Tectonic compiler is at `tools/tectonic-portable/tectonic.exe` in the
    main folder (gitignored). The artifact bundle was rebuilt there: 16.2 MB,
    9,384 files. The "3.8 MB" quoted in older entries of this file is wrong.
  - Future Paper B+C edits: a short-lived `paper/bc-<topic>` branch in the main
    folder, merged through `main` (ADR-0019). Close Word first.
- **Next Steps**
  1. [x] **Done 2026-10-02.** Zenodo v0.4.0 published as `10.5281/zenodo.23111684`
     (GitHub release `paper-bc-peerj-submission-2026-10-02`, `main` at
     `ba6e835f2`) and cited in the manuscript. Originally: publish the release; then set `\zenodoversiondoi` and
     `CITATION.cff`. The PDF prints "[ZENODO VERSION DOI PENDING]" until then.
  2. Author: decide payment (D3). PeerJ charges after acceptance: APC about
     US$2,155, or one Lifetime Membership from about US$755. Not waivable for
     Mexico. This blocks filing, not preparation.
  3. [x] **Confirmed by the author 2026-10-02:** no reference was first
     suggested by AI.
  4. [x] **Done 2026-10-02:** `scripts/pubs/export_peerj_upload.py` writes the
     separate figure and table files to `docs/reports/paper_bc/peerj_upload/`;
     in-image titles removed from Figures 1-2. Upload set: `PEERJ_SUBMISSION.md`
     §11. Remaining: the payment decision (item 2), then the author files.
  5. Optional: arXiv preprint (approved by the author).
  6. Then resume Task 3 / RCA-001 Phase 2 on this lane.
- **Notes**
  - Never invent hardware specifications: none were recorded for any run.
  - Git Bash heredocs on this machine collapse doubled backslashes; edit LaTeX
    and TOML with the Edit tool or a script file, never an inline heredoc.

## Session Handoff - 2026-10-02 (venue: Inteligencia Artificial, IBERAMIA)

**The author cannot pay publication fees, so PeerJ was dropped before filing
(ADR-0020). Paper B+C now targets *Inteligencia Artificial* (IBERAMIA): no
fees, Scopus/ESCI/DOAJ, double-blind, no page limit for research articles
(4 MB PDF limit).** Supersedes the PeerJ items in the handoff above.

- **Completed (refactor, same folder `docs/reports/paper_bc/`)**
  - `paper_bc_peerjcs.tex` -> `paper_bc_iberamia.tex` on the journal's
    `iberamia.sty` (unmodified; `logo.png` added); PeerJ supplement ->
    `paper_bc_iberamia_appendix.tex`, Appendix A (Tables S1-S6) of the one PDF;
    `PEERJ_SUBMISSION.md` -> `IBERAMIA_SUBMISSION.md` (rewritten). Removed
    `wlpeerj.cls`, `peerj_upload/`, `scripts/pubs/export_peerj_upload.py`.
  - Double-blind build via `\camerareadyfalse`: author block, GitHub URL and
    Zenodo DOI withheld; identity scan of the PDF clean apart from the
    third-person RIMI citation.
  - Spanish Resumen and Palabras clave added (`abstract_es_tex`,
    `keywords_es_tex` in `pub/claims.toml`; new fragments); abstract
    unstructured again; numbered citations.
  - Registry, coverage, guards, verify_sync (now checks the Spanish includes),
    scan_shared_literals, bundle script and Makefile point at the new files.
  - ADR-0020 written; ADR-0019 marked partly superseded; BUILD.md, the TMLR
    record, ZENODO_RELEASE.md and the manuscript-editing skill updated.
- **Current State**
  - `paper_bc_iberamia.pdf`: 32 pp A4, 0.36 MB, 0 undefined references.
    Verification: 321 claims / 487 sites; sync; 18 EXP4 pins; shared literals
    0 unexplained / 55 known.
- **Next Steps**
  1. Author: fill in the suggested reviewers' emails and check conflicts
     (`IBERAMIA_SUBMISSION.md` §4), review the Spanish Resumen, then submit
     the PDF at journal.iberamia.org.
  2. Do not post the arXiv preprint until after review (double-blind).
  3. At acceptance: `\camerareadytrue`, journal counters, a new Zenodo
     version, update `\zenodoversiondoi`.
  4. Then resume Task 3 / RCA-001 Phase 2.

## Session Handoff - 2026-10-03 (Paper D refocused; Paper E documented)

**Paper D is now "Are explanations less reliable when the model is wrong?"** for
*Tecnologia en Marcha*'s AI special issue (deadline 2026-10-15; Word, 5-15 pp, IEEE,
English with Spanish abstract, double-blind, no fees; author target 12 Word pages).
The first Paper D (claim-registry case study) was dropped by the author as off the XAI
line; it is preserved at tag `paper-d-registry-draft-2026-10-03`, and its registry claims,
data, figures and scripts were removed. Paper C was checked and is NOT usable (its taxonomy
is inside Paper B+C, under review).

- **Paper D (`docs/reports/paper_d/`):** `ANALYSIS_PLAN.md` written and committed BEFORE
  any result (RQ1 correct vs misclassified per explainer; RQ2 model family; RQ3 FP vs FN;
  RQ4 decision-margin control; German Credit external check; run as unit; Wilcoxon + Holm;
  overlap guard). `paper_d.tex` is a skeleton on the journal page. The Word build pipeline
  (`scripts/pubs/build_paper_d.py`) is kept. Data: 299 EXP2 runs, about 123k instance
  explanations, quadrant-balanced; stored models allow the margin control.
- **Paper E (`docs/reports/paper_e/README.md`):** "Do explainers agree on which features
  matter?", documented as an idea only; development after Paper D, at a different journal,
  with a new EXP3 LIME run saving per-instance attributions.
- **Next:** `scripts/pubs/paper_d_analysis.py` per the plan; register numbers; write; figures;
  rigor review; author items (ORCID, profession, Spanish, reference approval); submit about
  2026-10-13.

## Session Handoff - 2026-10-03 (Paper D first render and iteration 1)

**Paper D task complete. Active objective: Task 3 / RCA-001 Phase 2 (thesis lane).**
All existing Active Constraints and overarching goals stand unchanged.

### Completed
- **Analysis** (`scripts/pubs/paper_d_analysis.py` -> `outputs/analysis/paper_d/`) per
  `docs/reports/paper_d/ANALYSIS_PLAN.md`; four deviations logged in its §9:
  1. RQ4 restricted to runs whose predictions the stored model reproduces;
  2. RQ4 implementation details;
  3. post-hoc training-overlap sensitivity;
  4. post-hoc RQ3 mechanism check.
- **Findings:**
  - Stability is lower on misclassified instances for all four explainers, and the result
    holds on held-out instances.
  - Deficits are large for SHAP (−0.076, d_z −1.36) and DiCE (−0.210).
  - The DiCE deficit is mostly a decision-margin effect; the SHAP deficit is not.
  - The margin-adjusted SHAP faithfulness-gap deficit holds out of training data.
  - The faithfulness gap follows the predicted class.
- **Manuscript:**
  - Edit `paper_d_template.tex`; `paper_d.tex` is generated by
    `scripts/pubs/render_paper_d.py`, which also writes the registry block (158 Paper D claims).
  - Build: `build_paper_d.py` produces blind/full PDF, Word and TIFF figures in `submission/`.
  - **12 Word pages**; abstract 228 words, resumen 239.
  - Formal dataset framing: UCI Adult Income (primary), Statlog German Credit (external
    validation).
  - Four author-supplied references on uncertainty-aware XAI added; Chiaburu et al.
    confirmed: CCIS 2580, 2026.
  - ORCID added (full version).
  - AI-use declaration after the references, per the journal policy; Acknowledgments removed.
- **Tooling:**
  - `verify_claims.py`: exceptions can be scoped to one file.
  - `scan_shared_literals.py --paper-d`: 0 unexplained matches.
  - All verifiers green.

### Pending (author, before 2026-10-13 submission)
- Profession placeholder.
- Spanish read and "brecha de borrado".
- Check of the `NEW` references (Kruskal–Wallis, Cameron–Miller, Platt).
- Open and re-save the .docx in Word.
- Send to revistatm@tec.ac.cr.

### Blockers/Issues
- **RF provenance (affects Papers A and B+C):**
  - The stored `rf.joblib` reproduces only 75–82% of the predictions recorded by the
    Jan–Feb 2026 random-forest runs. The model those runs used is not in the repository.
  - Needs an RCA entry; not yet written.
- **Environment:** the project `.venv` cannot load SciPy (Windows Application Control), so
  the Paper D analysis ran in a separate venv.

### Next
- Resume Task 3 / RCA-001 Phase 2 on the thesis lane.
- Paper E stays documented-only until after Paper D is submitted.
- IBERAMIA submission ID for Paper B+C to be recorded when the author sends it.

## Session Handoff - 2026-10-03 (Paper E analysis artifacts)

- **Paper E status:** The protocol, structural audit, exact-ID EXP3 LIME cohort, deterministic
  analysis pipeline and generated report are complete. Paper E remains distinct from Paper D;
  no manuscript or claim-registry entry was created. Scientific interpretation, DOI/reference
  verification, author approval and venue selection remain.
- **Committed artifacts:** The results branch `results/paper-e-agreement` has commit
  `24d27176e` with 12 EXP3 LIME run files plus manifest, 18 analysis tables/diagnostics,
  three figures and `RESULTS.md` under `outputs/analysis/paper_e/`. The Paper E README and
  implementation plan document the workflow and limits.
- **Cohort and QC:** 335 source runs were inventoried across 87 primary pairing blocks. The
  primary SHAP-LIME analysis contains 31,411 matched instance records; the descriptive
  Anchors/DiCE feature-set analysis contains 107,335 records. Seventy-six of 87 primary
  blocks have exact valid-ID sets; ten SVM blocks have partial SHAP subsets and one EXP2
  block lacks usable SHAP IDs, leaving 4,936 unpaired valid method-IDs. Only intersections
  enter the primary analysis, with zero classification mismatches among matched SHAP-LIME
  IDs. Secondary classification mismatches and truncated Anchors rules are excluded and
  enumerated in their pairing diagnostics. QC recorded 278 malformed/error rows and two
  duplicate-ID groups; no attribution-order, empty-additive, or unknown-feature failures.
- **Descriptive result:** Mean run-level top-5 Jaccard was 0.393 for EXP2 Adult
  (seed-clustered 95% CI [0.377, 0.410]), 0.714 for Breast Cancer
  ([0.671, 0.792]) and 0.387 for German Credit ([0.343, 0.426]). The report also contains
  rank/sign agreement and exploratory correctness and quality associations. No p-values or
  confirmatory claims are reported; the small number of seed clusters limits inference.
  Breast Cancer correctness contrasts were not estimable under the prespecified minimum of
  ten cases in each correctness group.
- **Reproduction and verification:** All 12 EXP3 model configurations were regenerated in
  isolated temporary storage and validated against tracked configs, training summaries,
  feature order and stored SHAP labels/predictions. Regenerated hashes are in the LIME
  metadata; absent original binaries prevent byte-identity claims. The analysis was rerun
  twice: all 19 generated analysis files matched by SHA-256. The frozen pip versions were
  used (NumPy 2.2.6, pandas 2.3.3, SciPy 1.16.3, scikit-learn 1.7.1, joblib 1.5.3,
  LIME 0.2.0.1, XGBoost 3.1.2, matplotlib 3.10.8); only Python 3.13.15 was available,
  although `environment.yml` specifies Python 3.11. Sixteen focused unit tests,
  `py_compile`, `git diff --check` and `.ace/scripts/verify.sh` passed. Matplotlib emitted
  only a non-blocking boxplot-parameter deprecation warning.
- **Branch state:** Paper E was transplanted as five Paper E-only commits from
  `origin/main` onto `paper/e-feature-agreement-clean`, then integrated through local `main`.
  No pushes were made. The local `main` history includes an earlier local integration merge
  and its revert before the clean integration; inspect that history before any push. The
  unrelated uncommitted `docs/reports/paper_d/paper_d.tex` in the original worktree was
  preserved and not included.
- **Next:** The results branch was brought through `main` per ADR-0013; the cohort and analysis
  artifacts are now integrated. The author should review the exploratory findings, approve
  the literature/DOI audit, choose a distinct venue, and only then draft a manuscript. Do not
  add claim-registry coverage until that manuscript and its claims exist.
