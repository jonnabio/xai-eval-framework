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
  `[TO FILL: comparison citations to existing XAI benchmark/toolkit papers and novelty delta statement]`

Artifact packaging expected for submission:
- released code/configs/analysis outputs and failure reports are present;
- logs and lineage graph should be explicitly indexed in submission metadata. `[TO FILL: artifact index with paths for logs/lineage graph]`
