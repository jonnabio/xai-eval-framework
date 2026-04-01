# LIME vs SHAP: A Paired Empirical Comparison

This Markdown file mirrors the current LaTeX source content. Mathematical expressions, lists, and citations are preserved in LaTeX notation.

## Abstract


LIME and SHAP are widely used explainability methods, yet guidance on
when each is preferable remains limited and often anecdotal. This paper
presents a focused paired empirical comparison of the two methods on
tabular data using five primary technical metrics under a controlled
benchmarking protocol. Across 75 matched SHAP-LIME cells, SHAP
dominates on stability, fidelity, and faithfulness gap, while LIME
yields systematically sparser explanations and lower runtime in most
contexts. The cost trade-off is statistically significant but
heterogeneous across model families: matched-cell medians are 684.1 ms
for SHAP versus 65.7 ms for LIME, whereas means are 11,708.3 ms versus
3,660.7 ms because kernel-SHAP tails are heavy. These findings support
objective-driven deployment guidance: SHAP for high-assurance auditing
and LIME for latency-sensitive user-facing explanation workflows.


**Keywords:** explainable ai, lime, shap, interpretability, robustness benchmarking


## Introduction


Selecting an explanation method in production can be posed as a
constrained decision problem: given a fixed predictor \(f\) and instance
\(x\), choose \(E \in \{\mathrm{LIME}, \mathrm{SHAP}\}\) to maximize
explanation quality while satisfying operational constraints.
Concretely, we consider
\[
E^\star=\arg\max_{E \in \{\mathrm{LIME},\mathrm{SHAP}\}}
U(S_E,F_E,\Delta_{k,E},P_E)\quad\text{s.t.}\quad C_E \le \tau,
\]
where \(S\) is stability, \(F\) fidelity, \(\Delta_k\) faithfulness
gap, \(P\) sparsity/parsimony, \(C\) cost, and \(\tau\) a latency
budget.

LIME and SHAP optimize different principles. LIME explains locally by
fitting a sparse surrogate around \(x\),
\[
\xi(x)=\arg\min_{g\in G}\mathcal{L}(f,g,\pi_x)+\Omega(g),
\]
favoring local fidelity and explicit sparsity controls
\citep{ribeiro2016why}. SHAP explains predictions through additive
feature attributions \(f(x)=\phi_0+\sum_i \phi_i\), where \(\phi_i\)
are Shapley-based contributions with game-theoretic guarantees
\citep{lundberg2017unified}. These theoretical differences are well
known; however, they do not by themselves resolve deployment choices
across model families, sampling regimes, and runtime constraints
\citep{retzlaff2024posthoc,ali2023trustworthy}.

Recent synthesis and systematic studies show that XAI evaluation
remains fragmented, with no single accepted protocol and strong
dependence on which evaluation dimensions are prioritized
\citep{longo2024manifesto,ali2023trustworthy,pawlicki2024metrics,canha2025benchmark}.
This makes single-metric comparisons insufficient for claim-ready
method selection.

Open benchmarking toolchains and robustness-aware faithfulness
protocols further show that method rankings can change under different
metric families and perturbation settings
\citep{agarwal2022openxai,sithakoul2024beexai,zheng2025ffidelity}.

Within the broader benchmark program, this manuscript isolates the
matched LIME-versus-SHAP decision problem rather than repeating the
full multi-method framework contribution. This narrower scope allows a
more detailed paired analysis of quality-cost trade-offs across model
families and runtime regimes.

This paper provides a paired, multi-objective benchmark using an
audited, configuration-driven protocol on tabular data (UCI Adult). We
evaluate five technical endpoints with explicit directionality:
Stability (\(S\), higher is better), Fidelity (\(F\), higher is
better), Faithfulness Gap (\(\Delta_k\), higher is better under
top-\(k\) masking), Sparsity (active-feature ratio \(P\), lower is
better for parsimony), and Computational Cost (\(C\), lower is better).
Inference is performed on matched SHAP-LIME cells with identical
\((\mathrm{model},\mathrm{seed},N)\), using paired Wilcoxon tests
\citep{wilcoxon1945individual}, paired effect sizes (\(d_z\))
\citep{lakens2013calculating}, and Holm correction
\citep{holm1979simple}.

Our paired analysis indicates a consistent trade-off: SHAP tends to
provide stronger stability, fidelity, and top-\(k\) faithfulness
signals, while LIME offers systematically sparser explanations and
substantially lower runtime cost in most settings. This supports
objective-driven method selection rather than universal method supremacy
\citep{agrawal2025xaieval}.

