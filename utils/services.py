from typing import Generic, TypeVar, Type, Any
from django.db import transaction
from utils.repositories import BaseRepository

R = TypeVar('R', bound=BaseRepository)

class BaseService(Generic[R]):
    """Base class for all business services.

    Coordinates business processes, transaction control, validation, and triggers.
    Enforces a strict boundary between HTTP views and data persistence.
    """

    repository: R

    def __init__(self, repository: R) -> None:
        self.repository = repository

    @transaction.atomic
    def execute_in_transaction(self, callable_func: Any, *args: Any, **kwargs: Any) -> Any:
        """Helper to run code blocks atomically inside a database transaction."""
        return callable_func(*args, **kwargs)
