# 0003. Class-Based Model Wrappers

**Date**: 2025-12-16  
**Status**: Accepted

## Context
The initial implementation used standalone functions (`train_random_forest_adult`) for model training.
As requirements grew (need to save metadata, handle state, calculate XAI metrics later), passing dictionaries and separate variables became unwieldy. The functional approach lacked a clear "owner" of the model lifecycle.

## Decision
We refactored the core logic into classes (e.g., `AdultRandomForestTrainer`).
-   The class manages state (config, model, metrics).
-   The original functions remain as thin wrappers for backward compatibility with scripts.

## Consequences
-   **Positive**: Better encapsulation and extensibility for future experiments (Exp2).
-   **Negative**: Slightly more boilerplate code.