Our contributions are:
\begin{enumerate}[leftmargin=*]
\item \textbf{Formalized deployment trade-off}: we frame LIME-vs-SHAP as a
constrained multi-objective selection problem over quality, parsimony, and
cost.
\item \textbf{Paired inferential evidence}: we quantify method differences on
matched cells with corrected significance testing and effect sizes for each
endpoint.
\item \textbf{Operational heterogeneity analysis}: we characterize when cost
dominance changes by model family, including heavy-tail latency behavior.
\item \textbf{Decision guidance}: we derive deployment recommendations that map
system constraints to explainer choice.
\end{enumerate}

## Background

This section summarizes the two explainability methods compared in our
benchmark and highlights the technical properties that directly motivate
the evaluation metrics and hypotheses used in this paper.

### LIME (Local Interpretable Model-Agnostic Explanations)


LIME approximates a black-box model \(f\) locally around an instance
\(x\) by training an interpretable surrogate model \(g\) (e.g., linear
regression) on perturbed samples weighted by a kernel \(\pi_x\). It
solves:
\[
\xi(x) = \arg\min_{g \in G} \mathcal{L}(f, g, \pi_x) + \Omega(g).
\]
where \(\Omega(g)\) penalizes complexity (sparsity)
\citep{ribeiro2016why}. In practice, LIME behavior is strongly shaped by
its neighborhood construction and surrogate-design hyperparameters
(e.g., kernel width, number of perturbation samples, and feature budget).
These controls often yield compact explanations and low latency, but
they also introduce stochastic variation because local neighborhoods are
sampled rather than exhaustively enumerated.

### SHAP (Shapley Additive Explanations)


SHAP attributes prediction output to features based on their marginal
contribution across all possible coalitions, satisfying axioms of
efficiency, symmetry, and dummy properties
\citep{lundberg2017unified}. KernelSHAP estimates these quantities with
a weighted regression scheme over coalitions for model-agnostic usage,
whereas tree-specific implementations can exploit model structure.
Relative to local-surrogate methods, SHAP is typically denser and
computationally heavier in non-tree settings because many coalition
evaluations are required to estimate stable attributions.

### Implications for This Benchmark

For a fair LIME-versus-SHAP comparison, the benchmark must control
confounders unrelated to explainer design. This motivates the protocol
choices implemented in Section~3: identical transformed feature space,
shared model artifacts, fixed class target, and matched paired cells by
\((\mathrm{model}, \mathrm{seed}, N)\). Under these controls, expected
methodological trade-offs become testable: LIME should favor sparsity
and cost, while SHAP should favor stability and faithfulness-oriented
quality. This framing also aligns with recent calls for multi-metric,
functionally grounded XAI evaluation rather than single-endpoint
reporting \citep{pawlicki2024metrics,canha2025benchmark}.

## Methodology

This study uses a configuration-driven experimental pipeline for
reproducible XAI benchmarking. The pipeline fixes (i) preprocessing and
model artifacts before explanation, (ii) explainer hyperparameters via
versioned YAML configurations with deterministic seeds, (iii)
artifact-level logging per run (including \texttt{results.json}), and
(iv) explicit validity filters plus matched SHAP-LIME pairing for
inferential analysis. This structure follows recent recommendations for
functionally grounded, multi-metric XAI evaluation and transparent
benchmarking
\citep{canha2025benchmark,pawlicki2024metrics,agarwal2022openxai}. We
instantiate this pipeline for a focused LIME-versus-SHAP comparison to
produce claim-ready evidence on quality-cost trade-offs under controlled
conditions.

### Research Questions and Hypotheses

The methodology is model-agnostic and reproducibility-oriented, with
all confirmatory claims anchored in quantitative endpoints.

We address the following questions:
\begin{enumerate}[leftmargin=*]
\item \textbf{RQ1 (Robustness)}: Is SHAP more stable than LIME under
input perturbation?
\item \textbf{RQ2 (Parsimony)}: Is LIME sparser than SHAP?
\item \textbf{RQ3 (Efficiency)}: Is LIME computationally cheaper than
SHAP?
\item \textbf{RQ4 (Faithfulness)}: Does SHAP provide stronger
faithfulness/fidelity signals than LIME?
\end{enumerate}

Corresponding directional hypotheses are:
\begin{enumerate}[leftmargin=*]
\item \(H_1: S_{\mathrm{SHAP}} > S_{\mathrm{LIME}}\) (stability).
\item \(H_2: P_{\mathrm{LIME}} > P_{\mathrm{SHAP}}\) (sparsity).
\item \(H_3: C_{\mathrm{LIME}} < C_{\mathrm{SHAP}}\) (cost).
\item \(H_4: F_{\mathrm{SHAP}} > F_{\mathrm{LIME}}\) (fidelity/faithfulness).
\end{enumerate}

