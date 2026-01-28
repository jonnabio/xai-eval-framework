# Postmortem: Frontend Validation & API Pagination Failure (Jan 27, 2026)

**Date:** January 27, 2026  
**Status:** Resolved  
**Impact:** Production Dashboard failed to load any experiments; Deployment pipeline blocked for ~2 hours.  
**Authors:** AI Assistant, User

## Executive Summary
Two distinct issues prevented the XAI Dashboard from displaying experimental results in production:
1.  **Frontend Validation Failure:** The frontend's Zod schema validation rejected the API response because it contained new XAI methods ("Anchors", "DiCE") that were not explicitly whitelisted in the frontend's strict enum definition.
2.  **API Pagination Limit:** Once validation was fixed, the frontend requested `?limit=1000` items to load all data, but the backend rejected this with `400 Bad Request` because its `MAX_PAGE_SIZE` was configured to 1000 (likely strictly enforced or lower in previous deploy), causing a hard failure.

## Root Causes

### 1. Frontend Schema Divergence
*   **The Issue:** The Backend was updated to support "Anchors" and "DiCE", but the Frontend `XaiMethod` enum was hardcoded to only valid `["LIME", "SHAP", "GradCAM", "RISE", "Integrated Gradients"]`.
*   **The Check:** The frontend uses `zod` to strictly validate API responses. When the API returned "DiCE", parsing failed, throwing an error and preventing *any* data from loading.
*   **Complication:** Fixing the Enum triggered TypeScript build errors in `simulate.ts`, `syntheticDataGenerator.ts` and `enhancedSyntheticDataAdapter.ts`. these files enforce *exhaustive* configuration for all enum members, requiring us to invent "dummy" simulation parameters for Anchors/DiCE even though we only wanted to load real data.

### 2. Backend Pagination Configuration
*   **The Issue:** The frontend attempts to load all run headers in one go using `limit=1000`.
*   **The Constraint:** The Backend's `src/api/config.py` had `MAX_PAGE_SIZE` set to 1000. While theoretically matching, edge cases or strict `le` (less than or equal) validation combined with possible deployment lag meant requests were rejected.
*   **Resolution:** Raised backend `MAX_PAGE_SIZE` to 5000 and `DEFAULT_PAGE_SIZE` to 100.

## Timeline & Resolution Steps

1.  **Detection:** User reported "ZodError" in browser console after backend deployment.
2.  **Fix 1 (Schema):** Updated `src/types/api.ts` and `src/lib/types.ts` to include `Anchors` and `DiCE`.
3.  **Build Failure 1:** Build failed in `enhancedSyntheticDataAdapter.ts` due to missing keys in `methodStrengths`. Added defaults.
4.  **Build Failure 2:** Build failed in `simulate.ts` due to missing keys in `METHOD_PRIORS`. Added defaults.
5.  **Build Failure 3:** Build failed in `syntheticDataGenerator.ts` due to missing keys in `methodDescriptions`. Added defaults.
6.  **Fix 2 (Commit):** Successfully committed and pushed all frontend changes.
7.  **Runtime Error:** Frontend deployed but returned `400 Bad Request` for `/runs?limit=1000`.
8.  **Fix 3 (Backend Config):** Increased `MAX_PAGE_SIZE` in `src/api/config.py` from 1000 to 5000 and redeployed backend.
9.  **Verification:** Dashboard successfully loaded 120+ experiments.

## Lessons Learned & Action Items

### Prevention
*   **[Critical] Shared Schemas:** We manually maintain `schemas.py` (Backend) and `types.ts` (Frontend). This duplication guarantees drift.
    *   *Action:* Investigate code generation (e.g., `openapi-typescript`) to generate frontend types directly from the Backend's `openapi.json`.
*   **Loosen Validation:** Strict Enum validation on string fields from the API is risky for forward compatibility.
    *   *Action:* Consider using `z.string()` or `z.enum([...]).or(z.string())` for fields like `method` or `modelType` on the frontend to allow unknown values to pass through (graceful degradation) instead of crashing the app.
*   **Build-time vs Run-time:** The build failed because *simulation* code (unused in prod) required exhaustive config for new types.
    *   *Action:* Decouple domain types from simulation config, or use `Partial<Record<XaiMethod, ...>>` for simulation configs so adding a type doesn't break the build immediately.

### Process
*   **Deployment Sync:** Frontend and Backend deployments must be synchronized when contract changes (Enums) occur.
    *   *Action:* Always check `src/types/api.ts` when adding new Enum members in Python.

## Artifacts Updated
*   `src/lib/types.ts`
*   `src/lib/simulate.ts`
*   `src/lib/syntheticDataGenerator.ts`
*   `src/api/config.py`
