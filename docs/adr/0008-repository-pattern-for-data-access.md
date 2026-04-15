# 8. Repository Pattern for Data Access

Date: 2026-01-10
Status: Accepted

## Context

Currently, data access logic (reading experiment files from the filesystem) is tightly coupled with the API layer, specifically within service modules and sometimes even route handlers. This makes testing difficult, as it requires mocking filesystem operations. Furthermore, any future migration to a different storage backend (like a database) would require rewriting data access logic across multiple parts of the application.

## Decision

We will implement the Repository design pattern to abstract the data access layer from the rest of the application.

**Rationale**:
- **Abstraction**: It decouples the business logic (in API routes and services) from the storage implementation details.
- **Testability**: It allows for easy mocking of the data layer in unit tests. We can inject a `MockRepository` instead of a real one that hits the filesystem or a database.
- **Flexibility**: It makes the storage backend swappable. We can easily switch between a `FileSystemRepository` and a `DatabaseRepository` by changing the dependency injection configuration.
- **Clear Migration Path**: This pattern provides a clear path for a future database migration. We can even run both implementations in parallel during a transition period.

**Implementation**:
An abstract base class, `ExperimentRepository`, will define the data access interface.

```python
from abc import ABC, abstractmethod

class ExperimentRepository(ABC):
    @abstractmethod
    def list_experiments(self, filters, offset, limit) -> (List[Run], int):
        pass
    
    @abstractmethod
    def get_experiment_by_run_id(self, run_id: str) -> Optional[ExperimentResult]:
        pass
```

Concrete implementations like `FileSystemRepository` and `DatabaseRepository` will inherit from this ABC. The application will use dependency injection to provide the appropriate repository implementation to the service layer.

## Consequences

### Positive
-   Code becomes more modular and adheres to the Single Responsibility Principle.
-   Unit testing of services and routes is greatly simplified.
-   Eases the future transition to a database backend.

### Negative
-   Introduces a layer of abstraction, which can add a small amount of complexity and boilerplate code.
-   Requires setting up a dependency injection system to manage repository instances.