### Experimental Design and Analysis Units

The robustness cohort is instantiated from the repository-tracked
EXP2-scaled matrix with factors:
\begin{itemize}[leftmargin=*]
\item model family \(g \in \{\mathrm{logreg}, \mathrm{rf}, \mathrm{xgb},
\mathrm{svm}, \mathrm{mlp}\}\),
\item explainer \(k \in \{\mathrm{lime}, \mathrm{shap}\}\),
\item seed \(s \in \{42, 123, 456, 789, 999\}\),
\item sampling intensity \(N \in \{50, 100, 200\}\) per TP/TN/FP/FN stratum.
\end{itemize}

This defines \(5 \times 2 \times 5 \times 3 = 150\) planned LIME/SHAP
runs. In the current artifact state, we retain 150 analyzable LIME/SHAP
runs (75 LIME, 75 SHAP) and 75 matched SHAP-LIME cells on identical
\((g,s,N)\) coordinates for paired inference.
Accordingly, this manuscript reports the EXP2 robustness cohort rather
than the earlier EXP1 calibration subset, because paired multi-model
coverage is required for inferential claims.

To avoid pseudoreplication, we use a hierarchical analysis structure:
\begin{enumerate}[leftmargin=*]
\item \textbf{Instance level}: per-case metric values.
\item \textbf{Run level}: mean metric per configuration.
\item \textbf{Matched-cell level}: paired SHAP-LIME run means on shared
\((g,s,N)\) cells (primary inferential unit).
\end{enumerate}

### Data, Preprocessing, and Model Controls

All experiments use the UCI Adult data set \citep{kohavi1996scaling} with a
stratified split and deterministic seeds. The preprocessing pipeline
follows train-only fitting with:
\begin{itemize}[leftmargin=*]
\item numeric scaling (`StandardScaler`),
\item categorical one-hot encoding (`OneHotEncoder` with
\texttt{handle\_unknown='ignore'}).
\end{itemize}

Pre-trained black-box models are loaded from fixed artifacts and
reused across explainers to isolate explainer effects:
random forest \citep{breiman2001random} and gradient-boosted trees
(\texttt{xgb}) \citep{chen2016xgboost}, alongside additional tabular
families present in the robustness cohort.

Evaluation instances are sampled by error quadrants (TP, TN, FP, FN) via
stratified sampling. Nominal run size is \(4N\), with realized counts
bounded by quadrant availability and runtime failures (observed range:
27 to 800 instances; median 400).

### Explainer Protocol

Both explainers consume the same transformed feature space and target the
positive class probability:
\begin{itemize}[leftmargin=*]
\item \textbf{SHAP}: TreeExplainer for tree models, KernelExplainer for
non-tree models, with background subsampling (\(n=50\)).
\item \textbf{LIME}: tabular local surrogate with
\texttt{num\_features=10}, effective \texttt{num\_samples=1000}, and
\texttt{kernel\_width=3.0} in the EXP2 configuration family.
\end{itemize}

### Metric Operationalization

Primary metrics are computed per instance and aggregated per run:
\begin{enumerate}[leftmargin=*]
\item \textbf{Stability} \(S\): mean pairwise cosine similarity of
attribution vectors under Gaussian perturbations (\(T=15\),
\(\sigma=0.1\)):
\[
S = \frac{2}{T(T-1)}\sum_{a<b}\cos\!\left(e^{(a)},e^{(b)}\right).
\]
\item \textbf{Sparsity} \(P\): active-feature ratio above threshold
\(\tau=10^{-4}\) (lower active ratio indicates sparser explanations).
\item \textbf{Fidelity} \(F\): faithfulness correlation between
attribution magnitude and prediction drop under feature masking.
\item \textbf{Faithfulness Gap} \(\Delta_k\): absolute prediction change
after masking top-\(k\) features (\(k=5\)):
\[
\Delta_k=\left|f(x)-f(x_{\mathrm{mask\text{-}top\text{-}k})}\right|.
\]
\item \textbf{Cost} \(C\): per-instance wall-clock explanation time (ms).
\end{enumerate}

### Inferential Protocol

The statistical plan follows established comparative-ML practice
\citep{demsar2006statistical} and thesis ADR decisions:
\begin{enumerate}[leftmargin=*]
\item primary test: two-sided paired Wilcoxon signed-rank on matched
SHAP-LIME cells for each metric \citep{wilcoxon1945individual},
\item effect size: paired \(d_z\) for magnitude reporting
\citep{lakens2013calculating},
\item multiplicity control: Holm-Bonferroni over the five primary
metrics \citep{holm1979simple}.
\end{enumerate}

