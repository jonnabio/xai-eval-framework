# From Fidelity to Semantics: A Taxonomy and Survey of Evaluation Metrics for Model-Agnostic Explainability

This Markdown file mirrors the current LaTeX prototype content for Paper C. Mathematical expressions, lists, and citations are preserved in LaTeX-style notation where useful.

## Abstract

Evaluation remains the least consolidated part of explainable AI (XAI). While model-agnostic post-hoc methods such as LIME, SHAP, Anchors, and DiCE are widely used, the criteria used to judge them vary sharply across papers, toolkits, and application domains. Some studies emphasize faithfulness proxies, others prioritize stability, sparsity, or human plausibility, and newer work introduces Large Language Models (LLMs) as semantic evaluators without a unified framework for locating those judgments within the broader evaluation landscape. This paper presents a structured survey and taxonomy of evaluation metrics for model-agnostic explainability, focusing on how technical proxy metrics, benchmark-grounded metrics, human evaluation, and LLM-based semantic evaluation relate to one another. Using a cleaned 24-study coded review corpus derived from the thesis literature matrix, we organize XAI evaluation along four axes: evaluation target, evidence source, quality property, and task context. The taxonomy is grounded back into the thesis evidence stack: EXP1 supplies reproducibility evidence, EXP2 supplies confirmatory Adult benchmark evidence, and EXP3 supplies compact external-validation evidence on Breast Cancer and German Credit. The resulting taxonomy clarifies where current metrics overlap, where they leave construct gaps, and why semantic evaluation should be treated as a complementary layer rather than a replacement for robustness- and fidelity-oriented measurement. The paper closes by mapping the taxonomy back to the thesis framework, motivating the benchmark design of Paper B and the evaluator-validation agenda of Paper A.

**Keywords:** explainable ai, evaluation metrics, survey, taxonomy, semantic evaluation, llm-as-a-judge

## Introduction

Progress in explainable AI depends not only on generating explanations, but on evaluating whether those explanations are useful, faithful, stable, and meaningful. Yet the literature does not converge on a single definition of explanation quality. Surveys repeatedly note that XAI evaluation is fragmented across proxy metrics, qualitative user studies, and domain-specific desiderata \citep{adadi2018xai,arrieta2020xai,kadir2023metrics,canha2025functionally}. As a result, comparisons between explainers often depend as much on the chosen metric family as on the methods being compared.

This fragmentation is especially visible in model-agnostic post-hoc explainability. Faithfulness-style metrics remain common because they are relatively easy to compute, but they do not fully capture whether an explanation is understandable, semantically aligned with domain knowledge, or decision-useful in practice \citep{ali2023trustworthy,longo2024manifesto}. Multi-metric work argues that stability, sparsity, and computational cost are also part of explanation quality, and recent critical examinations show that different metrics can reveal complementary rather than redundant behavior \citep{pawlicki2024multiple,zheng2025ffidelity}.

At the same time, a new line of work uses LLMs as evaluators of explanation quality or human-centered criteria. This is promising because LLMs can score natural-language justifications, compare competing explanations, and operationalize semantic rubrics at scale. However, research on LLM-as-a-judge also warns that proxy judges can drift from human judgments, inherit style biases, and compress distinct quality dimensions into superficially coherent scores \citep{zheng2023judging,gu2024llmjudge,wu2025userperceptions}. For XAI, this raises a conceptual problem before it raises an empirical one: where should semantic evaluation sit relative to fidelity, robustness, and other established metric families?

This paper addresses that question through a structured survey and taxonomy for model-agnostic XAI evaluation. Rather than proposing a new explainer or a new benchmark, the paper organizes the metric space needed to interpret the rest of the thesis. In the current dissertation plan, Paper B provides the quantitative benchmark layer and Paper A validates LLM-based semantic evaluation against human judgments. Paper C supplies the conceptual bridge between them.

Our contributions are:

