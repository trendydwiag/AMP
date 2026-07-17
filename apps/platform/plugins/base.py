import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field

logger = logging.getLogger('platform')


@dataclass
class PluginMeta:
    """Metadata describing a plugin."""
    slug: str = ''
    name: str = ''
    description: str = ''
    version: str = '1.0.0'
    author: str = ''
    category: str = ''
    required_tier: str = ''
    dependencies: List[str] = field(default_factory=list)
    min_platform_version: str = '1.0.0'


class PluginBase(ABC):
    """Abstract base class for all plugins.

    Plugins extend platform functionality through hooks.
    """

    meta: PluginMeta

    @abstractmethod
    def install(self) -> bool:
        """Install the plugin (create tables, seed data, etc.)."""
        ...

    @abstractmethod
    def uninstall(self) -> bool:
        """Uninstall the plugin (cleanup)."""
        ...

    def on_enable(self) -> None:
        """Called when plugin is activated."""
        pass

    def on_disable(self) -> None:
        """Called when plugin is deactivated."""
        pass

    def get_template_tags(self) -> Dict[str, str]:
        """Return template tag module paths to register."""
        return {}

    def get_urls(self) -> List[Dict[str, Any]]:
        """Return URL patterns to include."""
        return []

    def get_admin_views(self) -> List[Dict[str, Any]]:
        """Return admin views to register."""
        return []


class PluginHook(ABC):
    """Base class for plugin hooks.

    Hooks allow plugins to extend or modify core platform behavior
    at predefined extension points.
    """

    hook_name: str = ''

    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> Any:
        """Execute the hook with given context."""
        ...


class BeforeContentPublishHook(PluginHook):
    """Hook executed before content is published."""

    hook_name = 'before_content_publish'

    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> Any:
        """
        context keys:
        - content_type: str
        - content_id: str
        - user: User
        - action: str ('publish', 'unpublish')
        Returns: bool (True to allow, False to block)
        """
        ...


class AfterContentPublishHook(PluginHook):
    """Hook executed after content is published."""

    hook_name = 'after_content_publish'

    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> None:
        """
        context keys:
        - content_type: str
        - content_id: str
        - user: User
        - action: str
        """
        ...


class BeforeUserLoginHook(PluginHook):
    """Hook executed before user login is processed."""

    hook_name = 'before_user_login'

    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> bool:
        """
        context keys:
        - request: HttpRequest
        - user: User
        Returns: True to allow login, False to block
        """
        ...


class AfterUserLoginHook(PluginHook):
    """Hook executed after successful user login."""

    hook_name = 'after_user_login'

    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> None:
        """
        context keys:
        - request: HttpRequest
        - user: User
        """
        ...


class OnStreamStartHook(PluginHook):
    """Hook executed when a radio stream goes live."""

    hook_name = 'on_stream_start'

    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> None:
        """
        context keys:
        - station: RadioStation
        - provider: RadioProvider
        - session: LiveSession
        """
        ...


class OnStreamEndHook(PluginHook):
    """Hook executed when a radio stream ends."""

    hook_name = 'on_stream_end'

    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> None:
        """
        context keys:
        - station: RadioStation
        - session: LiveSession
        """
        ...


class TransformContentHook(PluginHook):
    """Hook for transforming content (e.g., AI enhancement, translation)."""

    hook_name = 'transform_content'

    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> Any:
        """
        context keys:
        - content: str (raw content)
        - content_type: str
        - transform_type: str
        Returns: transformed content
        """
        ...


class DashboardWidgetHook(PluginHook):
    """Hook for adding custom dashboard widgets."""

    hook_name = 'dashboard_widget'

    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> Any:
        """
        context keys:
        - partner: Partner
        - user: User
        Returns: dict with widget data
        """
        ...
