---
name: StreamHealth Model Fields
description: Correct field names for the StreamHealth model in apps/radio/models.py — templates have historically used wrong names causing 500 errors.
---

## The Rule
Use the correct field names. Templates that were auto-generated or written before the model settled often use wrong names.

**Why:** StreamHealth model was built with specific names but templates referenced fields from an earlier/imagined schema, causing VariableDoesNotExist 500 errors in debug mode.

## Correct Fields (as of current model)
| Wrong name (template used) | Correct field |
|---|---|
| `h.status` | `h.provider_status` (choices: HEALTHY/DEGRADED/DOWN/TIMEOUT) |
| `h.get_status_display` | `h.get_provider_status_display` |
| `h.checked_at` | `h.last_checked` |
| `h.listener_count` | ❌ doesn't exist — use `h.response_time` (ms) |
| `h.bitrate` | `h.stream_bitrate` (kbps, PositiveIntegerField) |
| `h.codec` | `h.stream_format` (CharField) |

## Status Values (StreamHealthStatus enum)
- `HEALTHY` → display "Sehat"
- `DEGRADED` → display "Menurun"
- `DOWN` → display "Mati"
- `TIMEOUT` → display "Timeout"

Template badge condition: `{% if h.provider_status == 'HEALTHY' %}amp-badge-success{% elif h.provider_status == 'DEGRADED' %}amp-badge-warning{% else %}amp-badge-danger{% endif %}`
