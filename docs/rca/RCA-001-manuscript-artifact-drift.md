# RCA-001: Manuscript numbers drift from their source artifacts

**Status**: Closed (prevention in place)
**Severity**: High
**Opened**: 2026-08-22 | **Closed**: 2026-08-24
**Role**: Scientific Editor → Incident Responder
**Guard**: `docs/rca/regression-guards.yaml` → `RCA-001`

## Symptoms

A cross-document alignment audit of Paper A, Paper B+C and the PhD thesis
(`docs/review/tri-document-alignment-review_2026-08-22.md`) produced thirteen
findings, five of them major:

- Paper A stated that the EXP3 Anchors cross-dataset check "could not be
  executed" and booked 12 cells as a permanent limitation. The runs had
  completed on 2026-04-26 and their results were the source of numbers Paper B+C
  and the thesis already published (A01).
- Paper A and Paper B+C reported different values, 0.6165 and 0.607, for the
  same EXP3 cell (A03).
- Thesis Ch.5 reported Anchors fidelity 0.514 and DiCE fidelity 0.412, matching
  no artifact at any commit (A04).
- Thesis Ch.4's cost profile was off by factors of 2x, 14x and 16x, and mixed
  run-level means with single-cell Appendix C sensitivity values without
  labelling either (A05).
- A statistical-disclosure fix applied to Paper B+C on 2026-07-29 was never
  propagated to the identical table in the thesis (A08).

A fourteenth finding (A14) surfaced while building the prevention: Paper B+C
states a 48-paper coded corpus throughout, and the only committed corpus
artifact has 24 rows.

## Evidence

- Every number was re-derived from `outputs/analysis/` and
  `experiments/exp3_cross_dataset/results/`; the mismatches above are
  reproducible with `scripts/pubs/verify_claims.py`.
- `git log -S "Anchors: 0.514"` returns one commit, `f639935d0` (2026-05-10).
  At that commit `outputs/analysis/` did not exist in the repository, so the
  figures could not have been checked against anything when written.
- The EXP3 Anchors artifacts existed only on the unmerged branches
  `results/exp3-windows-breast-cancer` and `results/exp3-linux-german-credit`,
  so a reader following Paper B+C's artifact section could not find them.

## Five whys

1. **Why did the manuscripts disagree with the artifacts?** Because their
   numbers were transcribed by hand.
2. **Why did transcription errors survive?** Because nothing ever re-derived a
   published number from its source.
3. **Why was there no such check?** Because FOM-7 gate 7 ("claim-ready
   reporting ... traceable to source artifacts") was written as editorial
   policy, not as an executable gate.
4. **Why was the policy never mechanised?** Because the publication pipeline
   that could enforce it (`pub/claims.toml` → `pub/fragments/` → CI) was scoped
   to abstracts and keywords only, and did not cover the document bodies or
   Paper B+C at all.
5. **Why did that scope go unnoticed?** Because the outputs were rebuilt rarely
   — the thesis DOCX was 3.5 months stale — so drift produced no visible signal
   until a manual audit went looking for it.

**Root cause**: the repository's central methodological claim, end-to-end claim
traceability, was enforced by convention rather than by tooling, in a workflow
where the same quantity is authored independently in three documents.

## Fixes

**Immediate** (2026-08-22/23): all thirteen audit findings corrected across the
three manuscripts; the EXP3 Anchors cohort imported onto the publication branch;
all four rendered outputs rebuilt. No statistic, effect size, p-value or
hypothesis outcome changed — every correction replaced a transcription with the
artifact value.

**Permanent** (2026-08-24):

- `pub/claim_registry.toml` — the registry of published numbers, each with the
  resolver that re-derives it and the manuscripts that must carry it.
- `scripts/pubs/claim_sources.py` — resolvers over the committed artifacts.
  Distinguishes block-level from run-level aggregation, which is where A05
  originated.
- `scripts/pubs/verify_claims.py` — fails on a value that no longer matches its
  artifact, a manuscript that lost or altered a registered value, a retired
  value that reappears, or a cited artifact path missing from the working tree.
- Paper B+C wired into the fragment pipeline; it was previously outside it.
- `pubs-sync.yml` runs the verifier on every push and pull request;
  `.aceconfig` runs it in `pre_commit`.

## Prevention

| Failure mode | Guard |
|---|---|
| Number goes stale after re-analysis | Value re-derived from the artifact on every run |
| Number edited away from its source | Occurrence-count check per manuscript site |
| Retired value reintroduced | `[[retired]]` guards, one per corrected finding |
| Paper cites evidence not in the tree | `[[cited_artifact]]` existence check |
| Fix applied to one document, not its twin | Every claim lists all documents that carry it |

Verified by negative test on 2026-08-24: reintroducing `Anchors: 0.514`, editing
a Paper A table cell, and removing `exp3_lime_results.csv` each fail the
verifier with a specific message.

## Not covered

- **Prose claims.** The verifier checks numbers. It would not have caught A04's
  qualitative half, where DiCE — the second most expensive method — was
  described as efficient. Peer review remains necessary.
- **Numbers with no artifact.** EXP4's reliability figures (F04) cannot be
  verified because the scripts and raw judge data were never committed. Paper
  B+C's corpus (A14) was in the same position and was recoverable: it has since
  been reconstructed and is now verified like any other claim. The forward-looking rule is archival: no result artifact enters the
  repository without its generating script and raw inputs.
- **Render-time defects.** A13, a dangling cross-reference, was found only by
  rebuilding. Building all outputs in CI and failing on undefined references is
  Phase 2.

## Follow-up

1. Phase 2: generate the registry's values into LaTeX macros and Quarto inline
   values so a number exists in exactly one place.
2. Phase 2: rebuild all four outputs in CI, failing on undefined references and
   crossref warnings.
3. ~~Resolve A14~~ — done 2026-08-26: 44-row corpus reconstructed from the audit
   record plus the citation record, released, and CI-verified against the
   manuscript's printed distribution. The reconstruction is disclosed in
   Paper B+C §Validity.
4. Add the archival rule to `.ace/standards/documentation.md` and to the FOM-7
   gate 5 definition.
