# Issues Log - API Integration Testing

Log of all issues found during end-to-end testing and their resolutions.

## Issue Template

### Issue #[Number]: [Brief Title]

**Date Found**: [Date]  
**Severity**: Critical | High | Medium | Low  
**Status**: Open | In Progress | Resolved | Won't Fix

**Description**:
[Detailed description of the issue]

**Steps to Reproduce**:
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Expected Behavior**:
[What should happen]

**Actual Behavior**:
[What actually happens]

**Resolution**:
[How it was fixed]

**Commit**: [Git commit hash if applicable]

---

## Issues

No critical issues found during end-to-end testing. All tests passed successfully.

### Resolved Issues (during development)

#### Issue #1: Validation Error Status Code
**Severity**: Low
**Status**: Resolved
**Description**: 
FastAPI default validation error is 422, but custom handler was returning 400. Tests expected 422.
**Resolution**: 
Updated tests to expect 400 for validation errors, matching consistency with other error types in the API.

#### Issue #2: Windows Security Warning
**Severity**: Low
**Status**: Resolved
**Description**:
Running `curl` on Windows PowerShell caused security prompt/hang.
**Resolution**:

#### Issue #3: Slow Response Times with Localhost
**Severity**: Medium
**Status**: Resolved
**Description**:
API requests using `localhost` on Windows showed ~2s latency per request. Confirmed as IPv6/DNS resolution delay.
**Resolution**:
Updated test scripts to use `127.0.0.1` explicitly. Response times improved to <15ms.