All inferential claims are restricted to artifact-qualified runs:
parseable, non-empty results with explicit matched pairing. No semantic
endpoint enters the confirmatory analysis reported here.

### Reproducibility Contract

The protocol is fully configuration-driven (YAML + seeded execution),
with per-run `results.json` artifacts, explicit exclusion of malformed or
empty runs, and no synthetic imputation. This provides a deterministic
audit trail from configuration to manuscript-level claim.

## Results

Results are reported from the artifact-qualified EXP2 robustness cohort.
In the current merged recovery snapshot, the EXP2 analysis exports
contain 252 analyzable unique runs out of 300 planned cells overall.
For this paper's paired LIME-versus-SHAP inference, we use the fully
matched subset: 150 analyzable runs (75 LIME, 75 SHAP) forming 75
paired cells with identical \((\mathrm{model}, \mathrm{seed}, N)\).
Matched coverage spans all five model families
(\(\mathrm{xgb}=15\), \(\mathrm{logreg}=15\), \(\mathrm{rf}=15\),
\(\mathrm{mlp}=15\), \(\mathrm{svm}=15\)) and all sampling intensities
\(N\in\{50,100,200\}\) with near-balanced counts.

### Primary Paired Inference

Table~\ref{tab:paired_main} summarizes paired run-level outcomes on the
75 matched cells. All five primary endpoints remain significant under
Holm-adjusted testing.
All numeric entries in Table~\ref{tab:paired_main} are source-locked to
the analysis export \texttt{wilcoxon\_shap\_lime\_all\_models.csv} under
\texttt{outputs/analysis/paper\_a\_exp2\_stats/}.

\begin{table}[t]
\centering
\caption{Matched SHAP-versus-LIME paired results (\(n=75\) cells). For all metrics,
\(\Delta=\) SHAP - LIME. Sparsity is measured as active-feature ratio, so larger values indicate denser explanations.}
\label{tab:paired_main}
\begin{tabular}{lrrrrr}
\toprule
Metric & LIME Mean & SHAP Mean & \(\Delta\) & \(p_{\mathrm{Holm}}\) & \(d_z\) \\
\midrule
Stability & 0.014 & 0.732 & +0.718 & \(2.6\times10^{-13}\) & 3.00 \\
Sparsity (active ratio) & 0.085 & 0.226 & +0.142 & \(2.6\times10^{-13}\) & 0.84 \\
Fidelity & 0.560 & 0.808 & +0.248 & \(2.6\times10^{-13}\) & 4.82 \\
Faithfulness Gap & 0.334 & 0.380 & +0.045 & \(2.6\times10^{-13}\) & 2.63 \\
Cost (ms) & 3660.7 & 11708.3 & +8047.6 & \(1.2\times10^{-10}\) & 0.45 \\
\bottomrule
\end{tabular}
\end{table}

The stability effect is the largest practical separation in the study.
Median paired stability difference is \(+0.866\) in favor of SHAP, and
the direction is consistent in all 75 matched cells. This indicates that
LIME's local surrogate sampling introduces substantial run-to-run
volatility under perturbation, whereas SHAP is comparatively invariant.

For sparsity, the sign is also consistent in all 75 matched cells, but
interpretation requires care: the metric here is active-feature ratio.
SHAP's larger value means denser explanations; thus LIME is systematically
sparser and therefore easier to compress for user-facing narratives.

Fidelity favors SHAP in all 75 matched cells, with a mean paired
difference of \(+0.248\) and a very large paired effect size
\((d_z=4.82)\). Faithfulness gap also favors SHAP in 74 of 75 matched
cells, with a mean paired difference of \(+0.045\) and a large paired
effect size \((d_z=2.63)\). These results indicate not only statistical
separation but practically meaningful quality gains under this protocol.
Figure~\ref{fig:quality_endpoints} visualizes these paired mean
separations for the four quality-oriented endpoints.

\begin{figure}[t]
\centering
\includegraphics[width=0.95\linewidth]{figures/fig_b1_quality_endpoints.pdf}
\caption{Paired mean comparison across quality-oriented primary endpoints
(\(n=75\) matched SHAP-LIME cells). Active ratio is reported directly;
lower values imply sparser explanations.}
\label{fig:quality_endpoints}
\end{figure}

### Runtime Distribution and Heterogeneity

