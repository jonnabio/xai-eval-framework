# Data Persistence Strategy

## Overview
This document outlines how the XAI Evaluation Framework handles data persistence in production (Render.com).

## 1. Static Reference Data (Current Approach)
*   **What**: Baseline experiment results (e.g., `exp1_adult`).
*   **Mechanism**: **Git Repository**.
*   **How it works**:
    *   Results generated locally are committed to `main` (specifically `experiments/**/results/`).
    *   During deployment, Render builds a Docker image that *includes* these files.
    *   **Pros**: Simple, version-controlled, ensures reproducibility.
    *   **Cons**: Requires a commit/deploy cycle to update results. Read-only at runtime (changes are lost on restart).

## 2. Dynamic Runtime Data (Future/Batch Runs)
*   **What**: New experiments triggered via the API or Batch requests.
*   **Mechanism**: **Render Persistent Disk** (or external Database).
*   **Recommendation**:
    *   Attach a [Render Permanent Disk](https://docs.render.com/disks) to the `xai-eval-api` service.
    *   Mount it at `/app/experiments_data`.
    *   Configure the application to write new results there.
    *   The `DataLoader` should scan *both* the static directory (`/experiments`) and the persistent disk (`/app/experiments_data`).

## 3. Database (Metadata)
*   **What**: User data, annotations, lightweight run metadata.
*   **Mechanism**: **PostgreSQL** (Managed by Render).
*   **Status**: Currently used for Human Evaluation (`human_eval` tables).

## Summary table
| Data Type | Storage | Persistence | Valid For |
| :--- | :--- | :--- | :--- |
| **Baseline Results** | Git / Docker Image | Static (Build-time) | Fixed Benchmarks |
| **New Runs** | Render Disk | Persistent (Cross-deploy) | User Experiments |
| **Annotations** | PostgreSQL | Persistent | User Feedback |
