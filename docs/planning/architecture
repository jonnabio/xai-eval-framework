# Project Architecture: XAI Evaluation Framework & Benchmark

## 1. Executive Summary
This document details the software architecture of the PhD project "XAI Evaluation Framework". The system is designed to provide a rigorous, reproducible, and interactive environment for benchmarking Explainable AI (XAI) methods. It consists of two primary coupled repositories:
1.  **`xai-eval-framework` (Backend)**: A Python-based engine for orchestrating experiments, generating explanations (SHAP, LIME), and computing quantitative and semantic metrics.
2.  **`xai-benchmark` (Frontend)**: A Next.js/TypeScript web dashboard for visualizing results, comparing model performance, and conducting human validation.

The architecture emphasizes **modularity**, **scientific reproducibility**, and **scalability**.

---

## 2. System Context
The system operates as a client-server architecture where the backend performs heavy computational tasks (model training, explanation generation) and serves results via a REST API to the frontend dashboard.

```mermaid
graph TD
    User[User / Researcher] -->|Configures| Backend
    User -->|Views Results| Frontend
    
    subgraph "xai-eval-framework (Backend)"
        ExperimentRunner[Experiment Runner]
        API[FastAPI Server]
        Metrics[Metrics Engine]
        XAI[XAI Wrappers]
        Analysis[Analysis Module]
    end
    
    subgraph "xai-benchmark (Frontend)"
        Dashboard[Next.js Dashboard]
        Viz[Visualizations]
        HumanEval[Human Eval Interface]
    end
    
    Frontend -->|HTTP / JSON| API
    ExperimentRunner -->|Writes| Storage[(JSON / CSV Results)]
    API -->|Reads| Storage
```

---

## 3. Backend Architecture (`xai-eval-framework`)
**Repository**: `jonnabio/xai-eval-framework`  
**Language**: Python 3.11  
**Framework**: FastAPI

### 3.1 Core Components (`src/`)

#### 3.1.1 API Layer (`src/api/`)
*   **Framework**: FastAPI is used for its high performance (Asynchronous) and automatic OpenAPI generation.
*   **Entry Point**: `main.py` initializes the app, configuring middleware (CORS, Sentry for error tracking, Prometheus for metrics).
*   **Endpoints**:
    *   `/runs`: Lists and retrieves experiment results.
    *   `/human-eval`: Manages human validation sessions (sampling, submission, progress).
    *   `/health`: Production health checks.
    *   `/db`: Debug endpoints.
    *   `/metrics`: Prometheus metrics.
*   **Schemas**: Pydantic models define strict contracts for request/response bodies.

#### 3.1.2 Experimentation Engine (`src/experiment/`)
*   **`ExperimentRunner`**: The central orchestrator. It manages the lifecycle of a single experiment:
    1.  **Setup**: Loads data (`src/data_loading`) and models (`src/models`).
    2.  **Generation**: initializing Explainer wrappers.
    3.  **Sampling**: Selects test instances using `EvaluationSampler` (e.g., stratified by error quadrant).
    4.  **Evaluation**: Computes all configured metrics.
    5.  **Persistence**: Saves results to `results.json` and `metrics.csv`.
*   **`BatchExperimentRunner`**: Enables parallel execution of multiple configuration files.
*   **`CrossValidationRunner`**: Implements 5-fold stratified cross-validation for robust performance estimation.

#### 3.1.3 Metrics Engine (`src/metrics/`)
Modular strategy pattern where each metric implements a uniform interface (`compute`).
*   **Fidelity**: Measures faithfulness of explanations (Predictive Gap).
*   **Stability**: Robustness to Gaussian noise (Cosine Similarity).
*   **Sparsity**: Conciseness of feature importance.
*   **Causal Alignment**: Agreement with domain knowledge DAGs.
*   **Counterfactual Sensitivity**: Sensitivity to decision boundary shifts (using DiCE).

#### 3.1.4 XAI Abstraction (`src/xai/`)
Wrapper classes unify diverse explanation libraries into a common API:
*   `SHAPTabularWrapper`: Wraps `shap.TreeExplainer` / `KernelExplainer`.
*   `LIMETabularWrapper`: Wraps `lime.lime_tabular`.
*   `DiCETabularWrapper`: Wraps `dice_ml` for counterfactuals.

#### 3.1.5 LLM Integration (`src/llm/`)
*   **`LLMClientFactory`**: Factory pattern to instantiate clients for OpenAI (GPT-4) or Google (Gemini).
*   **Cost Tracking**: Middleware tracks token usage and estimates costs.

#### 3.1.6 Analysis & Scripts
*   **`src/analysis/`**: Statistical analysis modules (Friedman, Wilcoxon tests), confidence interval computation (Bootstrap), and sensitivity analysis.
*   **`src/scripts/`**: Utility scripts for running experiments, generating figures, and batch processing.

### 3.2 Data Management
*   **Input**: Datasets (UCI Adult) are loaded via cached loaders. Models are serialized via `joblib`.
*   **Configuration**: Experiments are defined by strict YAML configurations validated by Pydantic.
*   **Output**: Results are stored as structured JSON (metadata + aggregates) and CSV (instance-level details) in `experiments/<name>/results/`.

---

## 4. Frontend Architecture (`xai-benchmark`)
**Repository**: `jonnabio/xai-benchmark`  
**Framework**: Next.js 14 (App Router)  
**Language**: TypeScript  
**Styling**: Tailwind CSS + shadcn/ui
**State Management**: Zustand (Global state)

### 4.1 Application Structure (`src/`)

#### 4.1.1 Routing (`app/`)
Uses Next.js App Router for server-centric routing:
*   `experiments/[id]/page.tsx`: Dynamic route for specific experiment details.
*   `experiments/compare/page.tsx`: Comparison view for multiple models.
*   `validation/page.tsx`: Interface for human annotators.
*   `admin/page.tsx`: Admin dashboard for validation stats.

#### 4.1.2 Components (`components/`)
*   **UI Library**: `shadcn/ui` (Radix UI primitives) ensures accessible, high-quality interactive elements.
*   **Visualizations**:
    *   **Recharts**: Used for Radar charts (metric comparison) and Bar charts.
    *   **Plotly.js**: Used for complex interactive plots if necessary.
    *   **Custom**: `FeatureImportancePlot` for visualizing SHAP/LIME weights.

#### 4.1.3 Data Access (`lib/`)
*   **`api-client.ts`**: A typed wrapper around `fetch`. Handles error parsing and connects to the backend URL.
*   **Caching**: Next.js built-in caching strategies are leveraged for static experiment data.

---

## 5. Infrastructure & Deployment

### 5.1 Backend Deployment (Render)
*   **Platform**: Render.com (Web Service).
*   **Environment**: Docker-based (Python 3.11).
*   **Configuration**: `render.yaml` defines the service specification.
*   **Observability**:
    *   **Sentry**: Error and Exception monitoring.
    *   **Prometheus**: /metrics endpoint for scraping performance data.

### 5.2 Frontend Deployment (Vercel)
*   **Platform**: Vercel.
*   **Build**: Standard Next.js build process.
*   **Configuration**: `vercel.json`.
*   **Integration**: Environment variables link it to the live Backend API.

### 5.3 CI/CD
*   **GitHub Actions**: Automated workflows run tests (Pytest for backend, Playwright/Vitest for frontend), linting, and type checking on every push.

---

## 6. Architecture Analysis & Roadmap
For a detailed critique of the current architecture, security vulnerabilities, and the future improvement plan, please refer to the [Architecture Improvement Plan](architecture_improvement_plan.md).