The cost signal is significant but strongly heterogeneous. SHAP is slower
in 59 of 75 matched cells. Matched-cell median cost is 684.1 ms for
SHAP versus 65.7 ms for LIME, corresponding to a median SHAP/LIME cost
ratio of approximately \(5.3\times\). Means are more separated
(11,708.3 ms versus 3,660.7 ms) because the SHAP distribution is
heavy-tailed: the 90th and 95th percentile latencies are approximately
51,456 ms and 67,066 ms, respectively, compared with 12,825 ms and
13,192 ms for LIME. This tail behavior is concentrated in kernel-SHAP
contexts, especially SVM, which inflates mean cost beyond median
behavior.
Figure~\ref{fig:runtime_heterogeneity} shows both the overall log-scale
runtime distribution and model-level median heterogeneity.

Heterogeneity analysis by model family shows that quality ordering
(stability, sparsity-direction, fidelity, faithfulness gap) is robust,
while cost ranking is model dependent. In particular, SHAP is faster in
all 15 XGBoost matched cells and in one SVM cell, whereas LogReg, RF,
and MLP are uniformly SHAP-slower. Therefore, ``LIME is faster'' is a
majority statement in this cohort, but it is not universally true across
model classes.

\begin{figure}[t]
\centering
\includegraphics[width=0.98\linewidth]{figures/fig_b2_runtime_heterogeneity.pdf}
\caption{Runtime behavior under matched-cell pairing (\(n=75\)). Left:
overall cost distribution by method (log scale). Right: model-level
median cost (log scale), showing the XGBoost exception where SHAP is
faster while other families are SHAP-slower.}
\label{fig:runtime_heterogeneity}
\end{figure}

### Synthesis of Trade-offs

The empirical frontier is clear: SHAP delivers higher reliability and
faithfulness at substantially higher expected runtime, while LIME delivers
lower latency and stronger compression at the cost of robustness. The
results therefore support objective-driven selection rather than global
method supremacy. For assurance-critical analysis, SHAP's quality margin
is large and consistent. For interaction-critical systems, LIME's runtime
profile remains operationally attractive.

## Practical Recommendations


Based on these empirical findings, we propose the \textbf{Hybrid
Deployment Pattern}:

\begin{enumerate}[leftmargin=*]
\item \textbf{Tier 1: Real-Time / End-User (Use LIME)}
\begin{itemize}[leftmargin=*]
\item Use when explaining predictions to end-users in a live application
(e.g., ``Why was my loan denied?'' in a mobile app).
\item Evidence basis: lower matched median runtime (65.7 ms) and
systematically lower active-feature ratio under the current protocol.
\item Recommended use condition: interactive settings where sub-second
latency and compact explanations matter more than maximizing fidelity.
\item Caveat: XGBoost is an exception in this cohort, where SHAP is
consistently faster than LIME.
\end{itemize}
\item \textbf{Tier 2: Auditing / Data Science (Use SHAP)}
\begin{itemize}[leftmargin=*]
\item Use when analyzing model bias, debugging model logic, or responding
to regulatory inquiries.
\item Evidence basis: consistent paired advantages in stability,
fidelity, and faithfulness gap across the matched cohort.
\item Recommended use condition: analyst-mediated or offline workflows
where second-level or minute-level latency is acceptable.
\item Caveat: runtime costs depend strongly on whether SHAP operates in
tree-specific or kernel mode.
\end{itemize}
\end{enumerate}

## Validity Boundaries

### Statistical and Construct Validity

This manuscript's confirmatory claims are restricted to the 75 fully
matched SHAP-LIME cells in the EXP2 robustness cohort. Unlike the full
multi-method benchmark reported in Paper A, the pairwise subset used
here is claim-complete after artifact qualification: 75 LIME runs and
75 SHAP runs remain available for paired inference. Reported metrics are
implementation-bound rather than abstract labels; their operational
definitions are anchored in \path{src/metrics/fidelity.py},
\path{src/metrics/stability.py}, \path{src/metrics/sparsity.py},
\path{src/metrics/faithfulness.py}, and \path{src/metrics/cost.py}. No
semantic, human-utility, or LLM-judge claim enters the confirmatory
scope of this paper.

### Internal and External Validity

Runtime comparisons are protocol-specific. SHAP combines TreeExplainer
for tree models and KernelExplainer for non-tree models, whereas LIME is
run with fixed local-surrogate settings
(\texttt{num\_features=10}, effective \texttt{num\_samples=1000},
\texttt{kernel\_width=3.0}). Accordingly, the reported cost gap reflects
both method family and concrete implementation pathway. External
generalization beyond Adult tabular classification is not established;
rankings may shift under different datasets, modalities, feature
transformations, masking schemes, or hyperparameter settings.

### Reproducibility and Operational Validity