1. A taxonomy of XAI evaluation metrics structured by evaluation target, evidence source, quality property, and task context.
2. A comparative synthesis of technical proxy metrics, benchmark-grounded metrics, human evaluation, and LLM-based semantic evaluation.
3. A gap analysis showing where current metrics fail to capture explanation meaning or user-facing adequacy.
4. A thesis-facing integration layer that motivates why Paper B needs a multi-metric benchmark and why Paper A needs explicit evaluator validation.

Scope is intentionally limited to model-agnostic post-hoc explainability, with emphasis on tabular settings but attention to transfer issues across image, text, time series, and graph contexts. The paper is a structured narrative survey with explicit coding dimensions, corpus accounting, and traceable repository artifacts, not a claim of exhaustive bibliometric coverage or meta-analysis.

## Background and Definitions

To keep the taxonomy precise, we distinguish several terms that are often conflated in XAI writing.

First, intrinsic explainability and post-hoc explainability should not be evaluated as if they pose the same problem. Intrinsic models are designed to be interpretable by construction, whereas post-hoc methods attempt to explain black-box behavior after model training \citep{rudin2019stop,retzlaff2024posthoc}. This paper focuses on the latter because Papers A and B evaluate post-hoc model-agnostic explainers.

Second, explanation quality is not identical to model quality. A model may be accurate while producing unstable or semantically weak explanations; conversely, a model can support concise explanations without necessarily being more accurate. Evaluation therefore needs to specify whether the object under study is the explanation artifact, the explainer method, the predictive model, or the user-facing decision process.

Third, local and global explanations require different expectations. Local attributions or counterfactuals are often judged through faithfulness, sparsity, or actionability, while global summaries may be judged by coverage, consistency, or conceptual coherence. Many reported metric disagreements arise because these explanatory levels are mixed without an explicit task framing.

Finally, semantic evaluation should be separated from purely structural proxy metrics. A metric such as perturbation faithfulness evaluates whether feature rankings track model sensitivity under a chosen intervention scheme. A semantic judgment evaluates whether an explanation ``makes sense'' under domain, causal, or linguistic criteria. Both matter, but they are not interchangeable.

## Review Method and Coding Protocol

This prototype uses a structured narrative review protocol anchored in the repository's literature matrix, `docs/reports/literature_review_methodology_matrix.md`. For the current repository snapshot, the Paper C corpus was frozen on `2026-04-05`. The upstream matrix contained 25 rows; one duplicate record for the Pawlicki et al. multiple-metrics paper was removed during Paper C-specific cleaning, leaving 24 unique coded papers. The cleaned corpus is stored in `docs/reports/paper_c/paper_c_review_corpus.csv`, and a regenerated descriptive summary is stored in `docs/reports/paper_c/paper_c_review_summary.md`.

The coded corpus spans five thematic clusters already implied by the thesis materials: metric taxonomies and surveys (3 papers), benchmark and toolkit papers (3), faithfulness and robustness studies (8), modality-specific or domain-specific evaluations (6), and LLM-as-a-judge / proxy-human-evaluation papers (4). This spread is sufficient for thesis framing and gap analysis, but it is still better understood as a transparent working corpus than as an exhaustive bibliometric sample.

The review objective is to answer four organizing questions:

1. What kinds of objects are current XAI metrics actually evaluating?
2. What evidence sources do they rely on?
3. Which quality properties do they operationalize?
4. Where do semantic or human-centered judgments become necessary?

Each source in the coded corpus is assigned to one or more thematic clusters:

- metric taxonomies and surveys;
- benchmark and toolkit papers;
- faithfulness and robustness studies;
- modality-specific or domain-specific evaluations;
- LLM-as-a-judge and proxy-human-evaluation papers.

For the prototype, inclusion is defined pragmatically: a source must contribute either a formal evaluation construct, a benchmark design principle, a warning about metric misuse, or an evaluation paradigm directly relevant to post-hoc model-agnostic explanations. Exclusion applies to papers that focus solely on generating explanations without materially informing evaluation design.

