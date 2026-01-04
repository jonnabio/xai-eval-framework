# 5. Render Frontend Deployment Strategy

Date: 2026-01-04

## Status

Accepted

## Context

The XAI Dashboard is a Next.js application that requires hosting with:
1.  **Unified Infrastructure**: The backend is already on Render; consolidating simplifies management and billing.
2.  **Internal Networking**: Render allows private networking between services, reducing latency and exposure.
3.  **Cost Efficiency**: Leveraging the existing Render infrastructure avoids managing a separate provider (Vercel).

We considered:
*   **Vercel**: Best-in-class for Next.js (Edge Functions, ISR), but introduces a second platform, disjointed monitoring, and potentially higher costs for team seats.
*   **Render**: Simplifies ops (Monorepo support), offers private networking, but lacks native Next.js features like ISR and Edge Middleware.

## Decision

We will deploy the Dashboard Frontend to **Render** as a Node.js Web Service.

### Implementation Details

1.  **Service Type**: Web Service (Node.js Environment).
2.  **Build Command**: `cd xai-benchmark && npm ci && npm run build`.
3.  **Start Command**: `cd xai-benchmark && node .next/standalone/server.js`.
4.  **Configuration**:
    *   `output: 'standalone'` in `next.config.mjs` to create a minimal production build.
    *   `sharp` installed for image optimization.
5.  **Environment**: 
    *   `NODE_ENV=production`.
    *   `NEXT_PUBLIC_API_URL` points to `http://xai-eval-api:10000` (internal) if possible, or the public Render URL.

## Consequences

### Positive
*   **Simplified Ops**: Single dashboard for all services.
*   **Security**: Backend API can potentially be private (internal-only).
*   **Cost**: Leverages Render pricing model (predictable).

### Negative
*   **No ISR**: Incremental Static Regeneration is not supported on Node.js runtime (requires Vercel-like serverless or extra config). Apps must rely on SSR or standard caching.
*   **Build Times**: Generally slower than Vercel.
*   **Latency**: Single region (Oregon) serving all users, vs Vercel's global edge network. Accepted as this is a research tool.
