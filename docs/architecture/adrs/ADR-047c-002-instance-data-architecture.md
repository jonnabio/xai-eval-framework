# ADR-047c-002: Instance Data Fetching Architecture

## Status
Accepted

## Context
The experiment details page needs to display instance-level evaluation data (LLM evaluations). Currently, the page uses mock data:
```typescript
const mockInstances: ExperimentInstance[] = React.useMemo(() => {
    if (!run) return [];
    return Array.from({ length: 10 }).map((_, i) => ({
        id: `inst-${i}`,
        // ... mock data
    }));
}, [run]);
```

This approach has several problems:
1. **Not Real Data**: Shows fake data to users
2. **API Waste**: Backend has `/runs/{id}/instances` endpoint that's unused
3. **No Pagination**: Can't handle large result sets efficiently
4. **Testing Gaps**: Tests don't verify real data flow

## Decision
Create a dedicated `useExperimentInstances` hook following the established data fetching pattern in `useExperimentData.ts`.

**Implementation**:
```typescript
// src/lib/hooks/useExperimentData.ts
export function useExperimentInstances(
    runId: string, 
    limit: number = 20, 
    offset: number = 0
) {
    return useQuery({
        queryKey: [...experimentKeys.detail(runId), 'instances', limit, offset],
        queryFn: () => apiAdapter.getInstances(runId, limit, offset),
        enabled: !!runId,
        staleTime: 1000 * 60 * 5, // 5 minutes
    });
}
```

**API Adapter**:
```typescript
// src/lib/apiAdapter.ts
async getInstances(
    runId: string, 
    limit: number = 20, 
    offset: number = 0
): Promise {
    return this.request(
        `/runs/${runId}/instances?limit=${limit}&offset=${offset}`
    );
}
```

## Consequences

### Positive
- ✅ **Real Data**: Displays actual LLM evaluation results
- ✅ **Pagination**: Handles large datasets efficiently (backend supports it)
- ✅ **Consistency**: Follows established hook pattern
- ✅ **Caching**: React Query handles deduplication and caching
- ✅ **Error Handling**: Centralized error handling via React Query

### Negative
- ⚠️ **Additional Network Request**: Separate from run detail fetch
- ⚠️ **Complexity**: State management for pagination

### Neutral
- 📝 Must handle loading/error states in UI
- 📝 Pagination UI needed for large datasets

## Alternatives Considered

### Alternative 1: Embed Instances in Run Detail Response
- **Pros**: Single network request
- **Cons**: Large payload, not scalable, backend already separated this
- **Rejected**: Backend architecture already uses separate endpoint

### Alternative 2: Server-Side Pagination with Next.js
- **Pros**: Better SEO, faster initial load
- **Cons**: Complex state management, loses client-side caching
- **Rejected**: Client-side better for interactive dashboard

### Alternative 3: Infinite Scroll with React Query
- **Pros**: Better UX for scrolling
- **Cons**: More complex implementation, can revisit later
- **Deferred**: Start with simple pagination, iterate if needed

## Implementation Plan

### Phase 1: Hook Creation
1. Add `useExperimentInstances` to `useExperimentData.ts`
2. Add `getInstances` to `apiAdapter.ts`
3. Update types if needed (`InstancesResponse`, etc.)

### Phase 2: Page Integration
1. Replace mock data with `useExperimentInstances(runId)`
2. Pass real data to `LLMInstanceViewer`
3. Handle loading/error states

### Phase 3: Testing
1. Unit test hook with MSW
2. Integration test page with real data flow
3. Error scenario tests

## Pagination Strategy
- **Default**: 20 instances per page
- **Backend Max**: 100 instances per request (configurable)
- **UI**: Standard Previous/Next pagination
- **Future**: Can add infinite scroll if UX needs it

## Error Handling
Follow React Query error handling pattern:
```typescript
const { data, isLoading, error } = useExperimentInstances(runId);

if (error) {
    // Display error UI with retry button
}
```

## References
- Backend API: `xai-eval-framework/src/api/routes/runs.py`
- API schema: `ExperimentResultResponse`, `InstancesResponse`
- React Query docs: https://tanstack.com/query/latest

## Related ADRs
- ADR-047c-001: Presenter Pattern Adoption
- ADR-047c-003: Test Mocking Strategy