All reported claims are traceable to seeded YAML configurations, per-run
\texttt{results.json} artifacts, explicit exclusion of malformed or
empty runs, and inferential exports under
\path{outputs/analysis/paper\_a\_exp2\_stats/}. The current merged
recovery snapshot contains 252 analyzable unique runs overall, but the
Paper B subset is fully matched and therefore sufficient for the
SHAP-versus-LIME claims made here. Figures are regenerated directly from
\path{wilcoxon\_shap\_lime\_all\_models.csv} and
\path{paired\_cells\_shap\_lime\_all\_models.csv}, and no synthetic
imputation is used at any stage.

## Limitations and Future Work


\begin{itemize}
\item \textbf{Data Set Scope}: This study focuses on tabular data (Adult).
Image and text domains may exhibit different trade-offs.
\item \textbf{Configuration Space}: We compared standard configurations
(KernelSHAP versus standard LIME). Hyperparameter tuning (e.g., LIME
kernel width) can alter results.
\item \textbf{Runtime Heterogeneity}: Cost differences are strongly
model-family dependent; the XGBoost exception shows that ``LIME is
faster'' should not be interpreted as a universal rule.
\item \textbf{Human-Centered Utility}: This paper does not establish
human-grounded usefulness or semantic clarity; validated user studies or
human-calibrated semantic evaluation remain future work.
\item \textbf{Next Extensions}: Replication on additional datasets and
integration of thesis-planned causal or counterfactual endpoints remain
open follow-up tasks rather than current contributions.
\end{itemize}

## Code and Artifact Availability

