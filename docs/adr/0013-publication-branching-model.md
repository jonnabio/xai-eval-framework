# 13. Publication Branching Model (Lane Ownership, Trunk-Owned Claim Substrate)

Date: 2026-09-05
Status: Accepted

## Context

Until now the repository has had exactly one active lane. Every workstream
since May — the CIFIE book chapter, the tri-document alignment audit, RCA-001,
RCA-002, the thesis presentation pass and the RCA-001 Phase 2 coverage sweep —
ran on a single long-lived branch, and `main` was refreshed only when that
branch was judged finished. On 2026-09-05, immediately before this decision,
`main` was **29 commits behind** `thesis/rca-001-phase-2` and had been so for
six days.

Paper B+C work must now proceed in parallel with the thesis. Four properties of
this repository determine what a second lane may and may not do.

**1. The manuscript bodies are already disjoint.** The 29 thesis commits touch
24 files and not one of them lives under `docs/reports/paper_bc/`. Prose will
not conflict. Git is not the problem this ADR solves.

**2. The claim substrate is a single global object.** RCA-001 invariant 3 reads:
*a quantity appearing in more than one manuscript is registered once, listing
every document that carries it.* In `pub/claim_registry.toml`, 30 `[[claim]]`
blocks name both a thesis chapter and a Paper B+C document; 29 name Paper B+C
alone and 130 the thesis alone. A per-lane registry fork would register those
30 quantities twice and re-create the exact defect class RCA-001 exists to
prevent. The registry therefore **cannot** be branch-private.

**3. `verify_claims.py` is already a sufficient cross-document gate — against
the registry present on the branch.** Changing `0.808` in `paper_bc_tmlr.tex`
without the registry fails check (b), the per-site occurrence count; changing
the registry to match fails check (a) against the artifact. Drift cannot
survive a green verifier. It can only survive a *stale* one.

**4. Therefore the hazard is staleness, not concurrency.** A lane cut from a
trunk 29 commits behind would have begun on a 142-claim registry without the
`diff:` or `exp2_missing_pct` resolvers and without Chapters 5 and 6 under
`[coverage]` — verifying green while checking the wrong things.

Two further couplings constrain the model. RCA-002 guards
`paper_bc_tmlr_supplementary.tex` and `thesis/capitulo-5-taxonomia.qmd`
together, so its invariants (ICC reported as ICC(1,1); Cramér's V over
pairwise-complete cases) bind both lanes at once. And `[coverage]` enforcement
is repository-wide: the moment a file joins that list, every unregistered
result-shaped literal in it fails CI on *every* branch, not only the one that
added it.

## Decision

**Manuscript bodies are branch-private. The claim substrate is trunk-owned. A
work branch's `pub/` and `scripts/pubs/` may be ahead of `main`, never behind
it.**

### Lanes

| Pattern | Owns | Lifetime |
|---|---|---|
| `main` | integration trunk; always green under all three verifiers | permanent; never worked on directly |
| `thesis/<topic>` | `thesis/**`, `thesis/_output/*.docx`, `scripts/enforce_docx_thesis_format.py`, `pub/fragments/thesis_*` | one workstream |
| `paper/bc-<topic>` | `docs/reports/paper_bc/**`, `pub/fragments/paper_bc_*` | one workstream |
| `paper/a-<topic>` | `docs/reports/paper_a/**`, `pub/fragments/paper_a_*` | one workstream |
| `chapter/cifie-<topic>` | `publications/book_chapters/2026_cifie_xai_fom7/**` | one workstream |
| `pubs/<topic>` | the shared substrate, and nothing else | hours; merged to `main` first |
| `rca/<id>-<slug>` | anything the incident requires; highest merge priority | until the RCA closes |
| `results/<exp>-<env>` | `outputs/analysis/**` only | until merged |

### The shared substrate

These files are trunk-owned. A change to any of them is substrate-class
regardless of which lane discovered the need for it:

- `pub/claim_registry.toml`
- `pub/claims.toml` and everything generated into `pub/fragments/`
- `scripts/pubs/**`
- `docs/rca/regression-guards.yaml` and `docs/rca/RCA-*.md`
- `docs/reports/sync/thesis_paper_sync_matrix.md`
- `.github/workflows/pubs-sync.yml`
- `docs/context/ACTIVE_CONTEXT.md`

`outputs/analysis/**` and `src/**` are read-only inputs to every lane; they
change only through a `results/*` branch merged to `main`.

### Rules

1. **No commit mixes substrate files with manuscript-body files.** ACE already
   mandates atomic commits, so this costs nothing, and it is what makes rule 2
   mechanical: a substrate commit can always be cherry-picked cleanly.
2. **A substrate commit reaches `main` in the session it is made** — on a
   `pubs/` branch merged directly, or cherry-picked out of the work branch.
   Both lanes then pull `main`.
3. **`main` into the work branch whenever `main` moves**, at minimum at session
   start and before any merge. Merge, do not rebase, on pushed branches.
4. **Work branch into `main` at every completed, green, atomic unit of work**,
   not at the end of the workstream. The merge criterion is *green and
   self-contained*, never *finished*.
