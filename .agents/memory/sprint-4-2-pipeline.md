---
name: Media Pipeline Engine (Sprint 4.2)
description: Architecture, new files, and key decisions for the media upload pipeline built in Sprint 4.2.
---

# Media Pipeline Engine — Sprint 4.2

## Rule
All media uploads go through `MediaPipelineService`. Never write directly to storage or create `MediaFile` outside the pipeline.

**Why:** Ensures uniform validation, metadata extraction, status lifecycle, and event dispatch for every file uploaded to the system.

**How to apply:** Call `MediaFileService.upload_file()` (interface unchanged) — it delegates internally to `MediaPipelineService.process()`. Do not instantiate `MediaFile` manually for uploads.

## New Architecture Files
- `apps/media_manager/pipeline.py` — `MediaPipelineService`, `PipelineContext`, `PipelineResult`, `MediaMetadata`
- `apps/media_manager/storage.py` — `BaseStorageBackend` ABC + `LocalStorageBackend` (active); S3/R2/MinIO stubs
- `apps/media_manager/events.py` — `MediaEventDispatcher` pub/sub; `EVENT_MEDIA_*` constants

## New Model Fields on MediaFile
`pipeline_status` (UPLOADING/PROCESSING/READY/FAILED/ARCHIVED), `processed_at`, `storage_backend`, `duration` (seconds), `bitrate` (kbps), `audio_title`, `audio_artist`, `audio_album`, `pipeline_error`.

Default for existing rows: `pipeline_status='READY'`, all metadata fields null.

## Dependencies Added
`mutagen>=1.47.0` — audio/video metadata extraction (ID3, Vorbis, AAC, FLAC). Installed via `uv`.

## Inspector View
`/media/inspector/` → `media_manager:inspector` — admin page showing pipeline metadata for all files.

## Stubs (not yet implemented)
`generate_waveform()`, `analyze_audio()`, `generate_preview()` — log DEBUG, return None. Future: pydub/pyloudnorm/ffmpeg.

## Uploads NOT Routed Through Pipeline Yet
`broadcast.Episode.recording_audio/recording_video`, `podcast.PodcastEpisode.audio_file`, `settings.SiteSettings.logo/favicon`, `users.UserProfile.avatar`, `broadcast.Host.avatar` — all direct FileField, documented in changelog but not changed (sprint rules).

## Migration
`0003_sprint42_pipeline_fields` — adds 9 columns with defaults, zero-downtime safe.
