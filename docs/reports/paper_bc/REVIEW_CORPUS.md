# Paper B+C review corpus — how to commit it

Resolves finding **A14** (`docs/review/tri-document-alignment-review_2026-08-22.md`).

## The situation

Paper B+C states a **48-paper** coded corpus in five places: the abstract, the
PRISMA screening record (`tab:prisma`), the corpus profile (`tab:corpus_profile`),
Gap 1 ("29 of 48 coded studies"), and the second-reviewer audit ("16 papers,
one third of the coded corpus"). Its §Code and Artifact Availability tells
readers the corpus CSV is in the repository.

The only corpus artifact in the repository is
`docs/reports/paper_c/paper_c_review_corpus.csv`, which has **24 rows** and
belongs to Paper C.

**These are not the same corpus at two sizes.** The coding schemes differ:

| Cluster | Paper C corpus (committed) | Paper B+C (claimed) |
|---|---|---|
| faithfulness_robustness | 8 | 17 |
| human_grounded | — | 11 |
| taxonomy_survey | 3 | 9 |
| benchmark_toolkit | 3 | 5 |
| llm_judge | 4 | 4 |
| counterfactual_recourse | — | 2 |
| modality_domain | 6 | — |
| **total** | **24** | **48** |

Paper B+C uses two clusters the committed corpus does not have
(`human_grounded`, `counterfactual_recourse`) and drops one it does have
(`modality_domain`). That is a deliberately revised coding scheme, not a
truncated file — which is why this is most likely a corpus that was built and
never committed, rather than a number that was invented.

## Decide which case you are in

**Case A — the coding pass exists outside the repository.** A spreadsheet,
Zotero collection, or notes file that produced 17/11/9/5/4/2. Then this is a
data-entry job; follow "Committing it" below.

**Case B — it does not exist.** Then Paper B+C must be corrected to the corpus
that does exist, and the correction is larger than one number: the PRISMA chain
(312 identified → 65 deduplicated → 247 screened → 152 excluded → 95 full text →
47 excluded → 48 included), the corpus profile table, "29 of 48", and the
second-reviewer audit's "16 papers = one third" all follow from the corpus size.

Do not resolve this by editing 48 to 24. The two corpora have different cluster
vocabularies, so the rest of the paper's gap analysis would no longer follow
from the file.

## Committing it (Case A)

**1. Where the file goes**

```
docs/reports/paper_bc/paper_bc_review_corpus.csv
```

A new file — do **not** overwrite Paper C's. Paper C legitimately describes a
24-study corpus, still builds, and its abstract is registered against that file
in `pub/claim_registry.toml`. Two papers, two corpora.

Start from `paper_bc_review_corpus.template.csv` in this directory, which is the
schema with no rows.

**2. Where the papers go: one row per coded paper**

| Column | What goes in it |
|---|---|
| `study_id` | 1–48, unique |
| `record_slug` | short stable key, e.g. `kadir_metrics_taxonomy`; unique |
| `title_short` | quoted title |
| `primary_cluster` | one of: `faithfulness_robustness`, `human_grounded`, `taxonomy_survey`, `benchmark_toolkit`, `llm_judge`, `counterfactual_recourse` |
| `paper_role` | e.g. `survey`, `method`, `benchmark`, `critique` |
| `modality_context` | e.g. `general`, `tabular`, `image`, `text`, `graph` |
| `evaluation_targets` | `;`-separated: `artifact`, `explainer`, `model_behavior`, `user_task` |
| `evidence_sources` | `;`-separated: `proxy`, `benchmark`, `human_expert`, `end_user`, `llm_judge` |
| `quality_properties` | `;`-separated: `fidelity`, `stability`, `sparsity`, `plausibility`, … |
| `llm_validation_relevant` | `yes` / `no` |
| `source_confidence` | `high`, `medium`, `title_level` |
| `notes` | why the paper earns its place |

The multi-label columns are why the paper reports evidence-source counts summing
to more than 48; the checker handles that.

**3. Check as you go**

```bash
python scripts/pubs/check_review_corpus.py --corpus docs/reports/paper_bc/paper_bc_review_corpus.csv
```

Prints the observed distribution — run it any time to see how far the coding has
got. It validates the controlled vocabularies and catches duplicate slugs or ids.

**4. Check against the manuscript**

```bash
python scripts/pubs/check_review_corpus.py \
    --corpus docs/reports/paper_bc/paper_bc_review_corpus.csv --expect paper_bc
```

This compares the corpus to what Paper B+C claims, transcribed into
`[review_corpus.paper_bc]` in `pub/claim_registry.toml`. It passes only when
size, all six cluster counts, all five evidence-source counts and the confidence
mix agree.

If the coding legitimately lands somewhere else, change the manuscript and the
`[review_corpus.paper_bc]` expectation together — never the expectation alone.

**5. Wire it in**

- Add the CSV path to Paper B+C's §Code and Artifact Availability, alongside the
  EXP2/EXP3/EXP4 entries.
- Add a `[[cited_artifact]]` entry in `pub/claim_registry.toml` so the path is
  checked for existence like every other cited artifact.
- Add the corpus-size claim to the registry:

```toml
[[claim]]
id = "review.corpus.paper_bc.rows"
source = "review_corpus_rows:paper_bc"
value = "48"
tolerance = 0.5
appears_in = [{ file = "docs/reports/paper_bc/paper_bc_jmlr.tex", text = "48" }]
```

The `review_corpus_rows` resolver in `scripts/pubs/claim_sources.py` currently
takes no argument and reads Paper C's file; extend it to take a paper key.

- Add the corpus check to `.github/workflows/pubs-sync.yml` next to
  `verify_claims.py`.

**6. Then close A14** in the review report and the sync matrix.

## Why this is worth the effort

The corpus is load-bearing. The four-axis taxonomy, all three gap claims, and
the single-reviewer limitation discussion rest on it, and it is the first thing
a reviewer of a survey paper asks to see. This is the same failure mode as F04
(EXP4 scripts and raw judge data never committed) — except F04 is unrecoverable,
and this one probably is not.
