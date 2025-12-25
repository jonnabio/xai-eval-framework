# Pull Request Review Guide

## Overview
This guide helps reviewers systematically evaluate the integration PRs for both the backend (xai-eval-framework) and frontend (xai-benchmark) repositories.

## Review Checklist

### 1. Code Quality
- [ ] Code follows established patterns and style guide
- [ ] Functions are well-documented with docstrings
- [ ] Variable names are clear and descriptive
- [ ] No obvious code smells or anti-patterns
- [ ] Error handling is comprehensive
- [ ] Logging is appropriate and informative

### 2. Architecture & Design
- [ ] Follows ADR decisions (check docs/adr/)
- [ ] Separation of concerns is maintained
- [ ] Dependencies are properly managed
- [ ] API contracts are well-defined
- [ ] Database/file operations are safe
- [ ] Async patterns used correctly

### 3. Testing
- [ ] All tests pass locally
- [ ] Test coverage meets 80%+ requirement
- [ ] Tests cover edge cases and error conditions
- [ ] Integration tests verify end-to-end flows
- [ ] Test descriptions are clear
- [ ] Mocks are used appropriately

### 4. Documentation
- [ ] README updated if needed
- [ ] API documentation is complete
- [ ] ADRs document key decisions
- [ ] CHANGELOG entries are present
- [ ] Code comments explain "why" not "what"
- [ ] Setup instructions are clear

### 5. Security
- [ ] No secrets or credentials in code
- [ ] Environment variables used for config
- [ ] Input validation is thorough
- [ ] CORS settings are appropriate
- [ ] File operations use safe paths
- [ ] Dependencies have no known vulnerabilities

### 6. Performance
- [ ] No obvious performance issues
- [ ] Database queries are efficient
- [ ] API responses are reasonably fast
- [ ] Resources are properly cleaned up
- [ ] Caching used where appropriate

## Specific Review Points by Component

### Backend (xai-eval-framework)

#### API Layer (src/api/)
**Files to review:**
- `src/api/main.py` - FastAPI application setup
- `src/api/routes/` - Experiment endpoints
- `src/api/dependencies.py` - Dependency injection

**Key review points:**
1. Is CORS configuration appropriate for production?
2. Are all endpoints properly documented with OpenAPI?
3. Is error handling consistent across endpoints?
4. Are HTTP status codes used correctly?
5. Is request validation comprehensive?

#### Core Logic (src/core/)
**Files to review:**
- `src/api/services/` - Business logic services
- `src/api/config.py` - Configuration management

**Key review points:**
1. Is experiment execution logic clear and maintainable?
2. Are file operations atomic and safe?
3. Is configuration properly validated?
4. Are errors propagated correctly?
5. Is logging sufficient for debugging?

#### Data Models (src/models/)
**Files to review:**
- `src/api/models/schemas.py` - Pydantic models

**Key review points:**
1. Are Pydantic models properly validated?
2. Are all fields documented?
3. Are defaults appropriate?
4. Is serialization handled correctly?
5. Are validation errors user-friendly?

#### Tests (tests/)
**Files to review:**
- `src/api/tests/` - API endpoint tests

**Key review points:**
1. Do tests cover happy paths and error cases?
2. Are test fixtures well-organized?
3. Are assertions specific and meaningful?
4. Is test isolation maintained?
5. Are integration tests realistic?

### Frontend (xai-benchmark)

#### Components (src/components/)
**Files to review:**
- `src/components/` - React components
- `src/components/visualizations/` - Charts

**Key review points:**
1. Are components properly typed with TypeScript?
2. Is error handling implemented?
3. Are loading states shown to users?
4. Is accessibility considered?
5. Are components reusable?

#### API Integration (src/lib/)
**Files to review:**
- `src/lib/api.ts` - API wrapper
- `src/lib/types.ts` - TypeScript types

**Key review points:**
1. Does API client handle errors gracefully?
2. Are TypeScript types complete and accurate?
3. Is response data validated?
4. Are network errors handled?
5. Is caching implemented correctly?

#### Pages (src/app/)
**Files to review:**
- `src/app/page.tsx` - Home page
- `src/app/runs/[id]/page.tsx` - Detail page

**Key review points:**
1. Is server-side rendering used appropriately?
2. Are loading and error states handled?
3. Is SEO metadata present?
4. Are routes type-safe?
5. Is navigation intuitive?
