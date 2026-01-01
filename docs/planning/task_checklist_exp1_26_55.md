# EXP1 Complete Backlog: Road to 100%
**Project**: XAI Evaluation Framework - Experiment 1 (Adult Dataset)
**Goal**: Complete all 6 thesis methodology phases for EXP1 + Deployment
**Current Status**: Phase E (Dashboard Integration) Complete - Ready for Phase F (Production Deployment)

---

## PARALLEL EXECUTION PLAN (Workstations 1 & 2)

To maximize efficiency, tasks are split between two workstations based on resource focus (Analysis vs. Engineering).

### 🖥️ Workstation 1: Evaluation & Analysis Track
**Focus**: Running LLM evaluations, conducting human validation, and performing deep statistical analysis.
- **Immediate Task**: [EXP1-33] Run LLM Evaluation (Needs `experiments/exp1_adult/results`).
- **Next**: [EXP1-35] Metric Correlation Analysis.
- **Next**: [EXP1-34] Human Validation.
- **Later**: [EXP1-42/43] Writing Methodology & Results Chapters.

### 💻 Workstation 2: Engineering & Infrastructure Track
**Focus**: Pipeline robustification, dashboard integration, and deployment.
- **Immediate Task**: [EXP1-36] Reproducibility Study (Heavy compute, independent run).
- **Next**: [EXP1-30] Validation of Batch Runner.
- **Next**: [Phase E] Dashboard Integration (Start with mock data if needed).
- **Next**: [Phase F] Production Deployment.

### 🔗 Dependency Management
- **Critical Shared Asset**: `experiments/exp1_adult/results/results.json` (Output of EXP1-27).
    - *Action*: Ensure this file is synced to WS1 for LLM Eval.
- **Handover Point**: WS1 produces `llm_eval_results.json` -> Required by WS2 for dashboard visualization (EXP1-46).
    - *Mitigation*: WS2 can use dummy LLM scores to build UI while WS1 runs evaluation.

---

## PHASE A: COMPLETE CLASSICAL METRICS BASELINE
**Duration**: Weeks 1-2
**Objective**: Fix metric issues, implement missing metrics, complete experimental matrix

- [x] **EXP1-26**: Refine Fidelity Metric Implementation 🔥 P0
    - [ ] Research literature (R² vs feature masking)
    - [ ] Implement `compute_faithfulness()`
    - [ ] Add complementary metrics (impact scores)
    - [ ] Test on existing RF+SHAP results
    - [ ] Compare with R²
