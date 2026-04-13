# Paper A - JMLR-Track Positioning

This companion note contains the JMLR-track positioning material removed from the main draft.

## 5. JMLR-Track Positioning
This work is positioned for the **Datasets and Benchmarks** track.

- **Claim:** The submission provides a reusable XAI benchmark artifact stack.  
  **Evidence/artifact:** code (`src/`, `scripts/`), experiment configs (`configs/experiments/`), run artifacts (`experiments/exp2_scaled/results/**/results.json`), summary exports, and inferential outputs (`outputs/analysis/paper_a_exp2_stats/`).  
  **Why it matters to the track:** benchmark-track contributions require reusable resources, not only narrative findings.

- **Claim:** The benchmark is auditable with explicit failure accounting.  
  **Evidence/artifact:** coverage/missingness diagnostics, malformed-artifact reporting, and stage-gated FOM-7 execution with artifact gates.  
  **Why it matters to the track:** transparent handling of incomplete runs improves trustworthiness of benchmark evidence.

- **Claim:** The evaluation protocol supports multi-objective comparison rather than single-metric ranking.  
  **Evidence/artifact:** joint reporting of Fidelity, Stability, Sparsity, Faithfulness Gap, and Cost with omnibus and paired non-parametric tests.  
  **Why it matters to the track:** benchmark utility increases when trade-offs are measurable across quality, robustness, and compute axes.

- **Claim:** The framework is designed for extension and repeat execution.  
  **Evidence/artifact:** config-driven experiment matrix, deterministic analysis driver, reproducibility scripts, and FOM-7 operational protocol.  
  **Why it matters to the track:** reusable benchmark infrastructure supports follow-on comparisons and ablations by other groups.

- **Claim:** The methodological novelty is the combination of benchmark evidence with auditable execution governance (FOM-7).  
  **Evidence/artifact:** explicit stage/gate model linking protocol specification, integrity audit, inference export, and claim-ready reporting.  
  **Why it matters to the track:** this contributes a replicable benchmark operation model, not only method-level score tables.  

## 6. Novelty Delta Against Adjacent Benchmark Resources

Paper A should be framed as a benchmark-governance contribution rather than a
new explainer or generic metric library.

| Adjacent work | What it already contributes | Paper A novelty boundary |
| :--- | :--- | :--- |
| OpenXAI | Transparent evaluation of post-hoc explanations and reusable benchmark framing. | Paper A adds explicit claim governance: protocol freeze, artifact qualification, deterministic analysis export, and bounded claim eligibility. |
| Quantus | Broad toolkit support for responsible evaluation metrics across explanation methods. | Paper A treats metrics as one layer in a full benchmark operation protocol, with run inventory, recovery overlay rules, and block-level inference. |
| BEExAI | Benchmark infrastructure for evaluating explainable AI methods. | Paper A emphasizes auditable execution governance and failure accounting as primary contributions, not only method execution and score reporting. |
| Graph/chemistry XAI benchmarks | Domain-specific benchmark datasets and ground-truth assumptions. | Paper A is deliberately tabular and model-agnostic, with its novelty in snapshot governance and inferential claim control rather than modality-specific ground truth. |

The strongest wording for JMLR-track positioning is:

> Paper A contributes FOM-7, a reproducible benchmark operation protocol that
> connects metric computation, artifact integrity, deterministic inference
> export, and claim-ready reporting for model-agnostic XAI benchmarking.

Artifact packaging expected for submission:
- released code/configs/analysis outputs and failure reports are present;
- logs and lineage graph should be explicitly indexed in submission metadata.
- the path-level artifact index is maintained in
  `docs/reports/paper_a/paper_a_artifact_index.md`.
