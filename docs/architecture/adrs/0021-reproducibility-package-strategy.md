# 21. Reproducibility Package Strategy

Date: 2026-01-03

## Status

Accepted

## Context

The XAI Evaluation Framework produces complex experimental results that form the basis of a thesis. Ensuring these results are reproducible by others (and by the author in the future) is critical for scientific validity. 

We needed a strategy to bundle the code, data, and environment in a way that guarantees consistent execution across different machines and operating systems.

Key challenges:
*   **Dependency Drift**: Python packages update frequently, breaking older code.
*   **System Differences**: Reproducing results on Windows vs. Linux vs. macOS can lead to subtle variations.
*   **Process Complexity**: The pipeline involves multiple stages (training, extraction, generation) which are error-prone if run manually.
*   **Data Provenance**: Ensuring the correct version of the dataset is used.

## Decision

We decided to implement a **"Gold Standard" Reproducibility Package** that relies on three pillars:

1.  **Containerization (Docker)**: 
    *   We use a `Dockerfile` based on `python:3.11-slim` to encapsulate the entire runtime environment.
    *   This eliminates OS-level discrepancies and ensures system dependencies are correct.

2.  **Strict Environment Pinning**:
    *   We generate `requirements-frozen.txt` using `pip freeze` to lock all transitive dependencies to exact versions.
    *   We provide `environment.yml` for Conda users as a secondary supported method.

3.  **Unified Orchestration**:
    *   We implemented a master bash script `run_full_pipeline.sh` that automates the entire sequence: Data Download -> Training -> Experimentation -> Extraction -> Thesis Generation -> Verification.
    *   This removes the need for users to remember complex CLI commands.

4.  **Automated Verification**:
    *   We created `verify_reproducibility.py` which acts as a self-test.
    *   It checks file existence, MD5 checksums of data, and validates that key experimental metrics (e.g., Fidelity scores) match the expected "Ground Truth" within a small tolerance.

## Consequences

### Positive
*   **Guarantee**: Any user with Docker can reproduce the exact thesis results with a single command.
*   **Robustness**: The package is resistant to future library updates breaking the code.
*   **Verifyability**: The included validation script provides immediate feedback on success/failure.
*   **Portability**: The package can be easily archived on Zenodo.

### Negative
*   **Maintenance**: The frozen requirements must be updated if the core codebase changes significantly.
*   **Size**: Docker images can be large.
*   **Complexity**: Adding Docker and verification scripts increases the codebase surface area.

## Alternatives Considered

*   **Virtual Environment Only**: Rejected because it relies on the host OS having specific libraries (gcc, make) and doesn't solve cross-platform path issues.
*   **VM Image**: Too large and opaque. Docker is more lightweight and transparent (Dockerfile is readable).
*   **Manual Instructions**: Too error-prone and tedious for users. Automated orchestration is superior.