The current manuscript draft and supporting materials are available in
the public repository at
\url{https://github.com/jonnabio/xai-eval-framework}. Materials needed
to reproduce Paper B include:
\begin{itemize}[leftmargin=*]
\item \path{experiments/exp2\_scaled/results/}
\item inferential export directory:
\path{outputs/analysis/paper\_a\_exp2\_stats/}
\item key export: \texttt{analysis\_summary.json}
\item key export: \texttt{wilcoxon\_shap\_lime\_all\_models.csv}
\item key export: \texttt{paired\_cells\_shap\_lime\_all\_models.csv}
\item \path{scripts/run\_exp2\_statistical\_analysis.py}
\item \path{scripts/generate\_paper\_b\_figures.py}
\item manuscript sources under \path{docs/reports/paper\_b/}
\end{itemize}
The repository is released under the MIT License. Before journal
submission, the exact review snapshot should be frozen as a versioned
release and archived under a version-specific DOI.

## Conclusion


The choice between LIME and SHAP is not a matter of ``better,'' but of
``fit for purpose.'' Under this protocol, SHAP is the preferred choice
when stability and fidelity-oriented quality dominate the objective,
while LIME remains the pragmatic option when latency and compactness are
the primary constraints. Our paired analysis across 75 matched
robustness cells shows consistent SHAP advantages in stability,
fidelity, and faithfulness gap, alongside systematic LIME advantages in
sparsity and lower runtime for most (but not all) model contexts. This
evidence supports architecture-level deployment patterns that separate
user-facing low-latency explanation paths from high-assurance auditing
workflows.

### Acknowledgements

\acks{This work received no external funding. The study was self-funded
by the author, and the author reports no competing interests. This
draft was prepared from repository artifacts dated March 2026.}

## References

```latex
\begin{thebibliography}{99}

\bibitem[Agrawal et~al.(2025)Agrawal, El Shawi, and Ahmed]{agrawal2025xaieval}
Agrawal, K., El Shawi, R., and Ahmed, N. (2025).
XAI-Eval: A framework for comparative evaluation of explanation methods
in healthcare.
\emph{DIGITAL HEALTH}, 11:20552076251368045.
\url{https://doi.org/10.1177/20552076251368045}.

\bibitem[Agarwal et~al.(2022)Agarwal, Ley, Krishna, Saxena, Pawelczyk, Johnson,
Puri, Zitnik, and Lakkaraju]{agarwal2022openxai}
Agarwal, C., Ley, D., Krishna, S., Saxena, E., Pawelczyk, M., Johnson, N.,
Puri, I., Zitnik, M., and Lakkaraju, H. (2022).
OpenXAI: Towards a transparent evaluation of model explanations.
In \emph{Thirty-Sixth Conference on Neural Information Processing Systems
Datasets and Benchmarks Track}.
\url{https://openreview.net/forum?id=MU2495w47rz}.

\bibitem[Ali et~al.(2023)Ali, Abuhmed, El-Sappagh, Muhammad, Alonso-Moral,
Confalonieri, Guidotti, Del Ser, D\'{i}az-Rodr\'{i}guez, and Herrera]{ali2023trustworthy}
Ali, S., Abuhmed, T., El-Sappagh, S., Muhammad, K., Alonso-Moral, J. M.,
Confalonieri, R., Guidotti, R., Del Ser, J., D\'{i}az-Rodr\'{i}guez, N.,
and Herrera, F. (2023).
Explainable Artificial Intelligence (XAI): What we know and what is left
to attain Trustworthy Artificial Intelligence.
\emph{Information Fusion}, 99:101805.
\url{https://doi.org/10.1016/j.inffus.2023.101805}.

\bibitem[Breiman(2001)]{breiman2001random}
Breiman, L. (2001).
Random forests.
\emph{Machine Learning}, 45(1):5--32.

\bibitem[Canha et~al.(2025)Canha, Kubler, Fr\"{a}mling, and Fagherazzi]{canha2025benchmark}
Canha, D., Kubler, S., Fr\"{a}mling, K., and Fagherazzi, G. (2025).
A Functionally-Grounded Benchmark Framework for XAI Methods: Insights
and Foundations from a Systematic Literature Review.
\emph{ACM Computing Surveys}, 57(12):1--40.
\url{https://doi.org/10.1145/3737445}.

\bibitem[Chen and Guestrin(2016)]{chen2016xgboost}
Chen, T. and Guestrin, C. (2016).
XGBoost: A scalable tree boosting system.
In \emph{Proceedings of the 22nd ACM SIGKDD International Conference on
Knowledge Discovery and Data Mining}, 785--794.

\bibitem[Dems\v{s}ar(2006)]{demsar2006statistical}
Dems\v{s}ar, J. (2006).
Statistical comparisons of classifiers over multiple data sets.
\emph{Journal of Machine Learning Research}, 7:1--30.

\bibitem[Gu et~al.(2024)Gu, Jiang, Shi, Tan, Zhai, Xu, Li, Shen, Ma, Liu,
Wang, Zhang, Wang, Gao, Ni, and Guo]{gu2024llmjudge}
Gu, J., Jiang, X., Shi, Z., Tan, H., Zhai, X., Xu, C., Li, W., Shen, Y.,
Ma, S., Liu, H., Wang, S., Zhang, K., Wang, Y., Gao, W., Ni, L., and Guo, J.
(2024).
A survey on LLM-as-a-Judge.
\emph{arXiv preprint arXiv:2411.15594}.
\url{https://doi.org/10.48550/arXiv.2411.15594}.

\bibitem[Holm(1979)]{holm1979simple}
Holm, S. (1979).
A simple sequentially rejective multiple test procedure.
\emph{Scandinavian Journal of Statistics}, 6(2):65--70.

\bibitem[Kohavi(1996)]{kohavi1996scaling}
Kohavi, R. (1996).
Scaling up the accuracy of Naive-Bayes classifiers: A decision-tree
hybrid.
In \emph{Proceedings of the Second International Conference on Knowledge
Discovery and Data Mining}, 202--207.

\bibitem[Lakens(2013)]{lakens2013calculating}
Lakens, D. (2013).
Calculating and reporting effect sizes to facilitate cumulative science:
A practical primer for \(t\)-tests and ANOVAs.
\emph{Frontiers in Psychology}, 4:863.

\bibitem[Longo et~al.(2024)Longo, Brcic, Cabitza, Choi, Confalonieri, Del
Ser, Guidotti, Hayashi, Herrera, Holzinger, Jiang, Khosravi, Lecue,
Malgieri, P\'{a}ez, Samek, Schneider, Speith, and Stumpf]{longo2024manifesto}
Longo, L., Brcic, M., Cabitza, F., Choi, J., Confalonieri, R., Del Ser, J.,
Guidotti, R., Hayashi, Y., Herrera, F., Holzinger, A., Jiang, R.,
Khosravi, H., Lecue, F., Malgieri, G., P\'{a}ez, A., Samek, W.,
Schneider, J., Speith, T., and Stumpf, S. (2024).
Explainable artificial intelligence (XAI) 2.0: A manifesto of open
challenges and interdisciplinary research directions.
\emph{Information Fusion}, 106:102301.
\url{https://doi.org/10.1016/j.inffus.2024.102301}.

\bibitem[Lundberg and Lee(2017)Lundberg and Lee]{lundberg2017unified}
Lundberg, S. M. and Lee, S.-I. (2017).
A unified approach to interpreting model predictions.
In \emph{Advances in Neural Information Processing Systems}, 4765--4774.

\bibitem[Pawlicki et~al.(2024)Pawlicki, Pawlicka, Uccello, Szelest,
D'Antonio, Kozik, and Chora\'{s}]{pawlicki2024metrics}
Pawlicki, M., Pawlicka, A., Uccello, F., Szelest, S., D'Antonio, S.,
Kozik, R., and Chora\'{s}, M. (2024).
Evaluating the necessity of the multiple metrics for assessing
explainable AI: A critical examination.
\emph{Neurocomputing}, 602:128282.
\url{https://doi.org/10.1016/j.neucom.2024.128282}.

\bibitem[Retzlaff et~al.(2024)Retzlaff, Angerschmid, Saranti, Schneeberger,
R\"{o}ttger, M\"{u}ller, and Holzinger]{retzlaff2024posthoc}
Retzlaff, C. O., Angerschmid, A., Saranti, A., Schneeberger, D.,
R\"{o}ttger, R., M\"{u}ller, H., and Holzinger, A. (2024).
Post-hoc vs ante-hoc explanations: xAI design guidelines for data
scientists.
\emph{Cognitive Systems Research}, 86:101243.
\url{https://doi.org/10.1016/j.cogsys.2024.101243}.

\bibitem[Ribeiro et~al.(2016)Ribeiro, Singh, and Guestrin]{ribeiro2016why}
Ribeiro, M. T., Singh, S., and Guestrin, C. (2016).
Why should I trust you?: Explaining the predictions of any classifier.
In \emph{Proceedings of the 22nd ACM SIGKDD International Conference on
Knowledge Discovery and Data Mining}, 1135--1144.

\bibitem[Sithakoul et~al.(2024)Sithakoul, Meftah, and Feutry]{sithakoul2024beexai}
Sithakoul, S., Meftah, S., and Feutry, C. (2024).
BEExAI: Benchmark to evaluate explainable AI.
In \emph{Explainable Artificial Intelligence}, 445--468.
Springer Nature Switzerland.
\url{https://doi.org/10.1007/978-3-031-63787-2_23}.

\bibitem[Wilcoxon(1945)]{wilcoxon1945individual}
Wilcoxon, F. (1945).
Individual comparisons by ranking methods.
\emph{Biometrics Bulletin}, 1(6):80--83.

\bibitem[Wu et~al.(2025)Wu, Kaushik, Li, Bauer, and Onoue]{wu2025userperceptions}
Wu, X., Kaushik, R., Li, W., Bauer, L., and Onoue, K. (2025).
User perceptions vs. proxy LLM judges: Privacy and helpfulness in LLM
responses to privacy-sensitive scenarios.
\emph{arXiv preprint arXiv:2510.20721}.
\url{https://doi.org/10.48550/arXiv.2510.20721}.

\bibitem[Zheng et~al.(2023)Zheng, Chiang, Sheng, Zhuang, Wu, Zhuang, Lin, Li,
Li, Xing, Zhang, Gonzalez, and Stoica]{zheng2023judging}
Zheng, L., Chiang, W.-L., Sheng, Y., Zhuang, S., Wu, Z., Zhuang, Y.,
Lin, Z., Li, Z., Li, D., Xing, E. P., Zhang, H., Gonzalez, J. E.,
and Stoica, I. (2023).
Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena.
In \emph{Advances in Neural Information Processing Systems 36:
Datasets and Benchmarks Track}.
\url{https://doi.org/10.48550/arXiv.2306.05685}.

\bibitem[Zheng et~al.(2025)Zheng, Shirani, Chen, Lin, Cheng, Guo, and Luo]{zheng2025ffidelity}
Zheng, X., Shirani, F., Chen, Z., Lin, C., Cheng, W., Guo, W., and Luo, D.
(2025).
F-Fidelity: A robust framework for faithfulness evaluation of explainable AI.
In \emph{The Thirteenth International Conference on Learning
Representations (ICLR)}.
\url{https://openreview.net/forum?id=X0r4BN50Dv}.

\bibitem[Zhou et~al.(2025)Zhou, Xie, Li, Zhan, Song, Yang, Espinoza, Welton,
Mai, Jin, Xu, Chung, Xing, Tsai, Schaffer, Shi, Liu, Liu, and Zhang]{zhou2025medthink}
Zhou, S., Xie, W., Li, J., Zhan, Z., Song, M., Yang, H., Espinoza, C.,
Welton, L., Mai, X., Jin, Y., Xu, Z., Chung, Y.-H., Xing, Y., Tsai, M.-H.,
Schaffer, E., Shi, Y., Liu, N., Liu, Z., and Zhang, R. (2025).
Automating expert-level medical reasoning evaluation of large language models.
\emph{npj Digital Medicine}, 9(1):34.
\url{https://doi.org/10.1038/s41746-025-02208-7}.

\end{thebibliography}
```
