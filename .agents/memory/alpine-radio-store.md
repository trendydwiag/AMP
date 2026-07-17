---
name: Alpine Radio Store Pattern
description: Why radioPlayer() x-data failed and how Alpine.store('radio') fixed it
---

## The problem
Templates used `x-data="radioPlayer()"` in three places (sticky player, hero card, mobile player).
`hero_radio.html`'s right column card had NO enclosing `x-data="radioPlayer()"` — bindings
(`currentTrack.artwork`, `isPlaying`, etc.) were floating in the parent `mobileMenuOpen` scope
and threw ReferenceErrors.

The sticky player DID have `x-data="radioPlayer()"` but the `radioPlayer()` function registered
via `Alpine.data` in an `alpine:init` listener had timing/resolution issues (possibly Service
Worker serving a cached page with the old simple `radioPlayer` global that lacked `currentTrack`).

## The fix
Switched to `Alpine.store('radio', { ... })` in `static/js/radio-player.js`.
- `$store.radio` is available in ALL Alpine components via the `$store` magic property
- No `x-data="radioPlayer()"` or component resolution needed
- All templates now use `$store.radio.xxx` directly
- `Alpine.store()` init() must be called manually after registering: `Alpine.store('radio').init()`

**Why:** `Alpine.store` is the canonical Alpine 3 pattern for global shared state; `Alpine.data`
factory components require correct timing/registration and have resolution quirks when
called as `x-data="functionName()"`.

## Files changed
- `static/js/radio-player.js` — registers `Alpine.store('radio', {...})` in `alpine:init`
- `templates/website/components/sticky_player.html` — uses `$store.radio.*`
- `templates/website/components/home/hero_radio.html` — uses `$store.radio.*` (was missing scope entirely)
- `templates/website/home.html` — mobile player uses `$store.radio.*`
- `static/sw.js` — bumped cache to v2 to clear stale SW caches

## Debug Toolbar crash (also fixed)
`ProfilingPanel` crashes with `ValueError: Another profiling tool is already active` when
concurrent requests hit the same endpoint (radio status poller every 10s).
Fix: add `'DISABLE_PANELS': {'debug_toolbar.panels.profiling.ProfilingPanel'}` to
`DEBUG_TOOLBAR_CONFIG` in `config/settings/development.py`.
