from typing import Generic, TypeVar, Type, Optional, List, Any
from django.db import models
from django.core.exceptions import ObjectDoesNotExist

T = TypeVar('T', bound=models.Model)

class BaseRepository(Generic[T]):
    """Base generic repository implementing common CRUD operations using Django ORM.

    Encapsulates all database-specific query queries to insulate the service layer.
    """

    model: Type[T]

    def __init__(self) -> None:
        if not hasattr(self, 'model') or self.model is None:
            raise NotImplementedError("Repositories inheriting from BaseRepository must define a 'model' attribute.")

    def get_by_id(self, pk: Any) -> Optional[T]:
        """Fetch a single record by its primary key. Returns None if not found."""
        try:
            return self.model.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return None

    def list_all(self) -> List[T]:
        """Fetch all records of the model."""
        return list(self.model.objects.all())

    def create(self, **fields: Any) -> T:
        """Instantiate and save a new record with specified fields."""
        obj = self.model(**fields)
        obj.full_clean()
        obj.save()
        return obj

    def update(self, obj: T, **fields: Any) -> T:
        """Update fields of an existing model instance and save it."""
        for field, value in fields.items():
            setattr(obj, field, value)
        obj.full_clean()
        obj.save()
        return obj

    def delete(self, obj: T) -> bool:
        """Delete a record from the database. Returns True on success."""
        _, deleted = obj.delete()
        return bool(deleted)