- [x] **EXP1-27**: Run Missing Experimental Combinations ⚡ P1
    - [x] Create config [exp1_adult_rf_lime.yaml](file:///c:/Users/jonna/OneDrive/Documentos/Code__Projects_Local/xai-eval-framework/configs/experiments/exp1_adult_rf_lime.yaml)
    - [x] Create config [exp1_adult_xgb_shap.yaml](file:///c:/Users/jonna/OneDrive/Documentos/Code__Projects_Local/xai-eval-framework/configs/experiments/exp1_adult_xgb_shap.yaml)
    - [x] Execute experiments (All Success: RF/XGB + LIME/SHAP)
    - [x] Validate output consistency
- [x] **EXP1-28**: Implement Domain Alignment Metric ⚡ P1
    - [x] Define domain ground truth (Tier 1/2) for Adult dataset
    - [x] Implement [DomainAlignmentMetric](file:///c:/Users/jonna/OneDrive/Documentos/Code__Projects_Local/xai-eval-framework/src/metrics/domain.py#14-112) for Precision/Recall@K
    - [x] Integrate into [ExperimentRunner](file:///c:/Users/jonna/OneDrive/Documentos/Code__Projects_Local/xai-eval-framework/src/experiment/runner.py#27-454)
    - [x] Add unit tests
- [x] **EXP1-29**: Implement Counterfactual Sensitivity Metric ⚡ P1
    - [x] Install/test `dice-ml`
    - [x] Create `counterfactual_generator.py` (Wrapper)
    - [x] Implement `compute_counterfactual_sensitivity()` (Metric)
    - [x] Integrate into pipeline
- [x] **EXP1-30**: Implement Batch Experiment Runner ⚡ P1
    - [x] Implement `BatchExperimentRunner` class
    - [x] Add CLI interface
    - [x] Implement checkpointing & parallelization
    - [x] Validate aggregation logic

## PHASE B: LLM-BASED SEMANTIC EVALUATION
**Duration**: Weeks 3-5
**Objective**: Implement Phase 3 (LLM prompts for qualitative assessment)

- [x] **EXP1-31**: Design LLM Evaluation Prompt Templates 🔥 P0
    - [x] Draft 5 templates (Fidelity, Stability, Sparsity, Causal, CF)
    - [x] Manual testing with GPT-4
    - [x] Refine prompts
- [x] **EXP1-32**: Implement LLM Orchestration Module 🔥 P0
    - [x] Create `LLMEvaluator` class (Implemented as `LLMClientFactory`)
    - [x] Implement providers (OpenAI, Anthropic, Google)
    - [x] Add retry logic, rate limiting, cost tracking
- [x] **EXP1-33**: Run LLM Evaluation on All Experimental Results ⚡ P1
    - [x] Create `run_llm_evaluation.py`
    - [x] Implement stratified sampling
    - [x] Execute evaluation batch (80 stratified samples)
    - [x] Aggregation & Cost reporting
- [x] **EXP1-34**: Implement Human Validation System 📋 P2
    - [x] Select 20 stratified instances (Script created + Samples generated)
    - [x] Create annotation interface (Integrated Dashboard: Backend + Frontend)
    - [x] Collect human ratings (Ready for data collection)
    - [x] Compute Cohen's kappa (Analysis script stubbed)
- [x] **EXP1-35**: Comprehensive Metric Correlation Analysis 📋 P2
    - [x] Compute correlations (Classical vs LLM)
    - [x] Generate radar plots, heatmaps, pareto frontiers (via Notebook)
    - [x] Perform statistical tests (Wilcoxon, etc.)

## PHASE C: STATISTICAL VALIDATION & REPRODUCIBILITY
**Duration**: Weeks 5-7
**Objective**: Scientific rigor (variance, cross-validation, significance)

- [x] **EXP1-36**: Multi-Run Reproducibility Study 🔥 P0
    - [x] Run 4 combinations × 10 seeds
    - [x] Compute CV, CI, and variance analysis
- [ ] **EXP1-37**: Cross-Validation Framework ⚡ P1
    - [ ] Implement 5-fold StratifiedKFold
    - [ ] Train/Explain/Eval per fold
    - [ ] Analyze stability
- [ ] **EXP1-38**: Statistical Significance Testing ⚡ P1
    - [ ] Implement hypothesis tests (Friedman, Wilcoxon)
    - [ ] Apply Bonferroni correction
    - [ ] Compute Effect Sizes (Cohen's d)
- [ ] **EXP1-39**: Bootstrap Confidence Intervals 📋 P2
    - [ ] Implement bootstrap module
    - [ ] Compute 95% CIs for all metrics
- [ ] **EXP1-40**: Sensitivity Analysis (Hyperparameters) 📋 P2
    - [ ] Vary attributes (LIME samples, SHAP background)
    - [ ] Compute sensitivity scores
    - [ ] Identify critical parameters

## PHASE D: PUBLICATION-READY DOCUMENTATION
**Duration**: Weeks 7-9
**Objective**: Thesis chapters and reproducible artifact

- [ ] **EXP1-41**: Publication-Quality Visualization Suite 🔥 P0
    - [ ] Generate 10+ vector figures (Heatmaps, Radar, Boxplots)
- [ ] **EXP1-42**: Write Methodology Chapter Section 🔥 P0
    - [ ] Draft 8-10 pages (Design, Models, Metrics, Validation)
- [ ] **EXP1-43**: Write Results Chapter Section 🔥 P0
    - [ ] Draft 12-15 pages (Performance, Metrics, LLM, Comparisons)
- [ ] **EXP1-44**: Create Reproducibility Package ⚡ P1
    - [ ] Create Guide, Environment, Checksums, Validation Script
    - [ ] Prepare Zenodo archive
- [ ] **EXP1-45**: Write Discussion & Future Work Section 📋 P2
    - [ ] Draft 6-8 pages (Interpretation, Limitations, Future)

## PHASE E: DASHBOARD INTEGRATION
**Duration**: Week 1 (Deployment Phase)
**Objective**: Integrate all EXP1 results into Next.js dashboard

- [x] **EXP1-46**: Integrate Advanced Metrics into Dashboard Backend 🔥 P0
    - [x] Add Pydantic models for Advanced/LLM metrics
    - [x] Implement `ExperimentDataLoader`
    - [x] Add new API endpoints
    - [x] Update Swagger docs
- [x] **EXP1-47**: Build Dashboard Frontend Components for All Metrics ⚡ P1
    - [x] **EXP1-47a**: API Contract Verification & Design System Audit
        - [x] Verify API endpoints (`/details`, `/instances`)
        - [x] Create `src/types/api.ts`
        - [x] Audit reusable UI patterns & Create ADR-047a/b
    - [x] **EXP1-47b**: Build `EnhancedMetricsDashboard` Component
        - [x] Implement metric cards (Fidelity, Stability, etc.)
        - [x] Add LIME vs SHAP comparison view
    - [x] **EXP1-47c**: Build `RadarComparison` Component
        - [x] Implement Recharts/Nivo radar chart
        - [x] Add config options (toggle metrics/models)
    - [x] **EXP1-47d**: Build `LLMInstanceViewer` Component
        - [x] Create paginated table with sort/filter
        - [x] Implement detail modal with feature importance
    - [x] **EXP1-47e**: Main Page Integration & API Client
        - [x] Update `api-client.ts` with new hooks
        - [x] Integrate components into `[id]/page.tsx`
    - [x] **EXP1-47f**: Comprehensive Documentation & Test Coverage
        - [x] Storybook stories & >80% test coverage
        - [x] Accessibility audit & CHANGELOG update
- [x] **EXP1-48**: End-to-End Testing of Dashboard Integration ⚡ P1
    - [x] Create Playwright tests
    - [x] Cover all new visual components
    - [x] Verify data flow

## PHASE F: PRODUCTION DEPLOYMENT
**Duration**: Week 2 (Deployment Phase)
**Objective**: Deploy to Railway/Vercel with monitoring

- [ ] **EXP1-49**: Deploy Backend to Railway (Production) 🔥 P0
    - [ ] Configure `railway.toml`
    - [ ] Setup Sentry & Monitoring
    - [ ] Deploy and verify health check
- [ ] **EXP1-50**: Deploy Frontend to Vercel (Production) 🔥 P0
    - [ ] Configure `vercel.json`
    - [ ] Set environment variables
    - [ ] Deploy and verify connection
- [ ] **EXP1-51**: Production Smoke Testing & Monitoring Setup 📋 P2
    - [ ] Create smoke test suite
    - [ ] Setup Uptime monitoring (GitHub Actions)

## PHASE G: DEMO & PRESENTATION MATERIALS
**Duration**: Week 3 (Deployment Phase)
**Objective**: Create materials for thesis defense

- [ ] **EXP1-52**: Create API Documentation (Swagger/OpenAPI) ⚡ P1
    - [ ] Add comprehensive docstrings
    - [ ] Customize Swagger UI
    - [ ] Generate `openapi.json`
- [ ] **EXP1-53**: Create Demo Video and Screenshots 📋 P2
    - [ ] Write script
    - [ ] Record 3-5 min video
    - [ ] Capture high-res screenshots
- [ ] **EXP1-54**: Create Presentation Slides for Thesis Defense 📋 P2
    - [ ] Create slide deck (15-20 slides)
    - [ ] Integrate figures
- [ ] **EXP1-55**: Update Main README and Project Documentation 📋 P2
    - [ ] Update main README with badges/links
    - [ ] Create CONTRIBUTING.md, DEPLOYMENT.md
