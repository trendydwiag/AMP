---
name: Sprint 3.4B AMP Studio UX Polish
description: Changes made in Sprint 3.4B design polish pass across all studio pages
---

## Setup Wizard
- Redesigned to two-column layout: LEFT = vertical step list with connector lines + progress bar, RIGHT = single active step card with x-transition animations
- `goToStep(n)` only navigates backwards (completed steps); forward uses nextStep()
- Social platforms grid uses `{% empty %}` fallback to avoid context dependency

## Analytics
- No real analytics data yet; page uses hardcoded dummy data (CSS bar charts, horizontal heatmap bars, top programs horizontal bars)
- Do NOT use Django `split` template filter — it doesn't exist; hardcode data instead
- Added notice banner explaining data is demo

## Calendar
- `getEventsForDate(dateStr)` now populated with weekly Kabulhaden schedule (10 programs, days array)
- `getEventsForHour(hour)` filters by date + startHour
- Events have isLive (matches today + current hour), isPast, isLive flags
- Added event detail modal (x-show on selectedEvent)

## Media Explorer
- Fixed `⋯` button → proper SVG dots icon (three circles)  
- Added 10 dummy files (was 3); filteredFiles computed property with search + type filter
- Grid view has proper type-specific icons (audio=green, video=red, image=coffee, document=blue)

## Header
- Added `x-init="init()"` to header stream status widget (was missing, polling never started)

## ProfilingPanel Fix
- PANELS list in DEBUG_TOOLBAR_CONFIG explicitly excludes ProfilingPanel
- SHOW_TOOLBAR_CALLBACK approach was insufficient — only PANELS exclusion prevents the cProfile crash on concurrent requests

**Why:** ProfilingPanel uses cProfile which raises ValueError if two requests arrive simultaneously. Removing it from PANELS prevents it from being instantiated.
