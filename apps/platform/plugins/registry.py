import logging
from typing import Dict, List, Optional, Type
from .base import PluginBase, PluginHook, PluginMeta

logger = logging.getLogger('platform')

# Global plugin registry
_PLUGIN_REGISTRY: Dict[str, Type[PluginBase]] = {}
_HOOK_REGISTRY: Dict[str, List[Type[PluginHook]]] = {}


def register_plugin(plugin_class: Type[PluginBase]):
    """Register a plugin class in the global registry."""
    if not hasattr(plugin_class, 'meta') or not plugin_class.meta.slug:
        raise ValueError(f"Plugin {plugin_class} must define a 'meta' attribute with a slug.")
    _PLUGIN_REGISTRY[plugin_class.meta.slug] = plugin_class
    logger.debug(f"Registered plugin: {plugin_class.meta.slug}")


def register_hook(hook_class: Type[PluginHook]):
    """Register a hook implementation."""
    if not hook_class.hook_name:
        raise ValueError(f"Hook {hook_class} must define a 'hook_name'.")
    if hook_class.hook_name not in _HOOK_REGISTRY:
        _HOOK_REGISTRY[hook_class.hook_name] = []
    _HOOK_REGISTRY[hook_class.hook_name].append(hook_class)


def get_plugin(slug: str) -> Optional[Type[PluginBase]]:
    """Get a plugin class by slug."""
    return _PLUGIN_REGISTRY.get(slug)


def list_plugins() -> Dict[str, PluginMeta]:
    """List all registered plugins with their metadata."""
    return {
        slug: cls.meta
        for slug, cls in _PLUGIN_REGISTRY.items()
    }


def execute_hook(hook_name: str, context: Dict, default=None):
    """Execute all registered hooks for a given hook name.

    Returns the result of the last hook, or default if no hooks registered.
    """
    hooks = _HOOK_REGISTRY.get(hook_name, [])
    result = default
    for hook_class in hooks:
        try:
            hook = hook_class()
            result = hook.execute(context)
        except Exception as e:
            logger.error(f"Hook {hook_name} failed in {hook_class.__name__}: {e}")
    return result


def get_hooks_for_plugin(slug: str) -> List[str]:
    """Get all hook names that a given plugin registers."""
    # This is a simplification; real implementation would track plugin->hook mapping
    return list(_HOOK_REGISTRY.keys())
