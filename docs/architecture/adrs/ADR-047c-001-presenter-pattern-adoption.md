# ADR-047c-001: Adopt Presenter Pattern for Experiment Details Page

## Status
Accepted

## Context
The current `src/app/experiments/[id]/page.tsx` directly uses `useExperimentDetail` hook and manually passes props to child components. This creates several issues:

1. **Tight Coupling**: Page component knows too much about data transformation
2. **Repetitive Logic**: Same data transformation logic might be needed elsewhere
3. **Testing Complexity**: Tests must mock multiple hooks and handle transformation
4. **Inconsistency**: We created `useMetricsDashboardPresenter` for `EnhancedMetricsDashboard` but aren't using it

The Presenter pattern (also known as "Smart Component" pattern) separates:
- **Data fetching & transformation** (Presenter/Hook)
- **Presentation logic** (Component)

## Decision
We will refactor `page.tsx` to use the existing `useMetricsDashboardPresenter` hook instead of directly calling `useExperimentDetail` and manually passing props.

**Before**:
```typescript
const { data: run, isLoading, error } = useExperimentDetail(runId)

```

**After**:
```typescript
const { props } = useMetricsDashboardPresenter({ runId })

```

## Consequences

### Positive
- ✅ **Single Responsibility**: Page only handles composition, not data transformation
- ✅ **Reusability**: Presenter can be used in other contexts (e.g., embeddable widgets)
- ✅ **Testability**: Easier to test presenter logic independently
- ✅ **Consistency**: Aligns with existing pattern in codebase
- ✅ **Maintainability**: Data transformation logic centralized in one place

### Negative
- ⚠️ **Indirection**: One extra layer of abstraction
- ⚠️ **Learning Curve**: Developers must understand presenter pattern

### Neutral
- 📝 Additional file to maintain (presenter hook)
- 📝 Pattern must be documented for team

## Alternatives Considered

### Alternative 1: Keep Direct Hook Usage
- **Pros**: Simpler, more direct
- **Cons**: Violates DRY, hard to test, inconsistent with existing patterns
- **Rejected**: Doesn't solve coupling problem

### Alternative 2: Use Context API
- **Pros**: Could share data across components
- **Cons**: Overkill for this use case, adds unnecessary complexity
- **Rejected**: Too complex for current needs

### Alternative 3: Create Page-Level Presenter
- **Pros**: Could coordinate all page data
- **Cons**: Would duplicate logic from existing component presenters
- **Rejected**: Prefer composition over monolithic presenter

## Implementation Notes
1. `useMetricsDashboardPresenter` already exists and is tested
2. We'll extend it if needed to handle additional page-level concerns
3. Future components should follow this pattern
4. Document pattern in README for team reference

## References
- Existing implementation: `src/components/experiments/useMetricsDashboardPresenter.ts`
- React patterns: https://kentcdodds.com/blog/application-state-management-with-react
- Testing strategy: ADR-047c-003

## Related ADRs
- ADR-047c-002: Instance Data Architecture
- ADR-047c-003: Test Mocking Strategy
