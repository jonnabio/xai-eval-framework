# XAI Explainer Methods: Math, Implementation & Performance

This reference document details the four Explainable AI (XAI) methods implemented in the framework. It covers the **Mathematical Formulation**, **Implementation Details** (specific to this codebase), and **Performance Characteristics** for each method.

---

## 1. SHAP (SHapley Additive exPlanations)

### Mathematical Formulation
SHAP assigns each feature an importance value $\phi_i$ based on the **Shapley value** from cooperative game theory. It measures the average marginal contribution of a feature value across all possible feature coalitions.

$$
\phi_i(f, x) = \sum_{S \subseteq F \setminus \{i\}} \frac{|S|!(|F| - |S| - 1)!}{|F|!} [f_x(S \cup \{i\}) - f_x(S)]
$$

*   $F$: Set of all features.
*   $S$: Subset of features.
*   $f_x(S)$: Prediction of the model when only features in $S$ are present (marginalized over others).

### Implementation Details
*   **Wrapper**: `src/xai/shap_tabular.py` -> `SHAPTabularWrapper`
*   **Library**: `shap` (specifically `TreeExplainer` for tree models).
*   **Algorithm**: "Interventional" TreeSHAP (Lundberg et al., 2020).
    *   **Computation**: It does **not** sample. It recursively traverses the Decision Trees to compute the exact expectation $E[f(x) | x_S]$ in $O(Depth^2)$ time.
    *   **Background Data**: Uses `n_background_samples=100` (from `kmeans` or random sample) to estimate the baseline distribution.
    *   **Additivity Check**: We disabled `check_additivity` by default for performance, but the math guarantees it within floating point precision.

### Performance
*   **Complexity**: $O(T \cdot L \cdot D^2)$ where $T$=Trees, $L$=Leaves, $D$=Depth.
*   **Speed**: Extremely Fast (< 1 second/instance).
*   **Bottleneck**: None. It is the most efficient method for Random Forests/XGBoost.

---

## 2. LIME (Local Interpretable Model-agnostic Explanations)

### Mathematical Formulation
LIME approximates the black-box model $f$ locally with a simpler linear model $g$ (e.g., Ridge Regression). It solves the following minimization problem:

$$
\xi(x) = \text{argmin}_{g \in G} \ \mathcal{L}(f, g, \pi_x) + \Omega(g)
$$

*   $\pi_x(z) = \exp(-D(x,z)^2 / \sigma^2)$: Exponential kernel weighting samples $z$ by proximity to $x$.
*   $\mathcal{L}$: Weighted Squared Loss.
*   $\Omega(g)$: Complexity penalty (regularization).

### Implementation Details
*   **Wrapper**: `src/xai/lime_tabular.py` -> `LIMETabularWrapper`
*   **Library**: `lime` (`LimeTabularExplainer`)
*   **Configuration**:
    *   `num_samples`: **5000** (Fixed sample size). This is the key stability factor.
    *   `discretize_continuous`: `False` (We use continuous features to avoid boundary artifacts).
    *   `kernel_width`: Auto-calculated based on $\sqrt{\text{num_features}} * 0.75$.

### Performance
*   **Complexity**: $O(N \cdot F)$ where $N$=Samples (5000), $F$=Features.
*   **Speed**: Fast (~500ms/instance).
*   **Bottleneck**: Matrix inversion (Ridge Regression) is cheap. The cost is dominantly just making 5,000 predictions.

---

## 3. Anchors (High-Precision Rules)

### Mathematical Formulation
Anchors searches for a rule $A$ (predicate) such that the precision of the rule is high with high statistical confidence.

$$
P(\text{prec}(A) \ge \tau) \ge 1 - \delta
$$

*   $\tau$: Precision threshold (e.g., 0.95).
*   $\delta$: Confidence parameter (e.g., 0.15).
*   **Algorithm**: It uses a **Multi-Armed Bandit (MAB)** approach (using KL-LUCB or Hoeffding bounds) to efficiently explore the space of possible rules (Beam Search). It draws samples $z$ to estimate precision until the bounds tighten enough to accept/reject a rule.

### Implementation Details
*   **Wrapper**: `src/xai/anchors_wrapper.py` -> `AnchorsTabularWrapper`
*   **Library**: `alibi` (`AnchorTabular`)
*   **Parameters**:
    *   `threshold`: **0.95** (Very strict precision requirement).
    *   `coverage_samples`: Auto-adaptive.

### Performance
*   **Complexity**: $O(B \cdot S \cdot N)$ where $B$=Beam Width, $S$=Samples per candidate.
*   **Speed**: **Slow** (4s - 40s+ per instance).
*   **Bottleneck**: The 'Adaptive' nature. If a rule is borderline (e.g., precision 0.94 vs 0.96), it may sample **10,000+** times to prove it exceeds 0.95, causing massive processing spikes.

---

## 4. DiCE (Diverse Counterfactual Explanations)

### Mathematical Formulation
DiCE finds a set of $k$ counterfactual points $\{c_1, ... c_k\}$ that are close to the original input $x$ but flip the prediction, while being diverse from each other.

$$
C(x) = \text{argmin}_{c_1...c_k} \sum_{i} \text{yloss}(f(c_i), y_{target}) + \lambda_1 \text{dist}(c_i, x) - \lambda_2 \text{dpp_diversity}(c_1...c_k)
$$

*   **Diversity**: Modeled using Determinantal Point Processes (DPP) or simple distance.

### Implementation Details
*   **Wrapper**: `src/xai/dice_wrapper.py` -> `DiCETabularWrapper`
*   **Library**: `dice_ml`
*   **Method**: `method="random"` (Random Search).
    *   *Note*: We use "random" instead of "genetic" or "gradient" because our wrapper implementation setup favored a generic black-box approach. Even "random" search in high-dimensional space requires many queries to satisfy the constraints.
    *   **Output**: We convert the generated counterfactual $c$ into a feature importance vector by $|x - c|$.

### Performance
*   **Complexity**: $O(N_{iter} \cdot K)$ samples.
*   **Speed**: **Moderate/Slow** (1s - 20s per instance).
*   **Bottleneck**: The constraints (validity + proximity) are hard to satisfy simultaneously, leading to many rejected candidates and resampling loops.

---

## Summary of Processing Costs

| Method | Type | Queries/Instance | Time (N=100) | Main Cost Factor |
| :--- | :--- | :--- | :--- | :--- |
| **SHAP** | Structure Access | **0** | < 1 min | Tree recursion (CPU bound) |
| **LIME** | Linear Approx | 5,000 | ~5 min | Fixed sampling overhead |
| **DiCE** | Optimization | ~2,500+ | ~2.5 hrs | Solving constraints |
| **Anchors** | Search | ~10k - 50k+ | ~3 hrs | Statistical bound convergence |
