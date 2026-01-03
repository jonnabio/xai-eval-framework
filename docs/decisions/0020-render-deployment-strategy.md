# 20. Render Deployment Strategy

Date: 2026-01-02

## Status

Accepted

## Context

The XAI Evaluation Framework requires a production-like environment to host the API backend for two primary reasons:
1.  **Dashboard Integration**: The Next.js frontend needs a stable API endpoint for integration testing and eventual public demonstration.
2.  **Academic Validation**: To demonstrate the framework's utility in a real-world scenario as part of the PhD thesis defense.

We considered several options:
*   **Railway**: Previously the top choice, but recent pricing model changes and trial limitations make it less attractive for a zero-budget academic project.
*   **Heroku**: No longer offers a free tier.
*   **Self-Hosting (VPS)**: High maintenance burden for security, SSL, and updates.
*   **Render.com**: Offers a generous free tier, automatic HTTPS, Git integration, and sufficient resources for our workload (Python/FastAPI).

The application requires:
*   Python 3.11+ runtime.
*   Ability to install dependencies via `pip`.
*   Environment variable management for secrets (Sentry DSN).
*   Public HTTPS endpoint.

## Decision

We will deploy the backend to **Render.com** using their "Web Service" offering.

### Implementation Details

1.  **Infrastructure as Code**: We will use a `render.yaml` file in the repository root to define the service configuration. This allows for reproducible deployments and "Blueprint" usage.
2.  **Runtime**: Python 3 Native Environment (Render supports 3.11).
3.  **Server**: We will use `uvicorn` as the ASGI server.
4.  **Health Check**: A specific `/health` endpoint will be implemented for Render's zero-downtime deployment checks.

### Environment Management

We will use a strictly split environment strategy:
*   **Development**: `.env` file (git-ignored), `DEBUG=true`, `LOG_LEVEL=DEBUG`.
*   **Production**: Render Environment Variables, `DEBUG=false`, `LOG_LEVEL=INFO`.

**Required Production Variables:**
*   `ENVIRONMENT`: `production`
*   `SENTRY_DSN`: [Secret]
*   `CORS_ORIGINS`: `https://xai-dashboard-app.vercel.app` (or equivalent)
*   `PORT`: `10000` (Managed by Render)

## Consequences

### Positive
*   **Cost**: Zero cost for the initial stage (Free Tier).
*   **Automation**: Push-to-deploy from GitHub `main` branch.
*   **Security**: Automatic TLS/SSL certificates.
*   **Observability**: Integrated log streams and easy Sentry integration.

### Negative
*   **Cold Starts**: The free tier spins down after 15 minutes of inactivity, causing a ~30s delay for the first request. This is acceptable for the current phase but must be noted for the demo.
*   **Resource Limits**: 512MB RAM cap. We must monitor memory usage, specifically when loading heavy models (XGBoost/scikit-learn) and datasets.

### Rollback Strategy

In case of a bad deployment:
1.  **Immediate**: Use the Render Dashboard "Rollback" button to revert to the previous successful deploy history.
2.  **Fix**: Revert the problematic commit in GitHub (`git revert`) and push to trigger a new build.

## Compliance
*   **ADR**: This document satisfies the architecture decision record requirement.
*   **Thesis**: The deployment methodology will be described in Chapter 4 (Implementation).
