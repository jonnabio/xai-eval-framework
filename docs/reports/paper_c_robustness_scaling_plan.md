# Paper C: Robustness & Scaling Analysis Plan

**Target Status:** Planned (Following Paper A and B)
**Core Concept:** The Computational Economics of XAI Stability in Production

## 1. Executive Summary
This paper will address a critical gap in XAI deployment literature: the hidden computational cost of stabilizing fast but stochastic explainer methods. While methods like LIME and Anchors are celebrated for their low latency (often sub-second), our empirical baselines demonstrate catastrophic instability (variance across repeated runs with identical inputs). Paper C will argue that to achieve the stability guarantees required for production auditing (which SHAP provides natively), fast explainers must be stabilized via ensemble averaging, which completely negates their computational advantage.

## 2. Key Research Questions
1. **The Cost of Stability**: How many resampling runs are required to stabilize LIME and Anchors to match the baseline stability of deterministic SHAP?
2. **The Pareto Frontier Inversion**: At the required stabilization threshold, which method is actually computationally superior?
3. **Production Economics**: What is the financial and computational overhead of running non-deterministic explainers in high-throughput environments (e.g., credit scoring)?

## 3. Core Arguments & Hypotheses
*   **Hypothesis C1**: LIME's sampling-based local surrogates suffer from such high variance that single-run explanations are statistically unreliable for high-stakes decision auditing.
*   **Hypothesis C2**: Stabilizing LIME (e.g., averaging 50+ runs) incurs a cumulative latency that equals or exceeds the runtime of a single, exact SHAP computation.
*   **Hypothesis C3**: The perceived "speed vs. fidelity" trade-off is a false dichotomy when stability constraints are enforced. 

## 4. Supporting Data (The EXP2 Grid)
The paper will rely heavily on the **EXP2 (Comparative & Scaled)** robustness benchmarks currently executing on the `xai-eval-framework`.
*   **Data Source**: 300-run benchmarking grid across varied random seeds ($s \in \{42, 123, 456, 789, 999\}$) and sample sizes ($N \in \{50, 100, 200\}$).
*   **Key Metrics Tracked**: 
    - Wall-clock Time (ms)
    - Stability (Mean pairwise cosine similarity of attributions)
    - Fidelity ($R^2$)

## 5. Proposed Methodology
1. **Instability Baselining**: Quantify the baseline instability of LIME and Anchors using the EXP2 variance data.
2. **Stabilization Simulation**: Simulate an "Ensemble LIME" by aggregating $K$ independent runs. Plot Stability vs. $K$.
3. **Cost Intersection Analysis**: Identify the $K$ threshold where Ensemble LIME achieves SHAP-level stability, and compare the cumulative wall-clock time against a single run of Kernel/Tree SHAP.
4. **Latency vs. Throughput Recommendations**: Provide concrete engineering guidelines on explainer selection based on SLA latency limits and audit requirements.