Beyond the four core taxonomy axes, the Paper C coding file records paper role, modality context, LLM-validation relevance, and source-confidence labels. The confidence labels are inherited from the upstream literature matrix (`high`, `medium`, or `title-level`) so that uncertainty remains visible instead of being flattened away. Coding was conducted as a single-reviewer synthesis pass for thesis integration rather than as an inter-rater systematic review exercise.

Table 1 summarizes the coding dimensions used in this survey.

```latex
\begin{table}[t]
\centering
\caption{Coding dimensions used to build the Paper C taxonomy.}
\begin{tabularx}{\linewidth}{l X}
\toprule
\textbf{Dimension} & \textbf{Operational question} \\
\midrule
Evaluation target & What is being judged: explanation artifact, explainer, model behavior, or user/task outcome? \\
Evidence source & What kind of evidence supports the judgment: perturbation proxy, benchmark ground truth, human rating, user task, or LLM judge? \\
Quality property & Which property is being claimed: fidelity, stability, sparsity, plausibility, recourse quality, semantic alignment, etc.? \\
Task context & In what modality or domain is the metric assumed to be meaningful? \\
\bottomrule
\end{tabularx}
\end{table}
```

This protocol is intentionally lighter than PRISMA-style systematic review practice. The goal of the prototype is conceptual organization and thesis integration, not final exhaustive coverage claims.

Table 2 summarizes the current coded corpus at a glance.

```latex
\begin{table}[t]
\centering
\caption{Descriptive profile of the cleaned Paper C review corpus.}
\begin{tabularx}{\linewidth}{l X}
\toprule
\textbf{Profile item} & \textbf{Current value} \\
\midrule
Corpus freeze date & 2026-04-05 \\
Upstream matrix rows reviewed & 25 \\
Duplicate rows removed during Paper C cleaning & 1 \\
Unique coded papers & 24 \\
Primary cluster distribution & 8 faithfulness/robustness, 6 modality/domain, 4 LLM-judge, 3 benchmark/toolkit, 3 taxonomy/survey \\
Evidence-source coverage & 20 proxy, 6 benchmark, 4 LLM-judge, 4 end-user, 3 expert-human \\
Confidence mix & 19 high, 3 medium, 2 title-level \\
\bottomrule
\end{tabularx}
\end{table}
```

The descriptive profile immediately reveals a strong proxy skew: 20 of 24 coded papers rely on proxy evidence, whereas only 3 directly use expert-human evidence and 4 use end-user evidence. Paper C should therefore be read as a map of the current evidence landscape, not as proof that human-grounded constructs are already mature or standardized.

## Taxonomy of XAI Evaluation Metrics

The central claim of this paper is that XAI evaluation can be clarified by crossing four axes: evaluation target, evidence source, quality property, and task context. This section develops that taxonomy and shows why metrics that appear to answer the same question often do not.

### 1. Taxonomy by Evaluation Target

Many metric disagreements start with a hidden mismatch about what is being evaluated.

- **Explanation artifact metrics** evaluate the produced explanation itself, such as attribution sparsity, local fidelity, or semantic clarity.
- **Explainer method metrics** evaluate the behavior of the explainer across cases, such as stability, reproducibility, or computational cost.
- **Model-behavior metrics** evaluate whether explanations track model behavior under perturbations or alternative decision regions.
- **User/task outcome metrics** evaluate whether explanations improve decision performance, trust calibration, or actionability.

This distinction matters because one metric family cannot automatically stand in for another. For example, a sparse explanation can still be semantically misleading, and a faithful attribution can still be unusable in a decision-support workflow.

### 2. Taxonomy by Evidence Source

The second axis concerns the evidence used to justify the evaluation:

