---
name: CurrentProgramResolver Timezone
description: Schedule times are stored in WIB (Asia/Jakarta); resolver must use localtime(now) not timezone.now() to match correctly.
---

## Rule
`CurrentProgramResolver.resolve()` in `apps/broadcast/services.py` must use `timezone.localtime(now)` when extracting `.time()` and `.weekday()` — **not** `timezone.now()`.

## Why
With `TIME_ZONE='Asia/Jakarta'` and `USE_TZ=True`, `timezone.now()` returns UTC. Broadcast schedule `start_time`/`end_time` fields are plain `TimeField` values entered as WIB (UTC+7). Comparing UTC 06:26 against WIB schedule 13:00–15:00 produces no match → `program` is always null.

`timezone.localtime(now)` converts the UTC-aware datetime to the configured timezone (WIB), so `.time()` returns the WIB time and `.weekday()` returns the WIB day.

## How to Apply
Any future code that compares against schedule `TimeField` values or weekday labels must always use `timezone.localtime(timezone.now())` as the basis, not `timezone.now()` directly.

The `remaining_minutes` calculation also uses `local_now.replace(tzinfo=None)` for the same reason.