5. **Lanes never merge into each other.** All cross-pollination goes through
   `main`. In particular `results/*` merges into `main` only: artifacts are
   inputs to all three documents, and the 2026-08-23 import of
   `results/exp3-windows-breast-cancer` had to be done surgically with
   `git checkout <branch> -- <paths>` precisely because a lane-to-lane merge
   dragged in stale docs and two junk paths.

### Concurrent working trees

Lanes are checked out as `git worktree`s rather than by switching branches,
because switching is the expensive operation here: the thesis DOCX is held open
in Word (a recurring file lock) and a full render is slow.

```
git worktree add ../xai-paper-bc paper/bc-<topic>
```

`.git/info/exclude` excludes `/.ace/` and `/.aceconfig`. The exclusion does not
reach already-tracked files, so exactly four files travel to a new worktree --
`.ace/standards/{architecture,coding,documentation,security}.md` -- and
**everything else does not**: `roles/`, `skills/`, `packs/`, `prompts/`,
`scripts/`, `workflows/`, `schemas/`, `knowledge/`, `feedback/` and `.aceconfig`
are all absent. They must be copied in, and because the `standards/` directory
already exists there, the copy must be of the directory *contents*
(`cp -r .ace/. <worktree>/.ace/`), not of the directory, or it nests.

The same exclusion means `.aceconfig`'s `pre_commit` hooks are local-only and
never run in CI: any check that must actually hold across lanes belongs in
`pubs-sync.yml`.

## Consequences

### Positive

- A lane can never verify green against a substrate that no longer describes the
  project, which was the failure mode the model was designed against.
- Cross-document drift stays impossible without weakening RCA-001 invariant 3:
  the 30 dual-document claims keep exactly one registration.
- `main` becomes continuously releasable, so the state an examiner or a
  co-author would fetch is never six days and 29 commits stale.
- Rule 1 makes substrate history separable, so a registry change can be replayed
  onto any lane without carrying prose with it.
- Worktrees remove the interaction between branch switching and the Word file
  lock: the thesis can stay open while Paper B+C builds.

### Negative

- Rule 2 imposes a context switch: discovering mid-edit that a claim needs
  registering means committing the registry separately and merging it before
  continuing. This is deliberate friction and it is the price of invariant 3.
- `docs/context/ACTIVE_CONTEXT.md` is trunk-owned but written by every lane, so
  it conflicts on every concurrent session. Mitigated by lane-scoped
  subsections, not eliminated.
- Adding a Paper B+C document to `[coverage]` becomes a trunk event that must be
  triaged to `--coverage-report` exit 0 before merging, because it turns CI red
  on the thesis lane too. It can no longer ride along inside a prose commit.
- More branches to track for a solo author, and a worktree whose ACE framework
  must be seeded and kept in sync by hand, since git carries only the four
  tracked `.ace/standards/` files.

### Neutral

- No numeric value, manuscript claim, guard or artifact changed in adopting this
  model. The `main` checkpoint merge (`0ceb31f37`) was verified green before and
  after.
- The `results/*` and `thesis/*` prefixes already existed; this ADR names the
  convention rather than inventing it.

## Compliance

- `main` must be green under `verify_claims.py`, `verify_sync.py` and
  `verify_exp4_reconstruction.py` after every merge. `pubs-sync.yml` enforces
  this on `pull_request` and on push to `main`.
- Before starting work in any lane, confirm the substrate is not behind:

  ```
  git fetch origin
  git diff --stat origin/main...HEAD -- pub/ scripts/pubs/ docs/rca/
  ```

  Anything shown must be this lane's own additions. If `origin/main` carries
  substrate commits this branch lacks, merge `main` before editing.
- A commit touching both a substrate file and a manuscript body violates rule 1
  and should be split before it is pushed.
- `pub/fragments/` conflicts are never resolved by hand: take either side and
  re-run `scripts/pubs/generate_fragments.py`. CI's
  `git diff --exit-code pub/fragments` is the check that the resolution was
  correct.

## References

- `docs/rca/regression-guards.yaml` — RCA-001 invariant 3 (one registration per
  shared quantity) and invariant 7 (`[coverage]` completeness), which together
  make the registry trunk-owned; RCA-002, which co-guards
  `capitulo-5-taxonomia.qmd` and the Paper B+C supplementary
- `docs/adr/0011-publication-sync-pipeline.md` — the SSOT/fragment pipeline this
  model treats as substrate
- `docs/adr/0012-thesis-study-nomenclature.md` — nomenclature diverges between
  thesis and papers, so a lane-to-lane merge of prose would be wrong on its face
- `docs/reports/sync/thesis_paper_sync_matrix.md` — where the thesis/paper claim
  correspondence is maintained when a shared number moves
- `scripts/pubs/verify_claims.py` — the cross-document gate whose guarantee is
  conditional on a current registry
- `.github/workflows/pubs-sync.yml` — the only enforcement point that survives
  the `.ace/` and `.aceconfig` git exclusion