- **Proxy or perturbation metrics** infer quality from numerical sensitivity behavior.
- **Benchmark-grounded metrics** compare explanations to synthetic or domain-defined ground truth.
- **Human expert judgments** evaluate plausibility, correctness, or domain alignment.
- **End-user studies** assess comprehension, trust calibration, decision quality, or workload.
- **LLM judges** provide scalable semantic scoring using rubric-guided language-model evaluation.

These evidence sources are not equally strong for every construct. Proxy metrics are scalable and reproducible but may under-capture meaning. Human judgments are richer but expensive and variable. LLM judges sit in between: they are scalable like proxies but semantically expressive like human reviews, which is precisely why their validity must be established rather than assumed \citep{gu2024llmjudge,wu2025userperceptions,zhou2025medthink}.

### 3. Taxonomy by Quality Property

The literature repeatedly returns to a familiar set of quality properties, but not always with consistent definitions.

- **Fidelity / faithfulness:** whether the explanation tracks how the model actually behaves under feature interventions or masking \citep{ribeiro2016why,lundberg2017unified,zheng2025ffidelity}.
- **Stability / robustness:** whether similar inputs yield similar explanations under perturbation or reruns \citep{pawlicki2024multiple,canha2025functionally}.
- **Sparsity / parsimony:** whether the explanation is concise enough to be interpretable without unnecessary feature load.
- **Plausibility:** whether the explanation aligns with domain expectations or expert reasoning.
- **Counterfactual or recourse quality:** whether explanation-linked interventions are feasible, minimal, diverse, or actionable \citep{mothilal2020dice}.
- **Semantic alignment:** whether an explanation captures meaningful causal or conceptual structure, even when pure proxy metrics are agnostic to that structure.

The key observation is that these properties are only partly commensurable. A method can score strongly on fidelity while remaining weak on sparsity or semantic adequacy. Multi-metric reporting is therefore not a luxury; it is often the minimum needed to make XAI claims interpretable.

To reduce construct drift, Table 3 records the working construct dictionary used in this survey. The table does not claim universal definitions; it documents the meanings used to code the current corpus and to discipline later thesis claims.

```latex
\begin{table}[t]
\centering
\caption{Working construct dictionary used in the Paper C coding pass.}
\begin{tabularx}{\linewidth}{l X X}
\toprule
\textbf{Construct} & \textbf{Working operational meaning} & \textbf{Strongest direct evidence} \\
\midrule
Fidelity / faithfulness & Whether the explanation tracks model behavior under a specified intervention or masking scheme. & Proxy tests and benchmark-grounded checks \\
Stability / robustness & Whether explanations remain consistent across reruns, perturbations, or nearby inputs. & Proxy perturbation studies and repeated-run analyses \\
Sparsity / parsimony & Whether explanations keep feature load low enough to remain cognitively manageable. & Structural summaries of explanation size or weight concentration \\
Plausibility & Whether explanations align with expert expectations or domain logic. & Expert-human review with explicit rubrics \\
Semantic alignment & Whether explanations capture meaningful conceptual or causal structure beyond structural proxy success. & Expert review or validated semantic evaluators \\
User usefulness & Whether explanations improve comprehension, decision quality, or trust calibration in an actual task. & End-user studies with task outcomes \\
\bottomrule
\end{tabularx}
\end{table}
```

### 4. Taxonomy by Task Context

Metric validity also depends on context. Tabular benchmarks often make strong assumptions about feature independence, perturbation realism, and local neighborhoods. These assumptions can fail in image, text, graph, and time-series settings, where perturbations may create out-of-distribution examples or semantically invalid transformations \citep{agarwal2023gnn_eval,proszewska2025bxaic}. This does not make cross-modal benchmarks impossible, but it does mean that metric transport cannot be assumed.

Table 4 synthesizes the main metric families discussed in the prototype.

