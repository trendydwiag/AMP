"""
Media Pipeline — Event System
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Lightweight pub/sub event dispatcher for media lifecycle events.
No message broker needed — handlers are plain Python callables.
Designed to be swapped for Celery signals / Django signals in the future.

Usage:
    # Register a handler
    @MediaEventDispatcher.on(EVENT_MEDIA_UPLOADED)
    def notify_on_upload(event: MediaEvent):
        print(f"Uploaded: {event.media_file.title}")

    # Dispatch an event (done by MediaPipelineService)
    MediaEventDispatcher.dispatch(EVENT_MEDIA_UPLOADED, media_file, metadata={'size': 1024})
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Callable

logger = logging.getLogger(__name__)

# ── Event name constants ────────────────────────────────────────────────────
EVENT_MEDIA_UPLOADED = 'media.uploaded'
EVENT_MEDIA_PROCESSED = 'media.processed'
EVENT_MEDIA_DELETED = 'media.deleted'
EVENT_MEDIA_UPDATED = 'media.updated'
EVENT_MEDIA_FAILED = 'media.failed'
EVENT_MEDIA_ARCHIVED = 'media.archived'

ALL_EVENTS = (
    EVENT_MEDIA_UPLOADED,
    EVENT_MEDIA_PROCESSED,
    EVENT_MEDIA_DELETED,
    EVENT_MEDIA_UPDATED,
    EVENT_MEDIA_FAILED,
    EVENT_MEDIA_ARCHIVED,
)


# ── Event dataclass ─────────────────────────────────────────────────────────
@dataclass
class MediaEvent:
    """Immutable event payload passed to all registered handlers."""
    name: str                               # One of the EVENT_* constants
    media_file: object                      # MediaFile instance (typed as object to avoid circular import)
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: dict = field(default_factory=dict)

    def __repr__(self) -> str:
        return f"<MediaEvent name={self.name!r} media={getattr(self.media_file, 'title', '?')!r}>"


# ── Dispatcher ──────────────────────────────────────────────────────────────
class MediaEventDispatcher:
    """
    Class-level registry of event handlers.
    Thread-safe for read (dispatch) but not for concurrent register calls at runtime.
    For production, swap this for Django signals or Celery tasks.
    """
    _handlers: dict[str, list[Callable[[MediaEvent], None]]] = {}

    @classmethod
    def register(cls, event_name: str, handler: Callable[[MediaEvent], None]) -> None:
        """Register a callable to be called when event_name is dispatched."""
        if event_name not in cls._handlers:
            cls._handlers[event_name] = []
        if handler not in cls._handlers[event_name]:
            cls._handlers[event_name].append(handler)
            logger.debug("Registered handler %s for event %s", handler.__name__, event_name)

    @classmethod
    def on(cls, event_name: str) -> Callable:
        """Decorator shorthand for register()."""
        def decorator(fn: Callable) -> Callable:
            cls.register(event_name, fn)
            return fn
        return decorator

    @classmethod
    def dispatch(cls, event_name: str, media_file: object, metadata: dict | None = None) -> int:
        """
        Dispatch an event to all registered handlers.
        Returns the number of handlers called.
        Exceptions in individual handlers are caught and logged — dispatch always completes.
        """
        event = MediaEvent(
            name=event_name,
            media_file=media_file,
            metadata=metadata or {},
        )
        handlers = cls._handlers.get(event_name, [])
        called = 0
        for handler in handlers:
            try:
                handler(event)
                called += 1
            except Exception as exc:
                logger.exception(
                    "Handler %s raised an exception for event %s: %s",
                    getattr(handler, '__name__', repr(handler)),
                    event_name,
                    exc,
                )
        logger.debug("Dispatched %s to %d handler(s)", event_name, called)
        return called

    @classmethod
    def clear(cls, event_name: str | None = None) -> None:
        """Remove all handlers, optionally scoped to one event. Useful in tests."""
        if event_name:
            cls._handlers.pop(event_name, None)
        else:
            cls._handlers.clear()
