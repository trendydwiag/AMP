---
name: Radio Streaming Proxy
description: Why the Django streaming proxy fails in Replit dev, and the correct approach for audio delivery.
---

# Radio Streaming Proxy — Key Finding

## The Rule
Do NOT route browser audio through a Django `StreamingHttpResponse` proxy when running on Replit dev. The Replit reverse proxy buffers streaming responses before forwarding to the browser — the browser's `<audio>` element spins forever and never receives data.

**Why:** Replit's dev preview is an iframe proxied through `*.replit.dev`. The proxy appears to collect the full response body before forwarding, which breaks infinite live streams.

**How to apply:** `LiveRadioAPIView` should always return the provider's `stream_url` directly (the Icecast/ngrok URL). Icecast sends `Access-Control-Allow-Origin: *` so CORS is not an issue. The Django proxy endpoint (`/radio/stream/`) should remain as a fallback for non-Replit production deployments but must NOT be the default `stream_url`.

## Related
- `RadioStreamProxyView` in `apps/radio/views.py` — kept but not used as default
- `LiveRadioAPIView` returns `stream_url` (direct provider URL) not `/radio/stream/`

## ngrok Interstitial — Corrected Behavior (verified July 2026)
ngrok free-tier DOES show the HTML interstitial to ANY browser User-Agent, regardless of `Accept` header. Previous note was wrong.

- Without `ngrok-skip-browser-warning` header → ngrok returns HTML interstitial page (HTTP 200, content-type text/html)
- With `ngrok-skip-browser-warning: true` header → ngrok forwards to Icecast and returns audio
- `<audio src="ngrok-url">` cannot set custom headers → gets interstitial → NO audio on any device that hasn't previously clicked "Visit Site"
- Developer's own browser appeared to work because it had the bypass cookie from a prior manual visit

**Fix applied:** `LiveRadioAPIView` returns `/radio/stream/` (the Django proxy) as `stream_url`. The proxy adds the bypass header server-side. `stream_url_direct` field added for debugging.

## ngrok URL Note
ngrok free-tier URLs change on every restart. Must update `RadioProvider.stream_url` and `api_url` in DB via AMP Studio → Radio → Provider each time ngrok restarts.
