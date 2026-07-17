import uuid
from typing import Any
from django.db import models
from django.contrib.auth import get_user_model
import logging

security_logger = logging.getLogger('security')

class UUIDPrimaryKeyMixin(models.Model):
    """Abstract model mixin adding a UUID4 primary key instead of standard auto-incrementing integer."""

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Universally unique identifier (UUIDv4) primary key."
    )

    class Meta:
        abstract = True


class TimeStampedModel(models.Model):
    """Abstract model mixin adding automated audit timestamp fields for tracking creation and updates."""

    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        help_text="Timestamp when the object was created."
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the object was last updated."
    )

    class Meta:
        abstract = True


class AuditLogMixin:
    """Mixin for logging database write operations (creations, edits, deletions) to the security log.

    Integrates with views or models to output audit trails.
    """

    def log_action(self, user: Any, action: str, details: str = "") -> None:
        """Log administrative or system events to the security audit trail."""
        username = user.username if user and user.is_authenticated else "AnonymousSystem"
        ip_addr = getattr(user, '_ip_address', 'UnknownIP')
        security_logger.info(
            f"[AUDIT] Action: {action} | User: {username} | IP: {ip_addr} | Details: {details}"
        )
