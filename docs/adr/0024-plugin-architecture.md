# ADR-0024: Plugin Architecture

## Status
Accepted

## Date
2026-07-17

## Context
The platform needs an extensibility mechanism that allows adding new functionality without modifying core code. Plugins should be able to hook into content publishing, user login, stream events, and dashboard rendering.

## Decision
We define a **Plugin Architecture** with abstract base classes and a hook system. This is an interface-only implementation; no concrete plugins are built in this sprint.

### Architecture:
- **PluginBase**: Abstract class with `install()`, `uninstall()`, `on_enable()`, `on_disable()`, `get_urls()`, `get_template_tags()`, `get_admin_views()`
- **PluginMeta**: Dataclass with slug, name, description, version, author, category, dependencies
- **PluginHook**: Abstract hook class with `execute(context)` method
- **Built-in Hooks**:
  - `BeforeContentPublishHook` / `AfterContentPublishHook`
  - `BeforeUserLoginHook` / `AfterUserLoginHook`
  - `OnStreamStartHook` / `OnStreamEndHook`
  - `TransformContentHook`
  - `DashboardWidgetHook`
- **Registry**: `register_plugin()`, `register_hook()`, `execute_hook()`

### Plugin Lifecycle:
1. Plugin is registered via `register_plugin(PluginClass)`
2. Plugin's `install()` creates necessary DB tables/migrations
3. Plugin's `on_enable()` activates its hooks
4. Hooks are executed via `execute_hook(hook_name, context)`
5. Plugin's `on_disable()` deactivates hooks
6. Plugin's `uninstall()` cleans up

### Hook Execution:
```python
from apps.platform.plugins import execute_hook

result = execute_hook('before_content_publish', {
    'content_type': 'article',
    'content_id': str(article.pk),
    'user': request.user,
    'action': 'publish',
})
if result is False:
    # Plugin blocked the publish
    return HttpResponse('Publish blocked by plugin')
```

## Consequences
- Plugins are interfaces only; concrete plugins are future work
- Hook execution is synchronous and ordered by registration
- Failed hooks are logged but don't block the pipeline
- Plugin metadata enables a future plugin marketplace
- Plugin dependencies enforce ordering and compatibility

## References
- `apps/platform/plugins/base.py` - Plugin and Hook interfaces
- `apps/platform/plugins/registry.py` - Plugin and Hook registry
