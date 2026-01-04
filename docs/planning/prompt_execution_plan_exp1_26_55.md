# Prompt Execution Plan: EXP1 Road to 100%

This document defines the actionable prompts for executing tasks EXP1-26 through EXP1-55.

---

## PHASE A: CLASSICAL METRICS BASELINE

### Task: EXP1-26 Refine Fidelity Metric Implementation
**Priority**: 🔥 P0
**Trigger**: "Execute EXP1-26"
**Prompt Context**:
You are implementing the refined Fidelity metric to replace the problematic R² implementation.
**Objective**: Implement "Faithfulness" metric based on feature masking.
**Steps**:
1.  Analyze [src/metrics/fidelity.py](file:///c:/Users/jonna/OneDrive/Documentos/Code__Projects_Local/xai-eval-framework/src/metrics/fidelity.py).
2.  Implement `compute_faithfulness` function:
    -   Mask top-k features (mean/mode).
    -   Measure prediction change: `|baseline - masked| / range`.
3.  Add complementary metrics if feasible (removal impact).
4.  Update [ExperimentRunner](file:///c:/Users/jonna/OneDrive/Documentos/Code__Projects_Local/xai-eval-framework/src/experiment/runner.py#26-362) to use this new metric.
5.  Create a test script or unit test to validate it produces values in [0, 1].
**Files**: [src/metrics/fidelity.py](file:///c:/Users/jonna/OneDrive/Documentos/Code__Projects_Local/xai-eval-framework/src/metrics/fidelity.py), [src/experiment/runner.py](file:///c:/Users/jonna/OneDrive/Documentos/Code__Projects_Local/xai-eval-framework/src/experiment/runner.py), `tests/unit/metrics/test_fidelity.py`.

### Task: EXP1-27 Run Missing Experimental Combinations
**Priority**: ⚡ P1
**Trigger**: "Execute EXP1-27"
**Prompt Context**:
You are completing the experimental matrix (2x2).
**Objective**: Execute RF+LIME and XGB+SHAP experiments.
**Steps**:
1.  Create `configs/experiments/exp1_adult_rf_lime.yaml`.
2.  Create `configs/experiments/exp1_adult_xgb_shap.yaml`.
3.  Ensure `run_experiment.py` (or equivalent runner) can accept these configs.
4.  Execute both experiments.
5.  Verify output `results.json` and `metrics.csv` exist and match the schema.
**Files**: `configs/experiments/*.yaml`.

### Task: EXP1-28 Implement Causal Alignment Metric
**Priority**: ⚡ P1
**Trigger**: "Execute EXP1-28"
**Prompt Context**:
You are implementing the Causal Alignment metric.
**Objective**: Compare explanation features with domain causal knowledge.
**Steps**:
1.  Create `src/data_loading/causal_graphs.py` defining `CAUSAL_FEATURES` for Adult dataset.
2.  Implement `compute_causal_alignment` in `src/metrics/causal_alignment.py`.
    -   Calculate Precision@k for causal features.
3.  Integrate into [ExperimentRunner](file:///c:/Users/jonna/OneDrive/Documentos/Code__Projects_Local/xai-eval-framework/src/experiment/runner.py#26-362).
**Files**: `src/data_loading/causal_graphs.py`, `src/metrics/causal_alignment.py`.

### Task: EXP1-29 Implement Counterfactual Sensitivity Metric
**Priority**: ⚡ P1
**Trigger**: "Execute EXP1-29"
**Prompt Context**:
You are implementing Counterfactual Sensitivity using DiCE.
**Objective**: Measure explanation change under minimal prediction-flipping perturbations.
**Steps**:
1.  Ensure `dice-ml` is installed (add to env or pip install).
2.  Create `src/evaluation/counterfactual_generator.py` wrapping DiCE.
3.  Implement `compute_counterfactual_sensitivity` in `src/metrics/counterfactual_sensitivity.py`.
4.  Integrate into [ExperimentRunner](file:///c:/Users/jonna/OneDrive/Documentos/Code__Projects_Local/xai-eval-framework/src/experiment/runner.py#26-362).
**Files**: `src/evaluation/counterfactual_generator.py`, `src/metrics/counterfactual_sensitivity.py`.

### Task: EXP1-30 Implement Batch Experiment Runner
**Priority**: ⚡ P1
**Trigger**: "Execute EXP1-30"
**Prompt Context**:
You are creating a batch runner to orchestrate multiple experiments.
**Objective**: Robust orchestration with checkpointing.
**Steps**:
1.  Create `scripts/run_batch_experiments.py`.
2.  Implement `BatchExperimentRunner` class.
    -   Auto-discovery of YAML configs.
    -   Parallel execution option.
    -   Result aggregation into single CSV.
3.  Test with the 4 existing configs.
**Files**: `scripts/run_batch_experiments.py`.

---

## PHASE B: LLM-BASED EVALUATION

### Task: EXP1-31 Design LLM Evaluation Prompt Templates
**Priority**: 🔥 P0
**Trigger**: "Execute EXP1-31"
**Prompt Context**:
You are designing Jinja2 templates for LLM-based evaluation.
**Objective**: Create 5 prompt templates (Fidelity, Stability, Sparsity, Causal, CF).
**Steps**:
1.  Create `src/prompts/templates/system_prompt.j2`.
2.  Create templates for each metric (as specified in plan) in `src/prompts/templates/`.
3.  Create a validation script to render them with dummy data to ensure syntax correctness.
**Files**: `src/prompts/templates/*.j2`.

### Task: EXP1-32 Implement LLM Orchestration Module
**Priority**: 🔥 P0
**Trigger**: "Execute EXP1-32"
**Prompt Context**:
You are building the LLM evaluator engine.
**Objective**: Abstract API calls to OpenAI/Anthropic/Google with cost tracking.
**Steps**:
1.  Create `src/llm/client.py` (formerly `evaluator.py`).
2.  Implement `LLMClientFactory` class.
3.  Implement provider logic (OpenAI and Gemini).
4.  Add cost tracking and rate limiting.
**Files**: `src/llm/client.py`.

## Task: EXP1-33 Run LLM Evaluation
**Priority**: ⚡ P1
**Trigger**: "Execute EXP1-33"
**Prompt Context**:
You are executing the massive LLM evaluation batch.
**Objective**: Evaluate stratified samples from EXP1 results.
**Steps**:
1.  Create `scripts/run_llm_eval#uation.py`.
2.  Implement sample selection (Stratified by prediction type).
3.  Loop through samples and call `LLMEvaluator`.
4.  Save results to `experiments/exp1_adult/llm_eval/`.
**Files**: `scripts/run_llm_evaluation.py`.

### Task: EXP1-34 Implement Human Validation Sample
**Priority**: 📋 P2
**Trigger**: "Execute EXP1-34"
**Prompt Context**:
You are setting up human validation.
**Objective**: Create interface/form for human annotation.
**Steps**:
1.  Select 20 instances.
2.  Generate `experiments/exp1_adult/human_validation/annotation_form.html` (self-contained HTML).
3.  Create analysis script for Cohen's Kappa.
**Files**: `experiments/exp1_adult/human_validation/*`.

### Task: EXP1-35 Metric Correlation Analysis
**Priority**: 📋 P2
**Trigger**: "Execute EXP1-35"
**Prompt Context**:
You are analyzing relationships between metrics.
**Objective**: Create a notebook for correlation analysis.
**Steps**:
1.  Create `experiments/exp1_adult/notebooks/metric_correlation_analysis.ipynb`.
2.  Implement code to load Classical and LLM results.
3.  Generate Heatmaps and Radar plots code.
**Files**: `experiments/exp1_adult/notebooks/metric_correlation_analysis.ipynb`.

---

## PHASE C: STATISTICAL VALIDATION

### Task: EXP1-36 Multi-Run Reproducibility Study
**Priority**: 🔥 P0
**Trigger**: "Execute EXP1-36"
**Prompt Context**:
You are validating reproducibility.
**Objective**: Run experiments 10x with different seeds.
**Steps**:
1.  Create `scripts/run_reproducibility_study.py`.
2.  Implement looking for seeds and running `ExperimentRunner` in loop.
3.  Compute CV (Coefficient of Variation) for metrics.
**Files**: `scripts/run_reproducibility_study.py`.

### Task: EXP1-37 Cross-Validation Framework
**Priority**: ⚡ P1
**Trigger**: "Execute EXP1-37"
**Prompt Context**:
You are implementing k-Fold CV.
**Objective**: 5-fold CV to validation stability.
**Steps**:
1.  Create `scripts/run_cv_experiments.py`.
2.  Implement StratifiedKFold logic.
3.  Aggregate results across folds.
**Files**: `scripts/run_cv_experiments.py`.

### Task: EXP1-38 Statistical Significance Testing
**Priority**: ⚡ P1
**Status**: ✅ Completed
**Trigger**: "Execute EXP1-38"
**Prompt Context**:
You are calculating statistical significance.
**Objective**: Hypothesis testing (Wilcoxon, Friedman).
**Steps**:
1.  Create `src/analysis/statistical_tests.py`.
2.  Implement significance tests and Bonferroni correction.
3.  Generate results table.
**Files**: `src/analysis/statistical_tests.py`.

### Task: EXP1-39 Bootstrap Confidence Intervals
**Priority**: 📋 P2
**Status**: ✅ Completed
**Trigger**: "Execute EXP1-39"
**Prompt Context**:
You are computing CIs code.
**Objective**: Bootstrap resampling for error bars.
**Steps**:
1.  Create `src/analysis/bootstrap.py`.
2.  Apply to metric data arrays.
**Files**: `src/analysis/bootstrap.py`.

### Task: EXP1-40 Sensitivity Analysis
**Status**: Completed
**Priority**: 📋 P2
**Trigger**: "Execute EXP1-40"
**Prompt Context**:
You are checking hyperparameter sensitivity.
**Objective**: Vary LIME/SHAP params and check metric variance.
**Steps**:
1.  Create `scripts/run_sensitivity_analysis.py`.
2.  Define grid of parameters.
3.  Execute and compute sensitivity score.
**Files**: `scripts/run_sensitivity_analysis.py`.

---

## PHASE D: PUBLICATION

### Task: EXP1-41 Publication Visualization Suite
**Status**: Completed
**Priority**: 🔥 P0
**Trigger**: "Execute EXP1-41"
**Prompt Context**:
You are generating paper figures.
**Objective**: 10 High-quality plots.
**Steps**:
1.  Create `scripts/generate_publication_figures.py`.
2.  Implement using `matplotlib`/`seaborn` with academic styling.
**Files**: `scripts/generate_publication_figures.py`.

### Task: EXP1-42 Write Methodology Chapter
**Status**: Completed
**Priority**: 🔥 P0
**Trigger**: "Execute EXP1-42"
**Prompt Context**:
You are drafting the methodology chapter.
**Objective**: Write Chapter 3 sections.
**Steps**:
1.  Implemented `src/scripts/extract_methodology_metadata.py` and `src/scripts/generate_methodology_latex.py`.
2.  Generated content in `docs/thesis/`.
**Files**: `docs/thesis/chapter_3_methodology.tex`.

### Task: EXP1-43 Write Results Chapter
**Status**: Completed
**Priority**: 🔥 P0
**Trigger**: "Execute EXP1-43"
**Prompt Context**:
You are drafting the results chapter.
**Objective**: Write Chapter 5 sections.
**Steps**:
1.  Implemented `src/scripts/extract_results_metadata.py`.
2.  Generated `docs/thesis/chapter_5_results.tex` and tables.
**Files**: `docs/thesis/chapter_5_results.tex`.

### Task: EXP1-44 Create Reproducibility Package
**Status**: ✅ Completed
**Priority**: ⚡ P1
**Trigger**: "Execute EXP1-44"
**Prompt Context**:
You are packaging the artifact.
**Objective**: Create Guide and validation scripts.
**Steps**:
1.  Create `experiments/exp1_adult/reproducibility_package/REPRODUCIBILITY_GUIDE.md`.
2.  Create `validation_script.py`.
3.  Export environment.
**Files**: `experiments/exp1_adult/reproducibility_package/*`.

### Task: EXP1-45 Write Discussion Chapter
**Priority**: 📋 P2
**Trigger**: "Execute EXP1-45"
**Prompt Context**:
You are drafting the discussion.
**Objective**: Write Chapter 6 sections.
**Steps**:
1.  Create `docs/thesis_material/chapter_6_discussion_exp1.md`.
2.  Synthesize findings and limitations.
**Files**: `docs/thesis_material/chapter_6_discussion_exp1.md`.

---

## PHASE E: DASHBOARD INTEGRATION

### Task: EXP1-46 Integrate Advanced Metrics into Dashboard Backend
**Priority**: 🔥 P0
**Trigger**: "Execute EXP1-46"
**Prompt Context**:
You are updating the FastAPI backend to serve advanced and LLM metrics.
**Objective**: Extend API to serve all experimental results.
**Steps**:
1.  Update `src/api/routes.py` (or create `metrics.py`) with new endpoints.
2.  Add Pydantic models for `AdvancedMetrics` and `LLMEvaluationScore`.
3.  Implement `ExperimentDataLoader` to read the new JSON/CSV files created in EXP1.
**Files**: `src/api/routes.py`, `src/api/data_loader.py`.

### Task: EXP1-47 Build Dashboard Frontend Components
**Priority**: ⚡ P1
**Trigger**: "Execute EXP1-47"
**Prompt Context**:
You are building the React components to visualize the new metrics.
**Objective**: Create `EnhancedMetricsDashboard`, `RadarComparison`, `LLMInstanceViewer`.
**Steps**:
1.  Install `recharts` or `nivo` if needed.
2.  Create components in `xai-benchmark/src/components/`.
3.  Implement data fetching hooks in `xai-benchmark/src/lib/api-client.ts`.
4.  Integrate into the main experiment page.
**Files**: `xai-benchmark/src/components/*.tsx`, `xai-benchmark/src/app/experiments/[id]/page.tsx`.

### Task: EXP1-48 End-to-End Testing of Dashboard Integration
**Priority**: ⚡ P1
**Trigger**: "Execute EXP1-48"
**Prompt Context**:
You are Writing Playwright tests for the dashboard.
**Objective**: Validate visual components and data flow.
**Steps**:
1.  Check `tests/` folder setup (Playwright default).
2.  Create `tests/dashboard.spec.ts`, `tests/human-validation.spec.ts`, `tests/admin-dashboard.spec.ts`.
3.  Implement tests for verifying metric display, radar charts, and interaction.
4.  Implement proper API mocking.
**Files**: `tests/*.spec.ts`.

---

## PHASE F: PRODUCTION DEPLOYMENT

### Task: EXP1-49 Deploy Backend to Render
**Priority**: 🔥 P0
**Trigger**: "Execute EXP1-49"
**Prompt Context**:
You are executing the comprehensive Render deployment plan.
**Objective**: Production-ready deployment with monitoring and documentation.
**Steps**:
1.  **Documentation**: Create `docs/decisions/000X-render-deployment.md` (ADR).
2.  **Config**: Update `src/api/config.py` with Production settings (Sentry, Prometheus, CORS).
3.  **Code**: Update `src/api/main.py` with `/health` endpoint and lifecycle hooks.
4.  **Infra**: Create `render.yaml` using `$PORT` and defining env vars.
5.  **Tests**: Create `tests/integration/test_production.py`.
6.  **Verify**: Run local checks and commit for auto-deploy.
**Files**: `docs/decisions/*.md`, `render.yaml`, `src/api/*`.

### Task: EXP1-50 Deploy Frontend to Render
**Priority**: 🔥 P0
**Trigger**: "Execute EXP1-50"
**Prompt Context**:
You are deploying the frontend to Render.
**Objective**: Update `render.yaml` and configure Next.js for standalone mode.
**Steps**:
1.  **Pre-Deployment**:
    -   Create `docs/decisions/0005-render-frontend-deployment.md`.
    -   Configure `next.config.mjs` (CSP, standalone, no source maps).
    -   Create `rollback_plan.md`.
2.  **Infrastructure**:
    -   Update `render.yaml` (Node service, Health Check path, Env Vars).
    -   Implement `/api/health`.
    -   Setup Sentry.
3.  **Deployment**:
    -   Push to `main`. Render auto-deploys.
4.  **Verification**:
    -   Phase 1-4 Checks (Logs, Functional, Security, Performance).
**Files**: `render.yaml`, `next.config.mjs`, `src/app/api/health/route.ts`.

### Task: EXP1-51 Production Smoke Testing & Monitoring Setup
**Priority**: 📋 P2
**Trigger**: "Execute EXP1-51"
**Prompt Context**:
You are automating health checks.
**Objective**: Smoke tests and Github Action monitor.
**Steps**:
1.  Create `tests/smoke/production.spec.ts`.
2.  Create `.github/workflows/uptime-monitor.yml`.
**Files**: `tests/smoke/production.spec.ts`, `.github/workflows/uptime-monitor.yml`.

---

## PHASE G: DEMO & PRESENTATION

### Task: EXP1-52 Create API Documentation (Swagger/OpenAPI)
**Priority**: ⚡ P1
**Trigger**: "Execute EXP1-52"
**Prompt Context**:
You are finalizing API docs.
**Objective**: Interactive Swagger UI.
**Steps**:
1.  Add rich docstrings to FastAPI endpoints.
2.  Customize Swagger UI parameters in `main.py`.
3.  Generate `openapi.json` artifact.
**Files**: `src/api/main.py`, `src/api/routes/*.py`.

### Task: EXP1-53 Create Demo Video and Screenshots
**Priority**: 📋 P2
**Trigger**: "Execute EXP1-53"
**Prompt Context**:
You are creating media assets.
**Objective**: Script and visual assets.
**Steps**:
1.  Write `docs/media/DEMO_SCRIPT.md`.
2.  (User Action) Record video.
3.  Place assets in `docs/media/`.
**Files**: `docs/media/DEMO_SCRIPT.md`.

### Task: EXP1-54 Create Presentation Slides Coverage
**Priority**: 📋 P2
**Trigger**: "Execute EXP1-54"
**Prompt Context**:
You are preparing the defense slides.
**Objective**: Slide deck structure.
**Steps**:
1.  Create `docs/thesis_defense/slides_outline.md`.
2.  Generate latex beamer frame code if requested, or PPT structure.
**Files**: `docs/thesis_defense/slides_outline.md`.

### Task: EXP1-55 Update Main README and Project Documentation
**Priority**: 📋 P2
**Trigger**: "Execute EXP1-55"
**Prompt Context**:
You are performing the final documentation sweep.
**Objective**: Comprehensive project docs.
**Steps**:
1.  Update root `README.md` with features, links, badges.
2.  Create `CONTRIBUTING.md`.
3.  Create `DEPLOYMENT.md`.
**Files**: `README.md`, `CONTRIBUTING.md`, `DEPLOYMENT.md`.
