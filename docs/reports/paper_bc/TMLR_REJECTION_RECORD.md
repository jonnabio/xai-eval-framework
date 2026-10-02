# Paper B+C — TMLR rejection record

**Status: closed. TMLR is no longer a target for this paper.** The paper is now prepared for
PeerJ Computer Science (`PEERJ_SUBMISSION.md`).

## What happened

| | |
|---|---|
| Venue | Transactions on Machine Learning Research (TMLR), via OpenReview |
| Submission | 12779, forum `VkmWJZclmH` (https://openreview.net/forum?id=VkmWJZclmH) |
| Title as filed | From Fidelity to Semantics: A Taxonomy of XAI Evaluation Metrics and Paired Empirical Comparison of LIME versus SHAP |
| Filed | 2026-09-30, by the author |
| Version filed | tag `tmlr-submission-12779` (commit `75b93a7f4`) |
| Decision | **Rejected without further review (desk rejection)** |
| Decision reported | 2026-10-02 (the date the author passed the notice on; the notice's own date was not recorded) |
| Signed | "Teng" |

## The decision, as received

> Hi Jonathan Herrera-Vasquez, We are sorry to inform you that your TMLR submission "12779:
> From Fidelity to Semantics: A Taxonomy of XAI Evaluation Metrics and Paired Empirical
> Comparison of LIME versus SHAP" has been rejected without further review. It was deemed to be
> unlikely to meet one or both of TMLR criterion and could not be sent for further review due to
> high volume of submissions and scarce bandwidth of the volunteer reviewers and AEs.
>
> Teng

No further details were given.

## Reasons

These are the only reasons TMLR stated:

1. The submission was "deemed to be unlikely to meet one or both" of TMLR's acceptance
   criteria. TMLR's two criteria are (a) whether the claims are supported by accurate,
   convincing and clear evidence, and (b) whether some individuals in TMLR's audience would be
   interested in the findings.
2. It "could not be sent for further review due to high volume of submissions and scarce
   bandwidth of the volunteer reviewers and AEs."

**What is not known.** The notice does not say which of the two criteria was in doubt, and it
contains no comment on the manuscript: no reviewer report, no Action Editor assessment, no
named defect. Any more specific explanation would be a guess, and none is recorded here. No
scientific finding in the paper was challenged, so the rejection required no change to any
result, table or claim.

## Consequences

- No reviews exist, so there is nothing to carry to another journal as prior peer review.
- TMLR did not publish the paper.
- The editor note on prior publication (RIMI) had been emailed to tmlr-editors@jmlr.org after
  filing. The same disclosure now goes to PeerJ in the Notes to Staff (`PEERJ_SUBMISSION.md` §6).
- The double-blind constraint that applied while under TMLR review has ended. PeerJ review is
  single-blind.

## What was removed from this folder on 2026-10-02

The TMLR submission artifacts were deleted because the venue is deprecated:
`paper_bc_tmlr.tex`, `paper_bc_tmlr.pdf`, `paper_bc_tmlr_supplementary.tex`,
`paper_bc_tmlr_supplementary.pdf`, `tmlr.sty`, `fancyhdr.sty`, `jmlr2e.sty`,
`OPENREVIEW_SUBMISSION.md` (submission sheet and gate records) and
`EIC_ENQUIRY_prior_publication.md` (editor note).

They are not lost. Everything as filed is preserved at tag `tmlr-submission-12779`:

```
git show tmlr-submission-12779:docs/reports/paper_bc/paper_bc_tmlr.tex
git checkout tmlr-submission-12779 -- docs/reports/paper_bc/   # restore the whole folder
```

The pre-submission review and remediation records are kept, because their findings apply to
the paper whatever the venue: `docs/review/` (rigor review, reference audit, TMLR readiness
checklist) and `docs/planning/paper_bc_tmlr_*_2026-09-28.md`.

## What carried over to the PeerJ edition

Results, tables, figures and references moved verbatim from the filed source into
`paper_bc_peerjcs.tex` and `paper_bc_peerjcs_supplemental_S1.tex`. The claim registry
(`pub/claim_registry.toml`) now points at those files: 321 claims at 485 sites, the same counts
as the filed TMLR version.