```latex
\begin{table}[t]
\centering
\caption{Core metric families in model-agnostic XAI evaluation.}
\begin{tabularx}{\linewidth}{l l l X X}
\toprule
\textbf{Metric family} & \textbf{Typical evidence} & \textbf{Primary target} & \textbf{Strengths} & \textbf{Main blind spots} \\
\midrule
Fidelity / faithfulness & perturbation proxy & explanation-model relation & scalable, comparable, quantitative & intervention design may not reflect semantic validity \\
Stability / robustness & repeated perturbation or reruns & explainer behavior & detects volatility and stochastic fragility & high stability can coexist with low meaning \\
Sparsity / parsimony & structural summary & explanation artifact & captures concision and feature load & concise explanations may omit essential nuance \\
Benchmark-grounded correctness & synthetic or domain ground truth & explanation artifact & strong when ground truth is credible & ground truth is often unavailable or simplified \\
Human expert review & rubric-based judgment & explanation artifact / task & captures plausibility and domain alignment & expensive, slow, and subject to annotator variation \\
User-centered evaluation & user study or task success & decision support outcome & closest to real usage impact & hard to scale and compare across studies \\
LLM-based semantic evaluation & prompted rubric scoring & explanation semantics & scalable semantic scoring and decomposition & requires calibration; may drift from users or experts \\
\bottomrule
\end{tabularx}
\end{table}
```

## Comparative Synthesis and Open Gaps

The taxonomy exposes three recurring gaps in current XAI evaluation practice.

### Gap 1: Proxy metrics are necessary but not sufficient

Faithfulness, stability, and sparsity remain essential because they create reproducible, quantitative anchors for benchmark comparison. Papers B and related benchmark work depend on these anchors for statistical comparison across explainers \citep{agarwal2022openxai,hedstrom2023quantus,canha2025functionally}. However, the cleaned Paper C corpus shows how dominant these proxies have become: 20 of 24 coded studies use proxy evidence, while only 6 use benchmark-grounded evidence and even fewer use human-grounded evidence. This explains why structural metrics are comparatively well standardized while meaning-oriented constructs remain thinly operationalized. Proxy metrics do not directly answer whether an explanation reflects domain logic, causal relevance, or user-meaningful interpretation.

### Gap 2: Human-grounded constructs are underspecified

The literature frequently invokes interpretability, clarity, plausibility, and usefulness, but these are often under-operationalized. In the current coded corpus, only 3 studies directly use expert-human evidence and 4 use end-user evidence, and those papers are concentrated in evaluator-validation settings rather than in the core explainer-benchmark literature. When human studies do exist, their tasks, rubrics, and participant populations vary so widely that direct comparison is difficult \citep{ali2023trustworthy,longo2024manifesto}. This weakens cumulative progress because the same label may refer to different constructs across papers, which is why the construct dictionary in Table 3 is necessary even for a thesis-scoped survey.

### Gap 3: Semantic evaluation is rising faster than its validation base

LLM-based judging offers a practical way to score explanation quality at scale, especially when explanations or rubrics are textual. But the broader LLM-as-a-judge literature shows that proxy judges can display position bias, verbosity bias, or agreement illusions \citep{zheng2023judging,gu2024llmjudge}. The coded Paper C corpus contains 4 LLM-validation-relevant entries, one of which is itself a survey rather than a direct validation study. That is a visible but still small empirical base. In XAI, semantic evaluator outputs should therefore be treated as calibrated proxies rather than as self-validating replacements for expert review. This gap directly motivates Paper A.

Figure 1 summarizes the evaluation continuum emphasized by this survey.

```latex
\begin{figure}[t]
\centering
\fbox{\begin{minipage}{0.94\linewidth}
\centering
\textbf{Evaluation continuum for post-hoc XAI}\\[4pt]
Proxy metrics $\rightarrow$ benchmark-grounded checks $\rightarrow$ expert judgment $\rightarrow$ user-centered evaluation\\
\vspace{3pt}
\footnotesize LLM-based semantic evaluation occupies an intermediate role: more expressive than proxy metrics, more scalable than human review, but not self-validating.
\end{minipage}}
\caption{Conceptual placement of semantic evaluation within the broader XAI evaluation landscape.}
\label{fig:continuum}
\end{figure}
```

