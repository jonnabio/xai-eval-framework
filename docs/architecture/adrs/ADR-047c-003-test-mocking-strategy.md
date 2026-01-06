# ADR-047c-003: Test Mocking Strategy for Page Integration

## Status
Accepted

## Context
The current test file `src/app/experiments/[id]/__tests__/page.test.tsx` has a critical bug:

**Mocks non-existent hooks**:
```typescript
jest.mock("../../../lib/hooks/useExperimentData", () => ({
    useExperimentResult: jest.fn(),  // ❌ Doesn't exist!
    useExperimentInstances: jest.fn() // ❌ Doesn't exist yet!
}))
```

**Actual page uses**:
```typescript
const { data: run } = useExperimentDetail(runId)  // ✅ This is the real hook
```

This causes tests to:
1. ❌ Pass despite not testing real code paths
2. ❌ Provide false confidence in test coverage
3. ❌ Miss regressions in actual implementation

## Decision
Adopt a **strict hook mocking strategy** that mirrors actual implementation:

1. **Mock Exact Hooks**: Only mock hooks that the component actually uses
2. **Type-Safe Mocks**: Use TypeScript to catch mismatches
3. **Integration Tests**: Test data flow, not just rendering
4. **Presenter Testing**: Test presenters separately from page

## Implementation

### Page Test Strategy

**Mock the actual hooks used**:
```typescript
jest.mock("@/lib/hooks/useExperimentData", () => ({
    useExperimentDetail: jest.fn(),      // ✅ Actually used
    useExperimentInstances: jest.fn(),   // ✅ To be used
}))

jest.mock("@/components/experiments/useMetricsDashboardPresenter", () => ({
    useMetricsDashboardPresenter: jest.fn() // ✅ After refactor
}))
```

**Test scenarios**:
```typescript
describe('ExperimentDetailsPage', () => {
    it('renders with presenter pattern', () => {
        // Mock presenter return
        (useMetricsDashboardPresenter as jest.Mock).mockReturnValue({
            props: {
                metrics: mockMetrics,
                loading: false,
                error: null,
                isEmpty: false
            }
        })
        
        render()
        expect(screen.getByTestId('dashboard')).toBeInTheDocument()
    })
    
    it('handles loading state', () => {
        (useMetricsDashboardPresenter as jest.Mock).mockReturnValue({
            props: { loading: true }
        })
        
        render()
        expect(screen.getByText(/Loading/)).toBeInTheDocument()
    })
    
    it('handles error state', () => {
        (useMetricsDashboardPresenter as jest.Mock).mockReturnValue({
            props: { 
                error: new Error('API failed'),
                onRetry: jest.fn()
            }
        })
        
        render()
        expect(screen.getByText(/API failed/)).toBeInTheDocument()
    })
})
```

### Presenter Test Strategy

**Test presenters independently**:
```typescript
// src/components/experiments/__tests__/useMetricsDashboardPresenter.test.ts
import { renderHook } from '@testing-library/react'
import { useMetricsDashboardPresenter } from '../useMetricsDashboardPresenter'

describe('useMetricsDashboardPresenter', () => {
    it('transforms data correctly', () => {
        // Mock useExperimentMetrics
        (useExperimentMetrics as jest.Mock).mockReturnValue({
            data: mockMetrics,
            isLoading: false,
            error: null
        })
        
        const { result } = renderHook(() => 
            useMetricsDashboardPresenter({ runId: 'test-123' })
        )
        
        expect(result.current.props.metrics).toEqual(mockMetrics)
        expect(result.current.props.loading).toBe(false)
    })
})
```

## Consequences

### Positive
- ✅ **Accurate Tests**: Tests actually verify implementation
- ✅ **Catch Regressions**: Type errors caught at test-time
- ✅ **Documentation**: Tests serve as usage examples
- ✅ **Confidence**: High confidence tests cover real code paths

### Negative
- ⚠️ **Maintenance**: Must update mocks when hooks change
- ⚠️ **Verbosity**: More setup code per test

### Neutral
- 📝 Must mock both page hooks AND presenter hooks
- 📝 Integration tests may need MSW for API layer

## Testing Layers

### Layer 1: Unit Tests (Presenters)
- **What**: Test presenter hooks in isolation
- **Mocks**: Mock data fetching hooks only
- **Coverage**: Data transformation, error handling, loading states

### Layer 2: Integration Tests (Page)
- **What**: Test page composition with real components
- **Mocks**: Mock presenter hooks (not raw data hooks)
- **Coverage**: Component integration, user interactions

### Layer 3: E2E Tests (Playwright)
- **What**: Test full user flows
- **Mocks**: Real API with MSW or test backend
- **Coverage**: Critical user paths

## Coverage Targets
- **Presenter hooks**: 90%+ (critical business logic)
- **Page components**: 80%+ (integration testing)
- **Overall**: 80%+ (project standard)

## Mock Organization

### Good: Centralized Mock Factories
```typescript
// src/lib/test-utils/mock-factories.ts
export const createMockRun = (overrides?: Partial): Run => ({
    runId: 'test-123',
    modelName: 'RandomForest',
    metrics: createMockMetrics(),
    ...overrides
})

export const createMockMetrics = (): MetricSet => ({
    Fidelity: 0.85,
    Stability: 0.92,
    // ...
})
```

### Bad: Inline Mocks Everywhere
```typescript
// ❌ Repetitive, hard to maintain
const mockRun = { runId: '...', modelName: '...', ... }
```

## Related ADRs
- ADR-047c-001: Presenter Pattern Adoption
- ADR-047c-002: Instance Data Architecture

## References
- Jest docs: https://jestjs.io/docs/mock-functions
- Testing Library: https://testing-library.com/docs/react-testing-library/intro/
- React Query testing: https://tanstack.com/query/latest/docs/react/guides/testing
