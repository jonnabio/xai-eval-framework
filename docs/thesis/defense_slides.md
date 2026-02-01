# Thesis Defense: Agnostic Architecture for XAI Interpretability
**Candidate**: [Your Name]  
**Date**: January 2026

---

## 1. Problem Statement
**Black Box opacity** hinders trust in AI adoption in critical sectors (Finance, Healthcare).
*   **Challenge**: Existing evaluation tools are fragmented and model-specific.
*   **Goal**: Develop a **Model-Agnostic Framework** to benchmark explainer fidelity, stability, and utility.

---

## 2. Methodology (Experiment 1)
**Dataset**: Adult Census (Binary Classif: Income >50K)
**Model**: Random Forest (Baseline)
**Explainers**:
*   **LIME** (Local Linear Approximation)
*   **SHAP** (Shapley Values)

**Metrics**:
1.  **Fidelity** (R² of surrogate)
2.  **Stability** (Variance under perturbation)
3.  **Human Utility** (Simulated by LLM Proxies)

---

## 3. Architecture
**Tech Stack**:
*   **Backend**: Python (FastAPI, Scikit-learn, Dice-ML)
*   **Frontend**: Next.js (React, Recharts)
*   **Infrastructure**: Docker + Render.com

**Key Innovation**:
*   **Unified Interface**: `ExperimentRunner` handles data, model execution, and metric aggregation uniformly.
*   **Parallelism**: Optimized batch processing using `ProcessPoolExecutor`.

---

## 4. Key Results (Phase 4 & 5)
| Metric | LIME | SHAP | Analysis |
| :--- | :--- | :--- | :--- |
| **Fidelity (R²)** | 0.82 | **0.94** | SHAP provides significantly better global approximation. |
| **Stability** | Low | **High** | LIME results jitter with random sampling; SHAP is deterministic. |
| **Performance** | **Fast** | Slow | LIME is ~50x faster, making it suitable for real-time checks. |

---

## 5. Conclusions & Future Work
*   **Conclusion**: No "one size fits all" explainer exists. SHAP is superior for analysis; LIME for speed.
*   **Contribution**: Open-Source Framework validated with >1000 instances.
*   **Future**: Expansion to Deep Learning models (Image/NLP).

---

## Q & A
