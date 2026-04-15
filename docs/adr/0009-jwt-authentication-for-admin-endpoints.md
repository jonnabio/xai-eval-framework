# 9. JWT Authentication for Admin Endpoints

Date: 2026-01-10
Status: Accepted

## Context

Several API endpoints, particularly those for human evaluation administration (`/human-eval/admin/*`) and debugging (`/db/*`), are currently unprotected. This poses a critical security risk, as it allows unauthorized users to access potentially sensitive data, submit fake annotations, and gain information about the system's internal structure. The API is stateless, so a session-based authentication mechanism is not suitable.

## Decision

We will secure all administrative and sensitive endpoints using JSON Web Tokens (JWT) with a role-based access control (RBAC) mechanism.

**Rationale**:
- **Stateless Standard**: JWT is an industry standard for securing stateless APIs. The token contains all necessary information for verification, avoiding the need for server-side session storage.
- **RBAC for Granularity**: Including a `role` claim (e.g., "admin", "annotator") in the JWT payload allows for simple and effective role-based access control.
- **FastAPI Integration**: FastAPI has excellent built-in support for OAuth2 and JWT, including dependency injection for protecting routes.
- **No Database Dependency**: Token validation is cryptographic and does not require a database lookup, keeping the authentication process fast.

**Implementation**:
1.  **Token Generation**: A login endpoint will issue JWTs containing the user's identity (`sub`) and `role`.
2.  **Dependencies**: FastAPI dependencies (`Depends`) will be created to verify the token and check the user's role.
3.  **Protected Routes**: These dependencies will be applied to all sensitive endpoints.

```python
# Example of a protected route
@router.get("/admin/stats")
async def get_stats(current_user: User = Depends(get_admin_user)):
    # Code here will only execute if the user is an authenticated admin
    ...
```

## Consequences

### Positive
-   Critical security vulnerability is closed.
-   Access to sensitive data and operations is restricted to authorized users.
-   The system provides a clear and standard way to handle permissions.

### Negative
-   Requires secure management of a `JWT_SECRET_KEY` environment variable.
-   Tokens, once issued, are valid until they expire. A token revocation system (e.g., a denylist) would be needed for immediate revocation, which adds complexity (though it is not planned for the initial implementation).
-   The frontend application must be updated to handle the login flow and attach the JWT to requests.