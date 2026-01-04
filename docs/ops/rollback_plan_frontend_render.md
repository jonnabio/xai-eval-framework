# Frontend Rollback Plan (Render)

This document outlines the procedures for handling deployment failures or critical bugs in the XAI Dashboard production environment on Render.com.

## 1. Runtime Failure (Immediate Rollback)

**When to use**: Build succeeds but app crashes on startup, or critical bug found immediately after deploy.

1.  **Log in** to the Render Dashboard.
2.  **Navigate** to the Service: `xai-benchmark-frontend`.
3.  **Click** the **Deployments** tab.
4.  **Identify** the last known "Live" and "Healthy" deployment (green checkmark).
5.  **Click** the **three dots (...)** menu -> **Rollback**.
6.  **Verify**: Wait for the deployment to finish (~2 mins) and check the URL.

## 2. Build Failure (Code Revert)

**When to use**: Deployment fails to build, or prolonged outage requiring code fix.

1.  **Identify** the bad commit:
    ```bash
    git log --oneline
    ```
2.  **Revert** the commit locally:
    ```bash
    git revert <BAD_COMMIT_HASH>
    ```
3.  **Push** to `main`:
    ```bash
    git push origin main
    ```
4.  **Monitor** Render Dashboard for the new build triggers.

## 3. Configuration Rollback

**When to use**: Issue caused by bad Environment Variables.

1.  Go to Render Dashboard -> Service -> **Environment**.
2.  Revert the changed variable (e.g., `NEXT_PUBLIC_API_URL`).
3.  **Save Changes**. This will trigger an automatic re-deploy.

## 4. Communication

*   **Notify**: Team Slack channel `#deployment-alerts`.
*   **Log**: Incident in `CHANGELOG.md` under [Rolled Back].