The prototype synthesis therefore argues for layered evaluation. Proxy metrics should anchor reproducibility and comparative benchmarking. Human or semantic layers should be added when the claim concerns meaning, plausibility, or causal adequacy. The mistake is not using one family or the other; it is allowing any single family to monopolize the definition of explanation quality.

## Implications for the Thesis Framework

The value of Paper C is not only descriptive. It directly organizes the thesis architecture.

First, the taxonomy justifies the multi-metric benchmark design of Paper B. If explanation quality spans fidelity, stability, sparsity, and computational burden, then a benchmark based on one endpoint would understate meaningful trade-offs. Paper B therefore occupies the proxy-and-robustness layer of the taxonomy.

Second, the taxonomy explains why Paper A is necessary. Once the thesis claims to measure causal alignment, counterfactual sensitivity, or semantic adequacy through LLM evaluators, those evaluators become measurement instruments rather than convenience tools. Their agreement with human experts must therefore be validated. Paper A occupies the semantic-evaluator validation layer of the taxonomy.

At the current repository snapshot, the thesis already contains LLM-evaluation infrastructure, prompt templates, stratified sampling, and a human-annotation interface. The LLM-based semantic proxy layer is complete for thesis reporting, but the human-validation layer is not yet complete as confirmatory evidence: pilot human responses are insufficient for a human--LLM correlation claim, and human-rater agreement analysis remains a future calibration step. Paper A should therefore be framed as an active evaluator-validation study rather than as a finished human-validation layer.

Third, the survey suggests a thesis-wide minimal evaluation stack:

1. technical proxy metrics for fidelity, stability, sparsity, and cost;
2. benchmark reporting with explicit scope and artifact traceability;
3. semantic evaluation for constructs not captured by numerical proxies;
4. human validation whenever semantic claims become confirmatory rather than exploratory.

This layered view also clarifies claim discipline. Benchmark evidence can support comparative technical claims. Semantic evaluator outputs can support exploratory interpretation until calibrated. Human agreement evidence can then convert those semantic constructs into stronger confirmatory claims.

## Limitations

This prototype has several boundaries.

First, it is a structured narrative survey rather than a finalized systematic review. The coded corpus is explicit and traceable, but it is not yet a complete database-driven search with full screening logs, deduplication workflow reporting, and flow diagrams.

Second, the paper emphasizes model-agnostic post-hoc XAI because that is the thesis focus. Intrinsic interpretability, representation-level interpretability, and some modality-specific traditions are only covered insofar as they affect metric transfer or scope boundaries.

Third, the paper argues for semantic evaluation as a necessary layer but does not itself validate LLM judges. That validation belongs to Paper A.

Fourth, the current coding pass is single-reviewer and inherits 3 `medium`-confidence and 2 `title-level` records from the upstream thesis matrix. Future versions should either deepen those entries through full-text coding or replace them with higher-confidence sources.

Finally, the taxonomy organizes construct space, not effect sizes. It clarifies what should be measured and why, but it does not estimate a pooled numerical ranking across studies.

## Conclusion

XAI evaluation is not one problem but a family of related measurement problems. The literature has developed useful metric families for fidelity, robustness, sparsity, and benchmark reproducibility, yet these families do not fully capture semantic adequacy or human-centered meaning. By organizing model-agnostic post-hoc evaluation along the axes of evaluation target, evidence source, quality property, and task context, this paper clarifies why metric disagreement is common and why layered evaluation is necessary.

The main practical implication is simple: benchmark metrics and semantic evaluation should be treated as complementary rather than competing forms of evidence. Within the thesis, this means Paper B should provide the quantitative comparative baseline, while Paper A should validate the semantic evaluator layer that benchmark metrics alone cannot justify. Paper C provides the conceptual map that makes those two efforts cohere.
