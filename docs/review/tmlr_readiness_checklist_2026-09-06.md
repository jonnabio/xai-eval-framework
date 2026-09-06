# TMLR Submission Readiness — Paper B+C

**Date:** 2026-09-06
**Role:** Scientific Editor
**Manuscript:** `docs/reports/paper_bc/paper_bc_tmlr.tex` (25 pp) + supplementary (5 pp)
**Sources reviewed:** TMLR [acceptance criteria](https://jmlr.org/tmlr/acceptance-criteria.html),
[editorial policies](https://jmlr.org/tmlr/editorial-policies.html),
[author guide](https://jmlr.org/tmlr/author-guide.html)

**Verdict: not ready to submit.** One blocking policy conflict (B1), one blocking
authorship decision (B2), one blocking artifact task (B3). Everything mechanical is done.

---

## B1 — BLOCKING: prior publication of the shared cohort

TMLR's editorial policy states:

> "There should not be any reuse of written text, figures or results between the
> submitted paper and any paper which has been published, accepted for publication,
> or submitted in parallel at another archival, peer-reviewed venue."

Paper A — Herrera Vasquez & Herrero Uceda (2026), RIMI (3), doi:10.69850/rimi.vi3.307,
published 2026-09-01 — is an archival, peer-reviewed venue. The carve-out in the same
policy covers only **non-archival** venues (workshops, arXiv and other preprint servers).
It does not cover a journal with a DOI.

### Measured overlap

| Channel | Finding | Verdict |
| ------- | ------- | ------- |
| **Results** | **13 registered numeric results reported in both papers** | **conflict** |
| Written text | 2 verbatim shared sentences out of 405, both bibliography titles | clear |
| Figures | Paper A contains no figures; the three here are unique to it | clear |

The 13 shared results:

- EXP2 block-level fidelity for SHAP, LIME, Anchors, DiCE (4)
- EXP2 block-level stability for SHAP, LIME (2)
- Friedman χ² for fidelity and stability, and Kendall's W for fidelity (3)
- EXP3 SHAP cross-dataset fidelity, Breast Cancer and German Credit × RF and XGB (4)

The prose is independently written; the conflict is confined to the word *results*, and
it is real. Both papers also share one execution cohort, one preprocessing pipeline and
one set of model controls.

### Remediation options

**Option 1 — ask the Editors-in-Chief first (recommended).** TMLR's policy has no
"substantial extension" carve-out of the sort many journals grant, so the question is
genuinely one of editorial judgement rather than something to be resolved by reading
harder. Write before submitting, describing the overlap precisely: 13 shared numeric
results, no text or figure reuse, one shared cohort, prior venue a Spanish-language
regional journal, and the new material here (four-axis taxonomy, 44-paper scoping
corpus, LLM-judge reliability study, paired run-level LIME–SHAP inference,
cross-dataset extension). Cost: a few days. Benefit: definitive, and cheap next to a
desk rejection or a misconduct question raised after review.

**Option 2 — remove the reused results.** Cite Paper A for the omnibus rather than
restating it: drop the six EXP2 block-level values and three Friedman statistics from
tables and prose, replacing them with a cited one-sentence summary, and reconsider
whether the EXP3 SHAP section belongs here at all. What remains — the taxonomy, the
corpus and gap analysis, the LLM-judge reliability measurement, and the paired
run-level LIME–SHAP contrast — is entirely new and is the actual contribution. This
narrows the paper and would likely be requested anyway.

**Option 3 — different venue.** Choose one whose policy explicitly permits extensions
of prior published work with disclosure. Many journals do; TMLR does not say so.

Recommended sequence: Option 1, prepared to execute Option 2 on the answer.

### Consequence for the anonymity guard

§Validity "Relationship to Previously Published Work" is currently suppressed under
`\ifdeanonymised` so it does not appear in the reviewed PDF. That decision was taken
on the understanding that the overlap was a *disclosure* matter. If B1 resolves via
Option 1, the editors will have the facts directly and the guard is fine. If it resolves
via Option 2, the subsection should be rewritten and probably unguarded, because there
will no longer be reused results to hide. **Do not submit with the disclosure suppressed
and no editor notification** — that combination is the one indefensible outcome.

---

## B2 — BLOCKING: author set must be final at submission

> "The exact set of authors must be listed on OpenReview, with active OpenReview
> profiles, at the time of submission and throughout the review process. No authors may
> be added or removed after submission. There are no exceptions to this policy."

The submission lists **one** author. The published Paper A, which shares this cohort,
protocol and model controls, lists **two**: Jonathan Herrera Vasquez and Miguel Herrero
Uceda. TMLR's authorship criteria require substantial intellectual contribution,
involvement in drafting or revision, and accountability for the content.

**Remediation.** Decide, before submitting, whether Herrero Uceda's contribution to the
shared experimental base meets those criteria for *this* paper. This is a judgement only
the two of you can make, but it must be made now: the policy admits no exceptions, so
a co-author omitted at submission cannot be added later. If included, that author needs
an active OpenReview profile at submission time.

---

## B3 — BLOCKING: anonymous artifact link is still a placeholder

§Code and Artifact Availability currently reads "an anonymised mirror linked from the
OpenReview submission" in the anonymous build — placeholder wording, not a link. The
abstract states that all experimental artifacts are publicly available, so a reviewer
who tries to check has nothing to follow.

**Remediation.** Create an anonymous mirror (anonymous.4open.science or equivalent) and
substitute the real URL into the `\ifdeanon` false branch. The de-anonymised branch
already carries the real repository URL.

---

## Cleared

| # | Requirement | Status | Evidence |
| - | ----------- | ------ | -------- |
| 1 | Official TMLR stylefile, unaltered | **pass** | `tmlr.sty` byte-identical to upstream `JmlrOrg/tmlr-style-file` |
| 2 | Double-blind anonymisation | **pass** | built PDF: "Anonymous authors / Paper under double-blind review", no name, email, or affiliation |
| 3 | No link to an identified version | **pass** | repository URL guarded by `\ifdeanon`; no preprint posted |
| 4 | Length justified by content | **pass** | 25 pp; TMLR sets no limit but warns unusually long papers delay review |
| 5 | Supplementary format and size | **pass** | 5 pp PDF, 74 KB, anonymous — limit is 100 MB, PDF or ZIP |
| 6 | Acknowledgments suppressed under review | **pass** | `\ifdeanon`-guarded, absent from the anonymous build |
| 7 | Citations resolve | **pass** | zero unresolved citations in the built PDF |
| 8 | No concurrent submission elsewhere | **pass** (confirm) | no parallel submission known; author to confirm |
| 9 | Open access / fees | **pass** | TMLR charges no fees; CC BY 4.0 from submission |
| 10 | LLM use | **pass** | permitted as an assistive tool; the LLM judges in EXP4 are instruments and are described in the methodology |

---

## Recommended, not required

**Broader Impact Statement.** Required only when work carries significant risk of harm.
This paper is a measurement study, but it issues deployment recommendations for
explainers applied to Adult Income — a standard proxy for credit and employment
decisions. A short statement noting that explanation quality metrics are not fairness
guarantees, and that the recommendations are scoped to tabular classification, is cheap
and forecloses a reviewer objection.

**Author contributions.** Optional at TMLR. Worth including if B2 resolves to two
authors, since the division of labour across two papers sharing one cohort is exactly
what a reader will wonder about.

---

## Note on an earlier error in this workstream

The venue recommendation on 2026-09-05 was argued from the acceptance criteria, which
TMLR fits unusually well, without checking the editorial policies against the Paper A
overlap. The advice given at that point — "disclose the overlap to the Action Editor" —
described a disclosure regime. TMLR operates a prohibition. The fit argument for TMLR
still holds on its merits; B1 is a separate question that has to be settled first, and
it may yet send this paper elsewhere.
