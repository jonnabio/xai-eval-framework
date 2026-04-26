# 12. EXP3 Partitioned Result Merge Procedure

Date: 2026-04-26
Status: Accepted

## Context

EXP3 was designed as a compact cross-dataset validation package with 24 runs:

- 2 datasets: `breast_cancer`, `german_credit`
- 2 models: `rf`, `xgb`
- 2 explainers: `shap`, `anchors`
- 3 seeds: `42`, `123`, `456`

The experiment was partitioned by dataset to reduce wall-clock time and avoid
concurrent writes to the same result directories:

- Windows worker: `breast_cancer`
- Linux/WSL worker: `german_credit`

Each worker produced raw result artifacts under a disjoint subtree of
`experiments/exp3_cross_dataset/results/`. The Linux/WSL partition was completed
and pushed to `origin/results/exp3-linux-german-credit`. The Windows partition
was completed locally on `results/exp3-windows-breast-cancer`.

The project needed a reproducible merge procedure that preserved both raw
artifact sets and made EXP3 analyzable as a single 24-run unit.

## Decision

Use a branch-level result consolidation workflow:

1. Commit the completed Windows `breast_cancer` raw artifacts to
   `results/exp3-windows-breast-cancer`.
2. Merge `origin/results/exp3-linux-german-credit` into
   `results/exp3-windows-breast-cancer`.
3. Treat the merged Windows branch as the combined EXP3 analysis branch.
4. Verify completeness after merge by counting result artifacts under
   `experiments/exp3_cross_dataset/results/`.
5. Push the merged branch to origin.

The accepted merge commit is:

```text
aa22d1112 Merge remote-tracking branch 'origin/results/exp3-linux-german-credit' into results/exp3-windows-breast-cancer
```

The Windows result commit is:

```text
380c1576e EXP3: add completed Windows breast cancer results
```

The Linux result commit merged into it is:

```text
09ec51022 feat(exp3): add linux german credit results and anchors fix
```

## Verification

Post-merge artifact counts:

```text
results.json: 24 / 24
metrics.csv: 24 / 24
breast_cancer results.json: 12 / 12
german_credit results.json: 12 / 12
```

The pushed branch state was verified with:

```text
HEAD == origin/results/exp3-windows-breast-cancer == aa22d1112
```

## Consequences

### Positive

- EXP3 is now analyzable as one complete cross-dataset validation package.
- Dataset partitions remain auditable through their original branch commits.
- The raw artifact tree preserves the dataset-level partition boundary while
  presenting a single unified result root.
- The thesis can now report EXP3 as a completed external tabular validation
  package, rather than a Windows-only partial result.

### Negative

- The consolidated branch is large because it contains raw per-instance JSON
  checkpoints for both partitions.
- Broad Git commands such as `git status` can be slow on the Windows-mounted
  working tree. Use targeted Git commands where possible.
- The merged branch name still references the Windows partition even though it
  now contains both Windows and Linux/WSL results.

## Follow-Up

- Use the merged branch for EXP3 statistical analysis and paper/thesis result
  interpretation.
- If a neutral branch name is desired later, create it from `aa22d1112` rather
  than re-running either worker.
