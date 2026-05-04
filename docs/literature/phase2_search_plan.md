# Phase 2 Literature Review Search Plan

## Objective

Expand `thesis/03-capitulo-2-fundamentos.qmd` into a doctoral-level literature
review that justifies the FOM-7 contribution. The target chapter length is
8,000-12,000 words, with the chapter serving as the theoretical anchor for the
empirical design in Chapters 3 and 4.

## Skill Stack

Use these project skills in sequence:

| Skill | Location | Role |
|---|---|---|
| paper-lookup | `.ace/packs/scientific/paper-lookup/SKILL.md` | Discover and verify scholarly sources |
| ml-paper-writing | `.ace/packs/ai-research/ml-paper-writing/SKILL.md` | Enforce citation discipline and academic structure |
| research-manager | `.ace/packs/ai-research/research-manager/SKILL.md` | Track provenance of claims, inclusions, and exclusions |
| rigor-reviewer | `.ace/packs/ai-research/rigor-reviewer/SKILL.md` | Review scope calibration and evidence relevance |
| academic-plotting | `.ace/packs/ai-research/academic-plotting/SKILL.md` | Create conceptual diagrams and comparison figures |
| documentation-generation | `.ace/skills/documentation-generation/SKILL.md` | Produce tables, appendices, and traceability docs |
| testing-strategy | `.ace/skills/testing-strategy/SKILL.md` | Add citation/render/reproducibility checks |

## Source Discovery Rules

1. Do not create BibTeX from memory.
2. Prefer DOI, arXiv, publisher, OpenAlex, Crossref, Semantic Scholar, or official project pages.
3. Every selected paper must have a clear thesis use.
4. If a source cannot be verified, mark it as `needs-verification`.
5. Do not cite a source only because it is famous; cite it because it supports a defined claim.

## Search Clusters

### Cluster A: Historical Development of Interpretability and XAI

Purpose: establish how the field moved from intrinsic interpretability to
post-hoc explanation and human-centered explanation.

Initial queries:

- `interpretable machine learning survey transparent models post-hoc explanations`
- `explainable artificial intelligence concepts taxonomies opportunities challenges responsible AI`
- `model agnostic explanations local global interpretability survey`
- `human centered explainable AI evaluation systematic review`

Target sources:

- Surveys on XAI and interpretable ML
- Foundational papers on interpretability evaluation
- Human-centered XAI reviews

### Cluster B: Conceptual Distinctions

Purpose: define the conceptual vocabulary used by the thesis.

Initial queries:

- `interpretability vs explainability machine learning`
- `transparency explanation interpretability explainable AI`
- `fidelity faithfulness plausibility explainable AI`
- `robustness stability explanation methods XAI`
- `human-grounded functionally-grounded application-grounded evaluation`

Target concepts:

- Interpretability vs explainability
- Transparency vs explanation
- Fidelity vs faithfulness
- Plausibility vs correctness
- Robustness vs stability
- Usefulness vs truth of explanation

### Cluster C: Methods Evaluated in the Thesis

Purpose: provide doctoral-depth treatment of LIME, SHAP, Anchors, and DiCE.

Initial queries:

- `LIME local interpretable model agnostic explanations instability`
- `SHAP Shapley values TreeSHAP KernelSHAP computational cost`
- `Anchors high precision model agnostic explanations coverage`
- `DiCE diverse counterfactual explanations actionability`
- `counterfactual explanations actionability validity machine learning`

Target sources:

- Original method papers
- Follow-up analyses of instability, cost, assumptions, and limitations
- Comparative XAI benchmark studies

### Cluster D: Evaluation Frameworks

Purpose: position FOM-7 against existing XAI evaluation tools and protocols.

Initial queries:

- `Quantus explainable AI evaluation toolkit`
- `OpenXAI transparent evaluation model explanations`
- `XAI evaluation framework reproducibility benchmarking`
- `meta evaluation explainable AI metrics MetaQuantus`
- `functionally grounded evaluation explainable AI`

Frameworks to cover:

- Quantus
- OpenXAI
- Human-grounded, functionally grounded, and application-grounded evaluation
- Metric taxonomies
- Reproducibility-oriented benchmarking

### Cluster E: Critical Gap Synthesis

Purpose: support the final Chapter 2 argument that existing literature offers
metrics and tools but lacks a complete operational protocol linking design,
artifact qualification, statistical admissibility, and claim traceability.

Initial queries:

- `reproducibility explainable AI benchmarking artifact traceability`
- `statistical testing explainable AI evaluation benchmark`
- `XAI metrics taxonomy limitations reproducibility`
- `explainable AI evaluation pitfalls benchmark reproducibility`

Target gap labels:

- Metric fragmentation
- Construct mismatch
- OOD perturbation risk
- Missing artifact qualification
- Weak statistical admissibility
- Missing claim traceability

## Initial Verified Leads

| Topic | Lead | Verification Route | Thesis Use |
|---|---|---|---|
| Evaluation taxonomy | Doshi-Velez and Kim, 2017 | arXiv `1702.08608` | Human/function/application-grounded evaluation |
| Evaluation toolkit | Quantus, JMLR 2023 | JMLR paper page and arXiv | Compare metric toolkit vs operational protocol |
| Benchmarking framework | OpenXAI, NeurIPS 2022 | NeurIPS proceedings/project page | Compare transparent benchmarking vs FOM-7 |
| Human-centered evaluation | Frontiers systematic review 2024 | Publisher article | Support human-centered evaluation gap |
| Meta-evaluation | MetaQuantus, 2023 | arXiv/project | Support reliability of metric estimators |

## Target Chapter Structure

1. Desarrollo histórico de la interpretabilidad y la XAI
2. Distinciones conceptuales fundamentales
3. Métodos de explicación evaluados en esta tesis
4. Marcos y protocolos de evaluación XAI
5. Taxonomías de métricas y brechas de constructo
6. Reproducibilidad y trazabilidad en benchmarking XAI
7. Síntesis crítica: justificación de FOM-7

## Working Acceptance Criteria

- Chapter 2 reaches 8,000-12,000 words.
- Every subsection has a clear thesis function.
- Every cited paper appears in `thesis/references.bib`.
- Every major conceptual claim maps to at least one verified source.
- The chapter ends by explicitly justifying FOM-7.
- The review distinguishes existing tools from the thesis contribution.
