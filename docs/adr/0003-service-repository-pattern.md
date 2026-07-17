# 0003. Use Service-Repository Pattern

**Status:** Accepted
**Date:** 2024-07-01

## Context

Django views often accumulate business logic, database queries, and validation into monolithic view functions or CBV methods. This leads to:

- Untestable business logic tangled with HTTP concerns
- Duplicate query logic across views and management commands
- Difficulty reusing business rules outside the web layer (CLI, API, tests)

The project needs a clear separation between data access, business logic, and presentation.

## Decision

We adopt the **Service-Repository pattern** with two generic base classes:

### BaseRepository[T]

Located in `utils/repositories.py`. Encapsulates all database operations:

```python
class BaseRepository(Generic[T]):
    model: Type[T]

    def get_by_id(self, pk: Any) -> Optional[T]: ...
    def list_all(self) -> List[T]: ...
    def create(self, **fields: Any) -> T: ...
    def update(self, obj: T, **fields: Any) -> T: ...
    def delete(self, obj: T) -> bool: ...
```

### BaseService[R]

Located in `utils/services.py`. Orchestrates business logic:

```python
class BaseService(Generic[R]):
    repository: R

    def __init__(self, repository: R) -> None:
        self.repository = repository

    @transaction.atomic
    def execute_in_transaction(self, callable_func, *args, **kwargs):
        return callable_func(*args, **kwargs)
```

### Layer Flow

```
Views → Services → Repositories → Django ORM
```

Each app defines its own Repository and Service subclasses:

```python
# apps/radio/repositories.py
class RadioStationRepository(BaseRepository[RadioStation]):
    model = RadioStation

# apps/radio/services.py
class RadioStationService(BaseService[RadioStationRepository]):
    def __init__(self):
        super().__init__(RadioStationRepository())
```

## Consequences

**Positive:**

- Business logic is testable in isolation by mocking the repository.
- Repository subclasses can add custom query methods (e.g., `get_active_stations()`, `get_by_slug()`).
- Services can be consumed from views, management commands, tests, or future API endpoints.
- `@transaction.atomic` is centralized in the base service for multi-step operations.

**Negative:**

- Adds an extra layer of indirection compared to calling `Model.objects.filter()` directly.
- Requires discipline to avoid bypassing services from views.
- Each new model requires at least two new files (repository + service).

**Mitigations:**

- The website module is enforced to only consume Services (see ADR-0018).
- Base classes are minimal (48 and 22 lines respectively), keeping boilerplate low.
- Custom query methods in Repository subclasses keep complex queries DRY.
