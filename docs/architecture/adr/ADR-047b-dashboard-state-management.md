# ADR-047b: Dashboard State Management Strategy

## Status
Accepted

## Context
The "Detailed Results" view involves fetching:
1.  Heavy aggregate data (ExperimentResult).
2.  Paginated instance data (potentially 1000+ rows).

We need a strategy to handle loading states, caching, error retries, and pagination without polluting the component logic with `useEffect` spaghetti.

## Options Considered

### 1. Standard `useEffect` + `fetch`
- **Pros**: Zero dependencies.
- **Cons**: Manual handling of race conditions, deduplication, caching, and loading states. Hard to manage pagination cursors correctly.

### 2. SWR (Vercel)
- **Pros**: Lightweight, designed for Next.js.
- **Cons**: Slightly less features than TanStack Query for complex mutation/pagination flows (though capable).

### 3. TanStack Query (React Query)
- **Pros**:
    - Industry standard for server state.
    - First-class support for generic pagination (`keepPreviousData`).
    - Robust DevTools.
    - Auto-refetch on window focus (good for long running experiments).
- **Cons**: Additional boilerplate provider.

## Decision
We will use **TanStack Query (React Query)** (via `@tanstack/react-query`).

## Rationale
1.  **Pagination**: The `useQuery` hook with `placeholderData` (keepPreviousData) is perfect for the `LLMInstanceViewer` pagination, providing a smooth UI where the table doesn't flicker between pages.
2.  **DevTools**: Essential for debugging the exact payload coming from our new API endpoints.
3.  **Cache Management**: We can easily invalidate the cache if an experiment status changes from "Running" to "Completed".

## Consequences
- We will wrap the application (or the experiment layout) in a `QueryClientProvider`.
- We will create custom hooks:
    - `useExperimentDetails(runId)`
    - `useExperimentInstances(runId, page, limit)`
- We will rely on standard `fetch` or `axios` as the fetcher function passed to Query.
