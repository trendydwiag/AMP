---
name: Demo Seed Command
description: demo_seed management command for Kabulhaden Online demo environment. Real pitch-deck data, model field gotchas, and reset behavior.
---

## Command
`python manage.py demo_seed` — idempotent seed
`python manage.py demo_seed --reset` — wipe + re-seed

## Location
`apps/core/management/commands/demo_seed.py`

## Data Source
All program names, hosts, schedule times, team names, and org details are from the Kabulhaden Online pitch deck. NOT placeholder data.

## What It Creates (~340 records)
Partner (Enterprise), 4 users (superuser/CEO, administrator, editor/GM, viewer/CTO roles), RadioStation + AzuraCast provider, StreamHealth (31 records), ListenerStatistic (91 records), NowPlayingCache, LiveSession, **14 real programs** + 70 Episodes + 26 Schedules, **8 real hosts**, 12 Articles, 3 Podcasts + 15 Episodes, 5 Sponsors + 5 Ads, 6 MediaFolders, 5 Authors, 3 Announcements, 6 AuditLogEntries

## Model Field Gotchas
- `User.get_full_name` — property (string), not callable method
- `User` model has NO `partner` field
- `RadioStation` has NO `slug` field; use `station_name` to identify
- `RadioProvider` fields: `active` (not `is_active`), `provider_name` required; no `is_primary`
- `BroadcastSession.status` valid values: SCHEDULED, LIVE, FINISHED, CANCELLED, DELAYED (NOT 'COMPLETED')
- `Advertisement.start_date/end_date` are DateTimeField despite name; use timezone-aware datetime
- `SponsorPartner` is `apps.sponsor.models.Partner` (not Sponsor)
- `Article.tags` M2M name is `tags` (also has `tags_content` M2M)
- `PodcastEpisode.slug` is blank=True but null=False — must provide a slug

## Content String Gotchas
- All article `content` values must use tuple-of-strings or triple-quoted strings
- Single-quoted `'content': '<p>...'92...'` will break on the apostrophe in "Flight '92"
- Em-dashes (U+2014) can appear inside strings safely but must not appear OUTSIDE strings due to quote termination bugs; use `\u2014` escape in `patch_constants.py`-style scripts

## Reset Behavior
`--reset` must nullify `Partner.owner` FK before deleting users (PROTECTED FK constraint).
Order: `Partner.objects.update(owner=None)` → delete content → delete users.

**Why:**
These gotchas took multiple attempts to fix during initial seeding. Record them to avoid re-discovery.
